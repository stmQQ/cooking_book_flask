from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_cors import cross_origin

# from app.services import user_service  # будет позже

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    """Регистрация пользователя"""
    data = request.get_json(silent=True) or {}
    # TODO: Подключить user_service
    return jsonify({"message": "User registration endpoint - implement user_service"}), 501


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """Авторизация пользователя"""
    data = request.get_json(silent=True) or {}
    # TODO: Подключить user_service
    return jsonify({"message": "Login endpoint - implement user_service"}), 501
