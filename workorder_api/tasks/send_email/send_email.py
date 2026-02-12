from celery import shared_task
from core_api.send_email.send_email import send_email

@shared_task(bind=True,max_retries=3)
def send_email_task(self,subject,body,to_email):
    try:
        send_email(subject,body,to_email)
    except Exception as e:
        self.retry(countdown=2**self.request.retries,max_retries=3)
    return True