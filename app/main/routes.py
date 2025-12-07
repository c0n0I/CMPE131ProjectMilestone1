from flask import render_template
from . import main_bp
from flask_login import login_required, current_user
from app.models import Bookmark

@main_bp.route("/")
def index():
    return render_template("main/index.html")

@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html")

@main_bp.route("/bookmarks")
@login_required
def bookmarks():
    user_bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return render_template("main/bookmarks.html", bookmarks=user_bookmarks)
