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
        from_date = validated_data.get('from_date')
        to_date = validated_data.get('to_date')
        if from_date and to_date:
            time_difference = to_date - from_date
            validated_data['duration'] = int(time_difference.total_seconds())
        return super().update(instance, validated_data)