import sys

from django.contrib.auth.backends import BaseBackend

from accounts.models import Token, User


# upgrade custom auth for using BaseBackend(https://docs.djangoproject.com/en/4.1/topics/auth/customizing/)
class PasswordlessAuthenticationBackend(BaseBackend):
    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
