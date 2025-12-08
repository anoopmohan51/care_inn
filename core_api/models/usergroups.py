from django.db import models
from core_api.models.appusers import AppUsers
from core_api.models.tenant import Tenant

class UserGroup(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='usergroup_created_user')
    updated_user=models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='usergroup_updated_user')
    tenant=models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    is_delete=models.BooleanField(default=False)