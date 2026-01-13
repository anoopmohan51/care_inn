from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.serializers.room_type_serializer import RoomTypeSerializer
from workorder_api.models import RoomTypes,FloorPlan
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.permission.permission import has_permission
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q,Value
from django.db.functions import Concat


class RoomTypesCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("RoomTypes", "create")
    def post(self, request):
        try:
            data = request.data
            floor_plan = data.get('floor_plan',[])
            serializer = RoomTypeSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                responce_data = serializer.data
                return CustomResponse(
                    data=responce_data,
                    status="success",
                    message=["Room types created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Room types creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Room types creation failed"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoomTypesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("RoomTypes", "read")
    def get(self, request, pk):
        try:
            room_type = RoomTypes.objects.get(id=pk,is_delete=False)
            if not room_type:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Room type not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = RoomTypeSerializer(room_type)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Room type details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room type details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("RoomTypes", "update")
    def put(self, request, pk):
        try:
            data = request.data
            room_type = RoomTypes.objects.get(id=pk,is_delete=False)
            serializer = RoomTypeSerializer(room_type, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Room type updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Room type updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room type updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    # @has_permission("RoomTypes", "delete")
    def delete(self, request, pk):
        try:
            room_type = RoomTypes.objects.get(id=pk,is_delete=False)
            if not room_type:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Room type not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            room_type.is_delete = True
            room_type.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Room type deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room type deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RoomTypesFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # @has_permission("RoomTypes", "filter")
    def post(self, request):
        try:
            data = request.data
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
                RoomTypes,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=RoomTypeSerializer)
            return CustomResponse(
                data={
                    "data": queryset,
                    "count": count
                },
                status="success",
                message=["Room types filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Room types filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
