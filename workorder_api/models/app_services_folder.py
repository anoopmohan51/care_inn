from django.db import models
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from workorder_api.models.services import Services

class ServicesFolder(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    created_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='app_services_folder_created_user')
    updated_user = models.ForeignKey(AppUsers, on_delete=models.PROTECT,null=True,related_name='app_services_folder_updated_user')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.ForeignKey(StaticFiles, on_delete=models.PROTECT,null=True)
    parent_folder = models.ForeignKey('self', on_delete=models.PROTECT,null=True,related_name='parent_folder')
    class Meta:
        db_table = 'workorder_api_services_folder'

class ServicesFolderInformation(models.Model):
    folder = models.ForeignKey(ServicesFolder, on_delete=models.PROTECT,null=True)
    information = models.TextField(null=True)
    
    class Meta:
        db_table = 'workorder_api_app_services_folder_information'

class ServicesFolderServices(models.Model):
    folder = models.ForeignKey(ServicesFolder, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    
    class Meta:
        db_table = 'workorder_api_services_folder_services'

class ServicesFolderRequestedItems(models.Model):
    folder = models.ForeignKey(ServicesFolder, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(Services, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    min_quantity = models.IntegerField(null=True)
    max_quantity = models.IntegerField(null=True)

    class Meta:
        db_table = 'workorder_api_app_services_folder_requested_items'
