# Quản Lý Nhà Hàng - Flask Project

## Mô tả

Dự án **Quản Lý Nhà Hàng** được xây dựng bằng Flask, cung cấp các chức năng cơ bản như:

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
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=thuong
DB_NAME=mobileservice_n7
SECRET_KEY=supersecret
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
# MAIL_USE_SSL=False
MAIL_USERNAME=phanthuong2468@gmail.com
# MAIL_PASSWORD=crazyscientist(hawk)
MAIL_PASSWORD=huyg yjon pmqv vgvs
MAIL_DEFAULT_SENDER=phanthuong2468@gmail.com
ADMINS=your_email@gmail.com
VNPAY_URL = https://sandbox.vnpayment.vn/paymentv2/vpcpay.html
VNPAY_TMNCODE = VNPAY_TMN_CODE
VNPAY_SECRET_KEY = sRRRSC223@@#sdSD1225DS4F2SF_@
VNPAY_HASHSECRET = VNPARRSC223@@###sdS__ET
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
