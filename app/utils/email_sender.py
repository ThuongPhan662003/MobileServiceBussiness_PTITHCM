# app/utils/email_sender.py

import smtplib
import random
import string
import time
from email.message import EmailMessage
from flask import current_app, url_for
import smtplib
from email.mime.text import MIMEText

otp_storage = {}


def generate_random_password(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import current_app


def send_reset_email(to, name, new_password):
    subject = "Đặt lại mật khẩu nhân viên"
    sender_email = current_app.config["MAIL_USERNAME"]
    sender_password = current_app.config["MAIL_PASSWORD"]
    with current_app.app_context():
        login_url = url_for("auth.login", _external=True)

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <p>Xin chào <strong>{name}</strong>,</p>
        <p>Mật khẩu mới của bạn là: <strong>{new_password}</strong></p>
        <p>Vui lòng đăng nhập và đổi mật khẩu sau lần đăng nhập đầu tiên.</p>
        <p>
            <a href="{login_url}" style="
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            ">🔐 Đăng nhập ngay</a>
        </p>
        <p>Trân trọng,<br>Hệ thống quản lý nhân viên</p>
    </body>
    </html>
    """

    # Tạo email dạng multipart/alternative
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to

    # Gắn nội dung HTML vào email
    mime_html = MIMEText(html_body, "html")
    msg.attach(mime_html)

    # Gửi email qua SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


def send_otp_email(receiver_email, otp_code):
    sender_email = current_app.config["MAIL_USERNAME"]
    sender_password = current_app.config["MAIL_PASSWORD"]
    print("sender_email", sender_email)
    print("receiver_email", sender_password)
    msg = EmailMessage()
    msg.set_content(f"Mã xác thực của bạn là: {otp_code}")
    msg["Subject"] = "Mã xác thực - Quên mật khẩu"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


def generate_and_send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {"otp": otp, "timestamp": time.time()}
    send_otp_email(email, otp)


def verify_otp(email, user_input):
    record = otp_storage.get(email)
    if not record:
        return False
    if time.time() - record["timestamp"] > 300:
        return False
    return record["otp"] == user_input
