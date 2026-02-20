from core_api.fcm_push_notification.send_push import send_push_notification
from core_api.models.user_device_details import UserDeviceDetails
from workorder_api.models.workorder import WorkOrder
from .tasks.push_notification.push_notification import send_workorder_push_notification_task



def _send_workorder_push_notification(
    workorder_id,
    priority,
    start_date,
    end_date,
    sla_minutes,
    assigned_user_id,
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
        users_device_tokens = list(UserDeviceDetails.objects.filter(user=assigned_user_id,is_logged_in=True).values_list('device_id',flat=True))
        if users_device_tokens:
            send_workorder_push_notification_task(users_device_tokens,title,body,data)
    except Exception as e:
        print(e)
        return False
    return True