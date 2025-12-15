from rest_framework import serializers
from .models import User, Patient


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
    name = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'email',
            'address',
            'status',
            'medical_file'
        ]


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
        fields = [
            'id',
            'name',
            'email',
            'role',
            'is_approved'
        ]
