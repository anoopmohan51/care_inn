from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.workorder_settings import WorkOrderSettings
from staticfiles_api.models.staticfiles import StaticFiles

class Folder(models.Model):
    name = models.CharField(max_length=255)
    workorder_settings = models.ForeignKey(WorkOrderSettings, on_delete=models.PROTECT,null=True)
    parent_folder = models.ForeignKey('self', on_delete=models.PROTECT,null=True)
    position = models.IntegerField(default=0,null=True)
    static_file = models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
    icon = models.CharField(max_length=100,null=True)
    color = models.CharField(max_length=50,null=True)

    class Meta:
        db_table = 'workorder_api_folder'