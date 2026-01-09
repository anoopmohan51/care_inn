from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from core_api.models.permission import Permission
from rest_framework import status

class PermissionListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            limit=int(request.query_params.get('limit',10))
            offset=int(request.query_params.get('offset',0))
            permission = Permission.objects.all()[offset:offset+limit].values('id','name')
            return CustomResponse(
                data=permission,
                status="success",
                message=["User permission fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in fetch permission"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
          
            

