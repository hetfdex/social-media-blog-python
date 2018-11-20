from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from blog import db
from blog.models import BlogPost
from blog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint("blog_posts", __name__)

#Create Post Page: Show form for posting and saves it to database after validation. Requires logged in user
@login_required
@blog_posts.route("/create", methods=["GET", "POST"])
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(user_id=current_user.id, title=form.title.data, body=form.body.data)

        db.session.add(blog_post)
        db.session.commit()

        flash("Post Successful")

        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form)

#Blog Post Page: Shows post matching id (int)
@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    return render_template("blog_post.html", blog_post=blog_post)

#Update Post Page: Allows author to update post content matching id (int). Requires logged in user
@login_required
@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
def update_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.body = form.body.data

        db.session.commit()

        flash("Update Successful")

        return redirect(url_for("blog_posts.blog_post", blog_post_id=blog_post.id))

    elif request.method == "GET":
        form.title.data = blog_post.title
        form.body.data = blog_post.body

    return render_template("create_post.html", form=form)

#Delete Post Page: Allows author to delete post matching id (int). Requires logged in user
@login_required
@blog_posts.route("/<int:blog_post_id>/delete", methods=["POST"])
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()

    flash("Delete Successful")

    return redirect(url_for("core.index"))
