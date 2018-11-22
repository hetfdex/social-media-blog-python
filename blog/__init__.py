from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

#App init & config
app = Flask(__name__)

app.config["SECRET_KEY"] = "Abcde12345!"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Database init
db = SQLAlchemy(app)

Migrate(app, db)

#Login manager init & config
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "users.login"

jwt = JWTManager(app)

#Blueprint registration
from blog.core.views import core
from blog.users.views import users
from blog.blog_posts.views import blog_posts
from blog.endpoints.views import user_api
from blog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(user_api)
app.register_blueprint(error_pages)
