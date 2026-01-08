from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.permission import has_permission
from rest_framework import status
from datetime import datetime, timedelta
from workorder_api.views.workorder_dashboard.workorder_count_per_day import get_workorder_count_per_day

class WorkOrderPerDayView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            days = request.query_params.get('filter_type',10)
            tenant = request.user.tenant.id
            workorder_per_day = get_workorder_count_per_day(tenant,days)
            return CustomResponse(
                data=workorder_per_day,
                status="success",
                message=["Work order per day fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order per day fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        