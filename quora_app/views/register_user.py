import operator
import traceback
from functools import reduce
from quora.throttles import HeavyRateLimit
from simple_search import search_filter

from django.db.models import Q
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from oauth2_provider.contrib.rest_framework import OAuth2Authentication

""" utility """
from utility.response import ApiResponse
from utility.utils import (
    CreateRetrieveUpdateViewSet,
    date_filter,
    filter_array_list,
    get_ordered_queryset,
    get_pagination_resp,
    get_required_fields,
    transform_list,
    create_or_update_serializer,
)
from utility.constants import MESSAGES

""" model imports """
from ..models import User

""" serializers """
from ..serializers.users_serializer import RegisterUserSerializer

''' swagger '''


class RegisterUserView(CreateRetrieveUpdateViewSet, ApiResponse):
    """
    View for user registration
    """
    throttle_classes = [HeavyRateLimit]
    serializer_class = RegisterUserSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        Register a new user
        """
        try:
            sp1 = transaction.savepoint()
            req_data = request.data.copy()
            print("*********", req_data)
            if not req_data:
                return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_are_required'])

            # Required fields
            username = req_data.get('username')
            email = req_data.get('email')
            password = req_data.get('password')
            first_name = req_data.get('first_name')
            last_name = req_data.get('last_name')
            mobile = req_data.get('mobile')
            required_list = {
                "username": username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "mobile": mobile
            }

            if required_field := get_required_fields(required_list, req_data):
                return ApiResponse.response_bad_request(self, message=required_field)  
            
            # Check if username already exists
            if User.objects.filter(username=username, status__in=[1, 2]).exists():
                return ApiResponse.response_bad_request(self, message="Username already exists")

            # Check if email already exists
            if User.objects.filter(email=email, status__in=[1, 2]).exists():
                return ApiResponse.response_bad_request(self, message="Email already exists")

            # Create user instance
            user_instance, error = create_or_update_serializer(RegisterUserSerializer, req_data, sp1)
            if error:
                return ApiResponse.response_bad_request(self, message=error)

            # Set password
            user_instance.set_password(password)
            user_instance.save()

            transaction.savepoint_commit(sp1)
            
            # Return success response without sensitive data
            response_data = {
                'id': user_instance.id,
                'username': user_instance.username,
                'email': user_instance.email,
                'created_at': user_instance.created_at
            }
            
            return ApiResponse.response_created(
                self,
                data=response_data,
                message="User registered successfully"
            )

        except Exception as e:
            print("Error registering user: ", traceback.format_exc())
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=str(e))
