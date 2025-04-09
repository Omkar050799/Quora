from django.db import models
from .base import Base
from .users import User
from .questions import Questions


class Answers(Base):
    """Model to store information about answers"""
    answer = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        db_table = 'answers'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f"Answer to {self.question.question}"

    @staticmethod
    def to_dict(instance):
        return {
            'id': instance.id,
            'answer': instance.answer,
            'is_deleted': instance.is_deleted,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'user': User.to_dict(instance.user) if instance.user_id else None,
            'question': Questions.to_dict(instance.question) if instance.question_id else None,
        }
