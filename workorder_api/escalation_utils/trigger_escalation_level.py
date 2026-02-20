from workorder_api.models.workorder_escalations import WorkorderEscalationRecipients
from core_api.models.appusers import AppUsers
from workorder_api.workorder_activity.workorder_activity_service import WorkOrderActivityService
from core_api.send_email.send_email import send_email
from django.template.loader import render_to_string
from workorder_api.tasks.send_email import send_email_task
from workorder_api.models.workorder_escalations_log import WorkOrderEscalationsLog
from workorder_api.escalation_push.push_notification import send_escalation_push_notification

def _trigger_escalation_level(workorder,escalation_service,escalation_level):
    users_to_notify = resolve_recipients_users(escalation_service,workorder)
    if not users_to_notify:
        return False
    assignee_name = workorder.get_assignee_name()
    level = escalation_level.level
    priority = workorder.priority
    due_date = workorder.end_date
    subject = f"Escalation level {level} triggered for workorder {workorder.unique_id}"
    context = {
        'recipient_name':assignee_name,
        'workorder_unique_id':workorder.unique_id,
        'priority':priority,
        'assigned_to':assignee_name,
        'due_date':due_date,
        'level':level
    }
    notification_sent = False
    for user_record in users_to_notify:
        context.update({
            'recipient_name':user_record.get('name'),
        })
        body = render_to_string('escalation.html',context)
        # send_email(subject,body,user_record.get('email'))
        send_email_task(subject,body,user_record.get('email'))
        notification_sent = True
    send_escalation_push_notification(users_to_notify,workorder.id,escalation_level.id,level)
    if notification_sent:
        WorkOrderActivityService.create_workorder_activity({
            'activity': 'ESCALATED',
            'workorder': workorder,
            'initiated_by': None,
            'to_value': level,
            'message': f"Escalated to {level} level"
        })
        WorkOrderEscalationsLog.objects.create(
            workorder=workorder,
            escalation_level=escalation_level,
            level=level
        )
        return True
    return False


def resolve_recipients_users(escalation_level, workorder):
    recipients = list(
        WorkorderEscalationRecipients.objects.filter(
            escalation_level=escalation_level.id
        ).select_related('user', 'role')
    )
    if not recipients:
        return []

    users_to_notify = []
    seen_emails = set()

    role_ids = [
        r.role_id for r in recipients
        if r._type == WorkorderEscalationRecipients.TYPE_ROLE and r.role_id
    ]
    if role_ids:
        role_users = AppUsers.objects.filter(
            roles__id__in=role_ids,
            is_delete=False,
            tenant=workorder.tenant
        ).exclude(email__isnull=True).exclude(email='')
        for user in role_users:
            if user.email and user.email not in seen_emails:
                seen_emails.add(user.email)
                users_to_notify.append({
                    'name': user.get_full_name(),
                    'email': user.email
                })

    for recipient in recipients:
        if recipient._type == WorkorderEscalationRecipients.TYPE_USER:
            if not recipient.user or not recipient.user.email:
                continue
            key = recipient.user.email
            if key in seen_emails:
                continue
            seen_emails.add(key)
            users_to_notify.append({
                'name': recipient.user.get_full_name(),
                'email': key
            })

    return users_to_notify