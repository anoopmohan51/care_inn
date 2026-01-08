from rest_framework import serializers
from core_api.models.external_api_key import ExternalApiKey

class ExternalApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalApiKey
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['tenant'] = request.user.tenant
        return super().update(instance, validated_data)