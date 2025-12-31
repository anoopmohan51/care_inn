from django.db import models
from workorder_api.models.folder import Folder
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder_settings import WorkOrderSettings
from staticfiles_api.models.staticfiles import StaticFiles
from core_api.models.tenant import Tenant

class Informations(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT,null=True)
    title = models.CharField(max_length=255,null=True)
    information = models.TextField(null=True)
    workorder_settings = models.ForeignKey(WorkOrderSettings, on_delete=models.PROTECT,null=True)
    icon = models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='informations_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='informations_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'workorder_api_informations'