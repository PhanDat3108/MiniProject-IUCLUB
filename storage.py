# storage.py
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

MONGO_URI = "mongodb+srv://ibclubblog:iuclubblog123@iuclub.oe133jj.mongodb.net/?appName=Iuclub"
client = MongoClient(MONGO_URI)
db = client.get_database("blogDB")
users_collection = db.users

def add_user(username, password, full_name, email, role="user"):
    password_hash = generate_password_hash(password)
    user_data = {
        "username": username,
        "password_hash": password_hash,
        "full_name": full_name,
        "email": email,
        "role": role,
        "created_at": datetime.now(),
        "last_login": datetime.now(),
        "active": True
    }
    users_collection.insert_one(user_data)
    return user_data


for user in users_collection.find():
    print(user)