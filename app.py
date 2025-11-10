from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
from functools import wraps

from utils.user_utils import (
    add_user, 
    verify_user_credentials, 
    get_user_by_username, 
    get_all_users
)
from storage import users_collection

app = Flask(__name__)
app.secret_key = os.urandom(24)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Bạn cần đăng nhập để xem trang này.", "warning")
            return redirect(url_for("login"))

        user = get_user_by_username(session["username"])

        if not user or user.role != "admin":
            flash("Bạn không có quyền truy cập trang này!", "danger")
            return redirect(url_for("dashboard")) 

        return f(*args, **kwargs)
    return decorated_function



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]

        add_user(username, password, full_name, email)

        flash("Đăng ký thành công!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
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
                    return redirect(url_for("dashboard")) 
            else:
                flash("Không tìm thấy người dùng!", "danger")
        else:
            flash ("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template("login.html")

@app.route("/")
def home():
    """Trang chủ, gắn với route '/' """
    return render_template("home.html")


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


if __name__ == "__main__":
    app.run(debug=True)