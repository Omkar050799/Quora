from rest_framework import serializers

from quora_app.models import Roles


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"
