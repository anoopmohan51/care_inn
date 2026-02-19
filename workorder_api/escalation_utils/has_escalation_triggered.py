from workorder_api.models.workorder_escalations_log import WorkOrderEscalationsLog

def _has_escalation_been_triggered(workorder,escalation_level):
    level = escalation_level.level if escalation_level.level else None
    existing_escalation = WorkOrderEscalationsLog.objects.filter(
        workorder=workorder,
        escalation_level=escalation_level,
        level=level
    ).exists()
    return existing_escalation