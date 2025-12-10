from rest_framework.response import Response
from rest_framework.views import APIView
from workorder_api.models import WorkOrderAttributes
from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributesSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.workorder_attribute_utils.workorder_attribute_utils import create_workorder_attribute
from django.db import transaction
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from rest_framework import status
class WorkOrderAttributesCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            success,workorder_attribute_response = create_workorder_attribute(data,request)
            if success:
                if data.get('attrbute-type') == "ELEMENT":
                    if data.get('element-type') == "SERVICES":
                        services_response = create_update_workorder_attribute_services(
                            data,
                            request,
                            workorder_attribute_response.data.get('id')
                        )
                        workorder_attribute_response['services'] = services_response
                    elif data.get('element-type') == "REQUEST_ITEMS":
                        request_items_response = create_update_workorder_attribute_request_items(
                            data,
                            request,
                            workorder_attribute_response.data.get('id')
                        )
                        workorder_attribute_response['items'] = request_items_response
                else:
                    elements_response = create_update_workorder_attribute_elements(
                        data,
                        request,
                        workorder_attribute_response.data.get('id')
                    )
                    workorder_attribute_response['elements'] = elements_response
                instance = WorkOrderAttributes.objects.get(id=workorder_attribute_response.data.get('id'),is_delete=False)
                instance.cleanup_related_data()
                return CustomResponse(
                    data=data,
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

class WorkOrderAttributesDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
            workorder_attribute = WorkOrderAttributes.objects.get(id=pk,is_delete=False)
            serializer = WorkOrderAttributesSerializer(workorder_attribute)
            workorder_attribute_data=serializer.data
            if workorder_attribute_data.get('attribute-type') == "ELEMENT":
                if workorder_attribute_data.get('element-type') == "SERVICES":
                    workorder_attribute_data['services'] = WorkOrderAttributeServices.objects.filter(attribute=pk).all()
                    workorder_attribute_data['attributes'] = []
                    workorder_attribute_data['items'] = []
                elif workorder_attribute_data.get('element-type') == "REQUEST_ITEMS":
                    workorder_attribute_data['items'] = WorkOrderAttributeRequestItems.objects.filter(attribute=pk).all()
                    workorder_attribute_data['attributes'] = []
                    workorder_attribute_data['services'] = []
                else:
                    workorder_attribute_data['attributes'] = []
                    workorder_attribute_data['services'] = []
                    workorder_attribute_data['items'] = []
            else:
                workorder_attribute_data['attributes'] = WorkOrderAttributes.objects.filter(attribute=pk).all()
                workorder_attribute_data['services'] = []
                workorder_attribute_data['items'] = []
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

    
    @transaction.atomic
    def put(self, request,pk):
        try:
            data = request.data
            success,workorder_attribute_response = update_workorder_attribute(data,request,pk)
            if success:
                if data.get('attrbute-type') == "ELEMENT":
                    if data.get('element-type') == "SERVICES":
                        services_response = create_update_workorder_attribute_services(
                            data,
                            request,
                            workorder_attribute_response.data.get('id')
                        )
                        workorder_attribute_response['services'] = services_response
                    elif data.get('element-type') == "REQUEST_ITEMS":
                        request_items_response = create_update_workorder_attribute_request_items(
                            data,
                            request,
                            workorder_attribute_response.data.get('id')
                        )
                        workorder_attribute_response['items'] = request_items_response
                else:
                    elements_response = create_update_workorder_attribute_elements(
                        data,
                        request,
                        workorder_attribute_response.data.get('id')
                    )
                    workorder_attribute_response['elements'] = elements_response
                instance = WorkOrderAttributes.objects.get(id=workorder_attribute_response.data.get('id'),is_delete=False)
                instance.cleanup_related_data()
                return CustomResponse(
                    data=workorder_attribute_response,
                    status="success",
                    message=["WorkOrderAttributes updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )   
            else:
                return CustomResponse(
                    data=workorder_attribute_response.errors,
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
            workorder_attribute.cleanup_related_data()
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

class WorkOrderAttributesFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            field_lookup = {
                "id": "id",
                "name": "name",
                "attribute_type": "attribute_type",
                "element_type": "element_type",
                "is_primary": "is_primary",
                "created_at": "created_at",
                "updated_at": "updated_at"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrderAttributes,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result(
                created_user_name = F('created_user__first_name'),
            )
            return CustomResponse(
                data=queryset,
                status="success",
                message=["WorkOrderAttributes list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("error:::::::::::",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in WorkOrderAttributes filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )