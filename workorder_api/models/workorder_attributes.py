from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from core_api.models.service_type import ServiceType
from core_api.models.priority import Priority

class WorkOrderAttributes(models.Model):
    ATTRIBUTE_TYPE_ELEMENT = "1"
    ATTRIBUTE_TYPE_GROUP = "2"
    attribute_type_choices = [
        (ATTRIBUTE_TYPE_ELEMENT, "ELEMENT"),
        (ATTRIBUTE_TYPE_GROUP, "GROUP"),
    ]
    ELEMENT_TYPE_TEXT = "1"
    ELEMENT_TYPE_NUMBER = "2"
    ELEMENT_TYPE_DATE = "3"
    element_type_choices = [
        (ELEMENT_TYPE_TEXT, "INFORMATION"),
        (ELEMENT_TYPE_NUMBER, "SERVICES"),
        (ELEMENT_TYPE_DATE, "REQUEST_ITEMS"),
    ]
    name = models.CharField(max_length=255)
    attribute_type = models.CharField(max_length=10,choices=attribute_type_choices)
    element_type = models.CharField(max_length=10,choices=element_type_choices)
    is_primary = models.BooleanField(default=False)
    elment_type = models.CharField(max_length=30,null=True,choices=element_type_choices)
    icon = models.CharField(max_length=255,null=True)
    service_name = models.CharField(max_length=255,null=True)#only for elements requested items
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkOrderAttributeElements(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    group = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)

class WorkOrderAttributeServices(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)

class WorkOrderAttributeRequestItems(models.Model):
    attribute = models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    min_quantity = models.IntegerField(null=True)
    max_quantity = models.IntegerField(null=True)

