from rest_framework import serializers
from workorder_api.models.requested_items import RequestedItems, ItemDetails

class ItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')
    service_name = serializers.SerializerMethodField('get_service_name')
    def get_items(self, obj):
        return ItemDetails.objects.filter(item_id=obj.id).values()
    
    def get_service_name(self,obj):
        return obj.service.name if obj.service else None
    
    class Meta:
        model = RequestedItems
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_user'] = request.user
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data.pop('position',None)
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)