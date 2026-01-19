from rest_framework import serializers
from workorder_api.models.workorder_escalations import WorkOrderEscalations,WorkorderEscalationServices,WorkorderEscalationRecipients,WorkorderEscaltionLevels
from core_api.models.appusers import AppUsers
from core_api.models.role import Role
from django.db.models import Value, F
from django.db.models.functions import Concat
class WorkOrderEscalationsSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField('get_services')
    levels = serializers.SerializerMethodField('get_levels')
    created_by = serializers.SerializerMethodField('get_created_by')
    updated_by = serializers.SerializerMethodField('get_updated_by')
    identifier_name = serializers.SerializerMethodField('get_identifier_name')

    def get_identifier_name(self, obj):
        return obj.identifier.name if obj.identifier else None
    
    def get_created_by(self, obj):
        if obj.created_user:
            user = AppUsers.objects.filter(id=obj.created_user.id).annotate(
                name = Concat(F('first_name'),Value(' '),F('last_name'))
            ).values('name').first()
            name = user.get('name')
        else:
            name = None
        return name
    def get_updated_by(self, obj):
        if obj.updated_user:
            user = AppUsers.objects.filter(id=obj.updated_user.id).annotate(
                name = Concat(F('first_name'),Value(' '),F('last_name'))
            ).values('name').first()
            name = user.get('name')
        else:
            name = None
        return name

    def get_services(self, obj):
        services = WorkorderEscalationServices.objects.filter(workorder_escalation=obj)
        return WorkorderEscalationServicesSerializer(services, many=True).data
    
    def get_levels(self, obj):
        levels = WorkorderEscaltionLevels.objects.filter(escalation=obj)
        return WorkorderEscaltionLevelsSerializer(levels, many=True).data
    
    class Meta:
        model = WorkOrderEscalations
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_user'] = request.user
        validated_data['tenant'] = request.user.tenant
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_user'] = request.user
        return super().update(instance, validated_data)

class WorkorderEscalationServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkorderEscalationServices
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class WorkorderEscalationRecipientsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    def get_name(self, obj):
        if obj._type == WorkorderEscalationRecipients.TYPE_USER:
            user = AppUsers.objects.filter(id=obj.user.id).annotate(
                name = Concat(F('first_name'),Value(' '),F('last_name'))
            ).values('name').first()
            return user.get('name')
        else:
            role = Role.objects.filter(id=obj.role.id).values('name').first()
            return role.get('name')


    class Meta:
        model = WorkorderEscalationRecipients
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)

class WorkorderEscaltionLevelsSerializer(serializers.ModelSerializer):
    recipients = serializers.SerializerMethodField('get_recipients')
    def get_recipients(self, obj):
        recipients = WorkorderEscalationRecipients.objects.filter(escalation_level=obj)
        return WorkorderEscalationRecipientsSerializer(recipients, many=True).data
    class Meta:
        model = WorkorderEscaltionLevels
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)