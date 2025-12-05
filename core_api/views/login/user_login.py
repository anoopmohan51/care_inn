from ...models import AppUsers
from rest_framework.response import Response
from rest_framework import generics,status
from ...serializers import UserSerializer
from ...response_utils.custom_response import CustomResponse
from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(generics.CreateAPIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request=request,username=email,password=password)
            user_data = UserSerializer(user).data
            if user:
                refresh = RefreshToken.for_user(user)
                user_dict={
                    "user":user_data,
                    "access_token":str(refresh.access_token),
                    "refresh_token":str(refresh)
                }
                return CustomResponse(
                    data=user_dict,
                    status="success",
                    message=["User logged in successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
            else:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Invalid email or password"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in User login"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class TokenRefreshView(generics.CreateAPIView):
    def post(self,request):
        try:
            data=request.data
            refresh_token=data.get("refersh_token")
            if not refresh_token:
                return CustomResponse(
                    data=None,
                    status="error",
                    message=["Refresh token is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            token = RefreshToken(refresh_token)
            new_access = token.access_token
            new_refresh = token.rotate()
            return CustomResponse(
                data={
                    "access_token":str(new_access),
                    "refresh_token":str(new_refresh)
                },
                status="sucess",
                message=["Token generated"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="error",
                message=["Error in Token generation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
            