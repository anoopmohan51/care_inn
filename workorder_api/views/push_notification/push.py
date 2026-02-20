from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.fcm_push_notification.send_push import send_push_notification
from django.utils import timezone

class PushNotificationView(APIView):

    def post(self, request):
        try:
            data = request.data
            device_tokens = data.get('device_tokens')
            title = "Test Notification"
            body = "This is a test notification"
            data = {
                'activity':'TEST_NOTIFICATION',
                'time_stamp':timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            send_push_notification(device_tokens,title,body,data)
            return CustomResponse(
                data=None,
                status="success",
                message=["Push notification sent successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print(e)
            return CustomResponse(
                data=None,
                status="error",
                message=["Error in sending push notification"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
