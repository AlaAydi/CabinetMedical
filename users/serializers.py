from rest_framework import serializers
from .models import User, Patient, Doctor, Consultation


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            is_approved=False
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'address', 'status', 'medical_file']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'status' in validated_data:
            instance.user.is_approved = validated_data['status'] == 'Actif'
            instance.user.save()

        instance.save()
        return instance

class PatientCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['name', 'email', 'password', 'address', 'status', 'medical_file']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='PATIENT',
            is_approved=True
        )
        patient = Patient.objects.create(
            user=user,
            address=validated_data['address'],
            status=validated_data.get('status', 'Actif'),
            medical_file=validated_data.get('medical_file')
        )
        return patient

class AdminPatientListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'is_approved']

class PatientMedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'medical_file']
        read_only_fields = ['id', 'user']

class DoctorCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'username',
            'email',
            'password',
            'specialty',
            'phone',
            'schedule',
            'image'
        ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='DOCTOR',
            is_approved=True
        )

        doctor = Doctor.objects.create(
            user=user,
            **validated_data
        )

        return doctor



class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)
    patient_name = serializers.CharField(source='patient.user.username', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id',
            'doctor',
            'doctor_name',
            'patient',
            'patient_name',
            'start_time',
            'end_time'
        ]
        read_only_fields = ['end_time']