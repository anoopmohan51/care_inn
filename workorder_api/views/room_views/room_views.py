from ...serializers.room_serializer import RoomSerializer
from ...models import Rooms
from core_api.response_utils.custom_response import CustomResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from core_api.permission.permission import has_permission

class RoomCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Room", "create")
    def post(self, request):
        try:
            data=request.data
            serializer = RoomSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Room creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoomUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Room", "read")
    def get(self, request,pk):
        try:
            room = Rooms.objects.get(id=pk,is_delete=False)
            if not room:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=[f"Room not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = RoomSerializer(room)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Room fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )   
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    # @has_permission("Room", "update")
    def put(self, request,pk):
        try:
            data=request.data
            room = Rooms.objects.get(id=pk,is_delete=False)
            serializer = RoomSerializer(room, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Room updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("Room", "update")
    def patch(self, request,pk):
        try:
            data=request.data
            room = Rooms.objects.get(id=pk,is_delete=False)
            serializer = RoomSerializer(room, data=data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room updated successfully"],
                        status_code=status.HTTP_200_OK,
                        content_type="application/json"
                    )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Room updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    # @has_permission("Room", "delete")
    def delete(self, request,pk):
        try:
            room = Rooms.objects.get(id=pk,is_delete=False)
            room.is_delete = True
            room.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Room deleted successfully"],
                status_code=status.HTTP_204_NO_CONTENT,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoomFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Room", "read")
    def post(self, request):
        try:
            field_lookup = {
                "id": "id",
                "name": "name",
                "description": "description",
                "created_at": "created_at",
                "updated_at": "updated_at"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                Rooms,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result(
                created_user_name = F('created_user__first_name'),
            )
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Rooms filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Rooms filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )