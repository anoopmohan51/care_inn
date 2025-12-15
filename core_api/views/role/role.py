from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.serializers.role_serializer import RoleSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.models.role import Role
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from core_api.custom_error_message import get_message

class RoleCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            if Role.objects.filter(name=data['name'],is_delete=False).exists():
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Role with this name already exists"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            serializer = RoleSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Role created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Role creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
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
                message=["Error in Role creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoleDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request,pk):
        try:
            role = Role.objects.get(id=pk,is_delete=False)
            serializer = RoleSerializer(role)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Role details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Role details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def put(self, request,pk):
        try:
            data=request.data
            if Role.objects.exclude(id=pk).filter(name=data['name'],is_delete=False).exists():
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Role with this name already exists"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            role = Role.objects.get(id=pk,is_delete=False)
            serializer = RoleSerializer(role, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Role updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Role updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None, 
                status="failed",
                message=["Error in Role updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self, request,pk):
        try:
            role = Role.objects.get(id=pk,is_delete=False)
            role.is_delete = True
            role.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Role deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Role deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoleFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            field_lookup = {
                "id": "id",
                "name": "name",
                "description": "description",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "status": "status"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                Role,
                base_filter=Q(is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=RoleSerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Role list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("error:::::::::::",e.args[0])
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Role filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )