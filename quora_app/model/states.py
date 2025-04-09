from django.db import models
from .base import Base


class States(Base):

    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=True)

    class Meta:
        db_table = "states"

    def __str__(self):
        return self.name

    @property
    def get_name(self):
        return self.name.capitalize()

    @staticmethod
    def to_dict(instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "aadhar_card": instance.aadhar_card,
            "is_deleted": instance.is_deleted,
        }