from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models import Account


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            # DataRequired(message="Email không được để trống"),
            # Length(min=6, max=120, message="Độ dài email từ 6 đến 120 ký tự"),
            # Email(),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Mật khẩu không được để trống")]
    )
    submit = SubmitField("Login")


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    username = StringField(
        "Số điện thoại",
        validators=[
            DataRequired(message="Số điện thoại không được để trống"),
            Regexp(r"^\d{10}$", message="Số điện thoại phải gồm đúng 10 chữ số"),
        ],
    )
    password = PasswordField("Mật khẩu", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Xác nhận mật khẩu",
        validators=[DataRequired(), EqualTo("password", message="Mật khẩu không khớp")],
    )
    submit = SubmitField("Đăng ký")
