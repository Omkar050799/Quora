from django.db import models
from .base import Base
from .address import Addresses
from .assets import Assets


class Company(Base):
    #  Fields 
    company_name = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    incorporation_date = models.DateField(null=True, blank=True,db_index=True)
    website_url = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    registration_date = models.DateTimeField(null=True, blank=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    company_logo = models.ForeignKey(Assets, on_delete=models.SET_NULL, null=True, blank=True, related_name='company_logo_company')
    address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True, blank=True, related_name="address_company")

    class Meta:
        db_table = "companies"

    @staticmethod
    def to_dict(instance):
        resp_dict = {
            "id": instance.id,
            "company_name": instance.company_name,
            "incorporation_date": instance.incorporation_date,
            "website_url": instance.website_url,
            "registration_date": instance.registration_date,
            "description": instance.description,
            "created_at": instance.created_at,
            "update_at": instance.updated_at,
        }
        if instance.address_id:
            resp_dict['address'] = Addresses.to_dict(instance.address)

        return resp_dict
