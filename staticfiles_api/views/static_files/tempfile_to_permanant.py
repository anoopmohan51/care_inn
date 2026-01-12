import os
import shutil
from django.conf import settings
from staticfiles_api.models import StaticFiles
from pathlib import Path

def tempfile_to_permanant(temp_file_ids:list[str]):
    try:
        for temp_file_id in temp_file_ids:
            static_file = StaticFiles.objects.get(id=temp_file_id)
            old_file_path = os.path.join(settings.MEDIA_ROOT,static_file.file_path) 
            if not os.path.exists(old_file_path):
                print("file not found")
                continue
            old_path_obj = Path(old_file_path)
            timestamp = Path(old_file_path).parent.name
            new_file_name = Path(old_file_path).name
            new_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads',timestamp,new_file_name)
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            shutil.move(old_file_path,new_file_path)
            static_file.is_temp = False
            static_file.file_path = new_file_path
            static_file.save()
    except Exception as e:
        print("file move failed")