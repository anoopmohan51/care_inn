from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q,F
from workorder_api.models.informations import Informations
from workorder_api.serializers.information_serializer import InformationSerializer
from core_api.models.external_api_key import ExternalApiKey
from rest_framework import status


class InformationsDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def get(self, request, id):
        try:
            responce_data = Informations.objects.get(pk=id,is_delete=False)
            serializer = InformationSerializer(responce_data)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Information details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Informations.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Information not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Information details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )