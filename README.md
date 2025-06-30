# Kinh doanh dịch vụ di động

## Mô tả

Dự án **Kinh doanh dịch vụ di động** được xây dựng bằng Flask, cung cấp các chức năng cơ bản như:

- Đăng nhập, đăng ký, và đăng xuất người dùng.
- Hiển thị trang chủ.
- Xử lý các lỗi thông qua middleware và exception handler.
- Tích hợp template HTML để hiển thị giao diện.

---

## Cấu trúc thư mục

```
MobileService/
│
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── home_controller.py
│   │   └── ... (các controller khác)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── payment_service.py
│   │   └── ... (các service khác)
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── contract_repository.py
│   │   └── ... (các repository khác)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── contract.py
│   │   ├── country.py
│   │   ├── customer.py
│   │   ├── function.py
│   │   ├── network.py
│   │   ├── payment.py
│   │   ├── paymentdetail.py
│   │   ├── permissiondetail.py
│   │   ├── plan.py
│   │   ├── plannetwork.py
│   │   ├── rolegroup.py
│   │   ├── rolegroupdetail.py
│   │   ├── service.py
│   │   ├── staff.py
│   │   ├── subscription.py
│   │   ├── usage_log.py
│   │   ├── voucher.py
│   │   └── subscriber.py
│   ├── templates/
│   │   └── ... (các file .html)
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── ... (các file, thư mục khác nếu có)
│
├── venv/                  # Môi trường ảo (không cần commit lên git)
├── run.py                 # File chạy chính của ứng dụng
├── requirements.txt       # Danh sách thư viện cần cài đặt
├── README.md
└── .env                   # Thông tin cấu hình môi trường
```

## Cài đặt

### 1. Yêu cầu hệ thống

- Python 3.8 trở lên
- `pip` (Python package manager)

### 2. Cài đặt môi trường ảo

```bash
python -m venv venv
source venv/bin/activate        # Trên Linux/MacOS
venv\Scripts\activate           # Trên Windows

pip install -r [requirements.txt](http://_vscodecontentref_/2)
```

### Chạy ứng dụng

## Thêm file .env

```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
SECRET_KEY=supersecret
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
# MAIL_USE_SSL=False
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=
ADMINS=your_email@gmail.com
VNPAY_URL = 
VNPAY_TMNCODE = 
VNPAY_SECRET_KEY = 
VNPAY_HASHSECRET = 
```

## Chạy ứng dụng Flask:

```bash
python run.py
```

## Mở trình duyệt và truy cập:

```bash
http://localhost:5000/
```

### Các chức năng chính

1. Trang chủ
   URL: /
   Hiển thị giao diện trang chủ.
2. Đăng nhập
   URL: /auth/login
   Người dùng nhập tên đăng nhập và mật khẩu để đăng nhập.
3. Đăng ký
   URL: /auth/register
   Người dùng nhập thông tin để đăng ký tài khoản.
4. Đăng xuất
   URL: /auth/logout
   Đăng xuất người dùng và chuyển hướng về trang đăng nhập.
   Xử lý lỗi
   Ứng dụng sử dụng middleware và exception handler để xử lý các lỗi:

404 - Not Found: Hiển thị trang lỗi khi không tìm thấy tài nguyên.
500 - Internal Server Error: Hiển thị trang lỗi khi có lỗi nội bộ.
CustomException: Xử lý các lỗi tùy chỉnh.

### Thư viện sử dụng

Flask: Framework chính.
Jinja2: Template engine để render giao diện.
