from rest_framework.views import APIView
from core_api.serializers.tenant_serializer import TenantSerializer
from core_api.serializers.user_serializer import UserSerializer
from core_api.models.tenant import Tenant
from core_api.models.role import Role
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.custom_error_message import get_message
from rest_framework.exceptions import ValidationError

class TenantCreateView(APIView):
    def post(self, request):
        try:
            data=request.data
            email = data.get('email')
            name = data.get('name')
            password = "Tenant@123"
            serializer = TenantSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                role,created = Role.objects.get_or_create(
                    name="SUPERADMIN",
                    description="SUPERADMIN",
                    status=True,
                    is_delete=False
                )
                user_data = {
                    "email": email,
                    "password": password,
                    "first_name": name,
                    "last_name": None,
                    "role": role.id if role else None,
                    "tenant": serializer.data.get('id',None),
                    "is_delete": False
                }
                user_serializer = UserSerializer(data=user_data, context={'request': request})
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
                    return CustomResponse(
                        data=serializer.data,
                        status="success",
                        message=["Tenant created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )
        except ValidationError as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=get_message(self,e),
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[str(e)],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )