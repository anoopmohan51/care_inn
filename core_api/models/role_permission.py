from django.db import models
from core_api.models.role import Role
from core_api.models.permission import Permission

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT,null=True,related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT,null=True,related_name='user_permissions')
    create = models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'core_role_permission'
