from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from core_api.models.appusers import AppUsers
from workorder_api.workorder_activity.workorder_activity_service import WorkOrderActivityService
def _trigger_escalation_level(workorder,escalation,level):
    print("inside trigger escalation level::::::::::::::::::::::::::")
    recipients = WorkorderEscalationRecipients.objects.filter(
        escalation_level=level
    ).select_related('user','role')
    if not recipients.exists():
        return False
    users_to_notify = set()
    for recipient in recipients:
        if recipient._type == WorkorderEscalationRecipients.TYPE_USER:
            users_to_notify.add(recipient.user)
        else:
            role_users = AppUsers.objects.filter(
                roles=recipient.role,
                is_delete=False,
                tenant=workorder.tenant
            )
            users_to_notify.update(role_users)
    if not users_to_notify:
        return False
    # for user in users_to_notify:
    #     send_email(subject,body,user.email)
    notification_sent = False
    for user in users_to_notify:
        if user.email:
            pass
    if notification_sent:
        WorkorderActivityServices.create_workorder_activity({
            'activity': 'ESCALATED',
            'workorder': workorder,
            'initiated_by': workorder.created_user,
            'to_value': level,
            'message': f"Escalation level {level} triggered for workorder {workorder.id}"
        })
        return True
    return False