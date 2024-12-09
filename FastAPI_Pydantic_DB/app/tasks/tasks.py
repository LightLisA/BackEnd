from time import sleep

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_tasks import celery
from PIL import Image
from pathlib import Path
from app.tasks.email_templates import create_booking_confirmation_template
import smtplib


@celery.task()
def process_picture(
        path: str,
):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_200_100 = image.resize((200, 100))
    image_resized_1000_500.save(f"app/frontend/static/images/resized_1000_500_{image_path.name}")
    image_resized_200_100.save(f"app/frontend/static/images/resized_200_100_{image_path.name}")


@celery.task()
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    sleep(10)
    email_to_mock = settings.SMTP_USER
    # msg_content = create_booking_confirmation_template(booking, email_to)
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    # with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
    #     server.login(settings.SMTP_USER, settings.SMTP_PASS)
    #     server.send_message(msg_content)

    # Використання TLS замість SSL
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()  # Увімкнення TLS
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
            print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
