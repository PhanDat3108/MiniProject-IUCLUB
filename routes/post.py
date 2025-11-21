import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from utils.post_utils import add_post, get_all_posts
from utils.user_utils import get_user_by_username
from utils.post_utils import get_all_posts
from utils.decorators import admin_required

from utils.post_utils import add_post, get_all_posts

from bson.objectid import ObjectId
from storage import posts_collection
from datetime import datetime


post_bp = Blueprint('post', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route("/")
def home():
    posts = get_all_posts()
    return render_template("home.html", posts=posts)

@post_bp.route("/add_post", methods=["POST"])
def add_post_route():
    if "username" not in session:
        flash("Bạn cần đăng nhập để đăng bài.", "warning")
        return redirect(url_for("auth.login"))

    user = get_user_by_username(session["username"])
    caption = request.form.get("caption", "")
    image_file = request.files.get("image")
    image_url = None

    if image_file and image_file.filename != '' and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        # Sử dụng current_app.config để lấy đường dẫn upload
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)
        image_url = url_for('static', filename=f'uploads/{filename}')
    
    if not caption and not image_url:
        flash("Bạn phải nhập nội dung hoặc tải lên ảnh.", "warning")
        return redirect(url_for("post.home"))

    add_post(user.username, user.full_name, caption, image_url)
    flash("Đăng bài thành công!", "success")
    
    return redirect(url_for("post.home"))

@post_bp.route("/admin/posts")
@admin_required
def manage_posts():
    
    posts_list = get_all_posts()
    return render_template("admin_posts.html", posts=posts_list)
    
# Thêm nút tim
@post_bp.route("/like/<post_id>", methods=["POST"])
def like_post(post_id):
    if "username" not in session:
        flash("Bạn cần đăng nhập để like.", "warning")
        return redirect(url_for("auth.login"))

    posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$inc": {"likes": 1}}
    )

    return redirect(url_for("post.home"))

# Thêm tính năng comment
@post_bp.route("/comment/<post_id>", methods=["POST"])
def comment_post(post_id):
    if "username" not in session:
        flash("Bạn cần đăng nhập để bình luận.", "warning")
        return redirect(url_for("auth.login"))

    content = request.form.get("content")
    if not content:
        flash("Bình luận không được để trống.", "warning")
        return redirect(url_for("post.home"))

    username = session.get("username")
    full_name = session.get("full_name")

    new_comment = {
        "username": username,
        "full_name": full_name,
        "content": content,
        "created_at": datetime.now()
    }

    posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": new_comment}}
    )

    return redirect(url_for("post.home"))
