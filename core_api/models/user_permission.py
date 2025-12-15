from django.db import models
from core_api.models.appusers import AppUsers
from core_api.models.permission import Permission

class UserPermission(models.Model):
    user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT,null=True,related_name='user_permissions')
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_permission'
