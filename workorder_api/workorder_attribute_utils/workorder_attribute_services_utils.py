from workorder_api.models import WorkOrderAttributeServices
from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributeServicesSerializer

def create_update_workorder_attribute_services(data,request,workorder_attribute_id):
    services_data = data.get('services')
    response_data = []
    for service in services_data:
        is_added = service.get('is_added')
        if is_added:
            service_data = {
                "attribute": workorder_attribute_id,
                "service": service.get('service_id'),
            }
            serializer = WorkOrderAttributeServicesSerializer(
                data=service_data,
                context={'request':request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data.append(serializer.data)
        else:
            workorder_attributes_services=WorkOrderAttributeServices.objects.get(id=service.get('id'))
            serializer = WorkOrderAttributeServicesSerializer(
                workorder_attributes_services,
                data=service_data,
                context={'request':request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data.append(serializer.data)
    return response_data