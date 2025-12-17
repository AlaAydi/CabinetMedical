from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, PatientSerializer, PatientCreateSerializer, AdminPatientListSerializer, \
    PatientMedicalFileSerializer, DoctorCreateSerializer, ConsultationSerializer
from .models import User, Patient, Doctor, Consultation
from .permissions import IsAdminRole, IsDoctorRole
from rest_framework.parsers import MultiPartParser, FormParser

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Utilisateur créé avec succès. En attente d’approbation.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email incorrect"}, status=401)

        user = authenticate(request, username=user_obj.email, password=password)
        if not user:
            return Response({"error": "Mot de passe incorrect"}, status=401)
        if not user.is_approved:
            return Response({"error": "Compte non approuvé"}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role,
            "email": user.email
        })

class ApproveUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_approved:
                return Response({"message": "Compte déjà approuvé"})
            user.is_approved = True
            user.save()
            return Response({"message": "Compte approuvé avec succès"})
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)

class PatientListView(generics.ListAPIView):
    serializer_class = AdminPatientListSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        return User.objects.filter(role='PATIENT', is_approved=True)


class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]

class PatientUpdateView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]
    def get_object(self):
        user_id = self.kwargs['pk']
        try:
            return Patient.objects.get(user__id=user_id)
        except Patient.DoesNotExist:
            raise Http404("Patient non trouvé pour cet utilisateur")

class PatientMedicalFileView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientMedicalFileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminRole]
    def get_object(self):
        user_id = self.kwargs['pk']
        return Patient.objects.get(user__id=user_id)

class DoctorListView(generics.ListAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAdminRole]
    def get_queryset(self):
        return Doctor.objects.all()

class DoctorCreateView(generics.CreateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]


class DoctorUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'
    queryset = Doctor.objects.all()

class DoctorDeleteView(generics.DestroyAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id'
    queryset = Doctor.objects.all()




class ConsultationCreateView(generics.CreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, (IsAdminRole | IsDoctorRole)]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError(str(e))
