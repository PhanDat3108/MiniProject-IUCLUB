from models import User
from storage import users_collection

def add_user(username, password, full_name, email, role="user"):
    user = User(username, password, full_name, email, role)
    users_collection.insert_one(user.to_dict())
    return user
#làm 1 hàm lấy user từ monggodp dựa theo tên user
def get_user_by_username(username):
    data = users_collection.find_one({"username": username})
    if data:
        user = User(
            username=data["username"],
            password=data["password_hash"], 
            full_name=data["full_name"],
            email=data["email"],
            role=data.get("role", "user"),
            active=data.get("active", True)
        )
        user.password_hash = data["password_hash"]
        user.created_at = data.get("created_at")
        user.last_login = data.get("last_login")
        return user
    return None

#làm 1 hàm kiểm tra xem liệu user lấy từ mongodp có mật khẩu giống mk nhập ko,tận dụng def checkpassword đã thêm bên models
def verify_user_credentials(username, password):
    user = get_user_by_username(username)
    if not user:
        return False 
    
    return user.check_password(password)
#lấy tt user
def get_all_users():
    users_data = users_collection.find()
    
    user_list = []
    for data in users_data:
        user = User(
            username=data["username"],
            password=data["password_hash"], 
            full_name=data["full_name"],
            email=data["email"],
            role=data.get("role", "user"),
            active=data.get("active", True)
        )
        user.password_hash = data["password_hash"]
        user.created_at = data.get("created_at")
        user.last_login = data.get("last_login")
        user_list.append(user)
        
    return user_list