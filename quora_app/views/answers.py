import operator
import traceback
from functools import reduce
from quora.throttles import LiteRateLimit
from simple_search import search_filter

from django.db.models import Q
from django.db import transaction
from rest_framework.permissions import IsAuthenticated  

from oauth2_provider.contrib.rest_framework import OAuth2Authentication

""" utility """
from utility.response import ApiResponse
from utility.utils import (
    CreateRetrieveUpdateViewSet,
    date_filter,
    filter_array_list,
    get_ordered_queryset,
    get_pagination_resp,
    get_required_fields,
    transform_list,
    create_or_update_serializer,
)
from utility.constants import MESSAGES

""" model imports """
from ..models import Answers, Questions

""" serializers """
from ..serializers.answers_serializer import AnswersSerializer

''' swagger '''
from ..swagger.answers_swagger import (
    swagger_auto_schema_list,
    swagger_auto_schema_post,
    swagger_auto_schema,
    swagger_auto_schema_update,
    swagger_auto_schema_delete,
)


class AnswersView(CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = AnswersSerializer
    throttle_classes = [LiteRateLimit]
    
    singular_name = "Answer"
    model_class = Answers.objects.select_related("user", "question")
    search_fields = ["answer",]

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    @swagger_auto_schema
    def retrieve(self, request, *args, **kwargs):
        """
        :To get the single record
        """
        try:
            get_id = self.kwargs.get("id")

            if instance := self.get_object(get_id):
                view: str = request.query_params.get('view', 'short').lower()
                if view == 'detailed':
                    resp_dict = self.transform_single(instance)
                else:
                    resp_dict = self.transform(instance)
        
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + " not found")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=str(e))

    @swagger_auto_schema_post
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """
        :To create the new record
        """
        try:
            sp1 = transaction.savepoint()
            """capture data"""
            req_data: dict = request.data.copy()
            if not req_data:
                return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_are_required'])           

            # answer payload
            answer: str = req_data.get('answer')
            question_id: int = req_data.get('question')

            required_list = {"answer": answer, "question": question_id}
            if required_field := get_required_fields(required_list, req_data):
                return ApiResponse.response_bad_request(self, message=required_field)    

            # Check if question exists
            if not Questions.objects.filter(id=question_id).exists():
                return ApiResponse.response_not_found(self, message="Question does not exist.")

            req_data['user'] = request.user.id
            req_data['question'] = question_id

            answer_instance, error = create_or_update_serializer(AnswersSerializer, req_data, sp1)
            if error:
                return ApiResponse.response_bad_request(self, message=error)

            req_data['id'] = answer_instance.id
            transaction.savepoint_commit(sp1)
            return ApiResponse.response_created(self, data=req_data, message=self.singular_name + MESSAGES['created'])

        except Exception as e:
            print("Error creating ", traceback.format_exc())
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=str(e.args[0]))

    @swagger_auto_schema_update
    @transaction.atomic()
    def partial_update(self, request, *args, **kwargs):
        """
        :To update the existing record
        """
        sp1 = transaction.savepoint()
        """capture data"""
        req_data: dict = request.data.copy()

        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_are_required'])

        get_id = self.kwargs.get("id")
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])

        # answer payload   
        answer: str = req_data.get('answer')
        is_deleted: bool = req_data.get('is_deleted')
        question_id: int = req_data.get('question')

        
        if answer and len(answer.strip()) == 0:
            return ApiResponse.response_bad_request(self, message="Answer cannot be empty")
        elif answer:
            req_data['answer'] = answer.strip()

            
        if question_id:
            # Check if question exists
            if not Questions.objects.filter(id=question_id).exists():
                return ApiResponse.response_not_found(self, message="Question does not exist.")
            req_data['question'] = question_id

        req_data['user'] = request.user.id
        req_data['id'] = get_id
        answer_instance, error = create_or_update_serializer(AnswersSerializer, req_data, sp1, instance)
        if error:
            return ApiResponse.response_bad_request(self, message=error)

        """ success response """
        transaction.savepoint_commit(sp1)
        return ApiResponse.response_ok(self, data=req_data, message=self.singular_name + MESSAGES['updated'])

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        """
        :To get the all records
        """
        query_params: dict = request.query_params

        filter_array = {
            "is_deleted": "is_deleted"
        }
        obj_list = filter_array_list(filter_array, query_params)

        obj_list = date_filter(query_params, obj_list)

        if q_list := [Q(x) for x in obj_list]:
            queryset = self.model_class.filter(reduce(operator.and_, q_list))
        else:
            queryset = self.model_class

        """Search for keyword """
        if keyword := query_params.get('keyword'):
            queryset = queryset.filter(search_filter(self.search_fields, keyword))

        queryset = get_ordered_queryset(query_params, queryset, Answers)

        resp_data = get_pagination_resp(queryset, request)
        
        view: str = query_params.get('view', 'short').lower()
        
        response_data = transform_list(self, resp_data.get("data"), view)

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

    @swagger_auto_schema_delete
    def delete(self, request, *args, **kwargs):
        """
        :To delete the single record.
        """
        get_id = self.kwargs.get("id")
        """ get instance """
        instance = self.get_object(get_id)
        if instance is None:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])

        instance.delete()
        """ return success """
        return ApiResponse.response_ok(self, message=self.singular_name + MESSAGES['deleted'])

    @swagger_auto_schema
    def like(self, request, *args, **kwargs):
        """
        API to like or unlike an answer
        """
        answer_id = kwargs.get('id')
        try:
            answer = Answers.objects.get(id=answer_id)
            
            if request.user in answer.likes.all():
                answer.likes.remove(request.user)
                message = "Answer unliked successfully"
            else:
                answer.likes.add(request.user)
                message = "Answer liked successfully"
            
            return ApiResponse.response_ok(
                self, 
                data={"likes_count": answer.likes.count()}, 
                message=message
            )
        except Answers.DoesNotExist:
            return ApiResponse.response_not_found(self, message="Answer not found")
        except Exception as e:
            return ApiResponse.response_bad_request(self, message=str(e))

    # Generate the response
    def transform_single(self, instance):
        resp_dict = {}
        resp_dict = Answers.to_dict(instance)
        return resp_dict
    
    def transform(self, instance):
        return {
            'id': instance.id,
            'answer': instance.answer,
            'is_deleted': instance.is_deleted,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }