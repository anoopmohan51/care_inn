from rest_framework import serializers
from core_api.models.tenant import Tenant

class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)