from firebase_admin import messaging,credentials
from dotenv import load_dotenv
import os
load_dotenv()

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
        response = messaging.send_each_for_multicast(notification)
        for response in responses:
            if response.success:
                print(f"Notification sent to {response.token}")
            else:
                print(f"Error sending notification to {response.token}: {response.exception}")
        return "Notification sent successfully"
    except Exception as e:
        print(f"Error sending notification: {e}")
        return "Error sending notification"