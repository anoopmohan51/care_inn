from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder import WorkOrder

class WorkOrderTimeline(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.PROTECT,null=True)
    from_date =models.DateTimeField(null=True)
    to_date = models.DateTimeField(null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True)
    is_delete = models.BooleanField(default=False)
    duration = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_timeline'
    