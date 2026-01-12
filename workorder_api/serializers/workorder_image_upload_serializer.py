from rest_framework import serializers
from workorder_api.models.workorder import WorkOrderImages

class WorkOrderImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderImages
        fields = '__all__'
    
    def create(self, validated_data):
        return WorkOrderImages.objects.create(**validated_data)