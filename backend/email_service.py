import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_reset_email(email: str, reset_token: str):
    """Send password reset email"""
    
    smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_PORT", "587"))
    sender_email = os.getenv("EMAIL_HOST_USER")
    sender_password = os.getenv("EMAIL_HOST_PASSWORD")
    
    if not sender_email or not sender_password:
        raise Exception("Email configuration not found")
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Reset Password - Print Label App"
    
    # Email body
    body = f"""
    Halo,
    
    Anda telah meminta reset password untuk aplikasi Print Label.
    
    Gunakan token berikut untuk reset password:
    {reset_token}
    
    Token ini akan expire dalam 30 menit.
    
    Jika Anda tidak meminta reset password, abaikan email ini.
    
    Terima kasih,
    Tim Print Label App
    """
    
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, email, text)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False