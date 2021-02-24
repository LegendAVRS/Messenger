class User:
    """
    => Class lưu trữ tài khoản và mật khẩu của người dùng
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Users({self.username} {self.password})"
