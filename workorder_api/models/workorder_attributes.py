from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from core_api.models.service_type import ServiceType
from core_api.models.priority import Priority
from workorder_api.models.services import Services
from workorder_api.models.workorder_attribute_icons import WorkOrderAttributeIcons

class WorkOrderAttributes(models.Model):
    ATTRIBUTE_TYPE_ELEMENT = "ELEMENT"
    ATTRIBUTE_TYPE_GROUP = "GROUP"
    attribute_type_choices = [
        (ATTRIBUTE_TYPE_ELEMENT, "ELEMENT"),
        (ATTRIBUTE_TYPE_GROUP, "GROUP"),
    ]
    ELEMENT_TYPE_TEXT = "INFORMATION"
    ELEMENT_TYPE_NUMBER = "SERVICES"
    ELEMENT_TYPE_DATE = "REQUEST_ITEMS"
    element_type_choices = [
        (ELEMENT_TYPE_TEXT, "INFORMATION"),
        (ELEMENT_TYPE_NUMBER, "SERVICES"),
        (ELEMENT_TYPE_DATE, "REQUEST_ITEMS"),
    ]
    name = models.CharField(max_length=255)
    attribute_type = models.CharField(max_length=20,choices=attribute_type_choices)
    element_type = models.CharField(max_length=20,choices=element_type_choices)
    is_primary = models.BooleanField(default=False)
    elment_type = models.CharField(max_length=30,null=True,choices=element_type_choices)
    icon = models.ForeignKey(WorkOrderAttributeIcons, on_delete=models.PROTECT,null=True)
    service_name = models.CharField(max_length=255,null=True)#only for elements requested items
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='attribute_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='attribute_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    information = models.TextField(null=True)

    class Meta:
        db_table = 'workorder_attributes'
    
    def cleanup_related_data(self):
        if self.is_delete:
            WorkOrderAttributeElements.objects.filter(attribute=self.id).delete()
            WorkOrderAttributeRequestItems.objects.filter(attribute=self.id).delete()
            WorkOrderAttributeServices.objects.filter(attribute=self.id).delete()
        else:
            if self.attribute_type == "ELEMENT":
                if self.element_type == "SERVICES":
                    WorkOrderAttributeElements.objects.filter(attribute=self.id).delete()
                    WorkOrderAttributeRequestItems.objects.filter(attribute=self.id).delete()
                elif self.element_type == "REQUEST_ITEMS":
                    WorkOrderAttributeElements.objects.filter(attribute=self.id).delete()
                    WorkOrderAttributeServices.objects.filter(attribute=self.id).delete()
            else:
                WorkOrderAttributeRequestItems.objects.filter(attribute=self.id).delete()
                WorkOrderAttributeServices.objects.filter(attribute=self.id).delete()
    

class WorkOrderAttributeElements(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True,related_name='workorder_attribute_elements')
    attribute_element = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True,related_name='attribute_element')

    class Meta:
        db_table = 'workorder_attribute_elements'

class WorkOrderAttributeServices(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)

    class Meta:
        db_table = 'workorder_attribute_services'

class WorkOrderAttributeRequestItems(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    min_quantity = models.IntegerField(null=True)
    max_quantity = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_attribute_request_items'

