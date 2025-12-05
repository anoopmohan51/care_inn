from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)