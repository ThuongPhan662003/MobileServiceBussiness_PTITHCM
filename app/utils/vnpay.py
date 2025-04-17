# file: your_project/utils/vnpay.py
import hashlib, hmac
from urllib.parse import urlencode


class vnpay:
    def __init__(self):
        self.requestData = {}
        self.responseData = {}

    def get_payment_url(self, base_url, secret_key):
        data = self.requestData.copy()
        sorted_items = sorted(data.items())
        hash_data = urlencode(sorted_items)
        checksum = hmac.new(
            secret_key.encode(), hash_data.encode(), hashlib.sha512
        ).hexdigest()
        data["vnp_SecureHash"] = checksum
        return f"{base_url}?{urlencode(data)}"

    def validate_signature(self, secret_key):
        data = self.responseData.copy()
        secure_hash = data.pop("vnp_SecureHash", None)
        sorted_items = sorted(data.items())
        hash_data = urlencode(sorted_items)
        calculated = hmac.new(
            secret_key.encode(), hash_data.encode(), hashlib.sha512
        ).hexdigest()
        return calculated == secure_hash
