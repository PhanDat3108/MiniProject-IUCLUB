import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from utils.post_utils import add_post, get_all_posts
from utils.user_utils import get_user_by_username
from utils.post_utils import get_all_posts
from utils.decorators import admin_required

from utils.post_utils import add_post, get_all_posts

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