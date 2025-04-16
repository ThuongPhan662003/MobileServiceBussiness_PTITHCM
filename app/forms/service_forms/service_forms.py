from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ServiceForm(FlaskForm):
    name = StringField("Tên dịch vụ", validators=[DataRequired()])
    parent_id = SelectField("Thuộc dịch vụ", coerce=int)
    submit = SubmitField("Lưu")
