from django.db import models
from workorder_api.models.folder import Folder
from workorder_api.models.services import Services

class FolderRequestedItems(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    min_quantity = models.IntegerField(null=True)
    max_quantity = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_api_folder_requested_items'