from workorder_api.models.workorder_escalations import WorkorderEscaltionLevels
from workorder_api.serializers.workorder_escalations_serializer import WorkorderEscaltionLevelsSerializer
from django.db import transaction
from .workorder_escaltions import _create_update_escalation_services
from .workorder_recipients import _create_update_escalation_recipients


def _create_update_escalation_levels(request,data:list,workorder_escalation_id:int):
    try:
        with transaction.atomic():
            ids_list = []
            for record in data:
                if "id" in record:
                    update_data = {
                        "level": record.get('level'),
                        "trigger_time": record.get('trigger_time')
                    }
                    serializer = WorkorderEscaltionLevelsSerializer(
                        WorkorderEscaltionLevels.objects.get(id=record.get('id')),
                        data=update_data,
                        context={'request': request}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        _create_update_escalation_recipients(request,record.get('recipients'),serializer.data.get('id'))
                        ids_list.append(serializer.data.get('id'))
                else:
                    create_data = {
                        "level": record.get('level'),
                        "trigger_time": record.get('trigger_time'),
                        "escalation": workorder_escalation_id
                    }
                    serializer = WorkorderEscaltionLevelsSerializer(
                        data=create_data,
                        context={'request': request}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        _create_update_escalation_recipients(request,record.get('recipients'),serializer.data.get('id'))
                        ids_list.append(serializer.data.get('id'))
            WorkorderEscaltionLevels.objects.filter(escalation=workorder_escalation_id).exclude(id__in=ids_list).delete()
    except Exception as e:
        print("error in create update escalation levels",e)