from django.db.models import Q

from django.contrib.auth.backends import ModelBackend
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from account.models import EmailAddress


class UsernameAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        try:
            user = User.objects.get(username__iexact=credentials["username"])
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user


class EmailAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        qs = EmailAddress.objects.filter(Q(primary=True) | Q(verified=True))
        try:
            email_address = qs.get(email__iexact=credentials["username"])
        except EmailAddress.DoesNotExist:
            return None
        else:
            user = email_address.user
            if user.check_password(credentials["password"]):
                return user
