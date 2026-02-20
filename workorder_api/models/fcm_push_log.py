# from django.db import models
# from core_api.models.appusers import AppUsers


# class FcmPushLog(models.Model):
#     user = models.ForeignKey(AppUsers, on_delete=models.PROTECT)
#     push_data = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'workorder_api_fcm_push_log'