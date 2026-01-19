from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers,Role
from workorder_api.models.workorder import WorkOrder
from workorder_api.models.services import Services
from workorder_api.models.workorder_identifier import WorkOrderIdentifier


class WorkOrderEscalations(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    identifier = models.ForeignKey(WorkOrderIdentifier, on_delete=models.PROTECT,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_escalations_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_escalations_updated_user')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'workorder_api_escalations'


class WorkorderEscalationServices(models.Model):
    workorder_escalation = models.ForeignKey(WorkOrderEscalations, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)

    class Meta:
        db_table = 'workorder_api_escalations_services'

class WorkorderEscaltionLevels(models.Model):
    escalation = models.ForeignKey(WorkOrderEscalations, on_delete=models.PROTECT,null=True)
    level = models.IntegerField(null=True)
    trigger_time = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_api_escalations_levels'

class WorkorderEscalationRecipients(models.Model):
    TYPE_USER = 'USER'
    TYPE_ROLE = 'ROLE'
    TYPE_CHOICES = [
        (TYPE_USER, 'USER'),
        (TYPE_ROLE, 'ROLE'),
    ]
    escalation_level = models.ForeignKey(WorkorderEscaltionLevels, on_delete=models.PROTECT,null=True)
    user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT,null=True)
    _type = models.CharField(max_length=20,null=True,choices=TYPE_CHOICES)

    class Meta:
        db_table = 'workorder_api_escalations_recipients'

