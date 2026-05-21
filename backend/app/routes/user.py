from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from app.services.user_service import (
    get_user_by_id,
    update_user,
    change_password,
    delete_user
)

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/me', methods=['GET'])
@jwt_required()
@cross_origin()
def get_current_user():
    """Получить данные текущего пользователя"""
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "authored_recipes_count": len(user.authored_recipes) if user.authored_recipes else 0,
        "favorite_recipes_count": len(user.favorite_recipes) if user.favorite_recipes else 0
    }), 200


@user_bp.route('/me', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_current_user():
    """Обновить данные текущего пользователя"""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    try:
        user = update_user(
            user_id=user_id,
            full_name=data.get('full_name'),
            email=data.get('email')
        )
        return jsonify({
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/me/change-password', methods=['POST'])
@jwt_required()
@cross_origin()
def change_user_password():
    """Сменить пароль"""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    try:
        change_password(
            user_id=user_id,
            old_password=data.get('old_password'),
            new_password=data.get('new_password')
        )
        return jsonify({"message": "Password changed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/me', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_current_user():
    """Удалить аккаунт текущего пользователя"""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    # Опционально: подтверждение паролем
    password = data.get('password')
    if not password:
        return jsonify({"error": "Password is required to delete account"}), 400

    try:
        # Дополнительная проверка пароля перед удалением
        from app.services.user_service import authenticate_user
        user = get_user_by_id(user_id)
        if not user or not authenticate_user(user.email, password):
            return jsonify({"error": "Incorrect password"}), 401

        delete_user(user_id)
        return jsonify({"message": "Account deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_user_by_id_route(user_id):
    """Получить пользователя по ID (для публичного профиля)"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }), 200