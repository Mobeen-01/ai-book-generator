from app.services.notification_service import EmailNotificationService
from app.services.notification_events import NOTIFICATION_TEMPLATES


class NotificationDispatcher:

    def __init__(self):
        self.email_service = EmailNotificationService()

    def trigger(self, event_type: str, receiver_email: str, extra_message: str = None):

        if event_type not in NOTIFICATION_TEMPLATES:
            return {"status": "error", "message": "Invalid event type"}

        template = NOTIFICATION_TEMPLATES[event_type]

        subject = template["subject"]
        message = template["message"]

        if extra_message:
            message += f"\n\nDetails: {extra_message}"

        return self.email_service.send_email(
            subject=subject,
            message=message,
            receiver_email=receiver_email
        )