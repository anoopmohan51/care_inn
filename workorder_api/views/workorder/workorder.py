from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrder
from workorder_api.serializers.workorder_serializer import WorkOrderSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Value
from workorder_api.models import WorkOrderTemp
from django.db.models import Q
from core_api.permission.permission import has_permission
from django.db.models.functions import Concat

class WorkOrderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Workorder", "create")
    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json" 
                )
        except Exception as e:
            print("error:::::::",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
class WorkorderDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Workorder", "read")
    def get(self, request,pk):
        try:
            workorders = WorkOrder.objects.get(id=pk,is_delete=False)
            serializer = WorkOrderSerializer(workorders)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work orders fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except WorkOrder.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Work order not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work orders fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    # @has_permission("Workorder", "update")
    def put(self, request, pk):
        try:
            workorder = WorkOrder.objects.get(id=pk)
            serializer = WorkOrderSerializer(workorder, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except WorkOrder.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Work order not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    # @has_permission("Workorder", "update")
    def patch(self, request, pk):
        try:
            workorder = WorkOrder.objects.get(id=pk)
            serializer = WorkOrderSerializer(workorder, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except WorkOrder.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Work order not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkorderFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @has_permission("Workorder", "read")
    def post(self, request):
        try:
            field_lookup = {
                "id": "id",
                "name": "name",
                "description": "description",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "status": "status",
                "service": "service",
                "created_user": "created_user"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrder,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result(
                created_user_name = Concat(F('created_user__first_name'), Value(' '), F('created_user__last_name')),
                assigned_user = Concat(F('user__first_name'), Value(' '), F('user__last_name')),
                assigned_user_group = F('user_group__name'),
                service_name = F('service__name'),
                room_number = F('room__room_number'),
                room_description = F('room__description')
            )
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Work order list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )