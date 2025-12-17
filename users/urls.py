from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('approve/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),

    path('admin/patients/', PatientListView.as_view()),
    path('admin/patients/add/', PatientCreateView.as_view()),
    path('admin/patients/<int:pk>/update/', PatientUpdateView.as_view()),
    path('admin/patients/<int:pk>/medical-file/', PatientMedicalFileView.as_view()),
    path('admin/doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('admin/doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('admin/doctors/<int:id>/update/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('admin/doctors/<int:id>/delete/', DoctorDeleteView.as_view(), name='doctor-delete'),
]
