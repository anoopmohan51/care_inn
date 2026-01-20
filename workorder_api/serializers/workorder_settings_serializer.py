from rest_framework import serializers
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.models.folder import Folder
from workorder_api.models.services import Services
from workorder_api.models.informations import Informations
from workorder_api.models.requested_items import RequestedItems
from workorder_api.serializers.item_serializer import ItemSerializer
from core_api.models.appusers import AppUsers
from django.db.models import F,Value
from django.db.models.functions import Concat
from staticfiles_api.models.staticfiles import StaticFiles


class WorkOrderSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderSettings
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_user'] = request.user
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)

class WorkOrderSettingsListSerializer(serializers.ModelSerializer):
    created_user_name = serializers.SerializerMethodField('get_created_user_name')
    color = serializers.SerializerMethodField('get_color')
    icon = serializers.SerializerMethodField('get_icon')
    static_file = serializers.SerializerMethodField('get_static_file')
    folder_id = serializers.SerializerMethodField('get_folder_id')
    workorder_settings_id = serializers.SerializerMethodField('get_workorder_settings_id')
    name = serializers.SerializerMethodField('get_name')
    service_id = serializers.SerializerMethodField('get_service_id')
    item_id = serializers.SerializerMethodField('get_item_id')
    information_id = serializers.SerializerMethodField('get_information_id')
    request_id = serializers.SerializerMethodField('get_request_id')

    def get_information_id(self, obj):
        if obj.type == 'INFORMATION':
            information = Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return information.id if information else None
        return None

    def get_request_id(self, obj):
        if obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.id if request else None
        return None

    def get_item_id(self, obj):
        if obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.id if request else None
        return None

    def get_service_id(self, obj):
        if obj.type == 'SERVICE':
            service = Services.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return service.id if service else None
        return None

    def get_name(self, obj):
        if obj.type == 'FOLDER':
            folder = Folder.objects.filter(workorder_settings_id=obj.id,parent_folder_id__isnull=True).first()
            return folder.name if folder else None
        elif obj.type == 'SERVICE':
            service = Services.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return service.name if service else None
        elif obj.type == 'INFORMATION':
            information = Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return information.title if information else None
        elif obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.name if request else None
        return None

    def get_workorder_settings_id(self, obj):
        return obj.id
    
    def get_color(self, obj):
        if obj.type == 'FOLDER':
            folder = Folder.objects.filter(workorder_settings_id=obj.id,parent_folder_id__isnull=True).first()
            return folder.color if folder else None
        elif obj.type == 'SERVICE':
            service = Services.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return service.color if service else None
        elif obj.type == 'INFORMATION':
            information = Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return information.color if information else None
        elif obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.color if request else None
        return None
    
    def get_icon(self, obj):
        if obj.type == 'FOLDER':
            folder = Folder.objects.filter(workorder_settings_id=obj.id,parent_folder_id__isnull=True).first()
            return folder.icon if folder else None
        elif obj.type == 'SERVICE':
            service = Services.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return service.icon if service else None
        elif obj.type == 'INFORMATION':
            information = Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return information.icon if information else None
        elif obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.icon if request else None 
        return None
    
    def get_folder_id(self, obj):
        if obj.type == 'FOLDER':
            folder = Folder.objects.filter(workorder_settings_id=obj.id,parent_folder_id__isnull=True).first()
            return folder.id if folder else None
        return None
    
    def get_static_file(self, obj):
        if obj.type == 'FOLDER':
            folder = Folder.objects.filter(workorder_settings_id=obj.id,parent_folder_id__isnull=True).first()
            return folder.static_file.id if folder and folder.static_file else None
        elif obj.type == 'SERVICE':
            service = Services.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return service.static_file.id if service and service.static_file else None
        elif obj.type == 'INFORMATION':
            information = Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return information.static_file.id if information and information.static_file else None
        elif obj.type == 'REQUEST':
            request = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False,folder_id__isnull=True).first()
            return request.static_file.id if request and request.static_file else None
        return None
    
    def get_created_user_name(self, obj):
        user = AppUsers.objects.filter(id=obj.created_user.id,is_delete=False).annotate(
            name = Concat(F('first_name'), Value(' '), F('last_name'))
        ).values('name').first()
        return user.get('name') if user else None
    
    class Meta:
        model = WorkOrderSettings
        fields = '__all__'
    
    

class FolderDetailsListSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField('get_folders')
    services = serializers.SerializerMethodField('get_services')
    informations = serializers.SerializerMethodField('get_informations')
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Folder
        fields = '__all__'
    
    def get_folders(self, obj):
        return Folder.objects.filter(parent_folder_id=obj.id).values()
    
    def get_services(self, obj):
        return Services.objects.filter(folder_id=obj.id,is_delete=False).values()
    
    def get_informations(self, obj):
        return Informations.objects.filter(folder_id=obj.id,is_delete=False).values().first()
    
    def get_items(self, obj):
        request_items = RequestedItems.objects.filter(folder_id=obj.id,is_delete=False)
        return ItemSerializer(request_items,many=True).data

class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
