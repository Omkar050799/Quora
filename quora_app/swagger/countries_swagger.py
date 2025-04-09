from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    "message": ["Ok"],
    "code": 200,
    "success": True,
    "data": [
        {"id": 1, "name": "Afghanistan"},
        {"id": 2, "name": "Aland Islands"},
        {"id": 3, "name": "Albania"},
        {"id": 4, "name": "Algeria"},
        {"id": 5, "name": "American Samoa"},
    ],
    "paginator": {"total_count": 5, "total_pages": 1, "current_page": 1, "limit": 10},
}

response_unauthenticate = {
    "message": ["Authentication credentials were not provided."],
    "code": 401,
    "data": {},
}

response_unauthorized = {
    "message": ["You do not have permission to perform this action."],
    "code": 403,
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
        Parameter("name", IN_QUERY, description="name parameter", type="char"),
    ],
    responses={
        "200": json.dumps(response_list),
        "401": json.dumps(response_unauthenticate),
        "403": json.dumps(response_unauthorized),
    },
    operation_id="list countries",
    operation_description="API to list countries data",
)
