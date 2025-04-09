from rest_framework.permissions import BasePermission
from django.conf import settings
from django.core.exceptions import PermissionDenied
from quora_app.models import User
from utility.constants import COMPANY_ADMIN_ROLE, STATUS_ACTIVE, SUPER_ADMIN_ROLE, EMPLOYEE_ROLE


def is_model_permission(request, code_name):
    try:
        if not request.user.group:
            return False
        permissions = request.user.group.permissions.filter(codename=code_name)
        if permissions:
            return True
        else:
            return False
    except:
        return False

class is_super_admin(BasePermission):
    """
    check for super admin login or not
    """
    def has_permission(self, request, view):
        try:
            return request.user.group_id == settings.GRP_SUPER_ADMIN
        except:
            return False


class is_access(BasePermission):
    def has_permission(self, request, view):
        headers = settings.HEADERS
        # return request.META.get('HTTP_ACCESS_KEY') == headers
        return True

def is_only_company_admin(f):
    def validate(self, request, *args, **kwargs):
        if request.user.role_id != COMPANY_ADMIN_ROLE:
            raise PermissionDenied
        return f(self, request, *args, **kwargs)
    return validate

def is_super_admin_or_company_admin(f):
    def validate(self, request, *args, **kwargs):
        try:
            role_id = request.user.role_id
            if not role_id:
                raise PermissionDenied
            company_instance = None
            if role_id == COMPANY_ADMIN_ROLE:
                company_instance = request.user.company
            elif request.user.role_id == SUPER_ADMIN_ROLE:
                if company_id := get_company_id_from_request(request):
                    company_instance = Company.objects.filter(id=company_id).first()
            else:
                raise PermissionDenied
        except Exception as e:
            raise PermissionDenied
        return f(self, request, company_instance ,*args, **kwargs)
    return validate

def is_super_admin_or_company_admin_or_employee(f):
    def validate(self, request, *args, **kwargs):
        try:
            role_id = request.user.role_id
            if not role_id:
                raise PermissionDenied
            company_instance = None
            if role_id in [COMPANY_ADMIN_ROLE, EMPLOYEE_ROLE]:
                company_instance = request.user.company
            elif role_id == SUPER_ADMIN_ROLE:
                if company_id := get_company_id_from_request(request):
                    company_instance = Company.objects.filter(id=company_id).first()
            else:
                raise PermissionDenied
        except Exception:
            raise PermissionDenied
        return f(self, request, company_instance ,*args, **kwargs)
    return validate

def is_super_admin(f):
    def validate(self, request, *args, **kwargs):
        if request.user.role_id != SUPER_ADMIN_ROLE:
            raise PermissionDenied
        return f(self, request, *args, **kwargs)
    return validate

def is_super_admin_or_company_admin_or_accountant(f):
    def validate(self, request, *args, **kwargs):
        if not request.user.role_id:
            raise PermissionDenied
        company_instance = None
        if request.user.role_id in [EMPLOYEE_ROLE, COMPANY_ADMIN_ROLE]:
            employee_meta_instance = User.objects.filter(
                user_id=request.user.id,
                company__owner__status=STATUS_ACTIVE
            ).first()
            if not employee_meta_instance :
                raise PermissionDenied
            company_instance = employee_meta_instance.company

        elif request.user.role_id == SUPER_ADMIN_ROLE:
            # Company id if user is super admin 
            company_id = get_company_id_from_request(request)
            if company_id:
                company_instance = Company.objects.filter(
                    id=company_id, 
                    owner__status=STATUS_ACTIVE
                ).first()
        else:
            raise PermissionDenied
            
        return f(self, request, company_instance ,*args, **kwargs)
    return validate

def company_admin_or_employee(f):
    def validate(self, request, *args, **kwargs):
        if not request.user.role_id:
            raise PermissionDenied
        if request.user.role_id in [EMPLOYEE_ROLE, COMPANY_ADMIN_ROLE]:
            employee_meta_instance = User.objects.filter(
                user_id=request.user.id, 
                company__owner__status=STATUS_ACTIVE
            ).first()
            if not employee_meta_instance :
                raise PermissionDenied
            company_instance = employee_meta_instance.company
        else:
            raise PermissionDenied
            
        return f(self, request, company_instance ,*args, **kwargs)
    return validate


def is_super_admin_or_company_admin_or_executive(f):
    def validate(self, request, *args, **kwargs):
        if not request.user.role_id:
            raise PermissionDenied

        company_instance = None
        if  request.user.role_id in [EMPLOYEE_ROLE]:
            # Company instance if user is employee and has admin access
            employee_meta_instance = User.objects.filter(
                user_id=request.user.id, 
                company__owner__status=STATUS_ACTIVE
            ).first()
            if not employee_meta_instance :
                raise PermissionDenied
            company_instance = employee_meta_instance.company

        elif request.user.role_id == SUPER_ADMIN_ROLE:
            # Company id if user is super admin 
            company_id = get_company_id_from_request(request)
            if company_id:
                company_instance = Company.objects.filter(
                    id=company_id, 
                    owner__status=STATUS_ACTIVE
                ).first()
        else:
            raise PermissionDenied
        return f(self, request, company_instance ,*args, **kwargs)
    return validate

def is_company_admin(f):
    def validate(self, request, *args, **kwargs):
        if request.user.role_id != COMPANY_ADMIN_ROLE:
            raise PermissionDenied
        company_instance = None
        if request.user.role_id == COMPANY_ADMIN_ROLE:
            company_instance = Company.objects.filter(owner_id=request.user.id, owner__status=STATUS_ACTIVE).first()
            if not company_instance:
                raise PermissionDenied
        else:
            company_id=None
            if request.data.get('company_id'):
                company_id = request.data.get('company_id')
            elif request.query_params.get('company_id'):
                company_id = request.query_params.get('company_id')
            elif request.data.get('company'):
                company_id = request.data.get('company')
            elif request.query_params.get('company'):
                company_id = request.query_params.get('company')

            company_instance = Company.objects.filter(id=company_id, owner__status=STATUS_ACTIVE).first()

        return f(self, request, company_instance ,*args, **kwargs)
    return validate

def is_company_admin_or_manager_or_articaleship_or_executive(f):
    def validate(self, request, *args, **kwargs):
        if request.user.role_id not in [EMPLOYEE_ROLE]:
            raise PermissionDenied
        
        instance = None
        if request.user.role_id in [EMPLOYEE_ROLE]:
            if request.user.role_id == COMPANY_ADMIN_ROLE:
                company_instance = Company.objects.filter(owner_id=request.user.id, owner__status=STATUS_ACTIVE).first()
                if company_instance:
                    instance = User.objects.filter(company_id = company_instance.id).first()
            if not instance:
                raise PermissionDenied

        return f(self, request, instance ,*args, **kwargs)
    return validate

def is_only_company_admin_or_super_admin(f):
    def validate(self, request, *args, **kwargs):
        if request.user.role_id not in [SUPER_ADMIN_ROLE, COMPANY_ADMIN_ROLE]:
            raise PermissionDenied

        return f(self, request, *args, **kwargs)

    return validate

def get_company_id_from_request(request):
    company_id = None
    if isinstance(request.data, list):
        company_id = request.data[0].get('company_id')
    elif request.data.get('company_id'):
        company_id = request.data.get('company_id')
    elif request.query_params.get('company_id'):
        company_id = request.query_params.get('company_id')
    elif request.data.get('company'):
        company_id = request.data.get('company')
    elif request.query_params.get('company'):
        company_id = request.query_params.get('company')
    return company_id
