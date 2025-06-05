import smtplib
import random
import time
from email.message import EmailMessage

# Lưu mã OTP tạm thời
otp_storage = {}


# Hàm gửi email
def send_otp_email(receiver_email, otp_code):
    msg = EmailMessage()
    msg.set_content(f"Mã xác thực của bạn là: {otp_code}")
    msg["Subject"] = "Mã xác thực - Quên mật khẩu"
    msg["From"] = "phanthuong2468@gmail.com"
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                "phanthuong2468@gmail.com", "huygyjonpmqvvgvs"
            )  # 👉 App password
            server.send_message(msg)
        print("✅ Đã gửi email chứa mã xác thực.")
    except Exception as e:
        print("❌ Lỗi khi gửi email:", str(e))


# Sinh OTP và gửi email
def generate_and_send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {"otp": otp, "timestamp": time.time()}
    send_otp_email(email, otp)


# Xác minh mã OTP
def verify_otp(email, user_input):
    record = otp_storage.get(email)
    if not record:
        return False
    if time.time() - record["timestamp"] > 300:
        print("⚠️ OTP đã hết hạn.")
        return False
    return record["otp"] == user_input


# ======= TEST THỬ =======
if __name__ == "__main__":
    user_email = input("📨 Nhập email để gửi mã xác thực: ").strip()
    generate_and_send_otp(user_email)

    user_input = input("🔐 Nhập mã OTP bạn nhận được: ").strip()
    if verify_otp(user_email, user_input):
        print("✅ Mã OTP hợp lệ. Bạn có thể đặt lại mật khẩu.")
    else:
        print("❌ Mã OTP không đúng hoặc đã hết hạn.")
