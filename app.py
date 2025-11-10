from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
from utils.user_utils import add_user, verify_user_credentials,get_user_by_username
from storage import users_collection
app = Flask(__name__)
app.secret_key = os.urandom(24)

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
#làm 1 cái route login, lấy thông tin từ ô nhập login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if verify_user_credentials(username,password):
            user = get_user_by_username(username)
            if user:
                users_collection.update_one(
                    {"username": username},
                    {"$set": {"last_login": datetime.utcnow()}}
                )
                session["username"] = user.username
                flash("Đăng nhập thành công!","success")
                return redirect(url_for("dashboard"))
            else:
                flash("Không tìm thấy người dùng!", "danger")
        else:
            flash ("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template("login.html")

#làm 1 cái route tới trang dashboard.html sau khi đã đăng nhâp

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Vui lòng đăng nhập trước","warning")
        return redirect(url_for("login"))
    user = get_user_by_username(session["username"])
    return render_template("dashboard.html", user=user)
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
