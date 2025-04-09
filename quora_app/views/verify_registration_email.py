import traceback

from django.db import transaction
from rest_framework.viewsets import GenericViewSet

from quora_app.model.users import User
from utility.constants import MESSAGES

""" utility """
from utility.email_utility import verify_tamper_secure_token
from utility.response import ApiResponse
from utility.utils import (
    get_required_fields,
)

""" serializers """
from ..serializers.users_serializer import VerifyUserSerializer

''' swagger '''
from ..swagger.verify_registration_email_swagger import (
    swagger_auto_schema_post,
)


class VerifyRegistrationView(GenericViewSet, ApiResponse):
    serializer_class = VerifyUserSerializer

    @swagger_auto_schema_post
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        try:
            sp1 = transaction.savepoint()
            req_data: dict = request.data.copy()
            if not req_data:
                return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_are_required'])           

            password: str = req_data.get('password')
            token: str = request.query_params.get("token") or req_data.get('token')

            if required_field := get_required_fields({"password": password, "token": token}, req_data):
                return ApiResponse.response_bad_request(self, message=required_field)            

            email = verify_tamper_secure_token(token)

            if email == "expired":
                return ApiResponse.response_bad_request(self, message="Token has expired. Please request a new password reset link.")

            if email is None:
                return ApiResponse.response_bad_request(self, message="Invalid token.")

            user = User.objects.filter(email=email).first()
            if not user:
                return ApiResponse.response_not_found(self, message="User not found.")

            user.set_password(password)
            user.save()

            transaction.savepoint_commit(sp1)
            return ApiResponse.response_created(self, data={}, message="Successfully account activated.")

        except Exception as e:
            print("Error ", traceback.format_exc())
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=str(e.args[0]))
