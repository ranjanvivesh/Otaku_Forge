from django.contrib.auth.backends import BaseBackend
from accounts.models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        """Authenticate using email (or username fallback) and password.

        The Django admin passes the credential as ``username``. This backend
        now treats ``username`` as an email address when ``email`` is not
        explicitly supplied, ensuring admin logins work with the custom user
        model.
        """
        if not email:
            email = username
        if not email or password is None:
            return None
        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            return None
        if not user.is_email_verified:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
