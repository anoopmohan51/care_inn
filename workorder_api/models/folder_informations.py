from django.db import models
# from workorder_api.models.folder import Folder
from core_api.models.appusers import AppUsers

class FolderInformations(models.Model):
    # folder = models.ForeignKey(Folder, on_delete=models.PROTECT,null=True)
    information = models.TextField(null=True)