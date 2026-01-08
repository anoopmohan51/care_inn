from workorder_api.models.workorder_activity import WorkOrderActivity
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from core_api.models.usergroups import UserGroup
from workorder_api.models.workorder import WorkOrder
from django.db import transaction

class WorkOrderActivityService:

    @staticmethod
    @transaction.atomic
    def create_workorder_activity(
        data: dict
    ) -> WorkOrderActivity:
        if data.get('activity') not in dict(WorkOrderActivity.ACTIVITY_CHOICES):
            raise ValueError(f"Invalid activity: {activity}")
        activity = WorkOrderActivity.objects.create(**data)
        return activity
    
    @staticmethod
    def log_creation(
        data: list
    ) -> None:
        for record in data:
            WorkOrderActivityService.create_workorder_activity(record)