from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, PatientSerializer, PatientCreateSerializer, AdminPatientListSerializer
from .models import User, Patient
from .permissions import IsAdminRole
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated
from .utils import send_admin_notification, send_approval_email
# Inscription doctor/patient
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_admin_notification(user)  # Email à l'admin
            return Response({'message': 'Utilisateur créé avec succès. En attente d’approbation.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login avec vérification is_approved
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email incorrect"}, status=401)

        user = authenticate(
            request,
            username=user_obj.email,
            password=password
        )

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
# Approbation par l'admin
class ApproveUserView(APIView):
    permission_classes = []  # email link

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)

            if user.is_approved:
                return Response({"message": "Compte déjà approuvé"})

            user.is_approved = True
            user.save()

            send_approval_email(user)

            return Response({"message": "Compte approuvé avec succès"})
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)


#partie patient
class PatientListView(generics.ListAPIView):
    serializer_class = AdminPatientListSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        return User.objects.filter(
            role='PATIENT',
            is_approved=True
        )



class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]

class PatientUpdateView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]