from rest_framework.views import APIView
from core_api.permission.external_api_permission import HasValidApiKey
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.views.folder_details.folder_details_query import _get_folder_details
from workorder_api.serializers.workorder_settings_serializer import FolderSerializer
from rest_framework.permissions import AllowAny
from workorder_api.models.folder import Folder

class FolderDetailsView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]

    def get(self, request, id):
        try:
            limit = request.query_params.get('limit', 10)
            offset = request.query_params.get('offset', 0)
            folder = Folder.objects.get(id=id)
            if not folder:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=[f"Folder not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = FolderSerializer(folder)
            responce_data = serializer.data
            responce_data['type'] = 'FOLDER'
            responce_data['items'] = _get_folder_details(id,limit,offset)
            return CustomResponse(
                data=responce_data,
                status="success",
                message=[f"Folder details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Folder details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
