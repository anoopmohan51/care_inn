from celery import shared_task
from workorder_api.models.workorder_escalations import WorkOrderEscalations,WorkorderEscalationServices,WorkorderEscaltionLevels
from workorder_api.models.workorder import WorkOrder
from core_api.send_email.send_email import send_email
from django.utils import timezone
from dotenv import load_dotenv
from workorder_api.escalation_utils.has_escalation_triggered import _has_escalation_been_triggered
from workorder_api.escalation_utils.trigger_escalation_level import _trigger_escalation_level
import os
load_dotenv()

@shared_task
def workorder_escalations_task(tenant_id=1):
    try:
        print("inside escalation task::::::::::::::::::::::::::")
        workorders = WorkOrder.objects.filter(
            tenant_id=tenant_id,
            is_delete=False
        ).exclude(
            status=WorkOrder.WORKORDER_STATUS_CLOSED
        )
        if not workorders.exists():
            return True

        current_time = timezone.now()
        processed_count = 0
        escalated_count = 0
        
        # print("workorder_records::::::::::::::::::::::::::",workorders)
        for workorder in workorders:
            # print("workorder::::::::::::::::::::::::::",workorder)
            status = workorder.status
            workorder_escalations_services = WorkorderEscalationServices.objects.filter(service=workorder.service)
            # print("workorder_escalations::::::::::::::::::::::::::>>>:",workorder_escalations_services)
            if not workorder_escalations_services.exists():
                # print("no workorder_escalations::::::::::::::::::::::::::>>>:")
                continue
            
            for workorder_escalation in workorder_escalations_services:
                # print("workorder_escalation::::::::::::::::::::::::::>>>:",workorder_escalation)
                escalation = workorder_escalation.workorder_escalation
                # print("escalation::::::::::::::::::::::::::>>>:",escalation)
                # if escalation.is_active:
                #     continue
                
                escalation_levels = WorkorderEscaltionLevels.objects.filter(escalation=escalation).order_by('level')
                # print("escalation_levels::::::::::::::::::::::::::>>>:",escalation_levels)
                if not escalation_levels.exists():
                    continue
                
                for escalation_level in escalation_levels:
                    # print("escalation_level::::::::::::::::::::::::::>>>:",escalation_level)
                    # print("escalation_level.trigger_time::::::::::::::::::::::::::>>>:",escalation_level.trigger_time)
                    # print("current_time::::::::::::::::::::::::::>>>:",current_time)

                    start_time = workorder.start_date
                    # print("start_time::::::::::::::::::::::::::>>>:",start_time)
                    if not start_time:
                        continue
                    elapsed_minutes = (current_time - start_time).total_seconds()/60
                    # print("elapsed_minutes::::::::::::::::::::::::::>>>:",elapsed_minutes)
                    if elapsed_minutes >= escalation_level.trigger_time:
                        # print("escalation level triggered::::::::::::::::::::::::::>>>:")
                        if _has_escalation_been_triggered(workorder,escalation_level):
                            continue
                        if _trigger_escalation_level(workorder,workorder_escalation,escalation_level.level):
                            escalated_count += 1
                    processed_count += 1
    
    except Exception as e:
        print(e)
        return False
    return True


