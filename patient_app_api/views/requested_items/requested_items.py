from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q,F
from workorder_api.models.requested_items import RequestedItems
from workorder_api.serializers.item_serializer import ItemSerializer
from core_api.models.external_api_key import ExternalApiKey
from rest_framework import status

class RequestedItemsDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]
    
    def get(self, request, id):
        try:
            responce_data = RequestedItems.objects.get(id=id,is_delete=False)
            serializer = ItemSerializer(responce_data)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Requested items details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except RequestedItems.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Requested items not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Requested items details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )