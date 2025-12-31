from rest_framework import serializers
from workorder_api.models.requested_items import RequestedItems, ItemDetails

class ItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    def get_items(self, obj):
        return ItemDetails.objects.filter(item_id=obj.id).values()
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
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)