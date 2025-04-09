from drf_yasg.openapi import (
    Parameter,
    Schema,
    Response,
    IN_QUERY,
    TYPE_INTEGER,
    TYPE_STRING,
    TYPE_OBJECT,
)
from drf_yasg.utils import swagger_auto_schema
import json
from utility.constants import AHJ_PROVIDER_CHOICES

response_list = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": [
        {
            "id": 2,
            "name": "santacruz",
            "base_url": "https://co-santacruz-az.smartgovcommunity.com/Permitting/PermitLandingPage/Index/a7d9e12c-cece-4f51-969c-b24200aebc51?ShowConfirm=N&_conv=1",
            "is_active": True,
            "provider": 1,
            "provider_name": "Accela",
            "solar_app_url": "https://co-santacruz-az.smartgovcommunity.com/Permitting/PermitLandingPage/Index/a7d9e12c-cece-4f51-969c-b24200aebc51?ShowConfirm=N&_conv=1",
            "config_file": {
                "id": 1,
                "file_name": "static/b797490613134509841c37d167ee805b2025_02_21_11_10_29_507774.png",
                "actual_file_name": "Screenshot from 2025-02-19 19-01-05.png",
                "file_type": "image/png",
                "file_size": 0.0001,
            },
            "created_at": "2025-02-25T06:25:43.721435Z",
            "updated_at": "2025-02-25T06:25:43.721452Z",
        }
    ],
    "paginator": {"total_count": 1, "total_pages": 1, "current_page": 1, "limit": 10},
}

response_get = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": {
        "id": 6,
        "name": "Gilroy",
        "base_url": "https://co-santacruz-az.smartgovcommunity.com/Permitting/PermitLandingPage/Index/a7d9e12c-cece-4f51-969c-b24200aebc51?ShowConfirm=N&_conv=1",
        "is_active": True,
        "provider": 1,
        "provider_name": "Accela",
        "solar_app_url": "https://co-santacruz-az.smartgovcommunity.com/Permitting/PermitLandingPage/Index/a7d9e12c-cece-4f51-969c-b24200aebc51?ShowConfirm=N&_conv=1",
        "config_file": {
            "id": 1,
            "file_name": "static/b797490613134509841c37d167ee805b2025_02_21_11_10_29_507774.png",
            "actual_file_name": "Screenshot from 2025-02-19 19-01-05.png",
            "file_type": "image/png",
            "file_size": 0.0001,
        },
        "created_at": "2025-02-25T06:34:28.209597Z",
        "updated_at": "2025-02-25T06:34:28.209656Z",
    },
}

response_post = {
    "message": ["Ahj created successfully."],
    "code": 201,
    "success": True,
    "data": {
        "name": "SANDIEGO",
        "base_url": "https://aca-prod.accela.com/SANDIEGO/Default.aspx",
        "solar_app_url": "https://aca-prod.accela.com/SANDIEGO/Default.aspx",
        "provider": 1,
        "config_file": 1,
        "is_active": True,
    },
}

response_update = {
    "message": ["Ahj updated successfully."],
    "code": 200,
    "success": True,
    "data": {
        "name": "Sandiego",
        "base_url": "https://aca-prod.accela.com/SANDIEGO/Default.aspx",
        "solar_app_url": "https://aca-prod.accela.com/SANDIEGO/Default.aspx",
        "provider": 1,
        "config_file": 1,
    },
}

response_delete = {
    "message": ["Ahj deleted successfully."],
    "code": 200,
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
    "message": ["Ahj already exists."],
    "code": 400,
    "success": True,
    "data": {},
}

response_not_found = {
    "message": ["Ahj not found"],
    "code": 404,
    "success": True,
    "data": {},
}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter(
            "sort_by", IN_QUERY, description="sort by id", type="char", default="id"
        ),
        Parameter(
            "sort_direction",
            IN_QUERY,
            description="sort direction should be ascending or descending",
            type="char",
            default="ascending",
        ),
        Parameter(
            "id",
            IN_QUERY,
            description="id parameter",
            type="int",
        ),
        Parameter("keyword", IN_QUERY, description="keyword paramater", type="char"),
        Parameter(
            "page", IN_QUERY, description="page no. paramater", type="int", default=1
        ),
        Parameter(
            "limit", IN_QUERY, description="limit paramater", type="int", default=10
        ),
        Parameter(
            "type", IN_QUERY, description="All result set: type=all", type="char"
        ),
        Parameter(
            "start_date", IN_QUERY, description="start_date paramater", type="char"
        ),
        Parameter("end_date", IN_QUERY, description="end_date paramater", type="char"),
        Parameter(
            "view",
            IN_QUERY,
            description="response view type",
            type="char",
            default="short",
            enum=("short", "detailed"),
        ),
        Parameter("name", IN_QUERY, description="search ahj by ahj name", type="char"),
        Parameter(
            "provider",
            IN_QUERY,
            description="provider",
            type="int",
            enum=AHJ_PROVIDER_CHOICES,
        ),
    ],
    responses={
        "200": json.dumps(response_list),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "404": json.dumps(response_not_found),
    },
    operation_id="List Ahj",
    operation_description="API to list Ahj data",
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        "201": json.dumps(response_post),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "400": json.dumps(response_bad_request),
    },
    operation_id="Create Ahj",
    operation_description="API to add new Ahj",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "name": Schema(type=TYPE_STRING),
            "base_url": Schema(type=TYPE_STRING),
            "solar_app_url": Schema(type=TYPE_STRING),
            "provider": Schema(type=TYPE_INTEGER),
            "config_file": Schema(type=TYPE_INTEGER),
        },
    ),
)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        "200": json.dumps(response_update),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "400": json.dumps(response_bad_request),
        "404": json.dumps(response_not_found),
    },
    operation_id="Update Ahj",
    operation_description="API to update the existing Ahj",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "name": Schema(type=TYPE_STRING),
            "base_url": Schema(type=TYPE_STRING),
            "solar_app_url": Schema(type=TYPE_STRING),
            "provider": Schema(type=TYPE_INTEGER),
            "config_file": Schema(type=TYPE_INTEGER),
        },
    ),
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        "200": json.dumps(response_delete),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "404": json.dumps(response_not_found),
    },
    operation_id="Delete Ahj",
    operation_description="API to delete the Ahj",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_get),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "404": json.dumps(response_not_found),
    },
    operation_id="Get Ahj",
    operation_description="API to get Ahj",
)
