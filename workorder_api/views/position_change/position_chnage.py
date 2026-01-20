from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from rest_framework import status

class WorkorderPositionChangeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # try:
        data = request.data
        for record in data:
            print(record)