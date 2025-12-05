from rest_framework import serializers
from workorder_api.models import Rooms

class RoomSerializer(serializers.ModelSerializer):
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
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)
        