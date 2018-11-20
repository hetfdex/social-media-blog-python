from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from blog import db
from blog.models import User, BlogPost
from blog.users.forms import LoginForm, RegistrationForm, UpdateProfileForm
from blog.users.picture_handler import add_profile_picture

users = Blueprint("users", __name__)

#Login Page: Show and validate user login
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            flash("Login Successful")

            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("core.index")

            return redirect(next)

    return render_template("login.html", form=form)

#Registration Page: Show, validate and store user registration
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)

#Logout Page: Logs user out
@users.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("core.index"))

#Account Page: Shows user's account. Allows for updating of username and profile picture. Requires logged in user
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateProfileForm()
    update_profile = False

    if form.validate_on_submit():
        if form.username.data:
            current_user.username = form.username.data
            update_profile = True

        if form.userpicture.data:
            current_user.userpicture = add_profile_picture(current_user.username, form.userpicture.data)

            update_profile = True

        if update_profile:
            db.session.commit()

            flash("Update Successful")

        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username

    userpicture = url_for("static", filename="profile_pictures/" + current_user.userpicture)

    return render_template("account.html", userpicture=userpicture, form=form)

#User posts: Shows posts by user. Shows a maximum of 10 blog posts using pagination
@users.route("/<username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    return render_template("user_posts.html", blog_posts=blog_posts, user=user)
