from rest_framework import serializers
from core_api.models.role_permission import RolePermission
from core_api.models.permission import Permission

class RolePermissionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return obj.permission.name
       
    class Meta:
        model = RolePermission
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
        