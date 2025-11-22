from storage import posts_collection
from models import Post  
from datetime import datetime
from bson.objectid import ObjectId 

def add_post(username, full_name, caption, image_url=None):

    new_post = Post(username, full_name, caption, image_url)
    
    result = posts_collection.insert_one(new_post.to_dict())
    return result

def get_all_posts():
    """Lấy tất cả bài đăng, chuyển đổi thành list các object Post."""
    posts_cursor = posts_collection.find().sort("created_at", -1)
    
    posts_list = []
    for data in posts_cursor:

        post = Post(
            username=data["username"],
            full_name=data["full_name"],
            caption=data["caption"],
            image_url=data.get("image_url"),
            created_at=data["created_at"],
            _id=str(data["_id"]),
            likes=data.get("likes",0),
            comments=data.get("comments",[]) 
        )
        posts_list.append(post)
        
    return posts_list

