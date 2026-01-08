from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.models.role_permission import RolePermission
from core_api.serializers.role_permission_serializer import RolePermissionSerializer
from core_api.permission_utils.role_permission_utils import _bulk_update_role_permission

class RolePermissionBulkUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        # try:
            data = request.data
            permission_data = _bulk_update_role_permission(data)
            return CustomResponse(
                data=permission_data,
                status="success",
                message=["Role permission bulk updated successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        # except Exception as e:
        #     print(e)
        #     return CustomResponse(
        #         data=None,
        #         status="failed",
        #         message=["Error in role permission bulk updating"],
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content_type="application/json"
        #     )


            