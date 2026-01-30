from celery import shared_task
from workorder_api.models.workorder_escalations import WorkOrderEscalations,WorkorderEscalationServices
from workorder_api.models.workorder import WorkOrder
from core_api.send_email.send_email import send_email
from django.utils import timezone
from dotenv import load_dotenv
import os
load_dotenv()

@shared_task
def workorder_escalations_task(tenant_id=1):
    # try:
        print("inside escalation task::::::::::::::::::::::::::")
        workorder_records = WorkOrder.objects.filter(tenant_id=tenant_id,is_delete=False)
        print("workorder_records::::::::::::::::::::::::::",workorder_records)
        for workorder in workorder_records:
            print("workorder::::::::::::::::::::::::::",workorder)
            status = workorder.status
            service = workorder.service
            workorder_escalations = WorkorderEscalationServices.objects.filter(service=service)
            print("workorder_escalations::::::::::::::::::::::::::",workorder_escalations)
            if status == WorkOrder.WORKORDER_STATUS_ASSIGNED_NOT_STARTED:
                pass
            elif status == WorkOrder.WORKORDER_STATUS_CLOSED:
                pass
        
    # except Exception as e:
    #     print(e)
    #     return False
    # return True


