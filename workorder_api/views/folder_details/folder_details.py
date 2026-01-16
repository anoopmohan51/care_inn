from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models.folder import Folder
from rest_framework import status
from workorder_api.views.folder_details.folder_details_query import _get_folder_details

class FolderDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            data = _get_folder_details(request.user.tenant.id,id)
            return CustomResponse(
                data=data,
                status="success",
                message=[f"Folder details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("Error in Folder details fetching::::::::::",str(e))
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Folder details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )