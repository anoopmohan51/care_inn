from workorder_api.models import WorkOrderAttributeRequestItems
from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributeRequestItemsSerializer

def create_update_workorder_attribute_request_items(data,request,workorder_attribute_id):
    items_data = data.get('request_items')
    response_data = []
    for request_item in items_data:
        is_added = request_item.get('is_added')
        if is_added:
            request_item_data = {
                "attribute": workorder_attribute_id,
                "name": request_item.get('name'),
                "min_quantity": request_item.get('min_quantity'),
                "max_quantity": request_item.get('max_quantity'),
            }
        else:
            workorder_attribute_request_items=WorkOrderAttributeRequestItems.objects.get(id=request_item.get('id'))
            serializer = WorkOrderAttributeRequestItemsSerializer(
                workorder_attribute_request_items,
                data=request_item_data,
                context={'request':request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data.append(serializer.data)
    return response_data