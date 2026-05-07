from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User

class EmailAuthBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users using email instead of username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Find user by email
            user = User.objects.get(email=username)
            # Check if the password matches
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
