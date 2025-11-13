from storage import posts_collection
from datetime import datetime

def add_post(username, full_name, caption, image_url=None):
    """Thêm một bài đăng mới vào database."""
    post_data = {
        "username": username,
        "full_name": full_name,
        "caption": caption,
        "image_url": image_url,
        "created_at": datetime.now()
    }
    posts_collection.insert_one(post_data)
    return post_data

def get_all_posts():
    """Lấy tất cả bài đăng, sắp xếp mới nhất lên trước."""
    posts = posts_collection.find().sort("created_at", -1)
    return list(posts)