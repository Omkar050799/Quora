from django.db import models
from .base import Base
from .cities import Cities
from .states import States

class Addresses(Base):

    zipcode = models.IntegerField(null=True, blank=True)
    street1 = models.TextField(null=True, blank=True)
    address_line = models.TextField(null=True, blank=True)

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(States, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def to_dict(instance):
        resp_dict = {
            "address": instance.id,
            "street1": instance.street1,
            "address_line": instance.address_line,
            "zipcode": instance.zipcode,
        }
        if instance.city_id:
            resp_dict["city_id"] = instance.city_id
            resp_dict["city_name"] = instance.city.name
        if instance.state_id:
            resp_dict["state_id"] = instance.state_id
            resp_dict["state_name"] = instance.state.name

        return resp_dict