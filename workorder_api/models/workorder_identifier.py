from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder import WorkOrder

class WorkOrderIdentifier(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_identifier_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_identifier_updated_user')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'workorder_api_identifier'
        