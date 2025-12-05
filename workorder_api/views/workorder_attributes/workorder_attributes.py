from rest_framework.response import Response
from rest_framework.views import APIView
from workorder_api.models import WorkOrderAttributes
from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributesSerializer
from workorder_api.response_utils.custom_response import CustomResponse
from rest_framework.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class WorkOrderAttributesCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            serializer = WorkOrderAttributesSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["WorkOrderAttributes created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["WorkOrderAttributes creation failed"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderAttributesListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            workorder_attributes = WorkOrderAttributes.objects.all()
            serializer = WorkOrderAttributesSerializer(workorder_attributes, many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["WorkOrderAttributes list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes list fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderAttributesDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
            workorder_attribute = WorkOrderAttributes.objects.get(id=pk,is_delete=False)
            serializer = WorkOrderAttributesSerializer(workorder_attribute)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["WorkOrderAttributes detail fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes detail fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def put(self, request,pk):
        try:
            data = request.data
            workorder_attribute = WorkOrderAttributes.objects.get(id=pk,is_delete=False)
            serializer = WorkOrderAttributesSerializer(workorder_attribute, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["WorkOrderAttributes updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in WorkOrderAttributes updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    def delete(self, request,pk):
        try:
            workorder_attribute = WorkOrderAttributes.objects.get(id=pk,is_delete=False)
            workorder_attribute.is_delete = True
            workorder_attribute.save()
            return CustomResponse(
                data=None,
                status="success",
                message=["WorkOrderAttributes deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )