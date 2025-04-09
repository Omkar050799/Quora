from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "mobile", "email", "username", "address")


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password",]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "mobile", "email", "username", "password",]
