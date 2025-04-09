

from rest_framework import serializers
from ..model.answers import Answers 


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"
