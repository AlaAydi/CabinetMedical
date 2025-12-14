from django.core.mail import send_mail
from django.conf import settings

def send_admin_notification(user):
    approve_link = f"http://127.0.0.1:8000/api/users/approve/{user.id}/"

    subject = "Nouvelle inscription à approuver"
    message = (
        f"Nouvel utilisateur inscrit\n\n"
        f"Username : {user.username}\n"
        f"Role : {user.role}\n\n"
        f"Cliquez sur ce lien pour approuver le compte :\n"
        f"{approve_link}"
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ['aydiala123@gmail.com'],
        fail_silently=False
    )

def send_approval_email(user):
    subject = "Compte approuvé sur Clinique"
    message = (
        f"Bonjour {user.username},\n\n"
        f"Votre compte a été approuvé par l’administrateur.\n"
        f"Vous pouvez maintenant vous connecter."
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
