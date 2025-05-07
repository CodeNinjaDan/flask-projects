from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Length, Email
from flask_ckeditor import CKEditorField, CKEditor
from flask import Flask

app = Flask(__name__)
ckeditor = CKEditor(app)

# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign me up")

# LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Let me in!")

# CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit comment")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                      render_kw={"class": "form-control", "placeholder": "Your name"})
    email = StringField("Email", validators=[DataRequired(), Email()],
                      render_kw={"class": "form-control", "placeholder": "Your email"})
    phone = StringField("Phone Number",
                       render_kw={"class": "form-control", "placeholder": "Your phone (optional)"})
    message = StringField("Message", validators=[DataRequired()],
                          render_kw={"class": "form-control", "placeholder": "Your message", "rows": 5})
    submit = SubmitField("Send")