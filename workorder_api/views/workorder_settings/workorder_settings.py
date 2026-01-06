from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.models.folder import Folder
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsSerializer,WorkOrderSettingsListSerializer,FolderDetailsListSerializer,FolderSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.permission.permission import has_permission
from django.db import transaction
from django.db.models import Q
from core_api.filters.global_filter import GlobalFilter
from.delete_folder import _delete_folders_recursive
from workorder_api.models.services import Services
from workorder_api.models.informations import Informations
from workorder_api.models.requested_items import RequestedItems

class WorkOrderSettingsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_data = request.data
            folder = request_data.get('folder',None)
            folder_data = None
            data = None
            if request_data.get('type') == 'FOLDER':
                with transaction.atomic():
                    if not folder:
                        workorder_settings_data = {
                            'type': 'FOLDER'
                        }
                        serializer = WorkOrderSettingsSerializer(data=workorder_settings_data, context={'request': request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            data = serializer.data
                            request_data.update({
                                'workorder_settings': serializer.data.get('id')
                            })
                    serializer = FolderSerializer(data=request_data, context={'request': request})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    return CustomResponse(
                        data=serializer.data,
                        status="success",
                        message=[f"WorkOrderSettings created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )
            else:
                return CustomResponse(
                data=None,
                status="failed",
                message=["Only FOLDER type is supported in this endpoint"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderSettings creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderSettingsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            folder = Folder.objects.get(id=id,is_delete=False)
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
    def put(self, request, id):
        try:
            request_data = request.data
            folder = Folder.objects.get(id=id,is_delete=False)
            serializer = FolderSerializer(folder, data=request_data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=[f"WorkOrderSettings updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=[f"Error in WorkOrderSettings updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
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
                message=[f"Error in WorkOrderSettings updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self, request, id):
        try:
            folder = Folder.objects.get(id=id)
            if not folder.parent_folder:
                WorkOrderSettings.objects.filter(id=folder.workorder_settings.id).update(is_delete=True)
            _delete_folders_recursive(self,folder.id)
            Services.objects.filter(folder_id=folder.id).update(is_delete=True)
            Informations.objects.filter(folder_id=folder.id).update(is_delete=True)
            RequestedItems.objects.filter(folder_id=folder.id).update(is_delete=True)
            folder.delete()   
            return CustomResponse(
                data=None,
                status="success",
                message=[f"WorkOrderSettings deleted successfully"],
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
                message=[f"Error in WorkOrderSettings deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderSettingsFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
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
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
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
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in WorkOrderSettings filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )