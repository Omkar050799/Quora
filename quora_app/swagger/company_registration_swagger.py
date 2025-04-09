from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING
import json

response_post = {
    "message": ["Company registered successfully."],
    "code": 201,
    "success": True,
    "data": {
        "first_name": "mark",
        "last_name": "jose",
        "company_name": "Mark J",
        "mobile": "98520145",
        "email": "j.mark@gmail.com",
        "website_url": "www.xyz.com",
        "company": 9,
        "registration_date": "2025-02-25T07:10:09.281352",
        "user": 25,
    },
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
    "message": ["Company already exists."],
    "code": 400,
    "success": True,
    "data": {},
}

response_not_found = {
    "message": ["Company not found"],
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
        "404": json.dumps(response_not_found),
    },
    operation_id="Register company",
    operation_description="API to register new company",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "first_name": Schema(type=TYPE_STRING),
            "last_name": Schema(type=TYPE_STRING),
            "company_name": Schema(type=TYPE_STRING),
            "mobile": Schema(type=TYPE_STRING),
            "email": Schema(type=TYPE_STRING),
            "website_url": Schema(type=TYPE_STRING),
            "password": Schema(type=TYPE_STRING),
            "confirm_password": Schema(type=TYPE_STRING),
            "company_logo": Schema(type=TYPE_INTEGER),
            "address": Schema(
                type=TYPE_OBJECT,
                properties={
                    "address_line": Schema(type=TYPE_STRING),
                    "city": Schema(type=TYPE_INTEGER),
                    "state": Schema(type=TYPE_INTEGER),
                    "zipcode": Schema(type=TYPE_STRING),
                    "street1": Schema(type=TYPE_STRING),
                },
            ),
        },
    ),
)
