from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('approve/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),

    path('admin/patients/', PatientListView.as_view()),
    path('admin/patients/add/', PatientCreateView.as_view()),
    path('admin/patients/<int:pk>/update/', PatientUpdateView.as_view()),
]
