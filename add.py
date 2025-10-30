from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ibclubblog:iuclubblog@iuclub.oe133jj.mongodb.net/?appName=Iuclub"
client = MongoClient(MONGO_URI)
db = client.get_database("blogDB")
users_collection = db.users

# Lấy tất cả user
for user in users_collection.find():
    print(user)
