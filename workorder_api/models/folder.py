from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='folder_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='folder_updated_user')
    parent_folder = models.ForeignKey('self', on_delete=models.PROTECT,null=True)
    position = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'workorder_api_folder'