from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import main_bp
from app.forms import BookmarkForm
from app.models import Bookmark, db

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

@main_bp.route("/bookmarks/add", methods=["GET", "POST"])
@login_required
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        new_bm = Bookmark(
            title=form.title.data,
            url=form.url.data,
            user_id=current_user.id
        )
        db.session.add(new_bm)
        db.session.commit()
        flash("Bookmark added!", "success")
        return redirect(url_for("main.bookmarks"))

    return render_template("main/add_bookmark.html", form=form)
