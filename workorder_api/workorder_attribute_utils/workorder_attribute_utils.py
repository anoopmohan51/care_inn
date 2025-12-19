from workorder_api.serializers.workorder_attributes_serializer import WorkOrderAttributesSerializer
from workorder_api.models import WorkOrderAttributes

def create_workorder_attribute(data,request):
    attribute_data ={
        "name": data.get('name'),
        "attribute_type": data.get('attribute_type'),
        "element_type": data.get('element_type'),
        "is_primary": data.get('is_primary'),
        "information": data.get('information'),
        "tenant": data.get('tenant'),
        "created_user": data.get('created_user'),
        "updated_user": data.get('updated_user'),
        "icon": data.get('icon'),
        "is_delete": False,
    }
    serializer = WorkOrderAttributesSerializer(data=attribute_data,context={'request':request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return True,serializer.data
    else:
        return False,serializer.errors

def update_workorder_attribute(data,request,workorder_attribute_id):
    attribute_data ={
        "id": data.get('id'),
        "name": data.get('name'),
        "attribute_type": data.get('attribute_type'),
        "element_type": data.get('element_type'),
        "is_primary": data.get('is_primary'),
        "information": data.get('information'),
        "tenant": data.get('tenant'),
        "created_user": data.get('created_user'),
        "updated_user": data.get('updated_user'),
        "icon": data.get('icon'),
        "is_delete": False,
    }
    workorder_attribute = WorkOrderAttributes.objects.get(id=workorder_attribute_id,is_delete=False)
    serializer = WorkOrderAttributesSerializer(
        workorder_attribute,
        data=attribute_data,
        context={'request':request}
    )
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return True,serializer.data
    else:
        return False,serializer.errors