from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models.workorder import WorkOrderImages
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from staticfiles_api.models import StaticFiles
from staticfiles_api.views.static_files.tempfile_to_permanant import tempfile_to_permanant
from workorder_api.serializers.workorder_image_upload_serializer import WorkOrderImageUploadSerializer
from pathlib import Path
import os
from django.conf import settings

class WorkOrderImageUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            workorder_id = data.get('workorder_id')
            files_list = data.get('files', [])
            if not workorder_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Workorder ID is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            workorder_images =[
                    {
                    'workorder':workorder_id,
                        'image':file
                    } for file in files_list
                ]
            serializer = WorkOrderImageUploadSerializer(data=workorder_images, many=True, context={'request':request})
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                tempfile_to_permanant(files_list)
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Workorder images uploaded successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )   
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[str(e)],
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json"
            )

class WorkOrderImageDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, static_file_id):
        try:
            workorder_image = WorkOrderImages.objects.get(image=static_file_id)
            static_file = StaticFiles.objects.get(id=static_file_id)
            file_path_relative = static_file.file_path
            if file_path_relative:
                full_file_path = Path(settings.BASE_DIR) / 'uploads' / file_path_relative
                if full_file_path.exists():
                    try:
                        os.remove(full_file_path)
                    except OSError as e:
                        pass
            workorder_image.delete()
            static_file.delete()
            
            return CustomResponse(
                data=None,
                status="success",
                message=["Workorder image deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[str(e)],
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json"
            )
