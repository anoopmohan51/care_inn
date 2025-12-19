from rest_framework import serializers
from workorder_api.models import WorkOrder
from workorder_api.activity_context.activity_context import set_activity_user, clear_activity_user

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        extra_kwargs = {
            'created_user': {'read_only': True},
            'updated_user': {'read_only': True},
        }
    def create(self, validated_data):
        request = self.context.get('request')
        if  request and request.user:
            set_activity_user(request.user)
            validated_data['created_user'] = request.user
        try:
            return super().create(validated_data)
        finally:
            clear_activity_user()
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if  request and request.user:
            set_activity_user(request.user)
            validated_data['updated_user'] = request.user
        try:
            return super().update(instance, validated_data)
        finally:
            clear_activity_user()