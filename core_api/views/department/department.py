from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.serializers.department_serializer import DepartmentSerializer
from core_api.models.department import Department
from core_api.filters.global_filter import GlobalFilter
from django.db.models import F,Q
from core_api.permission.permission import has_permission
from rest_framework import status

class DepartmentFilterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # @has_permission("Department", "read")
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
                Department,
                base_filter=Q(tenant=request.user.tenant,is_delete=False),
                default_sort="created_at"
            )
            queryset, count = global_filter._get_result()
            return CustomResponse(
                data={
                    "count": count,
                    "data": queryset
                },
                status="success",
                message=["Departments filter fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Departments filter fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )