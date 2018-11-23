from blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#User loader callback (required)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#User Model: Stores user information with a relationship to their blog posts
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(96), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    userpicture = db.Column(db.String(32), nullable = False, default = "default_picture.png")

    blog_posts = db.relationship("BlogPost", backref = "author", lazy = True)

    def __init__(self, email, password):
        self.email = email
        self.username = email.split("@")[0]
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_username(self, username):
        self.username = username

    def __repr__(self):
        return f"Email: {self.email}"

#Blog Post Model: Stores blog posts information with a relationship to their authors
class BlogPost(db.Model):
    __tablename__ = "blogposts"

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    title = db.Column(db.String(96), nullable = False)

    body = db.Column(db.Text, nullable = False)

    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, user_id, title, body):
        self.user_id = user_id
        self.title = title
        self.body = body

    def __repr__(self):
        return f"User ID: {self.user_id}"
