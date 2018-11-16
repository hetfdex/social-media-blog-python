from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from blog import db
from blog.models import BlogPost
from blog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint("blog_posts", __name__)
