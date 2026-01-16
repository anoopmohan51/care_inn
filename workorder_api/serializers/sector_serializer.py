from rest_framework import serializers
from workorder_api.models import Sector
from core_api.models.appusers import AppUsers
from django.db.models.functions import Concat
from django.db.models import Value,F

class SectorSerializer(serializers.ModelSerializer):
    created_user_name = serializers.SerializerMethodField('get_created_user_name')
    updated_user_name = serializers.SerializerMethodField('get_updated_user_name')

    def get_created_user_name(self, obj):
        user = AppUsers.objects.filter(id=obj.created_user.id,is_delete=False).annotate(
            name = Concat(F('first_name'), Value(' '), F('last_name'))
        ).values('name').first()
        return user.get('name') if user else None

    def get_updated_user_name(self, obj):
        if obj.updated_user:
            user = AppUsers.objects.filter(id=obj.updated_user.id,is_delete=False).annotate(
                name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values('name').first()
            return user.get('name') if user else None
        return None

    class Meta:
        model = Sector
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        print("request.user::::::::::",request.user.tenant.id)
        validated_data['created_user'] = request.user
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)