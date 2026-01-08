from rest_framework import serializers
from workorder_api.models.workorder_activity import WorkOrderActivity
from core_api.models.appusers import AppUsers
from core_api.models.usergroups import UserGroup
from django.db.models.functions import Concat
from django.db.models import Value,F

class WorkOrderActivitySerializer(serializers.ModelSerializer):
    initiated_user = serializers.SerializerMethodField()
    from_name = serializers.SerializerMethodField()
    to_name = serializers.SerializerMethodField()
    class Meta:
        model = WorkOrderActivity
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)
    
    def get_initiated_user(self, obj):
        if obj.initiated_by:
            user = AppUsers.objects.filter(id=obj.initiated_by.id,is_delete=False).annotate(
                name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values('name').first()
            name = user.get('name')
            return name
        return None
    
    def get_from_name(self, obj):
        name = None
        if obj.from_value:
            if obj.from_value.startswith('TEAM-'):
                user_group = UserGroup.objects.filter(id=obj.from_value.split('-')[1],is_delete=False).values('name').first()
                name = user_group.get('name')
            elif obj.from_value.startswith('USER-'):
                user = AppUsers.objects.filter(id=obj.from_value.split('-')[1],is_delete=False).annotate(
                    name = Concat(F('first_name'), Value(' '), F('last_name'))
                ).values('name').first()
                name = name.get('name')
            else:
                name = obj.from_value
            return name
    
    def get_to_name(self, obj):
        name = None
        if obj.to_value:
            if obj.to_value.startswith('TEAM-'):
                user_group = UserGroup.objects.filter(id=obj.to_value.split('-')[1],is_delete=False).values('name').first()
                name = user_group.get('name')
            elif obj.to_value.startswith('USER-'):
                user = AppUsers.objects.filter(id=obj.to_value.split('-')[1],is_delete=False).annotate(
                    name = Concat(F('first_name'), Value(' '), F('last_name'))
                ).values('name').first()
                name = name.get('name')
            else:
                name = obj.to_value
            return name