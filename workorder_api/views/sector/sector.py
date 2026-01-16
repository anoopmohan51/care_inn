from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models import Sector
from workorder_api.serializers.sector_serializer import SectorSerializer
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from core_api.permission.permission import has_permission
from rest_framework import status

class SectorCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Sector", "create")

    def post(self, request):
        try:
            data = request.data
            serializer = SectorSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Sector created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Sector creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Sector creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class SectorDetailsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Sector", "read")

    def get(self, request, pk):
        try:
            sector = Sector.objects.get(id=pk,is_delete=False)
            serializer = SectorSerializer(sector)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Sector details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Sector.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Sector not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
    
    def put(self, request, pk):
        try:
            data = request.data
            sector = Sector.objects.get(id=pk,is_delete=False)
            if not sector:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Sector not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = SectorSerializer(sector, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Sector updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Sector updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Sector updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def delete(self, request, pk):
        try:
            sector = Sector.objects.get(id=pk,is_delete=False)
            if not sector:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Sector not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            sector.is_delete = True
            sector.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Sector deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Sector deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class SectorFilterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Sector", "read")
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
                Sector,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=SectorSerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Sectors filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Sectors filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )