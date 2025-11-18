import os
from flask import Flask, session
from utils.user_utils import get_user_by_username

from routes.auth import auth_bp
from routes.user import user_bp
from routes.post import post_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

@app.context_processor
def inject_user():
    if "username" in session:
        user = get_user_by_username(session["username"])
        return dict(current_user=user)
    return dict(current_user=None)

if __name__ == "__main__":
    app.run(debug=True)