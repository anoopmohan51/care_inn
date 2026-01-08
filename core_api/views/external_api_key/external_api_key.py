from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.models.external_api_key import ExternalApiKey
from rest_framework import status
from core_api.serializers.external_api_key_serializer import ExternalApiKeySerializer
import uuid

class ExternalApiKeyCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            tenant = request.user.tenant
            if not name:
                return CustomResponse(
                    status="failed",
                    message=["Name is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            data.update({
                'key': str(uuid.uuid4())
            })
            if ExternalApiKey.objects.filter(name=name,tenant=tenant,is_active=True).exists():
                return CustomResponse(
                    status="failed",
                    message=["External API key already exists"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            serializer = ExternalApiKeySerializer(data=data,context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    status="success",
                    message=["External API key created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    status="failed",
                    message=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                status="failed",
                message=["Error in External API key creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )