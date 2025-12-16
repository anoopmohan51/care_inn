from django.db import models

class PermissionCategory(models.Model):
    name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = 'core_permission_category'
