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


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Email không được để trống"),
            Length(min=2, max=20),
        ],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Length(min=6, max=120), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")
