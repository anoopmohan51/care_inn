from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.models.folder import Folder
from workorder_api.serializers.workorder_settings_serializer import FolderDetailsListSerializer
from rest_framework.permissions import AllowAny
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsListSerializer
from core_api.models.external_api_key import ExternalApiKey

class WorkorderSettingsDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def get(self, request, id):
        try:
            folder = Folder.objects.get(id=id)
            serializer = FolderDetailsListSerializer(folder)
            responce_data = serializer.data
            return CustomResponse(
                data=responce_data,
                status="success",
                message=[f"WorkOrderSettings details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Folder.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Folder not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )   
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderSettings details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkorderSettingsFilterView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def post(self, request):
        try:
            api_key = request.headers.get('X-API-KEY')
            external_api_key = ExternalApiKey.objects.get(key=api_key,is_active=True)
            field_lookup = {
                "id": "id",
                "name": "name",
                "icon": "icon",
                "created_at": "created_at",
                "updated_at": "updated_at"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrderSettings,
                base_filter=Q(tenant=external_api_key.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderSettingsListSerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=[f"WorkOrderSettings filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("error:::::::",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderSettings filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    