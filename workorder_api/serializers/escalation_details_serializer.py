from rest_framework import serializers
from workorder_api.models.workorder_escalations_log import WorkOrderEscalationsLog
from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from workorder_api.serializers.workorder_escalations_serializer import WorkOrderEscalationsSerializer
from django.db.models.functions import Concat
from django.db.models import Value,F
from django.db.models import Case, When, CharField


class EscalationDetailsSerializer(serializers.ModelSerializer):

    escalated_to_name = serializers.SerializerMethodField('get_escalated_to')
    role_name = serializers.SerializerMethodField('get_role_name')

    def get_role_name(self, obj):
        role = WorkorderEscalationRecipients.objects.filter(
            escalation_level=obj.escalation_level,
            escalation_level__level=obj.level
        ).annotate(
            role_name = F('user__role__name')
        ).values('role_name').first()
        return role.get('role_name') if role else None

    def get_escalated_to(self, obj):
        recipients = WorkorderEscalationRecipients.objects.filter(
            escalation_level=obj.escalation_level,
            escalation_level__level=obj.level
        ).annotate(
             display_name=Case(
            When(
                _type=WorkorderEscalationRecipients.TYPE_USER,
                then=Concat(
                    F('user__first_name'), Value(' '), F('user__last_name')
                )
            ),
            When(
                _type=WorkorderEscalationRecipients.TYPE_ROLE,
                then=F('role__name')
            ),
            default=Value(''),
            output_field=CharField()
        )
        ).values('display_name').first()
        return recipients.get('display_name') if recipients else None

    class Meta:
        model = WorkOrderEscalationsLog
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        return super().update(instance, validated_data)