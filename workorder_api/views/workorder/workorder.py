from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrder
from workorder_api.serializers.workoser_serializer import WorkOrderSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F

class WorkOrderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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

    def get(self, request):
        try:
            workorders = WorkOrder.objects.all()
            serializer = WorkOrderSerializer(workorders, many=True)
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
    