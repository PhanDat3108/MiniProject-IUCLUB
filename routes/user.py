from flask import Blueprint, render_template, session, flash, redirect, url_for
from utils.user_utils import get_user_by_username, get_all_users
from utils.decorators import admin_required
from storage import users_collection

user_bp = Blueprint('user', __name__)

@user_bp.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Vui lòng đăng nhập trước","warning")
        return redirect(url_for("auth.login"))
        
    user = get_user_by_username(session["username"])
    return render_template("dashboard.html", user=user)

@user_bp.route("/admin")
@admin_required  
def manage_users():
    users_list = get_all_users()
    return render_template("admin.html", users=users_list)

@user_bp.route('/delete_user/<string:username_to_delete>', methods=["POST"]) 
@admin_required
def delete_user(username_to_delete):
    if username_to_delete == session.get("username"):
        flash('Bạn không thể tự xoá chính mình.', 'danger')
        return redirect(url_for('user.manage_users'))

    try:
        users_collection.delete_one({"username": username_to_delete})
        flash(f'Đã xoá thành công người dùng {username_to_delete}.', 'success')
    except Exception as e:
        flash(f'Có lỗi xảy ra khi xoá: {e}', 'danger')
    
    return redirect(url_for('user.manage_users'))