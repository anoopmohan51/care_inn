from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models import WorkOrderRating
from workorder_api.serializers.workorder_rating_serializer import WorkOrderRatingSerializer
from rest_framework import status
from core_api.models.external_api_key import ExternalApiKey
from rest_framework.permissions import AllowAny
from core_api.permission.external_api_permission import HasValidApiKey


class WorkOrderRatingView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderRatingSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order rating created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order rating creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order rating creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

