# Định nghĩa model logic
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

    # làm 1 def checkpassword tận dụng check_password_hash anh đã import trên kia 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Post:
    def __init__(self, username, full_name, caption, image_url=None, created_at=None, _id=None, likes=0, comments=None):
        self._id = _id  
        self.username = username
        self.full_name = full_name
        self.caption = caption
        self.image_url = image_url
        self.created_at = created_at if created_at else datetime.now()

        # Thêm nút like,comment
        self.likes = likes
        self.comments = comments if comments is not None else []

    def to_dict(self):
        data = {
            "username": self.username,
            "full_name": self.full_name,
            "caption": self.caption,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "likes": self.likes,
            "comments": self.comments
            }

        return data


   