from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.views.workorder_summary.workorder_summary_query import _get_workorder_summary

class WorkorderSummaryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,workorder_id):
        try:
            tenant_id=request.user.tenant_id
            workorder_summary = _get_workorder_summary(tenant_id,workorder_id)
            return CustomResponse(
                data=workorder_summary,
                status="success",
                message=["Workorder summary fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Workorder summary fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )