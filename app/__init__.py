from datetime import timedelta
from flask import Flask, json, session
from flask_login import LoginManager
from app.controllers import *
from app.controllers.subscriber_controller import subscriber_bp
from app.exceptions import exceptions
from app.auth import auth
from app.models.account import Account
from app.services.account_service import AccountService
from config import Config
from app.database import db_instance
import paypalrestsdk
from app.utils import vnpay, ip


from app.controllers.customer_plan_controller import (
    customer_plan_bp,
)  # Import Blueprint


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)
    # Initialize database connection
    db_instance.get_connection()
    # Register blueprints here
    app.register_blueprint(voucher_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(function_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(role_group_bp)
    app.register_blueprint(role_group_detail_bp)
    app.register_blueprint(usagelog_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(payment_detail_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(plan_network_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(subscriber_bp)
    app.register_blueprint(plan_detail_bp)
    app.register_blueprint(permission_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_main_bp)
    app.register_blueprint(payment_api_bp)
    app.register_blueprint(customer_plan_bp)
    app.register_blueprint(report_bp)
    # Register error handlers
    app.register_blueprint(exceptions)
    app.register_blueprint(auth)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

    # Cấu hình Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    paypalrestsdk.configure(
        {
            "mode": app.config["PAYPAL_MODE"],
            "client_id": app.config["PAYPAL_CLIENT_ID"],
            "client_secret": app.config["PAYPAL_CLIENT_SECRET"],
        }
    )

    @login_manager.user_loader
    def load_user(id):
        return AccountService.get_account_by_id(id)

    return app
