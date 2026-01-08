from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers

class WorkOrderSettings(models.Model):
    type_choices = [
        ('FOLDER','FOLDER'),
        ('SERVICE','SERVICE'),
        ('REQUEST','REQUEST'),
        ('INFORMATION','INFORMATION')
    ]
    type = models.CharField(max_length=20,choices=type_choices)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_settings_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_settings_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workorder_settings'