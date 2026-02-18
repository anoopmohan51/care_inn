from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.sector import Sector
from workorder_api.models.room_types import RoomTypes
from workorder_api.models.patient_mrn import Mrn

class Rooms(models.Model):
    room_number = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='rooms_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='rooms_updated_user')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    is_delete = models.BooleanField(default=False)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT,null=True,related_name='rooms_sector')
    room_type = models.ForeignKey(RoomTypes, on_delete=models.PROTECT,null=True,related_name='rooms_room_type')
    mrn = models.ForeignKey(Mrn, on_delete=models.PROTECT,null=True,related_name='rooms_mrn')
    code = models.CharField(max_length=255,null=True,blank=True)