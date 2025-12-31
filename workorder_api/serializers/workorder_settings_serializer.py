from rest_framework import serializers
from workorder_api.models.workorder_settings import WorkOrderSettings
from workorder_api.models.folder import Folder
from workorder_api.models.services import Services
from workorder_api.models.informations import Informations
from workorder_api.models.requested_items import RequestedItems
from workorder_api.serializers.item_serializer import ItemSerializer

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
    folders = serializers.SerializerMethodField('get_folders')
    services = serializers.SerializerMethodField('get_services')
    informations = serializers.SerializerMethodField('get_informations')
    items = serializers.SerializerMethodField('get_items')
    class Meta:
        model = WorkOrderSettings
        fields = '__all__'
    
    def get_folders(self, obj):
        return Folder.objects.filter(workorder_settings_id=obj.id).values()
    
    def get_services(self, obj):
        return Services.objects.filter(workorder_settings_id=obj.id,is_delete=False).values()
    
    def get_informations(self, obj):
        return Informations.objects.filter(workorder_settings_id=obj.id,is_delete=False).values().first()
    
    def get_items(self, obj):
        request_items = RequestedItems.objects.filter(workorder_settings_id=obj.id,is_delete=False)
        return ItemSerializer(request_items,many=True).data

class FolderDetailsListSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField('get_folders')
    services = serializers.SerializerMethodField('get_services')
    informations = serializers.SerializerMethodField('get_informations')
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Folder
        fields = '__all__'
    
    def get_folders(self, obj):
        return Folder.objects.filter(folder_id=obj.id).values()
    
    def get_services(self, obj):
        return Services.objects.filter(folder_id=obj.id,is_delete=False).values()
    
    def get_informations(self, obj):
        return Informations.objects.filter(folder_id=obj.id,is_delete=False).values().first()
    
    def get_items(self, obj):
        request_items = RequestedItems.objects.filter(folder_id=obj.id,is_delete=False)
        return ItemSerializer(request_items,many=True).data
