import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_password_reset_email(recipient_email: str, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Your Password"
    message["From"] = settings.email_username
    message["To"] = recipient_email
    message.attach(MIMEText(f"Click here to reset your password: {reset_link}", "plain"))

    with smtplib.SMTP(settings.email_host, settings.email_port) as server:
        server.starttls()
        server.login(settings.email_username, settings.email_password)
        server.sendmail(settings.email_username, recipient_email, message.as_string())


def send_confirmation_email(recipient_email: str, token: str):
    confirmation_link = f"http://localhost:8000/auth/confirm-email?token={token}"

    html_content = f"""
    <html>
        <body>
            <h2>Welcome! Please confirm your email</h2>
            <p>Thank you for registering. Please click the link below to activate your account:</p>
            <a href="{confirmation_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; display: inline-block;">
                Confirm Email Address
            </a>
            <p>This link will expire in 2 hours.</p>
        </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirm Your Email Address"
    message["From"] = settings.email_username
    message["To"] = recipient_email
    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.email_host, settings.email_port) as server:
        server.starttls()
        server.login(settings.email_username, settings.email_password)
        server.sendmail(settings.email_username, recipient_email, message.as_string())
