from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models.workorder_escalations_log import WorkOrderEscalationsLog
from rest_framework import status
from workorder_api.serializers.escalation_details_serializer import EscalationDetailsSerializer
from django.db.models import Max
class WorkorderEscalationDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,workorder_id):
        try:
            max_level = WorkOrderEscalationsLog.objects.filter(workorder=workorder_id).aggregate(Max('level'))['level__max']
            escalations = WorkOrderEscalationsLog.objects.filter(workorder=workorder_id).order_by('-level')
            if not escalations:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Escalations not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = EscalationDetailsSerializer(escalations, many=True)
            return CustomResponse(
                data={
                    "escalation_level": max_level,
                    "escalated_to": serializer.data
                },
                status="success",
                message=["Escalations details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in fetching escalations details"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )