from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from core_api.models.appusers import AppUsers
from workorder_api.workorder_activity.workorder_activity_service import WorkOrderActivityService
from core_api.send_email.send_email import send_email
from django.template.loader import render_to_string
def _trigger_escalation_level(workorder,escalation_level,level):
    # print("inside trigger escalation level::::::::::::::::::::::::::")
    # print("workorder::::::::::::::::::::::::::>>>:",workorder)
    # print("escalation_level::::::::::::::::::::::::::>>>:",escalation_level.id)
    # print("level::::::::::::::::::::::::::>>>:",level)
    recipients = WorkorderEscalationRecipients.objects.filter(
        escalation_level=escalation_level.id
    ).select_related('user','role')
    # print("recipients::::::::::::::::::::::::::>>>:",recipients)
    if not recipients.exists():
        return False
    users_to_notify = set(["napowev989@desiys.com"])
    # for recipient in recipients:
    #     if recipient._type == WorkorderEscalationRecipients.TYPE_USER:
    #         users_to_notify.add(recipient.user)
    #     else:
    #         role_users = AppUsers.objects.filter(
    #             roles=recipient.role,
    #             is_delete=False,
    #             tenant=workorder.tenant
    #         )
    #         users_to_notify.update(role_users)
    if not users_to_notify:
        return False
    print("users_to_notify::::::::::::::::::::::::::>>>:",users_to_notify)
    # for user in users_to_notify:
    subject = f"Escalation level {level} triggered for workorder {workorder.id}"
    body = render_to_string('escalation.html',{'workorder':workorder,'escalation_level':escalation_level,'level':level})
    send_email(subject,body,"napowev989@desiys.com")
    notification_sent = False
    # for user in users_to_notify:
    #     if user.email:
    #         pass
    if notification_sent:
        # WorkorderActivityServices.create_workorder_activity({
        #     'activity': 'ESCALATED',
        #     'workorder': workorder,
        #     'initiated_by': workorder.created_user,
        #     'to_value': level,
        #     'message': f"Escalation level {level} triggered for workorder {workorder.id}"
        # })
        return True
    print("notification not sent::::::::::::::::::::::::::")
    return False