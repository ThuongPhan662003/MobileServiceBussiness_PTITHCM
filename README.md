# Quản Lý Nhà Hàng - Flask Project

## Mô tả

Dự án **Quản Lý Nhà Hàng** được xây dựng bằng Flask, cung cấp các chức năng cơ bản như:

- Đăng nhập, đăng ký, và đăng xuất người dùng.
- Hiển thị trang chủ.
- Xử lý các lỗi thông qua middleware và exception handler.
- Tích hợp template HTML để hiển thị giao diện.

---

## Cấu trúc thư mục

---

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

## Đảm bảo bạn đang ở trong môi trường ảo.

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
