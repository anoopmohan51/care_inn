from celery import shared_task
from workorder_api.models.workorder import WorkOrder
from core_api.fcm_push_notification.send_push import send_push_notification
from core_api.models.usergroups import UserGroupUsers
from core_api.models.user_device_details import UserDeviceDetails
from django.utils import timezone

@shared_task
def workorder_push_notification_task(
    workorder_id,
    priority,
    start_date,
    end_date,
    sla_minutes,
    assigned_user_id=None,
    assigned_user_group_id=None
):
        # try:
        print('assigned_user_id::::::::::::::::::',assigned_user_id)
        print('assigned_user_group_id::::::::::::::::::',assigned_user_group_id)
        title = f"Workorder Assigned"
        body = f"Workorder {workorder_id} has been assigned to you"
        data = {
            'activity':'WORKORDER_ASSIGNED',
            'workorder_id':str(workorder_id),
            'priority':str(priority),
            'start_date':str(start_date),
            'end_date':str(end_date),
            'sla_minutes':str(sla_minutes),
            'time_stamp':timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if assigned_user_id:
            assigned_user_ids = [assigned_user_id]
        else:
            assigned_user_ids = UserGroupUsers.objects.filter(user_group_id=assigned_user_group_id).values_list('user_id',flat=True)
        users_device_tokens = list(UserDeviceDetails.objects.filter(user=assigned_user_id,is_logged_in=True).values_list('device_id',flat=True))
        print("device tokens::::::::::::::::::",users_device_tokens)
        if users_device_tokens:
            send_push_notification(users_device_tokens,title,body,data)
    # except Exception as e:
    #     print(e)
    #     return False
    # return True

