from core_api.fcm_push_notification.send_push import send_push_notification
from core_api.models.user_device_details import UserDeviceDetails
from workorder_api.models.workorder import WorkOrder
from workorder_api.tasks.push_notification import send_escalation_push_notification_task
from core_api.models.usergroups import UserGroupUsers



def _send_workorder_push_notification(
    workorder_id,
    priority,
    start_date,
    end_date,
    sla_minutes,
    assigned_user_id=None,
    assigned_user_group_id=None
):
    try:
        title = f"Workorder Assigned"
        body = f"Workorder {workorder_id} has been assigned to you"
        data = {
            'activity':'WORKORDER_ASSIGNED',
            'workorder_id':workorder_id,
            'priority':priority,
            'start_date':start_date,
            'end_date':end_date,
            'sla_minutes':sla_minutes
        }
        if assigned_user_id:
            assigned_user_ids = [assigned_user_id]
        else:
            assigned_user_ids = UserGroupUsers.objects.filter(user_group_id=assigned_user_group_id).values_list('user_id',flat=True)
        users_device_tokens = list(UserDeviceDetails.objects.filter(user=assigned_user_id,is_logged_in=True).values_list('device_id',flat=True))
        if users_device_tokens:
            send_workorder_push_notification_task(users_device_tokens,title,body,data)
    except Exception as e:
        print(e)
        return False
    return True