from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models.workorder_escalations import WorkOrderEscalations,WorkorderEscalationServices,WorkorderEscalationRecipients,WorkorderEscaltionLevels
from workorder_api.serializers.workorder_escalations_serializer import WorkOrderEscalationsSerializer,WorkorderEscalationServicesSerializer,WorkorderEscalationRecipientsSerializer,WorkorderEscaltionLevelsSerializer
from rest_framework import status
from core_api.permission.permission import has_permission
from .workorder_services import _create_update_escalation_services
from .workorder_escaltion_levels import _create_update_escalation_levels
from django.db import transaction
from core_api.filters.global_filter import GlobalFilter
from django.db.models import Q


class WorkOrderEscalationsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("WorkOrderEscalations", "create")
    def post(self, request):
        # try:
            data = request.data
            with transaction.atomic():
                serializer = WorkOrderEscalationsSerializer(data=data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    _create_update_escalation_services(request,data.get('services'),serializer.data.get('id'))
                    _create_update_escalation_levels(request,data.get('levels'),serializer.data.get('id'))
                    escalations_instance = WorkOrderEscalations.objects.get(id=serializer.instance.id)
                    respance_serializer = WorkOrderEscalationsSerializer(escalations_instance)
                    return CustomResponse(
                        data=respance_serializer.data,
                        status="success",
                        message=["Work order escalations created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )
                else:
                    return CustomResponse(
                        data=serializer.errors,
                        status="failed",
                        message=["Error in Work order escalations creation"],
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json"
                    )
        # except Exception as e:
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=["Error in Work order escalations creation"],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )

class WorkorderEscalationsDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #@has_permission("WorkOrderEscalations", "view")
    def get(self,request,pk):
        try:
            escalation = WorkOrderEscalations.objects.get(id=pk,is_delete=False)
            if not escalation:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Work order escalations not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = WorkOrderEscalationsSerializer(escalation)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order escalations fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order escalations deletion"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    def put(self,request,pk):
        try:
            data = request.data
            escalation = WorkOrderEscalations.objects.get(id=pk,is_delete=False)
            if not escalation:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Work order escalations not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = WorkOrderEscalationsSerializer(
                escalation, 
                data=data, 
                context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                _create_update_escalation_services(request,data.get('services'),serializer.data.get('id'))
                _create_update_escalation_levels(request,data.get('levels'),serializer.data.get('id'))
                escalation_id = serializer.instance.id
                escalation = WorkOrderEscalations.objects.get(id=escalation_id,is_delete=False)
                escalation_serializer = WorkOrderEscalationsSerializer(escalation)
                return CustomResponse(
                    data=escalation_serializer.data,
                    status="success",
                    message=["Work order escalations updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=serializer.errors,
                    status="failed",
                    message=["Error in Work order escalations updating"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order escalations updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self,request,pk):
        try:
            escalation = WorkOrderEscalations.objects.get(id=pk,is_delete=False)
            if not escalation:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Work order escalations not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            escalation.is_delete = True
            escalation.save()
            WorkorderEscalationServices.objects.filter(workorder_escalation=escalation).delete()
            WorkorderEscalationRecipients.objects.filter(escalation_level__escalation=escalation).delete()
            WorkorderEscaltionLevels.objects.filter(escalation=escalation).delete()
            return CustomResponse(
                data=None,
                status="success",
                message=["Work order escalations deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order escalations deletion"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkorderEscalationsFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #@has_permission("WorkOrderEscalations", "view")
    def post(self,request):
        try:
            field_lookup = {
                "name": "name",
                "services": "services__service__name",
                "levels": "levels__level",
                "identifier_name": "identifier__name"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrderEscalations,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderEscalationsSerializer)
            return CustomResponse(
                data={
                    "data": queryset,
                    "total_count": count
                },
                status="success",
                message=["Work order escalations fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order escalations filtering"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )