from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers

class RoomTypes(models.Model):
    room_type = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=50,null=True)
    priority = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='room_types_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='room_types_updated_user')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'workorder_api_room_types'


class FloorPlan(models.Model):
    name = models.CharField(max_length=255,null=True)
    room_types = models.ForeignKey(RoomTypes, on_delete=models.PROTECT,null=True)
    code = models.CharField(max_length=50,null=True)


    class Meta:
        db_table = 'workorder_api_floor_plan'
