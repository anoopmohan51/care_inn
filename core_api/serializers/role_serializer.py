from rest_framework import serializers
from core_api.models.role import Role
from core_api.serializers.role_permission_serializer import RolePermissionSerializer

class RoleSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()
    def get_permission(self, obj):
        return RolePermissionSerializer(obj.role_permissions.all(), many=True).data
    class Meta:
        model = Role
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)