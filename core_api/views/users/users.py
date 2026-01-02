from ...models import AppUsers
from rest_framework.response import Response
from rest_framework import generics,status
from ...serializers.user_serializer import UserSerializer
from ...response_utils.custom_response import CustomResponse
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
from core_api.permission.permission import has_permission


class UserCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("User", "create")
    def post(self, request):
        try:
            data=request.data
            serializer = UserSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            return Response(
                data=serializer.errors,
                status="failed",
                message=["User creation failed"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("User", "read")
    def get(self, request,pk):
        try:
            user = AppUsers.objects.get(id=pk,is_delete=False)
            serializer = UserSerializer(user)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["User fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("User", "update")
    def put(self, request,pk):
        try:
            user = AppUsers.objects.get(id=pk,is_delete=False)
            serializer = UserSerializer(user, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            return CustomResponse(
                data=serializer.errors,
                status="failed",
                message=["Error in User updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("User", "update")
    def patch(self, request,pk):
        try:
            user = AppUsers.objects.get(id=pk,is_delete=False)
            serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["User updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            return CustomResponse(
                data=serializer.errors,
                status="failed",
                message=["Error in User updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("User", "delete")
    def delete(self, request,pk):
        try:
            user = AppUsers.objects.get(id=pk,is_delete=False)
            user.is_delete = True
            user.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["User deleted successfully"],
                status_code=status.HTTP_204_NO_CONTENT,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class UserResetPasswordView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("User", "update")
    def post(self, request,pk):
        try:
            data = request.data
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')
            request_user_id=request.user.id
            if request_user_id != pk:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["You are not authorized to reset this password"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if new_password != confirm_password:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Password and Confirm Password do not match"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            user = get_user_model().objects.get(id=pk)
            user.set_password(new_password)
            user.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Password reset successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Password resetting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class UserFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @has_permission("User", "view")
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
                AppUsers,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result()
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Users filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Users filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )