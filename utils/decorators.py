from functools import wraps
from flask import session, flash, redirect, url_for
from utils.user_utils import get_user_by_username

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Bạn cần đăng nhập để xem trang này.", "warning")
            return redirect(url_for("auth.login"))

        user = get_user_by_username(session["username"])

        if not user or user.role != "admin":
            flash("Bạn không có quyền truy cập trang này!", "danger")
            return redirect(url_for("post.home")) 

        return f(*args, **kwargs)
    return decorated_function