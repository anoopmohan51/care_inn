from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q,F
from workorder_api.models.services import Services
from workorder_api.serializers.service_serializer import ServiceSerializer
from core_api.models.external_api_key import ExternalApiKey



class ServiceDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]
    
    def get(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Service fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Services.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Service not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class ServiceFilterView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def post(self, request):
        try:
            api_key = request.headers.get('X-API-KEY')
            external_api_key = ExternalApiKey.objects.get(key=api_key,is_active=True)
            field_lookup = {
                "id": "id",
                "name": "name",
                "description": "description",
                "created_at": "created_at",
                "updated_at": "updated_at"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                Services,
                base_filter=Q(tenant=external_api_key.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result(
                created_user_name = F('created_user__first_name'),
            )
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Services filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("error:::::::",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )



