class CustomException(Exception):
    """
    Exception tùy chỉnh cho ứng dụng Flask.
    """
    def __init__(self, message, status_code=400):
        """
        Khởi tạo CustomException.

        Args:
            message (str): Thông báo lỗi.
            status_code (int): Mã trạng thái HTTP (mặc định là 400 - Bad Request).
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        Chuyển exception thành dictionary để trả về JSON.

        Returns:
            dict: Dictionary chứa thông tin lỗi.
        """
        return {"error": self.message, "status_code": self.status_code}