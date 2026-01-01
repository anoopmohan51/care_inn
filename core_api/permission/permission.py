from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from core_api.models.role_permission import RolePermission
from core_api.response_utils.custom_response import CustomResponse

def has_permission(permission_name,permission_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user=request.user
            if user.is_superuser:
                return func(self, request, *args, **kwargs)
            filter_data={
                "permission__name":permission_name,
                "role":user.role 
            }
            if permission_type=="create":
                filter_data.update(
                    create=True
                )
            elif permission_type=="view":
                filter_data.update(
                    view=True
                )
            elif permission_type=="edit":
                filter_data.update(
                    edit=True
                )
            elif permission_type=="delete":
                filter_data.update(
                    delete=True
                )
            else:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Invalid permission type"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if not RolePermission.objects.filter(**filter_data).exists():
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Permission denied"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator