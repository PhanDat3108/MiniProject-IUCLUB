from flask import Flask, render_template, request, redirect, url_for, flash
from storage import add_user  # import hàm từ storage.py

app = Flask(__name__)
app.secret_key = "YOUR_FLASK_SECRET"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        role = request.form["role"]
        add_user(username, password, full_name, email, role)

        flash("Đăng ký thành công!", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
