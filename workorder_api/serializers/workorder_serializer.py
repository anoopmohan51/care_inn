from rest_framework import serializers
from workorder_api.models import WorkOrder
from workorder_api.activity_context.activity_context import set_activity_user, clear_activity_user
from django.contrib.auth import get_user_model

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        # extra_kwargs = {
        #     'created_user': {'read_only': True},
        #     'updated_user': {'read_only': True},
        # }
    def create(self, validated_data):
        request = self.context.get('request')
        user = get_user_model().objects.get(id=request.user.id,is_delete=False)
        set_activity_user(user)
        try:
            return super().create(validated_data)
        finally:
            clear_activity_user()
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = get_user_model().objects.get(id=request.user.id,is_delete=False)
        set_activity_user(user)
        try:
            return super().update(instance, validated_data)
        finally:
            clear_activity_user()

class WorkOrderNursingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)