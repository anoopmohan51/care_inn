from django.db import models
from workorder_api.models.workorder import WorkOrder
from core_api.models.appusers import AppUsers

class WorkOrderFollowers(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.PROTECT,null=True)
    follower = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='workorder_followers_follower')
    created_at = models.DateTimeField(auto_now_add=True)