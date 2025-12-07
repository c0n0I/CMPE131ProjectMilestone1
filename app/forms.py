from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Log In")

class BookmarkForm(FlaskForm):
    title = StringField(
        "Title", 
        validators=[
            DataRequired(message="A title is required."),
            Length(min=2, max=255, message="Title must be between 2 and 255 characters.")
        ]
    )

    url = StringField(
        "URL", 
        validators=[
            DataRequired(message="A URL is required."),
            URL(message="Please enter a valid URL, including https://")
        ]
    )

    submit = SubmitField("Save")


class FolderForm(FlaskForm):
    name = StringField(
        "Folder Name",
        validators=[
            DataRequired(message="A folder name is required."),
            Length(min=1, max=255, message="Folder name must be between 1 and 255 characters.")
        ]
    )
    submit = SubmitField("Create Folder")

