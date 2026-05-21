from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin

from app.services.user_service import (
    create_user, 
    authenticate_user, 
    get_user_by_id
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    """Регистрация нового пользователя"""
    data = request.get_json(silent=True) or {}

    try:
        user = create_user(
            email=data.get('email'),
            password=data.get('password'),
            full_name=data.get('full_name')
        )
        return jsonify({
            "message": "User registered successfully",
            "user_id": user.id,
            "email": user.email
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """Авторизация пользователя"""
    data = request.get_json(silent=True) or {}

    user = authenticate_user(
        email=data.get('email'),
        password=data.get('password')
    )

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }), 200