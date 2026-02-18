from rest_framework import serializers
from workorder_api.models import Rooms
from core_api.models.appusers import AppUsers
from django.db.models.functions import Concat
from django.db.models import Value,F

class RoomSerializer(serializers.ModelSerializer):
    sector_name = serializers.SerializerMethodField('get_sector_name')
    room_type_name = serializers.SerializerMethodField('get_room_type_name')
    created_user_name = serializers.SerializerMethodField('get_created_user_name')

    def get_sector_name(self, obj):
        return obj.sector.name if obj.sector else None
    
    def get_room_type_name(self, obj):
        return obj.room_type.room_type if obj.room_type else None
    
    def get_created_user_name(self, obj):
        if obj.created_user:
            user = AppUsers.objects.filter(id=obj.created_user.id,is_delete=False).annotate(
                name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values('name').first()
            return user.get('name') if user else None
        return None

    class Meta:
        model = Rooms
        fields = '__all__'
        extra_kwargs = {
            'created_user': {'read_only': True},
            'updated_user': {'read_only': True},
        }
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_user'] = request.user
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)
        