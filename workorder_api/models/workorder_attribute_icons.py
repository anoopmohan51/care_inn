from django.db import models
import uuid
class WorkOrderAttributeIcons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    uploaded_file_name=models.CharField(max_length=255)
    file_path=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    file_type=models.CharField(max_length=30)

    class Meta:
        db_table = 'workorder_attribute_icons'

