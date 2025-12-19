from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder import WorkOrder
from core_api.models.usergroup import UserGroup

class WorkOrderActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('ACCEPTED','ACCEPTED'),
        ('ASSIGNED','ASSIGNED'),
        ('BEGIN','BEGIN'),
        ('CALL','CALL'),
        ('CREATED','CREATED'),
        ('DUE_DATE','DUE_DATE'),
        ('EMAIL','EMAIL'),
        ('EXECUTE','EXECUTE'),
        ('NOTE','NOTE'),
        ('PRIMARY_ESCALATED','PRIMARY_ESCALATED'),
        ('PRIMARY_ESCALATION_DONE','PRIMARY_ESCALATION_DONE'),
        ('PRIORITY','PRIORITY'),
        ('SECONDARY_ESCALATED','SECONDARY_ESCALATED'),
        ('SLA_START_TIME','SLA_START_TIME'),
        ('SMS','SMS'),
        ('STATUS','STATUS'),
        ('TIME_START','TIME_START'),
        ('TIMER_END','TIMER_END'),
        ('WAITING','WAITING'),
    ]
    workorder = models.ForeignKey(WorkOrder, on_delete=models.PROTECT,null=True)
    activity = models.CharField(max_length=255,choices=ACTIVITY_CHOICES,null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True)
    is_added_by_patient = models.BooleanField(default=False)
    from_value = models.CharField(max_length=255,null=True)
    to_value = models.CharField(max_length=255,null=True)
    from_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_from_user')
    to_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_to_user')
    assigned_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_assigned_user')
    accepted_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_activity_accepted_user')
    user_group = models.ForeignKey(UserGroup, on_delete=models.PROTECT,null=True,related_name='workorder_activity_user_group')


    class Meta:
        db_table = 'workorder_activity'
