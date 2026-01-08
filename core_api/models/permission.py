from django.db import models
from core_api.models.permission_category import PermissionCategory

class Permission(models.Model):
    name = models.CharField(max_length=255,unique=True)
    category = models.ForeignKey(
        PermissionCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="permission"
    )
    create = models.BooleanField(default=True)
    view = models.BooleanField(default=True)
    edit = models.BooleanField(default=True)
    delete = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_permission'