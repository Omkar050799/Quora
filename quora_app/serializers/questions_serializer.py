

from rest_framework import serializers
from ..model.questions import Questions 


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"
