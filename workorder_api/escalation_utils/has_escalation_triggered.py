# from workorder_api.models.workorder_escalations import WorkOrderEscalations

# def _has_escalation_been_triggered(workorder,escalation,level):
#     print("inside has escalation been triggered::::::::::::::::::::::::::")
#     existing_escalation = WorkOrderEscalations.objects.filter(
#         workorder=workorder,
#         escalation=escalation,
#         to_value=str(level)
#     ).exists()
#     return existing_escalation