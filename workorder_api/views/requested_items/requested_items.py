from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from workorder_api.models.requested_items import RequestedItems,ItemDetails
from core_api.response_utils.custom_response import CustomResponse
from rest_framework import status
from core_api.permission.permission import has_permission
from django.db import transaction
from workorder_api.serializers.workorder_settings_serializer import WorkOrderSettingsSerializer
from workorder_api.serializers.item_serializer import ItemSerializer

class RequestedItemsCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_data = request.data
            folder = request_data.get('folder',None)
            with transaction.atomic():
                if request_data.get('type') == 'REQUEST':
                    if not folder:
                        workorder_settings_data={
                            'type': 'REQUEST'
                        }
                        serializer = WorkOrderSettingsSerializer(data=workorder_settings_data, context={'request': request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()   
                            request_data.update({
                                'workorder_settings': serializer.data.get('id')
                            })
                    items_serializer = ItemSerializer(data=request_data, context={'request': request})
                    if items_serializer.is_valid(raise_exception=True):
                        items_serializer.save()
                        _create_update_item_details(request_data.get('items'),items_serializer.data.get('id'))
                    return CustomResponse(
                        data=items_serializer.data,
                        status="success",
                        message=[f"Requested items created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )
                else:
                    return CustomResponse(
                        data=None,
                        status="failed",
                        message=[f"wrong type of request"],
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json"
                    )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Requested items creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class RequestedItemsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            responce_data = RequestedItems.objects.get(id=id,is_delete=False)
            serializer = ItemSerializer(responce_data)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Requested items details fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Requested items details fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def put(self, request, id):
        try:
            request_data = request.data
            requested_items = RequestedItems.objects.get(id=id)
            with transaction.atomic():
                serializer = ItemSerializer(requested_items, data=request_data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    _create_update_item_details(request_data.get('items'),serializer.data.get('id'))
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=[f"Requested items updated successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Requested items updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def delete(self, request, id):
        try:
            ItemDetails.objects.filter(item_id=id).delete()
            RequestedItems.objects.filter(id=id).update(is_delete=True)
            return CustomResponse(
                data=None,
                status="success",
                message=[f"Requested items deleted successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=[f"Error in Requested items deleting"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

def _create_update_item_details(items_data,item_id):
    id_list = []
    for item in items_data:
        item.update({
            'item_id': item_id
        })
        if "id" not in item:
            ItemDetails.objects.create(**item)
        else:
            ItemDetails.objects.filter(id=item.get('id')).update(**item)
        id_list.append(item.get('id'))
    ItemDetails.objects.filter(item_id=item_id).exclude(id__in=id_list).delete()

        
