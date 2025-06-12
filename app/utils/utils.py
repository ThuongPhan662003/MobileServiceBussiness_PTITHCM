from datetime import datetime

from flask import app


@app.template_filter("datetimeformat")
def datetimeformat(value, format="%H:%M %d-%m-%Y"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(format)
