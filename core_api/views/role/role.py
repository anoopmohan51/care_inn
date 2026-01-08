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
from core_api.permission_utils.role_permission_utils import _create_update_role_permission
from core_api.filters.constants import FILTER_CONDITION_LOOKUP

class RoleCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            permission_data=data.pop('permissions')
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
                role_data = serializer.data
                role_data['permissions'] = _create_update_role_permission(serializer.data.get('id'),permission_data)

                return CustomResponse(
                    data=role_data,
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
        except Role.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Role not found"],
                status_code=status.HTTP_404_NOT_FOUND,
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
            permission_data=data.pop('permissions')
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
                role_data = serializer.data
                role_data['permissions'] = _create_update_role_permission(serializer.data.get('id'),permission_data)
                return CustomResponse(
                    data=role_data,
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
        except Role.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Role not found"],
                status_code=status.HTTP_404_NOT_FOUND,
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
        except Role.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Role not found"],
                status_code=status.HTTP_404_NOT_FOUND,
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
                "name": "name"
            }

            data = request.data
            filters = data.get('filters',[])
            sort_by = data.get('sort_by',[])
            limit = int(request.query_params.get('limit',10))
            offset = int(request.query_params.get('offset',0))
            filter_query = Q(is_delete=False)
            if filters:
                filter_condition = filters[0].get('conditions')
                for condition in filter_condition:
                    column = field_lookup.get(condition.get('colname'))
                    lookup = FILTER_CONDITION_LOOKUP.get(condition.get('condition'))
                    key = column if lookup is None else f"{column}__{lookup}"
                    value = condition.get('value')
                    if lookup == "isnull":
                        filter_query &= Q(**{key:bool(value)})
                    elif lookup is None:
                        filter_query &= ~Q(**{key:value})
                    else:
                        filter_query &= Q(**{key:value})
            if sort_by:
                sort_args = sort_by[0].get('colname')
                sort_query = sort_args.desc(nulls_last=True) if sort_by[0].get('direction') == "desc" else sort_args
            else:
                sort_query = "-created_at"
            queryset = Role.objects.exclude(name__exact="SUPERADMIN").filter(filter_query).order_by(sort_query)
            serializer = RoleSerializer(queryset[offset:offset+limit], many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Role list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Role filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )