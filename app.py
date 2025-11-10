from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from utils.user_utils import add_user

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
    
    return render_template("login.html")

#làm 1 cái route tới trang dashboard.html sau khi đã đăng nhâp


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
