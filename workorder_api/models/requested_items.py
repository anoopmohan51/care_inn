from django.db import models
from workorder_api.models.folder import Folder
from workorder_api.models.services import Services
from workorder_api.models.workorder_settings import WorkOrderSettings
from core_api.models.appusers import AppUsers
from core_api.models.tenant import Tenant

class RequestedItems(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    workorder_settings = models.ForeignKey(WorkOrderSettings, on_delete=models.PROTECT,null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='requested_items_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='requested_items_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workorder_api_requested_items'


class ItemDetails(models.Model):
    item = models.ForeignKey(RequestedItems, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255,null=True)
    min_quantity = models.IntegerField(null=True)
    max_quantity = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_api_item_details'