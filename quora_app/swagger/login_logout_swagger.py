from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_STRING, TYPE_OBJECT
import json

login = {
    "message": ["Login successful"],
    "code": 200,
    "success": True,
    "data": {
        "id": 5,
        "first_name": "john",
        "last_name": "mark",
        "email": "john@gmail.com",
        "mobile": "812442483",
        "username": None,
        "token": {
            "access_token": "iEOgjQlZnwWyiG6m6C64Ai488P7PdC",
            "token_type": "Bearer",
            "expires_in": 36000,
            "refresh_token": "UtvBMQgZDOH61Ska0B2NvVWNajA7aF",
            "scope": {"read": "Read scope"},
        },
    },
}

invalid_login = {
    "message": ["Invalid username or password. Please try again."],
    "code": 403,
    "success": False,
    "data": {},
}

logout = {"message": ["Logout successful"], "code": 200, "success": True, "data": []}

swagger_auto_schema_logout = swagger_auto_schema(
    responses={
        "200": json.dumps(logout),
    },
    operation_id="logout ",
    operation_description="API to logout",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(login),
        "403": json.dumps(invalid_login),
    },
    operation_id="login",
    operation_description="API to login",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "username": Schema(type=TYPE_STRING),
            "password": Schema(type=TYPE_STRING),
        },
    ),
)
