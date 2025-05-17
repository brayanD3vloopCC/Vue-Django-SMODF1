# usuarios/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class CorreoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, correo=None, **kwargs):
        # Permitir autenticación tanto por username como por correo
        if correo is None:
            correo = username
        if correo is None or password is None:
            return None
        try:
            user = Usuario.objects.get(correo=correo)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Usuario.DoesNotExist:
            return None