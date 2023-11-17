from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token
from ..models import User
from datetime import timedelta
from . import auth_blueprint as auth


@auth.post("/register")
def handle_register():
    data = request.json
    if not data:
        return jsonify({"message": "username, email, and password are required to register"}), 400

    username = data.get("username")
    email = data.get("email")  
    password = data.get("password")

    if not username:
        return jsonify({"message": "username is required"}), 400
    if not email:
        return jsonify({"message": "email is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "username already in use"}), 400

    user = User(username=username, email=email, password=password)  
    user.create()

    return jsonify({"message": "user registered", "data": user.to_response()}), 201


@auth.post("/login")
def handle_login():
    data = request.json
    if not data:
        return jsonify({"message": "username and password are required to login"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"message": "username is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "please create an account before trying to login"}), 400

    if not user.verify_password(password):
        return jsonify({"message": "invalid credentials"}), 401

    auth_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    response = jsonify({
        "message": "successfully logged in",
        "token": auth_token,
        "user": user.to_response()
    })
    response.headers["Authorization"] = f"Bearer {auth_token}"
    return response, 200

