from workorder_api.models import WorkOrderAttributeElements
from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributeElementsSerializer

def create_update_workorder_attribute_elements(data,request,workorder_attribute_id):
    data = data.get('elements')
    response_data = []
    for element in data:
        is_added = element.get('is_added')
        if is_added:
            element_data = {
                "attribute": workorder_attribute_id,
                "service": element.get('id'),
            }
            serializer = WorkOrderAttributeElementsSerializer(
                data=element_data,
                context={'request':request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data.append(serializer.data)
        else:
            workorder_attribute_elements=WorkOrderAttributeElements.objects.get(id=element.get('id'))
            serializer = WorkOrderAttributeElementsSerializer(
                workorder_attribute_elements,
                data=element_data,
                context={'request':request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data.append(serializer.data)
    return response_data