from drf_yasg.openapi import (
    Parameter,
    Schema,
    IN_QUERY,
    TYPE_STRING,
    TYPE_OBJECT,
    TYPE_INTEGER,
)
from drf_yasg.utils import swagger_auto_schema
import json

response_get = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": {
        "id": 5,
        "first_name": "john",
        "last_name": "mark",
        "email": "john@gmail.com",
        "mobile": "812442483",
        "username": None,
        "status": "Active",
        "company": {
            "id": 7,
            "company_name": "john",
            "incorporation_date": None,
            "website_url": "www.abc.net",
            "registration_date": None,
            "description": None,
            "created_at": "2025-02-21T11:30:01.054761Z",
            "update_at": "2025-02-21T11:30:01.054775Z",
            "address": {
                "address": 1,
                "street1": None,
                "address_line": "JK street",
                "zipcode": None,
            },
        },
    },
}

response_update = {
    "message": ["Profile updated successfully."],
    "code": 200,
    "success": True,
    "data": {
        "first_name": "john",
        "last_name": "mark",
        "mobile": "9119533077",
        "email": "john@gmail.com",
        "address": 66,
        "user": 5,
    },
}

response_unauthenticate = {
    "message": ["Authentication credentials were not provided."],
    "code": 401,
    "data": {},
}
response_bad_request = {
    "message": ["All fields should not be empty"],
    "code": 400,
    "success": False,
    "data": {},
}

response_not_found = {
    "message": ["Profile not found"],
    "code": 404,
    "success": False,
    "data": {},
}

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        "200": json.dumps(response_update),
        "400": json.dumps(response_bad_request),
        "401": json.dumps(response_unauthenticate),
        "404": json.dumps(response_not_found),
    },
    operation_id="Update profile",
    operation_description="API to update self profile",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "first_name": Schema(type=TYPE_STRING),
            "last_name": Schema(type=TYPE_STRING),
            "mobile": Schema(type=TYPE_STRING),
            "email": Schema(type=TYPE_STRING),
            "address": Schema(
                type=TYPE_OBJECT,
                properties={
                    "street1": Schema(type=TYPE_STRING),
                    "address_line": Schema(type=TYPE_STRING),
                    "zipcode": Schema(type=TYPE_INTEGER),
                    "city": Schema(type=TYPE_INTEGER),
                    "state": Schema(type=TYPE_INTEGER),
                },
            ),
        },
    ),
)

swagger_auto_schema_retrive = swagger_auto_schema(
    manual_parameters=[
        Parameter(
            "is_all_data", IN_QUERY, description="is_all_data parameter", type="char"
        ),
    ],
    responses={
        "200": json.dumps(response_get),
        "400": json.dumps(response_bad_request),
        "401": json.dumps(response_unauthenticate),
        "404": json.dumps(response_not_found),
    },
    operation_id="Get profile",
    operation_description="API to retrieve profile",
)
