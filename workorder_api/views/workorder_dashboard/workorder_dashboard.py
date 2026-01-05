from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.permission import has_permission
from workorder_api.views.workorder_dashboard.workorder_type_count import get_workorder_type_count
from rest_framework import status

class WorkOrderTypeDashboardCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # try:
            data = request.data
            tenant = request.user.tenant.id
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if not start_date or not end_date:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Start date and end date are required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            workorder_type_count = get_workorder_type_count(tenant,start_date,end_date)
            return CustomResponse(
                data=workorder_type_count,
                status="success",
                message=["Work order type count fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        # except Exception as e:
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=["Error in Work order type count fetching"],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )


            