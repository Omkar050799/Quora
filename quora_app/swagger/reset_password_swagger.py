from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, Schema, IN_QUERY, TYPE_OBJECT, TYPE_STRING
import json

response_ok = {
    "message": ["Password changed successfully"],
    "code": 200,
    "success": True,
    "data": {},
}

response_not_found = {
    "message": ["Invalid email or token"],
    "code": 404,
    "success": False,
    "data": {},
}

response_bad_request = {
    "message": ["Link expires"],
    "code": 400,
    "success": False,
    "data": {},
}

swagger_auto_schema = swagger_auto_schema(
    manual_parameters=[
        Parameter("token", IN_QUERY, description="token paramater", type="char"),
    ],
    responses={
        "200": json.dumps(response_ok),
        "400": json.dumps(response_bad_request),
        "404": json.dumps(response_not_found),
    },
    operation_id="reset password",
    operation_description="API to reset password.",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "email": Schema(type=TYPE_STRING),
            "password": Schema(type=TYPE_STRING),
            "confirm_password": Schema(type=TYPE_STRING),
        },
    ),
)
