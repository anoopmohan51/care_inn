from workorder_api.models.workorder import WorkOrder
from core_api.models.appusers import AppUsers
from core_api.models.usergroups import UserGroup
from core_api.send_email.send_email import send_email


def send_alerts(workorder_id,roles_id:list[int]):
    users = AppUsers.objects.filter(roles__in=roles_id,is_delete=False)
    for user in users:
        send_email(subject,body,user.email)