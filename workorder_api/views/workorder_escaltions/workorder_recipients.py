from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from workorder_api.serializers.workorder_escalations_serializer import WorkorderEscalationRecipientsSerializer
from django.db import transaction

def _create_update_escalation_recipients(request,data:list,workorder_escalation_id:int):
    try:
        with transaction.atomic():
            ids_list = []
            for record in data:
                user = record.get('user')
                role = record.get('role')
                if not user and not role:
                    continue
                recipient_type = (
                    WorkorderEscalationRecipients.TYPE_USER if user else 
                    WorkorderEscalationRecipients.TYPE_ROLE
                )
                base_data = {
                    "user": user,
                    "role": role,
                    "_type": recipient_type
                }
                existing = None
                if user:
                    existing = WorkorderEscalationRecipients.objects.filter(
                        user=user,
                        escalation_level=workorder_escalation_id
                    ).first()
                if not existing and role:
                    existing = WorkorderEscalationRecipients.objects.filter(
                        role=role,
                        escalation_level=workorder_escalation_id
                    ).first()
                if existing:
                    serializer = WorkorderEscalationRecipientsSerializer(
                        existing,
                        data=base_data,
                        context={'request': request}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        ids_list.append(serializer.data.get('id'))
                else:
                    create_data = {
                        **base_data,
                        "escalation_level": workorder_escalation_id
                    }
                    serializer = WorkorderEscalationRecipientsSerializer(
                        data=create_data,
                        context={'request': request}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        ids_list.append(serializer.data.get('id'))
            WorkorderEscalationRecipients.objects.filter(
                escalation_level=workorder_escalation_id
            ).exclude(id__in=ids_list).delete()
    except Exception as e:
        print(e)
            