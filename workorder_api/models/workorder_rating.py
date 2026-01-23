from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder import WorkOrder

class WorkOrderRating(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.PROTECT,null=True)
    rating = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workorder_api_workorder_rating'