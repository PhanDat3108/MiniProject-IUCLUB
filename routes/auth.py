from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from utils.user_utils import add_user, verify_user_credentials, get_user_by_username
from storage import users_collection

# Tạo Blueprint tên là 'auth'
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("post.home"))
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        
        if get_user_by_username(username):
             flash("Tên đăng nhập đã tồn tại.", "danger")
             return redirect(url_for("auth.register"))

        add_user(username, password, full_name, email)
        flash("Đăng ký thành công!", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("post.home"))
        
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
                    return redirect(url_for("user.manage_users"))
                else:
                    return redirect(url_for("post.home")) 
            else:
                flash("Không tìm thấy người dùng!", "danger")
        else:
            flash ("Sai tên đăng nhập hoặc mật khẩu!", "danger")
            
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("post.home"))