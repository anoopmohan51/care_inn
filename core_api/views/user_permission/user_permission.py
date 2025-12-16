from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from core_api.models.user_permission import UserPermission
from django.db.models import F
from rest_framework import status
from django.db import transaction

class UserPermissionDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,user_id):
        try:
            user_permission = UserPermission.objects.filter(user_id=user_id).annotate(
                permission_name=F('permission__name'),
            ).values("id","user","permission","create","read","update","delete","permission_name")
            return CustomResponse(
                data=user_permission,
                status="success",
                message=["User permission fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print("eeeeeeee",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in fetch permission"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

    def put(self,request,user_id):
            # try:
            data=request.data
            data_list = []
            for record in data:
                data_list.append(
                    UserPermission(
                        id=record["id"],
                        create=record["create"],
                        read=record["read"],
                        update=record["update"],
                        delete=record["delete"],
                        user_id=user_id
                    )
                )
            with transaction.atomic():
                d =UserPermission.objects.bulk_update(
                    data_list,
                    ["create", "read", "update", "delete"]
                )
            return CustomResponse(
                status="success",
                message=["User permission updated successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        
            
            

