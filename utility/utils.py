import re
import requests
from random import randint
from cryptography.fernet import Fernet
from datetime import datetime, timedelta, timezone
# from stark_utilities.utilities import *
from quora.tasks import app
import traceback

from django.conf import settings
from django.db import transaction
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings


""" mixins to handle request url """
class CreateRetrieveUpdateViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    pass


class MultipleFieldPKModelMixin(object):
    """
    Class to override the default behaviour for .get_object for models which have retrieval on fields
    other  than primary keys.
    """
    lookup_field = []
    lookup_url_kwarg = []

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        get_args = {field: self.kwargs[field] for field in self.lookup_field if field in self.kwargs}

        get_args.update({"pk": self.kwargs[field] for field in self.lookup_url_kwarg if field in self.kwargs})
        return get_object_or_404(queryset, **get_args)


""" login response """
def get_login_response(user=None, token=None):
    resp_dict = dict()
    resp_dict["id"] = user.id
    resp_dict["first_name"] = user.first_name
    resp_dict["last_name"] = user.last_name
    resp_dict["email"] = user.email
    resp_dict["mobile"] = user.mobile
    resp_dict["username"] = user.username
    # resp_dict["group"] = user.group_id
    return resp_dict

# def send_common_email(subject, message, email_to, from_emails):
#     try:
#         msg = EmailMessage(subject, message, to=[email_to], from_email=from_emails)
#         msg.content_subtype = "html"
#         msg.send()
#     except:
#         pass

@app.task
def send_common_email(subject: str, message, to_email, cc=[], attachment=None):
    try:
        from_emails: str = settings.FROM_EMAIL
        email = EmailMessage(subject, message, to=to_email, cc=cc, from_email=from_emails)
        if attachment:
            response = requests.get(attachment, timeout=15)
            email.attach("Letter", response.content, mimetype="application/pdf")

        email.content_subtype = "html"
        email.send()
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f"Could not send email \n{str(e)}")
    

def get_otp_expirity(expiry_time=15):
    """ set otp expiry time """
    return timezone.now() + timedelta(minutes=expiry_time)

