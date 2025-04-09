from django.db import models
from django.contrib.auth.models import  User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class EmailOrUsernameModelBackend(object):

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

""" Import all the models """
from .model.users import User
from .model.address import Addresses
from .model.assets import Assets
from .model.base import Base
from .model.cities import Cities
# from .model.otp import OTP
from .model.roles import Roles
from .model.states import States
from .model.questions import Questions
from .model.answers import Answers
