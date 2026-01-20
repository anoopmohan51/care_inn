from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core_api.response_utils.custom_response import CustomResponse
from core_api.permission.external_api_permission import HasValidApiKey
from rest_framework import status
from workorder_api.models.informations import Informations
from workorder_api.models.requested_items import RequestedItems
from workorder_api.models.services import Services
from workorder_api.models.folder import Folder
from django.db import transaction

class WorkorderPositionChangeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            data = request.data
            if not isinstance(data, list):
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Data should be a list"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if not data:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Data should not be empty"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            with transaction.atomic():
                for index,record in enumerate(data):
                    record_type = record.get('type')
                    position = record.get('position')
                    if position is None and not isinstance(position, int):
                        return CustomResponse(
                            data=None,
                            status="failed",
                            message=["invalid position at index " + str(index)],
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                        )
                    if record_type == 'INFORMATION':
                        information_id = record.get('information_id')
                        if not information_id:
                            return CustomResponse(
                                data=None,
                                status="failed",
                                message=["invalid information id at index " + str(index)],
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json"
                            )
                        Informations.objects.filter(
                            id=information_id,is_delete=False
                        ).update(position=position)
                    elif record_type == 'REQUEST':
                        item_id = record.get('item_id')
                        if not item_id:
                            return CustomResponse(
                                data=None,
                                status="failed",
                                message=["invalid item id at index " + str(index)],
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json"
                            )
                        RequestedItems.objects.filter(
                            id=item_id,is_delete=False
                        ).update(position=position)
                    elif record_type == 'SERVICE':
                        service_id = record.get('service_id')
                        if not service_id:
                            return CustomResponse(
                                data=None,
                                status="failed",
                                message=["invalid service id at index " + str(index)],
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json"
                            )
                        Services.objects.filter(
                            id=service_id,is_delete=False
                        ).update(position=position)
                    elif record_type == 'FOLDER':
                        folder_id = record.get('folder_id')
                        if not folder_id:
                            return CustomResponse(
                                data=None,
                                status="failed",
                                message=["invalid folder id at index " + str(index)],
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json"
                            )
                        Folder.objects.filter(id=folder_id).update(position=position)
                    else:
                        return CustomResponse(
                            data=None,
                            status="failed",
                            message=["invalid record type at index " + str(index)],
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                        )
                return CustomResponse(
                    data=None,
                    status="success",
                    message=["Position updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in position update"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )