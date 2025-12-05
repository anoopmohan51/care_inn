# from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # Allow password in requests but not in responses
        }
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        password = request.data.get('password')
        user = super().update(instance, validated_data)
        user.save()
        return user
