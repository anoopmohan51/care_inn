from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from core_api.models.user_permission import UserPermission
from django.db.models import F
from rest_framework import status

class UserPermissionDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk):
            # try:
            print("pk:::::::::::::",request.user.id)
            user_permission = UserPermission.objects.filter(user_id=pk).annotate(
                permission_name=F('permission__name'),
            ).values()
            response = []
            
            # for record in user_permission:
            #     response.append({
            #     record['permission_name']:{
            #         "id":record['id'],
            #         'create':record['create'],
            #         'read':record['read'],
            #         'update':record['update'],
            #         'delete':record['delete'],
            #     }
            #     })
            return CustomResponse(
                data=user_permission,
                status="success",
                message=["User permission fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )