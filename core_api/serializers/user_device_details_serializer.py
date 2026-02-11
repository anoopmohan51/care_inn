from rest_framework import serializers
from core_api.models.user_device_details import UserDeviceDetails

class UserDeviceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDeviceDetails
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)