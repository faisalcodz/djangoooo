from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, **kwargs):
        if username is None or email is None:
            return None
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            return None
        return user
