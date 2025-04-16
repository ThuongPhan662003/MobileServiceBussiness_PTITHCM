# file: your_project/utils/ip.py
from flask import request


def get_client_ip(request):
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    if "X-Real-IP" in request.headers:
        return request.headers["X-Real-IP"]
    return request.remote_addr
