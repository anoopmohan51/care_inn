from rest_framework.response import Response
from rest_framework import generics,status
from workorder_api.models import Services
from workorder_api.serializers.service_serializer import ServiceSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from rest_framework.views import APIView
from core_api.permission.permission import has_permission
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsSerializer

class ServiceCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Service", "create")
    def post(self, request):
        try:
            data=request.data
            folder_id = data.get('folder_id',None)
            workorder_settings = data.get('workorder_settings',None)
            if not folder_id:
                workorder_settings_data={
                    'type': 'SERVICE'
                }
                workorder_settings_serializer =  WorkOrderSettingsSerializer(data=workorder_settings_data, context={'request': request})
                if workorder_settings_serializer.is_valid(raise_exception=True):
                    workorder_settings_serializer.save()
                    workorder_settings_id = workorder_settings_serializer.data.get('id')
                    data.update({
                        'workorder_settings_id': workorder_settings_id
                    })
            serializer = ServiceSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Service creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class ServiceUpdateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Service", "read")
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

    # @has_permission("Service", "update")
    def put(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Service updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
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
                message=["Error in Service updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    # @has_permission("Service", "update")
    def patch(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            serializer = ServiceSerializer(service, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Service updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(  
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Service updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
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
                message=["Error in Service updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    # @has_permission("Service", "delete")
    def delete(self, request,pk):
        try:
            service = Services.objects.get(id=pk,is_delete=False)
            service.is_delete = True
            service.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["Service deleted successfully"],
                status_code=status.HTTP_204_NO_CONTENT,
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
                message=["Error in Service deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        
class ServiceFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Service", "read")
    def post(self, request):
        try:
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
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
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
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Service filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )