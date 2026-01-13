from workorder_api.models import FloorPlan
from django.db import transaction
from workorder_api.serializers.floor_plan_serializer import FloorPlanSerializer


def _create_update_floor_plan(room_type_id,floor_plan_data):
    if not floor_plan_data:
        return []
    to_create = []
    to_update = []
    floor_plan_ids = [record.get('id') for record in floor_plan_data if record.get('id')]
    
    for record in floor_plan_data:
        if record.get('id'):
            to_update.append(
                FloorPlan(
                    id=record.get('id'),
                    name=record.get('name'),
                    code=record.get('code'),
                    room_types_id=room_type_id
                )
            )
        else:
            to_create.append(
                FloorPlan(
                    name=record.get('name'),
                    code=record.get('code'),
                    room_types_id=room_type_id
                )
            )
    with transaction.atomic():
        created = FloorPlan.objects.bulk_create(to_create)
        updated = FloorPlan.objects.bulk_update(to_update,['name','code'])
    if created:
        created_ids = [ obj.id for obj in created if hasattr(obj,'id')]
        floor_plan_ids.extend(created_ids)
    if floor_plan_ids:
        floor_plan = FloorPlan.objects.filter(id__in=floor_plan_ids)
        all_data = FloorPlanSerializer(floor_plan,many=True).data
        return all_data
    else:
        return []
