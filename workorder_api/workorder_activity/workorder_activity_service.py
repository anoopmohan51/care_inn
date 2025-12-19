from workorder_api.models.workorder_activity import WorkOrderActivity
from workorder_api.serializers.workorder_activity_serializer import WorkOrderActivitySerializer
from core_api.models.tenant import Tenant
from core_api.models.appusers import AppUsers
from core_api.models.usergroup import UserGroup
from workorder_api.models.workorder import WorkOrder
from django.db import transaction

class WorkOrderActivityService:

    @staticmethod
    @transaction.atomic
    def create_workorder_activity(
        workorder: WorkOrder,
        activity: str,
        message: str,
        is_added_by_patient: bool,
        from_value: str,
        to_value: str,
        from_user: AppUsers,
        to_user: AppUsers,
        assigned_user: AppUsers,
        accepted_user: AppUsers,
        user_group: UserGroup,
        created_user: AppUsers = None,

    ) -> WorkOrderActivity:
        if activity not in dict(WorkOrderActivity.ACTIVITY_CHOICES):
            raise ValueError(f"Invalid activity: {activity}")
        activity = WorkOrderActivity.objects.create(
            workorder=workorder,
            activity=activity,
            message=message,
            is_added_by_patient=is_added_by_patient,
            from_value=from_value,
            to_value=to_value,
            from_user=from_user,
            to_user=to_user,
            assigned_user=assigned_user,
            accepted_user=accepted_user,
            user_group=user_group,
            created_user=created_user,
        )
        return activity
    
    @staticmethod
    def log_status_change(
        workorder: WorkOrder,
        from_status: str,
        to_status: str,
        user: AppUsers,
    ) -> None:
        return WorkOrderActivityService.create_workorder_activity(
            workorder=workorder,
            activity='STATUS',
            message=f"Status changed from {from_status} to {to_status}",
            is_added_by_patient=False,
            from_value=from_status,
            to_value=to_status,
            from_user=user,
            to_user=user,
            assigned_user=None,
            accepted_user=None,
            user_group=None,
        )
    
    @staticmethod

    def log_assingment(
        workorder: WorkOrder,
        assigned_user: AppUsers = None,
        user_group=None,
        from_user: AppUsers = None,
        created_user: AppUsers = None,
        message: str = None
    ) -> None:
        return WorkOrderActivityService.create_workorder_activity(
            workorder=workorder,
            activity='ASSIGNED',
            message=message,
            is_added_by_patient=False,
            from_value=None,
            to_value=None,
            from_user=from_user,
            to_user=assigned_user,
            assigned_user=assigned_user,
            accepted_user=None,
            user_group=user_group,
        )
    
    @staticmethod
    def log_accepted(
        workorder: WorkOrder,
        accepted_user: AppUsers = None,
        from_user: AppUsers = None,
        created_user: AppUsers = None,
        message: str = None
    ) -> None:
        return WorkOrderActivityService.create_workorder_activity(
            workorder=workorder,
            activity='ACCEPTED',
            message=message,
            is_added_by_patient=False,
            from_value=None,
            to_value=None,
            from_user=from_user,
            to_user=accepted_user,
            assigned_user=None,
            accepted_user=accepted_user,
            user_group=None,
        )
    
    @staticmethod
    def log_creation(
        workorder: WorkOrder,
        created_user: AppUsers = None,
        message: str = None
    ) -> None:
        return WorkOrderActivityService.create_workorder_activity(
            workorder=workorder,
            activity='CREATED',
            message=None,
            is_added_by_patient=False,
            from_value=None,
            to_value=None,
            created_user=created_user
        )
    
    @staticmethod
    def log_priority_change(
        workorder: WorkOrder,
        from_priority: str,
        to_priority: str,
        user: AppUsers,
    ) -> None:
        return WorkOrderActivityService.create_workorder_activity(
            workorder=workorder,
            activity='PRIORITY',
            message=f"Priority changed from {from_priority} to {to_priority}",
            is_added_by_patient=False,
            from_value=from_priority,
            to_value=to_priority,
            from_user=user,
            to_user=user,
            assigned_user=None,
            accepted_user=None,
            user_group=None,
        )
    
    @staticmethod
    def log_due_date_change(
        workorder: WorkOrder,
        from_due_date: str,
        to_due_date: str,
        user: AppUsers,