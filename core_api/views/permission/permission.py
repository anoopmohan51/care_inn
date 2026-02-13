from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.models.role_permission import RolePermission
from core_api.serializers.role_permission_serializer import RolePermissionSerializer

class PermissionListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            role_permission = RolePermission.objects.filter(role=request.user.role)
            role_permission_data = RolePermissionSerializer(role_permission,many=True).data
            return CustomResponse(
                data=role_permission_data,
                status="success",
                message=["Permission fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in fetching permission"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
