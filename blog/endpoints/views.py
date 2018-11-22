from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from blog.models import User

user_api = Blueprint("user_api", __name__)

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

    if user.check_password(password):
        access_token = create_access_token(identity=email)

        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

@user_api.route('/api/user', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
