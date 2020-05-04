from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

SECRET_KEY = current_app.config['SENDGRID_SECRET_KEY']


class Mailer:
    @staticmethod
    def send_mail(
            from_email: str,
            to_emails: list or str,
            subject: str,
            html_content: str
    ) -> dict:
        # Build message
        message = Mail(from_email=from_email, to_emails=to_emails, subject=subject, html_content=html_content)
        # Setup client
        sendgrid_client = SendGridAPIClient(SECRET_KEY)
        # Send message
        resp = sendgrid_client.send(message)
        # Return response
        return {
            'code': resp.status_code,
            'body': resp.body,
            'headers': resp.headers
        }
