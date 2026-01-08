from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q,Count
from rest_framework import status
from core_api.models.usergroups import UserGroup,UserGroupUsers
from core_api.serializers.usergroup_serializer import UserGroupSerializer
from ..user_group.usergroup_utils.user_group_utils import UserGroupUsersService
from core_api.permission.permission import has_permission

class UserGroupCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Usergroup", "create")
    def post(self, request):
        try:
            data=request.data
            serializer = UserGroupSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if 'users' in data:
                    UserGroupUsersService().get_user_group_users(data['users'],serializer.data['id'])
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User group created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class UserGroupDetialsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Usergroup", "read")
    def get(self, request,pk):
        try:
            user_group = UserGroup.objects.get(id=pk,is_delete=False)
            serializer = UserGroupSerializer(user_group)
            data = serializer.data
            data['users'] = UserGroupUsersService().get_user_group_users_list(user_group.id)

            return CustomResponse(
                data=data,
                status="success",
                message=["User group details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except UserGroup.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"User group not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("Usergroup", "update")
    def put(self,request,pk):
        try:
            data=request.data
            user_group = UserGroup.objects.get(id=pk,is_delete=False)
            serializer = UserGroupSerializer(user_group, data=data,context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if 'users' in data:
                    UserGroupUsersService().get_user_group_users(data['users'],serializer.data['id'])
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User group updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            return CustomResponse(
                data=serializer.errors,
                status="failed",
                message=["Error in User group updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except UserGroup.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"User group not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    # @has_permission("UsUsergrouper", "update")
    def patch(self,request,pk):
        try:
            data=request.data
            user_group = UserGroup.objects.get(id=pk,is_delete=False)
            serializer = UserGroupSerializer(user_group, data=data, partial=True,context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if 'users' in data:
                    UserGroupUsersService().get_user_group_users(data['users'],serializer.data['id'])
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User group updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            return CustomResponse(
                data=serializer.errors,
                status="failed",
                message=["Error in User group updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except UserGroup.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"User group not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    # @has_permission("Usergroup", "delete")   
    def delete(self,request,pk):
        try:
            user_group = UserGroup.objects.get(id=pk,is_delete=False)
            UserGroupUsersService().delete_whole_user_group(user_group.id)
            user_group.is_delete = True
            user_group.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["User group deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except UserGroup.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"User group not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class UserGroupFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Usergroup", "read")
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
                UserGroup, 
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result(
                created_user_name = F('created_user__first_name'),
                members_count = Count('user_group_users')
            )
            return CustomResponse(
                data=queryset,
                status="success",
                message=["User group list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
class UserGroupUsersDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Usergroup", "update")
    def delete(self,request,pk):
        try:
            UserGroupUsers.objects.filter(id=pk).delete()
            return CustomResponse(
                data=None,
                status="success",
                message=["User group deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User group deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    