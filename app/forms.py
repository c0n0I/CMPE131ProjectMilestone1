from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Log In")

class BookmarkForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Add Bookmark")
