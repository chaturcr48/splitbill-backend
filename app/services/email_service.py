import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
env = os.environ

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = env.get("EMAIL_USER")
EMAIL_PASSWORD = env.get("EMAIL_PASSWORD")


def send_invitation_email(to_email: str, group_name: str):
    msg = EmailMessage()
    msg["Subject"] = f"Invitation to join {group_name} on Splitwise"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(
        f"You have been invited to join the group '{group_name}'.\n"
        f"Please login to Splitwise to accept the invitation."
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
