from rest_framework import serializers
from workorder_api.models import WorkOrderRating

class WorkOrderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderRating
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)