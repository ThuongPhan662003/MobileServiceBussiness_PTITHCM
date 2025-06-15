from datetime import datetime
import random
import string
from flask import app
import unicodedata

def generate_random_password(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def normalize_name(name):
    if not name:
        return ""
    # Loại bỏ dấu
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    # Loại bỏ khoảng trắng và chuyển về in thường
    return name.replace(" ", "").lower()
