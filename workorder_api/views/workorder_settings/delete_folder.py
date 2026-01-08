from workorder_api.models.folder import Folder
from workorder_api.models.services import Services
from workorder_api.models.informations import Informations
from workorder_api.models.requested_items import RequestedItems
def _delete_folders_recursive(self, parent_folder_id):
    child_folders = Folder.objects.filter(parent_folder_id=parent_folder_id)
    for child_folder in child_folders:
        self._delete_folders_recursive(child_folder.id)
        Services.objects.filter(folder_id=child_folder.id).update(is_delete=True)
        Informations.objects.filter(folder_id=child_folder.id).update(is_delete=True)
        RequestedItems.objects.filter(folder_id=child_folder.id).update(is_delete=True)
        child_folder.delete()
