from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from blog.models import User, BlogPost

user_api = Blueprint("user_api", __name__)

#API Login: Validates json request & user information and returns access token
@user_api.route("/api/login", methods=["POST"])
def api_login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200

#API User: Returns user's email
@user_api.route("/api/user", methods=["GET"])
@jwt_required
def api_user():
    user = get_jwt_identity()

    return jsonify(user), 200

#API Blog Posts: Returns user's blog posts
@user_api.route("/api/blog_posts", methods=["GET"])
@jwt_required
def api_blog_posts():
    to_json = []

    user = User.query.filter_by(email=get_jwt_identity()).first_or_404()

    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc())

    for blog_post in blog_posts:
        entry = {"date published": blog_post.date, "title":blog_post.title,"body":blog_post.body}

        to_json.append(entry)

    return jsonify({"user_id":blog_posts[0].user_id, "blog_posts":to_json}), 200
