from rest_framework.views import APIView
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models import WorkOrderAttributeIcons,WorkOrderAttributes
import os
from rest_framework import status
from django.conf import settings
from pathlib import Path
from datetime import datetime
from django.http import HttpResponse


class WorkOrderAttributeIconCreateView(APIView):
    def post(self, request):
        try:
            files = request.FILES.getlist("files", None)
            if not files:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["No files uploaded"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            saved_files = []
            for file in files:
                # Get file extension and type
                file_extension = os.path.splitext(file.name)[1].lower()
                file_type = file.content_type or 'application/octet-stream'

                 # Generate timestamp for folder and filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                
                # Create timestamp-based folder name (e.g., 20240115_143045_123456)
                timestamp_folder = timestamp
                
                # Create upload directory path
                upload_subdir = 'workorder_icons'
                upload_dir = Path(settings.MEDIA_ROOT) / upload_subdir / timestamp_folder
                
                # Create directory if it doesn't exist
                upload_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate unique filename
                import uuid
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                
                # Full file path
                file_path = upload_dir / unique_filename
                
                # Save file to disk
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                # Store relative path from MEDIA_ROOT
                # This will be: workorder_icons/uuid.png
                relative_path = f"{upload_subdir}/{timestamp_folder}/{unique_filename}"
                
                # Save to database
                icon_instance = WorkOrderAttributeIcons.objects.create(
                    name=unique_filename,
                    uploaded_file_name=file.name,
                    file_path=relative_path,
                    file_type=file_type
                )
                
                saved_files.append({
                    'id': str(icon_instance.id),
                    'name': icon_instance.name,
                    'file_path': icon_instance.file_path,
                    'uploaded_file_name': icon_instance.uploaded_file_name,
                    'file_type': icon_instance.file_type
                })
            
            return CustomResponse(
                data=saved_files,
                status="success",
                message=[f"Successfully uploaded"],
                status_code=status.HTTP_201_CREATED,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderAttributeIcon creating: {str(e)}"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    

class WorkOrderAttributeIconDetailView(APIView):
    def get(self, request, pk):
        try:
            workorder_attribute_icon = WorkOrderAttributeIcons.objects.get(id=pk)
            file_path = workorder_attribute_icon.file_path
            full_file_path = Path(settings.BASE_DIR) / 'media' / file_path
            if full_file_path.exists():
                with open(full_file_path, 'rb') as f:
                    file_data = f.read()
            else:
                file_data = None
            return HttpResponse(
                file_data, 
                content_type=workorder_attribute_icon.file_type
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderAttributeIcon detail fetching: {str(e)}"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self, request, pk):
        try:
            workorder_attribute_icon = WorkOrderAttributeIcons.objects.get(id=pk)
            workorder_attributes = WorkOrderAttributes.objects.filter(icon=workorder_attribute_icon,is_delete=False).update(icon=None)
            
            # Get the file path from database
            file_path_relative = workorder_attribute_icon.file_path
            
            # Construct full file path
            # If file_path is relative like "workorder_icons/uuid.png"
            if file_path_relative:
                full_file_path = Path(settings.BASE_DIR) / 'media' / file_path_relative
                
                # Delete file from filesystem if it exists
                if full_file_path.exists():
                    try:
                        os.remove(full_file_path)
                    except OSError as e:
                        # Log error but continue with database deletion
                        # You might want to log this: logger.error(f"Failed to delete file {full_file_path}: {e}")
                        pass
            
            # Mark as deleted in database
            workorder_attribute_icon.delete()
            
            return CustomResponse(
                data=None,
                status="success",
                message=["WorkOrderAttributeIcon deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except WorkOrderAttributeIcons.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=["WorkOrderAttributeIcon not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error deleting WorkOrderAttributeIcon: {str(e)}"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )            