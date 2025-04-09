from django.db import models
from .base import Base
from .states import States


class Cities(Base):

    state = models.ForeignKey(States, null=True, blank=True, on_delete=models.SET_NULL, related_name="cities_state")
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    is_deleted = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "cities"

    @property
    def get_name(self):
        return self.name.capitalize()

    @staticmethod
    def to_dict(instance):
        return {
            'id': instance.id,
            'name': instance.name,
            "is_deleted": instance.is_deleted,
        }
