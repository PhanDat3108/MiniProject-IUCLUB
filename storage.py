#kết nối database
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

MONGO_URI = "mongodb+srv://ibclubblog:iuclubblog123@iuclub.oe133jj.mongodb.net/?appName=Iuclub"
client = MongoClient(MONGO_URI)
db = client.get_database("blogDB")
users_collection = db.users

