from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q,F
from workorder_api.models import WorkOrderTemp
from workorder_api.serializers.workorder_temp_serializer import WorkOrderTempSerializer
from core_api.models.external_api_key import ExternalApiKey
from rest_framework import status

class WorkorderDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def get(self, request, id):
        try:
            workorder = WorkOrderTemp.objects.get(id=id,is_delete=False)
            serializer = WorkOrderTempSerializer(workorder)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Workorder details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except WorkOrderTemp.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Workorder not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Workorder details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )


class WorkorderFilterView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def post(self, request):
        try:
            api_key = request.headers.get('X-API-KEY')
            mrd_id = request.query_params.get('mrd_id')
            room_number = request.query_params.get('room_number')
            external_api_key = ExternalApiKey.objects.get(key=api_key,is_active=True)
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
                WorkOrderTemp,
                base_filter=Q(tenant=external_api_key.tenant,mrd_id=mrd_id,room__room_number=room_number,is_delete=False,is_approved=True),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderTempSerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=[f"Workorder filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Workorder filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )