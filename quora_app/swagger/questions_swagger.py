from drf_yasg.openapi import (
    Parameter,
    Schema,
    Response,
    IN_QUERY,
    TYPE_INTEGER,
    TYPE_STRING,
    TYPE_OBJECT,
    TYPE_BOOLEAN,
)
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "is_deleted": False,
            "created_at": "2025-02-25T07:21:57.895092Z",
            "updated_at": "2025-02-25T08:40:24.380813Z",
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2025-02-21T11:30:01.054761Z",
                "updated_at": "2025-02-21T11:30:01.054775Z",
            }
        }
    ],
    "paginator": {"total_count": 1, "total_pages": 1, "current_page": 1, "limit": 10},
}

response_get = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": {
        "id": 1,
        "question": "What is the capital of France?",
        "is_deleted": False,
        "created_at": "2025-02-25T07:21:57.895092Z",
        "updated_at": "2025-02-25T08:40:24.380813Z",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "created_at": "2025-02-21T11:30:01.054761Z",
            "updated_at": "2025-02-21T11:30:01.054775Z",
        }
    },
}

response_post = {
    "message": ["Question created successfully."],
    "code": 201,
    "success": True,
    "data": {
        "question": "What is the capital of France?",
        "user": 1,
        "id": 1
    },
}

response_update = {
    "message": ["Question updated successfully."],
    "code": 200,
    "success": True,
    "data": {
        "question": "What is the capital of France?",
        "is_deleted": False,
        "user": 1,
        "id": 1
    },
}

response_delete = {
    "message": ["Question deleted successfully."],
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
    "message": ["Question already exists."],
    "code": 400,
    "success": True,
    "data": {},
}

response_not_found = {
    "message": ["Question not found"],
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
        Parameter(
            "is_deleted",
            IN_QUERY,
            description="filter by is_deleted status",
            type=TYPE_BOOLEAN,
        ),
    ],
    responses={
        "200": json.dumps(response_list),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "404": json.dumps(response_not_found),
    },
    operation_id="List questions",
    operation_description="API to list questions data",
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        "201": Response(description=response_post),
        "403": Response(description="Forbidden"),
        "401": Response(description="Unauthorized"),
        "400": Response(description="Bad Request"),
    },
    operation_id="Create question",
    operation_description="API to add new question",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "question": Schema(type=TYPE_STRING),
            "user": Schema(type=TYPE_INTEGER),
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
    operation_id="Update question",
    operation_description="""API to update question""",
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "question": Schema(type=TYPE_STRING),
            "is_deleted": Schema(type=TYPE_BOOLEAN),
            "user": Schema(type=TYPE_INTEGER),
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
    operation_id="Delete question",
    operation_description="API to delete question",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_get),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
        "404": json.dumps(response_not_found),
    },
    operation_id="Get question",
    operation_description="API to get question",
)
