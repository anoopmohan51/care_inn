from celery import shared_task
from core_api.fcm_push_notification.send_push import send_push_notification

def send_escalation_push_notification_task(users_device_tokens:list[str],title:str,body:str,data:dict={}):
    try:
        send_push_notification(users_device_tokens,title,body,data)
    except Exception as e:
        print("error in send escalation push notification task",e)