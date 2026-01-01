from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from staticfiles_api.models.staticfiles import StaticFiles
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.models.folder import Folder
from core_api.models.usergroups import UserGroup

class Services(models.Model):
    ASSIGNEE_USER = "USER"
    ASSIGNEE_TEAM = "TEAM"
    ASSIGNEE_CHOICES = [
        (ASSIGNEE_USER, "USER"),
        (ASSIGNEE_TEAM, "TEAM"),
    ]
    service_type_choices = [
        ("COMPLAINT", "COMPLAINT"),
        ("REQUEST", "REQUEST"),
        ("SPECIAL_REQUEST", "SPECIAL_REQUEST")
    ]
    PRIORITY_CHOICES = [
        ('LOW','LOW'),
        ('MEDIUM','MEDIUM'),
        ('HIGH','HIGH'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    service_type = models.CharField(max_length=20,choices=service_type_choices,null=True)
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,null=True)
    sla = models.CharField(max_length=10,null=True)
    keywords = models.TextField(null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='service_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='service_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignee_type = models.CharField(
        max_length=10,
        choices=ASSIGNEE_CHOICES,
        default=ASSIGNEE_USER,
    )
    user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='service_user')
    user_group=models.ForeignKey(UserGroup, on_delete=models.PROTECT,null=True,related_name='service_user_group')
    static_file = models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
    workorder_settings = models.ForeignKey(WorkOrderSettings, on_delete=models.PROTECT,null=True)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT,null=True)
    icon = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = 'workorder_api_services'