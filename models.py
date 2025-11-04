#Định nghĩa model logic
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, full_name, email, role="user", active=True):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.full_name = full_name
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        self.last_login = datetime.now()
        self.active = active

    def to_dict(self):
        return self.__dict__

    #làm 1 def checkpassword tận dụng check_password_hash anh đã import trên kia


   