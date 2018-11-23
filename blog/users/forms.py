from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from blog.models import User

#User Login Form: Requires email and password
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

#User Registration Form: Requires email and password confirmation. Checks if email is already in use
class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password_confirm", message="Password Doesn't Match!")])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Email already in use")

#Update Profile Form: Requires usermane. Picture optional. Picture must be jpg or png. Checks if username is already in use
class UpdateProfileForm(FlaskForm):
    username = StringField("Change Username", validators=[DataRequired()])
    userpicture = FileField("Change Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update Profile")

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Username already in use")
