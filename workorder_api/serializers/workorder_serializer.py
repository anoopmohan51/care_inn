from rest_framework import serializers
from workorder_api.models import WorkOrder
from workorder_api.activity_context.activity_context import set_activity_user, clear_activity_user
from django.contrib.auth import get_user_model
from workorder_api.models.workorder import WorkOrderImages
from core_api.models.appusers import AppUsers
from core_api.models.usergroups import UserGroup
from django.db.models.functions import Concat
from django.db.models import Value,F
from workorder_api.models.workorder_timeline import WorkOrderTimeline
from django.db.models import Sum

class WorkOrderSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    service_name = serializers.SerializerMethodField('get_service_name')
    assignee_name = serializers.SerializerMethodField('get_assignee_name')
    department_name = serializers.SerializerMethodField('get_department_name')
    created_user_name = serializers.SerializerMethodField('get_created_user_name')
    timeline_id = serializers.SerializerMethodField('get_timeline_id')
    total_working_time = serializers.SerializerMethodField('get_total_working_time')
    room_number = serializers.SerializerMethodField('get_room_number')

    def get_created_user_name(self, obj):
        if obj.created_user:
            user = AppUsers.objects.filter(id=obj.created_user.id,is_delete=False).annotate(
                name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values('name').first()
            return user.get('name') if user else None
        return None
    def get_department_name(self, obj):
        return obj.service.department.name if obj.service and obj.service.department else None

    def get_assignee_name(self, obj):
        if obj.assignee_type == 'USER':
            user = AppUsers.objects.filter(id=obj.user.id,is_delete=False).annotate(
                name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values('name').first()
            return user.get('name') if user else None
        elif obj.assignee_type == 'TEAM':
            user_group = UserGroup.objects.filter(id=obj.user_group.id,is_delete=False).values('name').first()
            return user_group.get('name') if user_group else None
        return None

    def get_service_name(self, obj):
        return obj.service.name if obj.service else None

    def get_images(self, obj):
        return WorkOrderImages.objects.filter(workorder=obj.id).values()
    
    def get_timeline_id(self, obj):
        timeline = WorkOrderTimeline.objects.filter(workorder=obj.id,is_delete=False).order_by('-created_at').first()
        return timeline.id if timeline else None
    
    def get_total_working_time(self, obj):
        return WorkOrderTimeline.objects.filter(workorder=obj.id,is_delete=False, is_close=False).aggregate(total_duration=Sum('duration'))['total_duration']
    
    def get_room_number(self, obj):
        return obj.room.room_number if obj.room else None

    class Meta:
        model = WorkOrder
        fields = '__all__'
        # extra_kwargs = {
        #     'created_user': {'read_only': True},
        #     'updated_user': {'read_only': True},
        # }
    def create(self, validated_data):
        request = self.context.get('request')
        user = get_user_model().objects.get(id=request.user.id,is_delete=False)
        validated_data['status'] = WorkOrder.WORKORDER_STATUS_ASSIGNED_NOT_STARTED
        set_activity_user(user)
        try:
            return super().create(validated_data)
        finally:
            clear_activity_user()
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = get_user_model().objects.get(id=request.user.id,is_delete=False)
        set_activity_user(user)
        try:
            return super().update(instance, validated_data)
        finally:
            clear_activity_user()

class WorkOrderNursingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)