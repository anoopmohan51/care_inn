from firebase_admin import messaging,credentials
from dotenv import load_dotenv
import os
load_dotenv()
import firebase_admin
from core_api.models.fcm_log import FcmPushLog
from core_api.models.user_device_details import UserDeviceDetails

def send_push_notification(token:list[str],title:str,body:str,data:dict={}):
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_FILE'))
            firebase_admin.initialize_app(cred)
        notification = messaging.MulticastMessage(
            tokens=token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data = data
        )
        batch_response = messaging.send_each_for_multicast(notification)
        for tok,response in zip(token,batch_response.responses):
            if response.success:
                print(f"Notification sent to {tok}")
                user_device_details = UserDeviceDetails.objects.get(device_id=tok,is_logged_in=True)
                FcmPushLog.objects.create(
                    user=user_device_details.user if user_device_details else None,
                    push_data=data
                )
            else:
                print(f"Error sending notification to {tok}: {response.exception}")
        return "Notification sent successfully"
    except Exception as e:
        print(f"Error sending notification: {e}")
        return "Error sending notification"