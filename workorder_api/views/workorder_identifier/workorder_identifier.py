from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from workorder_api.models.workorder_identifier import WorkOrderIdentifier
from workorder_api.serializers.workorder_identifier_serializer import WorkOrderIdentifierSerializer
from core_api.permission.permission import has_permission
from django.db.models import Q
from core_api.filters.global_filter import GlobalFilter
from rest_framework import status

class WorkOrderIdentifierFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    #@has_permission("WorkOrderIdentifier", "create")
    def post(self,request):
        try:
            field_lookup = {
                "name": "name",
                "description": "description"
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrderIdentifier,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter.get_serialized_result(serializer=WorkOrderIdentifierSerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Work order identifier fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order identifier filtering"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )