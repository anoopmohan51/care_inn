from django.db import models
from core_api.models.appusers import AppUsers


class UserDeviceDetails(models.Model):
    SOURCE_CHOICES = [
        ('WEB','WEB'),
        ('ANDROID','ANDROID'),
        ('IOS','IOS'),
    ]
    user = models.ForeignKey(AppUsers, on_delete=models.PROTECT)
    source = models.CharField(max_length=30,choices=SOURCE_CHOICES,default='WEB')
    device_id = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_logged_in = models.BooleanField(default=False)