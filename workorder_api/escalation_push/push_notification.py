from django.utils import timezone
from core_api.models.appusers import AppUsers
from core_api.models.user_device_details import UserDeviceDetails
from workorder_api.tasks.push_notification.push_notification import send_escalation_push_notification_task

def send_escalation_push_notification(users_to_notify,workorder_id,escalation_level,level):
    time_stamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    title = "Escalation Level Triggered"
    body = f"Escalation level Triggered for Workorder {workorder_id}"
    push_data = {
        'activity':'ESCALATION_TRIGGERED',
        'workorder_id':str(workorder_id),
        'escalation_level':str(escalation_level),
        'level':str(level),
        'time_stamp':str(time_stamp)
    }
    users_email = [user.get('email') for user in users_to_notify]
    users_device_tokens = list(UserDeviceDetails.objects.filter(user__email__in=users_email).values_list('device_id',flat=True))
    if users_device_tokens:
        send_escalation_push_notification_task(users_device_tokens,title,body,push_data)
