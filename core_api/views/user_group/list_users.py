from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core_api.response_utils.custom_response import CustomResponse
from core_api.views.user_group.usergroup_utils.users_query import _get_users
from rest_framework import status

class ListUsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            limit=int(request.query_params.get('limit',10))
            offset=int(request.query_params.get('offset',0))
            user_group_id=request.query_params.get('user_group_id',None)
            if not user_group_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["User group id is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            users = _get_users(user_group_id,limit,offset)
            return CustomResponse(
                data=users,
                status="success",
                message=["Users fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Users fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )