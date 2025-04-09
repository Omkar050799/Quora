import operator
from functools import reduce
from simple_search import search_filter
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from utility.response import ApiResponse
from utility.utils import (
    CreateRetrieveUpdateViewSet,
    date_filter,
    filter_array_list,
    get_ordered_queryset,
    get_pagination_resp,
    transform_list,
)

""" model imports """
from ..models import States

"""swagger"""
from ..swagger.states_swagger import swagger_auto_schema_list

class StateView(CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    
    singular_name = "State"
    model_class = States.objects.filter(is_deleted=False)
    
    search_fields = ["name"]

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        '''
        :To get the all records
        '''
        query_params: dict = request.query_params

        filter_array = {'id':'id'}

        obj_list = filter_array_list(filter_array, query_params)

        obj_list = date_filter(query_params, obj_list)

        if q_list := [Q(x) for x in obj_list]:
            queryset = self.model_class.filter(reduce(operator.and_, q_list))
        else:
            queryset = self.model_class

        """Search for keyword """
        if keyword := query_params.get('keyword'):
            queryset = queryset.filter(search_filter(self.search_fields, keyword))

        queryset = get_ordered_queryset(query_params, queryset, States)

        resp_data = get_pagination_resp(queryset, request)

        response_data = transform_list(self, resp_data.get("data"))

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

    # Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        if instance:
            resp_dict['id'] = instance.id
            resp_dict['name'] = instance.name
        return resp_dict

    # Generate the response
    def transform(self, instance):
        return{
            "id": instance.id,
            "name": instance.name
        }
    