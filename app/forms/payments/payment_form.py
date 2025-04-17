from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    order_type = StringField("Order Type", validators=[DataRequired()])
    order_id = StringField("Order ID", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired()])
    order_desc = StringField("Description", validators=[DataRequired()])
    bank_code = StringField("Bank Code")  # optional
    language = StringField("Language")  # optional
