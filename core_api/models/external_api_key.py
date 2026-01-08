from django.db import models
from core_api.models.tenant import Tenant

class ExternalApiKey(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
