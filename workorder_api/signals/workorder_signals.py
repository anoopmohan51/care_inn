from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from workorder_api.models.workorder import WorkOrder
from workorder_api.workorder_activity.workorder_activity_service import WorkOrderActivityService
from workorder_api.activity_context.activity_context import set_activity_user, clear_activity_user
import logging

logger = logging.getLogger(__name__)

_workorder_cache ={}

important_fields = ['status', 'assignee_type', 'user_group', 'priority', 'when_to_start', 'sla_minutes', 'patient_id', 'description']

@receiver(post_save, sender=WorkOrder)
def workorder_pre_save(sender, instance, **kwargs):
    if kwargs.get('raw',False) or not instance.pk:
        return
    try:
        # Use only() to fetch only important fields - reduces query overhead
        original = WorkOrder.objects.only(
            'status', 'user', 'user_group', 'priority', 'tenant'
        ).select_related('user', 'user_group', 'priority', 'tenant').get(pk=instance.pk)
        _workorder_cache[instance.pk] = original
    except WorkOrder.DoesNotExist:
        _workorder_cache[instance.pk] = None
    except Exception as e:
        logger.warning(f"Error caching workorder original: {str(e)}")
        _workorder_cache[instance.pk] = None

@receiver(post_save, sender=WorkOrder)
def workorder_post_save(sender, instance, created, **kwargs):
    if kwargs.get('raw',False):
        return
    update_fields = kwargs.get('update_fields')
    if update_fields and 'status' in update_fields:
        if not any(field in IMPORTANT_FIELDS for field in update_fields):
            return
    created_user = get_activity_user() or (instance.created_user if created else instance.updated_user)
    try:
        if created:
            WorkOrderActivityService.log_creation(
                workorder=instance,
                created_user=created_user,
            )
        else:
            original = _workorder_cache.get(instance.pk,None)
            if orginal:
                changes = []
                activity_type = 'NOTE'
                from_value = None
                to_value = None
                from_user = None
                to_user = None
                assigned_user = None
                user_group = None
                
                # Track status changes
                if original.status != instance.status:
                    activity_type = 'STATUS'
                    from_value = original.status or 'None'
                    to_value = instance.status or 'None'
                    changes.append(f"Status: {from_value} → {to_value}")
                
                # Track assignment changes
                elif original.user != instance.user or original.user_group != instance.user_group:
                    activity_type = 'ASSIGNED'
                    from_user = original.user
                    to_user = instance.user
                    assigned_user = instance.user
                    user_group = instance.user_group
                    changes.append("Assignment changed")
                
                # Track priority changes
                elif original.priority != instance.priority:
                    activity_type = 'PRIORITY'
                    from_value = original.priority.name if original.priority else 'None'
                    to_value = instance.priority.name if instance.priority else 'None'
                    changes.append(f"Priority: {from_value} → {to_value}")
                
                # Only create activity if there are actual changes
                if changes:
                    WorkOrderActivityService.create_activity(
                        workorder=instance,
                        activity_type=activity_type,
                        created_user=created_user,
                        message=" | ".join(changes),
                        from_value=from_value,
                        to_value=to_value,
                        from_user=from_user,
                        to_user=to_user,
                        assigned_user=assigned_user,
                        user_group=user_group
                    )
    except Exception as e:
        # Don't break the save operation - log error but continue
        logger.error(f"Error creating workorder activity: {str(e)}", exc_info=True)
                