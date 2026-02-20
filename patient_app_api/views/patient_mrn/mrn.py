from workorder_api.models.patient_mrn import Mrn
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from rest_framework import status
from patient_app_api.serializers.mrn_serializer import MrnSerializer

class MrnView(APIView):
    permission_classes = [AllowAny,HasValidApiKey]
    def post(self, request):
        try:
            data = request.data
            mrn = data.get('mrn',None)
            if mrn in [None, '', 'null']:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["MRN is required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            mrn_data = {
                'mrn':mrn,
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'arabic_first_name': data.get('arabic_first_name'),
                'arabic_last_name': data.get('arabic_last_name'),
                'mobile_number': data.get('mobile_number'),
                'language': data.get('language'),
                'ward_code': data.get('ward_code')
            }
            if Mrn.objects.filter(mrn=mrn).exists():
                mrn = Mrn.objects.get(mrn=mrn)
                serializer = MrnSerializer(mrn, data=mrn_data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            else:
                serializer = MrnSerializer(data=mrn_data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["MRN created successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in MRN creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )