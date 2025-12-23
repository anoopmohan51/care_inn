from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from workorder_api.models.workorder import WorkOrder
from workorder_api.workorder_activity.workorder_activity_service import WorkOrderActivityService
from workorder_api.activity_context.activity_context import set_activity_user, clear_activity_user, get_activity_user
import logging

logger = logging.getLogger(__name__)

_workorder_cache ={}

important_fields = ['priority', 'assignee_type', 'user_group', 'priority', 'when_to_start', 'sla_minutes', 'patient_id', 'description']

@receiver(pre_save, sender=WorkOrder)
def workorder_pre_save(sender, instance, **kwargs):
    if kwargs.get('raw',False) or not instance.pk:
        return
    try:
        # Use only() to fetch only important fields - reduces query overhead
        original = WorkOrder.objects.get(pk=instance.pk)
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
            activity_data=[]
            activity_data.append({
                'activity': 'CREATED',
                'workorder': instance,
                'initiated_by': created_user
            })
            if instance.user_group or instance.user: 
                activity_data.append({
                    'activity': 'ASSIGNED',
                    'to_value': f"TEAM-{instance.user_group}" if instance.user_group else f"USER-{instance.user}",
                    'initiated_by': created_user,
                    'workorder': instance
                })
            if instance.priority:
                activity_data.append({
                    'activity': 'PRIORITY',
                    'to_value': f"PRIORITY-{instance.priority}",
                    'initiated_by': created_user,
                    'workorder': instance
                })
            if instance.priority:
                activity_data.append({
                    'activity': 'SLA_START_TIME',
                    'to_value': instance.created_at,
                    'initiated_by': created_user,
                    'workorder': instance
                })
            if instance.sla_minutes:
                activity_data.append({
                    'activity': 'SLA',
                    'to_value': instance.sla_minutes,
                    'initiated_by': created_user,
                    'workorder': instance
                })
            WorkOrderActivityService.log_creation(activity_data)
        else:
            original = _workorder_cache.get(instance.pk,None)
            if original:
                changes = []
                activity_type = 'NOTE'
                from_value = None
                to_value = None
                from_user = None
                to_user = None
                assigned_user = None
                user_group = None
                if original.priority != instance.priority:
                    changes.append({
                        'activity': 'PRIORITY',
                        'from_value': original.priority,
                        'to_value': instance.priority,
                        'initiated_by': created_user,
                        'workorder': instance
                    })
                elif original.assignee_type != instance.assignee_type:
                    if instance.assignee_type == 'USER' and original.assignee_type=='TEAM':
                        changes.append({
                            'activity': 'ASSIGNED',
                            'from_value': f"TEAM-{original.user_group}",
                            'to_value': f"USER-{instance.user}",
                            'initiated_by': created_user,
                            'workorder': instance
                        })
                    elif instance.assignee_type == 'TEAM' and original.assignee_type=='USER':
                        changes.append({
                            'activity': 'ASSIGNED',
                            'from_value': f"USER-{original.user}",
                            'to_value': f"USER-{instance.user_group}",
                            'initiated_by': created_user,
                            'workorder': instance
                        })
                elif instance.start_date!=original.start_date:
                    changes.append({
                        'activity': 'START_DATE',
                        'from_value': original.start_date,
                        'to_value': instance.start_date,
                        'initiated_by': created_user,
                        'workorder': instance
                    })
                elif instance.end_date!=original.end_date:
                    if original.end_date==None:
                        from_value = None
                        to_value = instance.end_date
                    elif instance.end_date==None:
                        from_value = original.end_date
                        to_value = instance.end_date
                    changes.append({
                        'activity': 'END_DATE',
                        'from_value':from_value,
                        'to_value': to_value,
                        'initiated_by': created_user,
                        'workorder': instance
                    })
                print(""""..............changes""""",changes)
                # Only create activity if there are actual changes
                if changes:
                    WorkOrderActivityService.log_creation(changes)
    except Exception as e:
        # Don't break the save operation - log error but continue
        logger.error(f"Error creating workorder activity: {str(e)}", exc_info=True)
                