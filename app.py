from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename

from utils.user_utils import (
    add_user, 
    verify_user_credentials, 
    get_user_by_username, 
    get_all_users,
)
from utils.post_utils import add_post, get_all_posts
from storage import users_collection

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Bạn cần đăng nhập để xem trang này.", "warning")
            return redirect(url_for("login"))

        user = get_user_by_username(session["username"])

        if not user or user.role != "admin":
            flash("Bạn không có quyền truy cập trang này!", "danger")
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    if "username" in session:
        user = get_user_by_username(session["username"])
        return dict(current_user=user)
    return dict(current_user=None)



@app.route("/")
def home():
    """Trang chủ, gắn với route '/' """
    posts = get_all_posts()
    return render_template("home.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        
        if get_user_by_username(username):
             flash("Tên đăng nhập đã tồn tại.", "danger")
             return redirect(url_for("register"))

        add_user(username, password, full_name, email)

        flash("Đăng ký thành công!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        if verify_user_credentials(username, password):
            user = get_user_by_username(username) 
            if user:
                users_collection.update_one(
                    {"username": username},
                    {"$set": {"last_login": datetime.utcnow()}}
                )
                session["username"] = user.username
                flash("Đăng nhập thành công!","success")
        
                if user.role == "admin":
                    return redirect(url_for("manage_users"))
                else:
                    return redirect(url_for("home")) 
            else:
                flash("Không tìm thấy người dùng!", "danger")
        else:
            flash ("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Đăng xuất người dùng."""
    session.pop("username", None)
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    """Trang dashboard, gắn với route '/dashboard' """
    if "username" not in session:
        flash("Vui lòng đăng nhập trước","warning")
        return redirect(url_for("login"))
    user = get_user_by_username(session["username"])
    return render_template("dashboard.html", user=user)


@app.route("/admin")
@admin_required  
def manage_users():
    """Trang admin, gắn với route '/admin' """
    users_list = get_all_users()
    return render_template("admin.html", users=users_list)




@app.route("/add_post", methods=["POST"])
def add_post_route():
    """Xử lý việc đăng bài mới."""
    if "username" not in session:
        flash("Bạn cần đăng nhập để đăng bài.", "warning")
        return redirect(url_for("login"))

    user = get_user_by_username(session["username"])
    caption = request.form.get("caption", "")
    image_file = request.files.get("image")
    image_url = None

    if image_file and image_file.filename != '' and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)
        image_url = url_for('static', filename=f'uploads/{filename}')
    
    if not caption and not image_url:
        flash("Bạn phải nhập nội dung hoặc tải lên ảnh.", "warning")
        return redirect(url_for("home"))

    add_post(user.username, user.full_name, caption, image_url)
    flash("Đăng bài thành công!", "success")
    
    return redirect(url_for("home"))
@app.route('/delete_user/<string:username_to_delete>', methods=["POST"])
@admin_required
def delete_user(username_to_delete):
    """Xoá user, gắn với route '/delete_user/<string:username_to_delete>' """
    if username_to_delete == session.get("username"):
        flash('Bạn không thể tự xoá chính mình.', 'danger')
        return redirect(url_for('manage_users'))

    try:
        users_collection.delete_one({"username": username_to_delete})
        flash(f'Đã xoá thành công người dùng {username_to_delete}.', 'success')
    except Exception as e:
        flash(f'Có lỗi xảy ra khi xoá: {e}', 'danger')
    
    return redirect(url_for('manage_users'))


if __name__ == "__main__":
    app.run(debug=True)