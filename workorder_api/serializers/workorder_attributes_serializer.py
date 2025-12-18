from rest_framework import serializers
from workorder_api.models import WorkOrderAttributes
from workorder_api.models import WorkOrderAttributeElements
from workorder_api.models import WorkOrderAttributeServices
from workorder_api.models import WorkOrderAttributeRequestItems

class WorkOrderAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAttributes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class WorkOrderAttributeElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAttributeElements
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class WorkOrderAttributeServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAttributeServices
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class WorkOrderAttributeRequestItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAttributeRequestItems
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