def is_valid_email(email):
    """Validate email format using a regex pattern."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def generate_token(request, user):
    expire_seconds = oauth2_settings.user_settings["ACCESS_TOKEN_EXPIRE_SECONDS"]

    scopes = oauth2_settings.user_settings["SCOPES"]

    application = Application.objects.first()
    expires = datetime.now() + timedelta(seconds=expire_seconds)
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token=random_token_generator(request),
        expires=expires,
        scope=scopes,
    )

    refresh_token = RefreshToken.objects.create(
        user=user, token=random_token_generator(request), access_token=access_token, application=application
    )

    token = {
        "access_token": access_token.token,
        "token_type": "Bearer",
        "expires_in": expire_seconds,
        "refresh_token": refresh_token.token,
        "scope": scopes,
    }
    return token

def revoke_oauth_token(request):
    """ revoke token """
    try:
        client_id = settings.CLIENT_ID
    except:
        raise Exception('Add CLIENT_ID in settings.')

    try:
        client_secret = settings.CLIENT_SECRET
    except:
        raise Exception('Add CLIENT_SECRET in settings.')
    
    try:
        SERVER_PROTOCOLS = settings.SERVER_PROTOCOLS
    except:
        raise Exception('Add SERVER_PROTOCOLS in settings.')

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "token": request.META["HTTP_AUTHORIZATION"][7:],
        "token_type_hint": "access_token",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # host request
    host = request.get_host()
    response = requests.post(
        SERVER_PROTOCOLS + host + "/o/revoke_token/", data=payload, headers=headers
    )
    return response

def get_pagination_resp(data, request):
    query_params: dict = request.query_params
    if query_params.get('type') == 'all':
        return {"data": data}
    page = query_params.get('page', 1)
    limit = query_params.get('limit', settings.PAGE_SIZE)
    paginator = Paginator(data, limit)
    category_data = paginator.get_page(page).object_list
    page_response = {"total_count": paginator.count, "total_pages": paginator.num_pages, "current_page": page, "limit": limit}
    current_page = paginator.num_pages
    paginator = {"paginator": page_response}
    if int(current_page) < int(page):
        return {"data": [], "paginator": paginator.get('paginator')}
    return {"data": category_data, "paginator": paginator.get('paginator')}

def transform_list(self, data, view: str = "short"):
    try:
        if view.lower() == "detailed":
            return map(self.transform_single, data)
        else:
            return map(self.transform, data)
    except Exception:
        return None
    
def get_serielizer_error(serializer, with_key=False):
    """handle serializer error"""
    msg_list = []
    try:
        mydict = serializer.errors
        for key in sorted(mydict.keys()):
            msg = ""

            if with_key:
                msg = key + " : "

            msg += str(mydict.get(key)[0])

            msg_list.append(msg)
    except:
        msg_list = ["Invalid format"]
    return msg_list

def create_or_update_serializer(serializer_class, data, savepoint=None, instance=None):
    if instance:
        serializer = serializer_class(instance, data=data, partial=True)
    else:
        serializer = serializer_class(data=data)

    if serializer.is_valid():
        serializer.save()
        return  serializer.instance, None
    print("serializer : ", serializer.errors)
    if savepoint:
        transaction.savepoint_rollback(savepoint)

    return None, get_serielizer_error(serializer)

def generate_otp_number():
    range_start = 10 ** (settings.OTP_LENGTH - 1)
    range_end = (10 ** settings.OTP_LENGTH) - 1
    return randint(range_start, range_end)

def filter_array_list(filter_array: dict, where_array: dict, obj_list: list = []):
    for key, value in filter_array.items():
        if key in where_array.keys():
            val = where_array[key]
            obj_list.append((value, val))
    return obj_list

def date_filter(where_array: dict, obj_list: list = []):
    start_date = where_array.get('start_date')
    end_date = where_array.get('end_date')
    if start_date and end_date:
        from datetime import datetime
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = datetime.combine(end_date, datetime.max.time())
        obj_list.append(['created_at__range', [start_date, end_date]])

    elif start_date:
        obj_list.append(['created_at__startswith', start_date])

    elif end_date:
        obj_list.append(['created_at__startswith', end_date])

    return obj_list

def validate_list_enum_fields(validations, obj_list: list):
    for value, valid_set, key in validations:
        if value:
            if not int(value) in valid_set:
                return obj_list, f"Invalid {key.replace('_', ' ')}."
            else:
                obj_list.append([f'{key}__in', [value]])
    return obj_list, None

def get_sort_direction(query_params: dict):
    sort_by = query_params.get('sort_by', 'id')
    sort_direction = query_params.get('sort_direction', 'ascending')
    if sort_direction == 'descending':
        return f'-{sort_by}'
    return sort_by

def get_field_type(model, field):
    try:
        field = model._meta.get_field(field)
        if field in model._meta.fields:
            return type(field).__name__
    except Exception:
        return None
    
def ordering(model, field):
    """ Checks if the given field in the model supports case-insensitive ordering."""
    return get_field_type(model, field) in ['CharField', 'TextField', 'EmailField', 'SlugField', 'URLField', 'GenericIPAddressField']

def get_ordered_queryset(query_params: dict, queryset, model):
    sort_by = get_sort_direction(query_params)
    if ordering(model, sort_by):
        queryset = queryset.order_by(Lower(sort_by))
    else:
        queryset = queryset.order_by(sort_by)
    return queryset

def decrypt(text: bytes) -> str:
    cipher_suite = Fernet(settings.S_KEY)
    decrypted_bytes = cipher_suite.decrypt(text)
    decrypted_text = decrypted_bytes.decode("utf-8")
    return decrypted_text

def encrypt(text: str):
    cipher_suite = Fernet(settings.S_KEY)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text

def get_required_fields(data_dict: dict, req_data: dict):
    for key, value in data_dict.items():
        if not key in req_data:
            return f"{key.replace('_', ' ').capitalize()} is required."
        elif value and not str(value).strip():
            return f"{key.replace('_', ' ').capitalize()} is required."
        elif not str(value):
            return f"{key.replace('_', ' ').capitalize()} is required."

def get_required_fields(data_dict: dict, req_data: dict):       
    for key, value in data_dict.items():
        if not key in req_data:
            return f"{key.replace('_', ' ').capitalize()} is required."
        elif value and not str(value).strip():
            return f"{key.replace('_', ' ').capitalize()} is required."
        elif not str(value):
            return f"{key.replace('_', ' ').capitalize()} is required."

def validate_url(base_url):
    validator = URLValidator()
    try:
        validator(base_url)
    except ValidationError:
        return "Error"

def validate_strings_data(data_dict, req_data):
    for key, value in data_dict.items():
        if not key in req_data:
            pass
        elif value and not str(value).strip():
            return f"{key.replace('_', ' ').capitalize()} cannot be empty."
        elif not value:
            return f"{key.replace('_', ' ').capitalize()} cannot be empty."
        
        elif value.replace(' ', '') and not value.replace(' ', '').isalpha():
                return f"{key.replace('_', ' ').capitalize()} should not contain special characters."

def validate_enum_fields(validations):
    for value, valid_set, error_message in validations:
        if value and value not in valid_set:
            return f"Invalid {error_message}."

def validate_empty_strings(data_dict, req_data):
    for key,value in data_dict.items():
        if not key in req_data:
            pass
        elif value and not str(value).strip():
            return f"{key.replace('_', ' ').capitalize()} cannot be empty."
        elif not value:
            return f"{key.replace('_', ' ').capitalize()} cannot be empty."

