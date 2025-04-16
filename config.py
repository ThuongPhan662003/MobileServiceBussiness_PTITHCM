import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", default=587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", default=True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    VNPAY_URL = os.getenv("VNPAY_URL")
    VNPAY_TMN_CODE = os.getenv("VNPAY_TMN_CODE")
    VNPAY_SECRET_KEY = os.getenv("VNPAY_SECRET_KEY")
    VNPAY_HASH_SECRET = os.getenv("VNPAY_HASH_SECRET")
    VNPAY_RETURN_URL = os.getenv("VNPAY_RETURN_URL")
    PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")  # sandbox hoặc live
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
