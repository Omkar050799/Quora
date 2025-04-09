from django.db import models
from .base import Base
from .users import User

class Questions(Base):
    """Model to store information about questions"""
    question = models.CharField(max_length=355)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question

    @staticmethod
    def to_dict(instance):
        return {
            'id': instance.id,
            'question': instance.question,
            'is_deleted': instance.is_deleted,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'user': instance.user.to_dict(instance.user) if instance.user else None,
        }

