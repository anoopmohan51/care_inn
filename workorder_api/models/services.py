from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from core_api.models.service_type import ServiceType
from core_api.models.priority import Priority
from staticfiles_api.models.staticfiles import StaticFiles

class Services(models.Model):
    ASSIGNEE_USER = "USER"
    ASSIGNEE_TEAM = "TEAM"
    ASSIGNEE_CHOICES = [
        (ASSIGNEE_USER, "USER"),
        (ASSIGNEE_TEAM, "TEAM"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT,null=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT,null=True)
    sla = models.CharField(max_length=10,null=True)
    keywords = models.TextField(null=True)
    primary_image = models.CharField(max_length=255,null=True)
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
    icon=models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
   