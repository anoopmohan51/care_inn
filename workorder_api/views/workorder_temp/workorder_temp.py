from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from workorder_api.models import WorkOrderTemp
from workorder_api.serializers.workorder_temp_serializer import WorkOrderTempSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.filters.global_filter import GlobalFilter
import string
import random
import datetime
# from rest_framework.authentication import BasicAuthentication

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class WorkOrderTempCreateView(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            print(""""dataa""""",data)
            now = datetime.datetime.now()
            year = '{:02d}'.format(now.year)
            month = '{:02d}'.format(now.month)
            data["unique_number"] = "WO-" + year + month + id_generator()
            print(""""dataa""""",data)
            serializer = WorkOrderTempSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order template created successfully"],
                    status_code=status.HTTP_201_CREATED,
                    content_type="application/json"
                )
        except Exception as e:
            print(e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Temp Work order creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
