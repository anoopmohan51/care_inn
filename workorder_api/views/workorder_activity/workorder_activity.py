from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrderActivity
from core_api.response_utils.custom_response import CustomResponse
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q,OuterRef,Subquery
from rest_framework import status
from core_api.models.appusers import AppUsers
from core_api.models.usergroups import UserGroup
from workorder_api.serializers.workorder_activity_serializer import WorkOrderActivitySerializer


class WorkOrderActivityListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, workorder_id):
        try:
            field_lookup = {
                workorder_id: "workorder_id",
            }
            global_filter = GlobalFilter(
                request,
                field_lookup,
                WorkOrderActivity,
                base_filter=Q(workorder_id=workorder_id),
                default_sort="-created_at"
            )
            queryset, count = global_filter.get_serialized_result(WorkOrderActivitySerializer)
            return CustomResponse(
                data=queryset,
                status="success",
                message=["Work order activity list fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print(""""e""""",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order activity list fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )