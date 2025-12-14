from django.urls import path
from .views import UserRegisterView, LoginView, ApproveUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('approve/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),
]
