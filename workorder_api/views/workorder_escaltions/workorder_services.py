from workorder_api.models import WorkorderEscalationServices
from workorder_api.serializers.workorder_escalations_serializer import WorkorderEscalationServicesSerializer
from django.db import transaction


def _create_update_escalation_services(request,data:list,workorder_escalation_id:int):
    try:
        with transaction.atomic():
            to_create = []
            incoming_service_ids = set(data)
            existing_service_ids = set(
                WorkorderEscalationServices.objects.filter(
                    workorder_escalation_id=workorder_escalation_id
                ).values_list("service_id",flat=True)
            )
            to_create = [
                WorkorderEscalationServices(
                    workorder_escalation_id=workorder_escalation_id,
                    service_id=service_id
                )
                for service_id in incoming_service_ids - existing_service_ids
            ]
            if to_create:
                WorkorderEscalationServices.objects.bulk_create(to_create)
            WorkorderEscalationServices.objects.filter(
                workorder_escalation_id=workorder_escalation_id
            ).exclude(
                service_id__in=incoming_service_ids
            ).delete()
    except Exception as e:
        print(e)