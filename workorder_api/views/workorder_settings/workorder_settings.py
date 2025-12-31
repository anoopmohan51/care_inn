from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.models.folder import Folder
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsSerializer,WorkOrderSettingsListSerializer,FolderDetailsListSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.permission.permission import has_permission
from django.db import transaction
from django.db.models import Q
from core_api.filters.global_filter import GlobalFilter

class WorkOrderSettingsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_data = request.data
            parent_folder_id = request_data.get('parent_folder_id',None)
            folder_data = None
            data = None
            if request_data.get('type') == 'FOLDER':
                with transaction.atomic():
                    folder_data = {
                                'name': request_data.get('name'),
                                'parent_folder': parent_folder_id,
                                'position': request_data.get('position'),
                                'icon': request_data.get('icon'),
                                'workorder_settings_id': request_data.get('id',None)
                            }
                    if not parent_folder_id:
                        serializer = WorkOrderSettingsSerializer(data=request_data, context={'request': request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            data = serializer.data
                            folder_data.update({
                                'workorder_settings_id': serializer.data.get('id')
                            })
                    else:
                        workorder_settings = WorkOrderSettings.objects.get(id=request_data.get('id'))
                        serializer = WorkOrderSettingsSerializer(request_data, context={'request': request})
                        data = serializer.data
                    folder = Folder.objects.create(**folder_data)
                    data.update({
                        "name":folder.name,
                        "icon":folder.icon
                    })
                    return CustomResponse(
                        data=data,
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
            folder_id = request.query_params.get('parent_folder_id',None)
            responce_data = None
            if  not folder_id:
                workorder_settings = WorkOrderSettings.objects.get(id=id)
                serializer = WorkOrderSettingsListSerializer(workorder_settings)
                responce_data=serializer.data
            else:
                folder = Folder.objects.get(id=folder_id)
                serializer = FolderDetailsListSerializer(folder)
                responce_data = serializer.data
            return CustomResponse(
                data=responce_data,
                status="success",
                message=[f"WorkOrderSettings details fetched successfully"],
                status_code=status.HTTP_200_OK,
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
            responce_data = {}
            folder_id = request.query_params.get('parent_folder_id',None)
            if not folder_id:
                workorder_settings = WorkOrderSettings.objects.get(id=id)
                serializer = WorkOrderSettingsSerializer(workorder_settings, data=request_data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    responce_data = serializer.data
                    folder = Folder.objects.get(workorder_settings_id=id)
                    folder.name = request_data.get('name')
                    folder.icon = request_data.get('icon')
                    folder.save()
                    responce_data.update({
                        "name":folder.name,
                        "icon":folder.icon
                    })
            else:
                folder = Folder.objects.get(id=id)
                folder.name = request_data.get('name')
                folder.icon = request_data.get('icon')
                folder.save()
                responce_data.update({
                    "name":folder.name,
                    "icon":folder.icon
                })
            return CustomResponse(
                data=responce_data,
                status="success",
                message=[f"WorkOrderSettings updated successfully"],
                status_code=status.HTTP_200_OK,
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

class WorkOrderSettingsFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # try:
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
        # except Exception as e:
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=[f"Error in WorkOrderSettings filter fetching"],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )