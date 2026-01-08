from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.views.workorder_dashboard.workorder_time_query import get_workorder_time_query

class WorkOrderTimeView(APIView):
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
            workorder_time = get_workorder_time_query(tenant,start_date,end_date)
            return CustomResponse(
                data=workorder_time,
                status="success",
                message=["Work order time fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        # except Exception as e:
        #     print("error",e)
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=["Error in Work order time fetching"],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )