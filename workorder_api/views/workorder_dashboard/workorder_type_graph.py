from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.views.workorder_dashboard.workorder_type_count_perweekdays import get_workorder_type_count_perweekdays

class WorkOrderTypeGraphView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tenant = request.user.tenant.id
            workorder_type_count_perweekdays = get_workorder_type_count_perweekdays(tenant)
            return CustomResponse(
                data=workorder_type_count_perweekdays,
                status="success",
                message=["Work order type count per weekdays fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order type count per weekdays fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )