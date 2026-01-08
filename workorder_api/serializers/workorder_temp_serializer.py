from rest_framework import serializers
from workorder_api.models import WorkOrderTemp

class WorkOrderTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderTemp
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
