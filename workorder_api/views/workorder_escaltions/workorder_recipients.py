from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from workorder_api.serializers.workorder_escalations_serializer import WorkorderEscalationRecipientsSerializer
from django.db import transaction

def _create_update_escalation_recipients(request,data:list,workorder_escalation_id:int):
    try:
        with transaction.atomic():
            ids_list = []
            for record in data:
                if "id" in record:
                    update_data = {
                        "user": record.get('user'),
                        "role": record.get('role'),
                        "_type": WorkorderEscalationRecipients.TYPE_USER if record.get('user') else WorkorderEscalationRecipients.TYPE_ROLE
                    }
                    serializer = WorkorderEscalationRecipientsSerializer(
                        WorkorderEscalationRecipients.objects.get(id=record.get('id')),
                        data=update_data,
                        context={'request': request}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                else:
                    create_data = {
                        "user": record.get('user'),
                        "role": record.get('role'),
                        "escalation_level": workorder_escalation_id,
                        "_type": WorkorderEscalationRecipients.TYPE_USER if record.get('user') else WorkorderEscalationRecipients.TYPE_ROLE
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
            