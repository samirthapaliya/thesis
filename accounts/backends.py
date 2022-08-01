# External Import
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

# Using the Custom User Model
UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """ This Class Allows user to login using either email or password """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Authentication function which runs during the login process """

        try:
            # If the User with the usersame of email exist storing user in user variable
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
