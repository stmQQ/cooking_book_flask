from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from app.services import product_service

product_bp = Blueprint('product', __name__, url_prefix='/api/products')


@product_bp.route('/<int:product_id>', methods=['GET'])
@cross_origin()
def get_product(product_id):
    """Получить продукт по ID"""
    product = product_service.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        'id': product.id,
        'title': product.title,
        'type': product.type,
        'manufacture': product.manufacture,
        'calories': product.calories,
        'proteins': product.proteins,
        'fats': product.fats,
        'carbs': product.carbs,
        'sugar': product.sugar,
        'fiber': product.fiber
    }), 200


@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """Создать продукт"""
    data = request.get_json(silent=True) or {}
    try:
        product = product_service.create_product(
            title=data.get('title'),
            type=data.get('type'),
            manufacture=data.get('manufacture'),
            calories=data.get('calories'),
            proteins=data.get('proteins'),
            fats=data.get('fats'),
            carbs=data.get('carbs'),
            sugar=data.get('sugar'),
            fiber=data.get('fiber')
        )
        return jsonify({
            'id': product.id,
            'title': product.title,
            'message': 'Product created successfully'
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
