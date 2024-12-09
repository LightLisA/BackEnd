from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr
):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Confirm the booking</h1>
            You are booking {booking["room_id"]} room from {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html"
    )
    return email