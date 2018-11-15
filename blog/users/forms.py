from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from blog.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired(), EqualTo("password_confirm", message="Passwords must match")])
    password_confirm = StringField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Email already in use")

class UpdateProfileForm(FlaskForm):
    username = StringField("Change Username", validators=[DataRequired()])
    userpicture = FileField("Change Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update Profile")

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Username already in use")
