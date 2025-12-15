from rest_framework import serializers
from workorder_api.models import WorkOrderTimeline

class WorkOrderTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderTimeline
        fields = '__all__'
        extra_kwargs = {
            'created_user': {'read_only': True},
            'updated_user': {'read_only': True},
        }
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)