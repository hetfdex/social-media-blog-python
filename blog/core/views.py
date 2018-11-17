from flask import render_template, request, Blueprint
from blog.models import BlogPost

core = Blueprint("core", __name__)

#Home Page: Shows a maximum of 5 blog posts using pagination
@core.route("/")
def index():
    page = request.args.get("page", 1, type=int)

    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template("index.html", blog_posts=blog_posts)

#About Page: Just a sample
@core.route("/about")
def about():
    return render_template("about.html")
