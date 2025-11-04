from models import User
from storage import users_collection

def add_user(username, password, full_name, email, role="user"):
    user = User(username, password, full_name, email, role)
    users_collection.insert_one(user.to_dict())
    return user
#làm 1 hàm lấy user từ monggodp dựa theo tên user

#làm 1 hàm kiểm tra xem liệu user lấy từ mongodp có mật khẩu giống mk nhập ko,tận dụng def checkpassword đã thêm bên models
