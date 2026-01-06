from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models.informations import Informations
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsSerializer
from django.db import transaction
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.serializers.information_serializer import InformationSerializer


class InformationsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_data = request.data
            folder = request_data.get('folder',None)
            with transaction.atomic():
                if request_data.get('type') == 'INFORMATION':
                    if not folder:
                        workorder_settings_data={
                            'type': 'INFORMATION'
                        }
                        serializer = WorkOrderSettingsSerializer(data=request_data, context={'request': request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            responce_data = serializer.data
                            request_data.update({
                                'workorder_settings': serializer.data.get('id')
                            })
                    serializer = InformationSerializer(data=request_data, context={'request': request})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()

                    return CustomResponse(
                        data=serializer.data,
                        status="success",
                        message=[f"Information created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )
                else:
                    return CustomResponse(
                        data=None,
                        status="failed",
                        message=[f"wrong folder type"],
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json"
                    )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Information creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )


class InformationsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            responce_data = Informations.objects.get(pk=id,is_delete=False)
            if not responce_data:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=[f"Information not found"],
                    status_code=status.HTTP_404_NOT_FOUND,
                    content_type="application/json"
                )
            serializer = InformationSerializer(responce_data)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Information details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            print(e)
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Information details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    
    def put(self, request, id):
        try:
            request_data = request.data
            information = Informations.objects.get(id=id)
            serializer = InformationSerializer(information, data=request_data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Information updated successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Information updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self, request, id):
        try:
            information = Informations.objects.filter(id=id).update(is_delete=True)
            return CustomResponse(
                data=None,
                status="success",
                message=[f"Information deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Information deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
