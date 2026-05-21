from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from app.services import kitchen_service

kitchen_bp = Blueprint('kitchen', __name__, url_prefix='/api/kitchens')


@kitchen_bp.route('/', methods=['GET'])
@cross_origin()
def get_all_kitchens():
    """Получить все кухни"""
    kitchens = kitchen_service.get_all_kitchens()
    return jsonify([{
        'id': k.id,
        'title': k.title,
        'description': k.description,
        'background_url': k.background_url,
        'recipe_count': len(k.recipes) if hasattr(k, 'recipes') and k.recipes else 0
    } for k in kitchens]), 200


@kitchen_bp.route('/<int:kitchen_id>', methods=['GET'])
@cross_origin()
def get_kitchen(kitchen_id):
    """Получить кухню по ID"""
    kitchen = kitchen_service.get_kitchen_by_id(kitchen_id)
    if not kitchen:
        return jsonify({"error": "Kitchen not found"}), 404

    return jsonify({
        'id': kitchen.id,
        'title': kitchen.title,
        'description': kitchen.description,
        'background_url': kitchen.background_url,
    }), 200


@kitchen_bp.route('/', methods=['POST'])
@jwt_required()
def create_kitchen():
    """Создать кухню"""
    data = request.get_json(silent=True) or {}
    try:
        kitchen = kitchen_service.create_kitchen(
            title=data.get('title'),
            desc=data.get('description', ''),
            bg_url=data.get('background_url')
        )
        return jsonify({
            'id': kitchen.id,
            'title': kitchen.title,
            'message': 'Kitchen created successfully'
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@kitchen_bp.route('/<int:kitchen_id>', methods=['DELETE'])
@jwt_required()
def delete_kitchen(kitchen_id):
    """Удалить кухню"""
    try:
        kitchen_service.delete_kitchen(kitchen_id)
        return jsonify({"message": "Kitchen deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
