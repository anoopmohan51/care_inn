from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core_api.models.user_device_details import UserDeviceDetails
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.serializers.user_device_details_serializer import UserDeviceDetailsSerializer

class UserDeviceDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # try:
            data = request.data
            user = request.user.id
            source = data.get('source')
            device_id = data.get('device_id')
            is_logged_in = data.get('is_logged_in')
            data.update({'user':user})
            flag = False
            if not user:
                return CustomResponse(
                        data=None,
                        status="failed",
                        message=["User is required"],
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json"
                )
            if not device_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Device ID is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if not source:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Source is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if not UserDeviceDetails.objects.filter(user=user, device_id=device_id).exists():
                serializer = UserDeviceDetailsSerializer(data=data,context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    flag = True
            else:
                user_device_details = UserDeviceDetails.objects.get(user=user, device_id=device_id)
                serializer = UserDeviceDetailsSerializer(user_device_details,data=data,context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    flag = True
            if flag:
                return CustomResponse(
                    data=None,
                    status="success",
                    message=["User device details updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["User device details not updated"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        # except Exception as e:
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=[str(e)],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )




