from django.db import models
from core_api.models.tenant import Tenant
from workorder_api.models.workorder import WorkOrder
from workorder_api.models.workorder_escalations import WorkorderEscaltionLevels
from core_api.models.appusers import AppUsers


class WorkOrderEscalationsLog(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.PROTECT,null=True)
    escalation_level = models.ForeignKey(WorkorderEscaltionLevels, on_delete=models.PROTECT,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(null=True)


    class Meta:
        db_table = 'workorder_api_escalations_log'