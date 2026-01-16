from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers

class Sector(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='sector_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='sector_updated_user')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'workorder_api_sector'