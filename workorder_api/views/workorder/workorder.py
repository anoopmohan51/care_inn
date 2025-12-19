from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrder
from workorder_api.serializers.workorder_serializer import WorkOrderSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F
from workorder_api.models import WorkOrderTemp
from django.db.models import Q
from core_api.permission.permission import has_permission

class WorkOrderCreateView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # @has_permission("Workorder", "create")
    def post(self, request):
        try:
            data = request.data
            workorder_data = WorkOrderTemp.objects.filter(id=data['id']).values('workorder_type','workorder_attribute','room','assignee_type','user','user_group','tenant','description','priority','when_to_start','sla_minutes','patient_id','status','created_at','updated_at','created_user','updated_user','is_delete','unique_id').first()
            if not workorder_data:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Error in Work order creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            serializer = WorkOrderSerializer(data=workorder_data, context={'request': request})
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
                print(""""serializer.errors""""",serializer.errors)
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order creation"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json" 
                )
        except Exception as e:
            print(""""e""""",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
class WorkorderDeleteView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # @has_permission("Workorder", "read")
    def get(self, request,pk):
        try:
            workorders = WorkOrder.objects.get(id=pk)
            serializer = WorkOrderSerializer(workorders)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work orders fetched successfully"],
                status_code=status.HTTP_200_OK,
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
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkorderFilterView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # @has_permission("Workorder", "read")
    def post(self, request):
        try:
            field_lookup = {
                "id": "id",
                "name": "name",
                "description": "description",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "status": "status"
            }
            tenant_id = request.query_params.get('tenant_id')
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrder,
                base_filter=Q(is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderSerializer)
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