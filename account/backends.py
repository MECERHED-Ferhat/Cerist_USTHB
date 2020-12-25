from django.contrib.auth.backends import *
from django.contrib.auth.models import User

class EmailAuthBackend(AllowAllUsersModelBackend):
	
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.EMAIL_FIELD)
        if username is None or password is None:
            return
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user