from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.services import Services
from workorder_api.models.rooms import Rooms
from workorder_api.models.workorder_attributes import WorkOrderAttributes
from core_api.models.usergroups import UserGroup
from staticfiles_api.models.staticfiles import StaticFiles

class WorkOrder(models.Model):
    ASSIGNEE_USER = "USER"
    ASSIGNEE_TEAM = "TEAM"
    ASSIGNEE_CHOICES = [
        (ASSIGNEE_USER, "USER"),
        (ASSIGNEE_TEAM, "TEAM"),
    ]
    WHEN_TO_START_NOW = "IMMEDIATE"
    WHEN_TO_START_LATER = "LATER"
    WHEN_TO_START_CHOICES = [
        (WHEN_TO_START_NOW, "NOW"),
        (WHEN_TO_START_LATER, "LATER"),
    ]
    WORKORDER_STATUS_UNASSIGNED = "UNASSIGNED"
    WORKORDER_STATUS_ASSIGNED_NOT_STARTED = "ASSIGNED NOT STARTED"
    WORKORDER_STATUS_IN_PROGRESS = "IN PROGRESS"
    WORKORDER_STATUS_PAUSED = "PAUSED"
    WORKORDER_STATUS_CLOSED = "CLOSED"
    WORKORDER_STATUS_CHOICES = [
        (WORKORDER_STATUS_UNASSIGNED, "UNASSIGNED"),
        (WORKORDER_STATUS_ASSIGNED_NOT_STARTED, "ASSIGNED NOT STARTED"),
        (WORKORDER_STATUS_IN_PROGRESS, "IN PROGRESS"),
        (WORKORDER_STATUS_PAUSED, "PAUSED"),
        (WORKORDER_STATUS_CLOSED, "CLOSED")
    ]
    WORKORDER_TYPE_SERVICE = "COMPLAINT"
    WORKORDER_TYPE_REQUEST = "REQUEST"
    WORKORDER_TYPE_CHOICES = [
        (WORKORDER_TYPE_SERVICE, "COMPLAINT"),
        (WORKORDER_TYPE_REQUEST, "REQUEST"),
    ]
    SOURCE_CHOICES = [
        ('SYSTEM','SYSTEM'),
        ('USER','USER'),
    ]
    PRIORITY_CHOICES = [
        ('LOW','LOW'),
        ('MEDIUM','MEDIUM'),
        ('HIGH','HIGH'),
    ]
    workorder_type = models.CharField(max_length=255,choices=WORKORDER_TYPE_CHOICES,null=True)
    workorder_attribute=models.ForeignKey(WorkOrderAttributes, on_delete=models.PROTECT,null=True)
    room=models.ForeignKey(Rooms, on_delete=models.PROTECT,null=True)
    assignee_type=models.CharField(max_length=255,choices=ASSIGNEE_CHOICES,null=True)
    user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True)
    user_group=models.ForeignKey(UserGroup, on_delete=models.PROTECT,null=True)
    tenant=models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    description=models.TextField(null=True)
    priority=models.CharField(max_length=255,choices=PRIORITY_CHOICES,null=True)
    when_to_start=models.CharField(max_length=255,choices=WHEN_TO_START_CHOICES,null=True)
    sla_minutes=models.CharField(max_length=255,null=True)
    mrd_id=models.CharField(max_length=60,null=True)
    status=models.CharField(max_length=50,choices=WORKORDER_STATUS_CHOICES,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_created_user')
    updated_user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_updated_user')
    is_delete=models.BooleanField(default=False)
    unique_id=models.CharField(max_length=30,null=True)
    source = models.CharField(max_length=20,null=True,choices=SOURCE_CHOICES,default='USER')
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    primary_image = models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
    test_field123 = models.CharField(max_length=255,null=True)  


    class Meta:
        db_table = 'workorder'