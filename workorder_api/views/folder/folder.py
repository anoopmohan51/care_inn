from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import Folder
from workorder_api.serializers import FolderSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.permission.permission import has_permission

class FolderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Folder", "create")
    def post(self, request):
        try:
            data = request.data
            serializer = FolderSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Folder created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Folder creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Folder creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class FolderListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Folder", "list")
    def get(self, request):
        try:
            folders = Folder.objects.filter(is_delete=False)
            serializer = FolderSerializer(folders, many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Folders fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Folder list fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    def delete(self, request, folder_id):
        try:
            folder = Folder.objects.get(id=folder_id)
            folder.is_delete = True
            folder.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Folder deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Folder deletion"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )