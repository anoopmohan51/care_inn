from rest_framework import serializers
from core_api.models.role import Role
from core_api.serializers.role_permission_serializer import RolePermissionSerializer
from core_api.models.permission import Permission

class RoleListSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()
    def get_permission(self, obj):
        role_permissions = RolePermissionSerializer(obj.role_permissions.all(), many=True).data
        if role_permissions:
            return role_permissions
        else:
            permission_data = Permission.objects.all().values('id','name')
            data = [
                {
                    "name": record.get('name'),
                    "create": False,
                    "view": False,
                    "edit": False,
                    "delete": False,
                    "role": obj.id,
                    "permission": record.get('id')
                } for record in permission_data
            ]
            return data
    class Meta:
        model = Role
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
