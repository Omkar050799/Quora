import operator
from simple_search import search_filter
from functools import reduce
from django.db.models import Q
from django.db.models.functions import Lower
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
# from dbt.permissions import ModulePermission


""" utility """
from dbt.throttles import LightRateLimit
from utility.dbt_utility import get_field_type
from utility.response import ApiResponse
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    filter_array_list,
    get_pagination_resp,
    transform_list,
)

""" model imports """
from ..models import Country

"""swagger"""
from ..swagger.countries_swagger import swagger_auto_schema_list


class CountryView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [LightRateLimit]
    
    model_class = Country.objects.filter(is_deleted=False)

    search_fields = ["name"]

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        '''
        :To get the all records
        '''
        ''' capture data '''
        sort_by = request.query_params.get('sort_by') if request.query_params.get('sort_by') else 'id'
        
        sort_direction = request.query_params.get('sort_direction') if request.query_params.get(
            'sort_direction') else 'ascending'

        if sort_direction == 'descending':
            sort_by = '-' + sort_by

        where_array = request.query_params
        
        ''' filters '''
        obj_list = []
        
        filter_array = {'id':'id', "name":"name__icontains"}
        
        obj_list = filter_array_list(filter_array, where_array, obj_list)

        q_list = [Q(x) for x in obj_list]
        if q_list:
            queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
        else:
            queryset = self.model_class.order_by(sort_by)

        """Search for keyword"""
        if where_array.get("keyword"):
            queryset = queryset.filter(
                search_filter(self.search_fields, where_array.get("keyword"))
            )
        if field_type := get_field_type(Country, sort_by):
            if field_type == 'CharField':
                queryset = queryset.order_by(Lower(sort_by))

        resp_data = get_pagination_resp(queryset, request)
        response_data = transform_list(self, resp_data.get("data"))

        return ApiResponse.response_ok(
            self, data=response_data, paginator=resp_data.get("paginator")
        )

    # Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        if instance:
            resp_dict['id'] = instance.id
            resp_dict['name'] = instance.name

        return resp_dict
