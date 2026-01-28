from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q
from workorder_api.models.workorder_temp import WorkOrderTemp
from workorder_api.serializers.workorder_temp_serializer import WorkOrderTempSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.models.external_api_key import ExternalApiKey
class WorkorderListApprovalView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def post(self, request):
        try:
            api_key = request.headers.get('X-API-KEY')
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
                base_filter=Q(tenant=external_api_key.tenant,is_delete=False,is_approved=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderTempSerializer)
            return CustomResponse(
                data={
                    "data": queryset,
                    "total_count": count
                },
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