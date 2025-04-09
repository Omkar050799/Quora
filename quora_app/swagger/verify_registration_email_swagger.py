from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
import json

response_post = {
    "message": ["Successfully account activated."],
    "code": 201,
    "success": True,
    "data": {},
}

response_unauthenticate = {
    "message": ["Authentication credentials were not provided."],
    "code": 403,
    "success": True,
    "data": {},
}

response_unauthorized = {
    "message": ["Unauthorized"],
    "code": 401,
    "success": True,
    "data": {},
}

response_bad_request = {
    "message": ["User is not registered."],
    "code": 400,
    "success": True,
    "data": {},
}

response_not_found = {
    "message": ["User not found"],
    "code": 404,
    "success": True,
    "data": {},
}

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        "201": json.dumps(response_post),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "400": json.dumps(response_bad_request),
    },
    operation_id="Verify email address",
    operation_description="API to verify email address",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "password": Schema(type=TYPE_STRING),
            "token": Schema(type=TYPE_STRING),
        },
        required=["password", "token"],
    ),
)
