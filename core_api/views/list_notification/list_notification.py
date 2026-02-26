from rest_framework.views import APIView
from rest_framework import status
from core_api.response_utils.custom_response import CustomResponse
from core_api.models.fcm_log import FcmPushLog
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.permission.permission import has_permission
from rest_framework.permissions import IsAuthenticated

class ListNotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,user_id):
        try:
            if not user_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["User id is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            limit = request.query_params.get('limit',10)
            offset = request.query_params.get('offset',0)
            notifications = FcmPushLog.objects.filter(user_id=user_id).values('id','push_data','created_at').order_by('-created_at')[offset:offset+limit]
            return CustomResponse(
                data=notifications,
                status="success",
                message=["Notifications fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in fetching notifications"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )