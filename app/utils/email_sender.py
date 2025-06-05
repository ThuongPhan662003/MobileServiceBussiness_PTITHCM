# app/utils/email_sender.py

import smtplib
import random
import time
from email.message import EmailMessage
from flask import current_app

otp_storage = {}


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
