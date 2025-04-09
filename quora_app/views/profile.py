from email.headerregistry import Address
from django.db.models import Q
from django.db import transaction

""" permissions """
from rest_framework.permissions import IsAuthenticated
from quora.permissions import is_super_admin_or_company_admin
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

""" utility """
from utility.constants import MESSAGES, STATUS_ACTIVE, STATUS_INACTIVE
from utility.response import ApiResponse
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    create_or_update_serializer,
    is_valid_email,
    validate_empty_strings,
    validate_enum_fields,
    validate_strings_data,
)

""" serializers """
from ..serializers.users_serializer import ProfileSerializer
from ..serializers.address_serializer import AddressesSerializer

""" model imports """
from ..model.cities import Cities
from ..model.users import User
from ..model.address import Addresses
from ..model.company import Company

""" swagger """
from ..swagger.profile_swagger import (
    swagger_auto_schema_retrive,
    swagger_auto_schema_update,
)


class ProfileView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    singular_name = "Profile"

    model_class = User.objects.filter(status=STATUS_ACTIVE).select_related("company", "role")
    
    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk, status__in=[STATUS_ACTIVE, STATUS_INACTIVE])
        except:
            return None

    @swagger_auto_schema_retrive
    def retrieve(self, request, *args, **kwargs):
        """
        :To get the single record
        """
        try:
            get_id = request.user.id

            if instance := self.get_object(get_id):
                view: str = request.query_params.get('view', 'short').lower()
                if view == 'detailed':
                    resp_dict = self.transform_single(instance)
                else:
                    resp_dict = self.transform(instance)
        
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + " not found")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=str(e))

    @swagger_auto_schema_update
    @transaction.atomic()
    @is_super_admin_or_company_admin
    def partial_update(self, request, *args, **kwargs):
        """
        :To update the existing record
        """
        sp1 = transaction.savepoint()

        req_data: dict = request.data.copy()
        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES["all_fields_should_not_empty"])

        get_id = request.user.id
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES["not_found"])

        first_name = req_data.get("first_name")
        last_name = req_data.get("last_name")
        mobile = req_data.get("mobile")
        email = req_data.get("email")
        status = req_data.get("status")

        if error_message := validate_strings_data({"first_name": first_name, "last_name": last_name}, req_data):
            return ApiResponse.response_bad_request(self, message=error_message)

        if email and not is_valid_email(email):
            return ApiResponse.response_bad_request(self, message="Invalid email.")

        if mobile and len(mobile) < 4 or len(mobile) > 10:
            return ApiResponse.response_bad_request(self, message="Invalid mobile number.")

        enum_fields = [(status, [STATUS_ACTIVE, STATUS_INACTIVE], "status"),]
        if error_message := validate_enum_fields(enum_fields):
            return ApiResponse.response_bad_request(self, message=error_message)

        if address_data := req_data.get("address"):
            city_id = address_data.get("city")
            state_id = address_data.get("state")
            zipcode = address_data.get("zipcode")

            if error_message := validate_empty_strings({"address":address_data.get('address')}, address_data):
                return ApiResponse.response_bad_request(self, message=error_message)

            if zipcode and len(str(zipcode)) < 4 or len(str(zipcode)) > 6:
                return ApiResponse.response_bad_request(self, message="Please enter the valid zipcode.")

            if state_id or city_id:
                if not Cities.objects.filter(Q(id=city_id) | Q(state_id=state_id), is_deleted=False).exists():
                    return ApiResponse.response_bad_request(message="Please select a valid state or city.")

            """ Address update"""
            if instance.address_id:
                address_instance, error = create_or_update_serializer(AddressesSerializer, address_data, sp1, instance.address)
                if error:
                    return ApiResponse.response_bad_request(self, message=error)
            else:
                address_instance, error = create_or_update_serializer(AddressesSerializer, address_data, sp1)
                if error:
                    return ApiResponse.response_bad_request(self, message=error)

        if address_data: req_data['address'] = address_instance.id

        """ User update"""
        req_data.pop('password', None)
        req_data.pop('role', None)
        req_data.pop('id', None)

        user_instance, error = create_or_update_serializer(ProfileSerializer, req_data, sp1, instance)
        if error:
            return ApiResponse.response_bad_request(self, message=error)
        req_data["user"] = user_instance.id

        transaction.savepoint_commit(sp1)
        return ApiResponse.response_ok(self, data=req_data, message=self.singular_name + MESSAGES["updated"])

    
    def transform_single(self, instance):
        resp_dict = {}
        resp_dict = User.to_dict(instance)
        if instance.company_id:
            resp_dict['company'] = Company.to_dict(instance.company)
        return resp_dict

    def transform(self, instance):
        resp_dict = {}
        resp_dict['id'] = instance.id
        resp_dict['first_name'] = instance.first_name
        resp_dict['last_name'] = instance.last_name
        resp_dict['email'] = instance.email
        resp_dict['mobile'] = instance.mobile
        resp_dict['username'] = instance.username
        resp_dict['status'] = instance.get_status_display()

        return resp_dict
