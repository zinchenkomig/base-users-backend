from conf import settings
from src.service.email_template import registration_template
from utils import comms


def send_registration_email(to):
    sender = comms.Gmail(token=settings.GMAIL_API_TOKEN, from_="zinchenkomig.sup@gmail.com")
    verification_link = f'{settings.FRONTEND_URL}/verify/'
    message = registration_template.replace('{{verification_link}}', verification_link)
    sender.send_with_retries(to=to,
                             subject="Account Created",
                             message_text=message)

