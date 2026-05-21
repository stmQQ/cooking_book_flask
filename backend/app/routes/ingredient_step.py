from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from app.services import ingredient_service, recipe_step_service

ingredient_step_bp = Blueprint(
    'ingredient_step', __name__, url_prefix='/api/recipes')


@ingredient_step_bp.route('/<int:recipe_id>/ingredients', methods=['POST'])
@jwt_required()
def add_ingredient(recipe_id):
    """Добавить ингредиент в рецепт"""
    data = request.get_json(silent=True) or {}
    try:
        ingredient = ingredient_service.add_ingredient_to_recipe(
            recipe_id=recipe_id,
            product_id=data.get('product_id'),
            measure=data.get('measure'),
            amount=data.get('amount')
        )
        return jsonify({
            'id': ingredient.id,
            'message': 'Ingredient added successfully'
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@ingredient_step_bp.route('/<int:recipe_id>/steps', methods=['POST'])
@jwt_required()
def add_recipe_step(recipe_id):
    """Добавить шаг приготовления"""
    data = request.get_json(silent=True) or {}
    try:
        step = recipe_step_service.add_step_to_recipe(
            recipe_id=recipe_id,
            serial_number=data.get('serial_number'),
            text=data.get('text'),
            photo_url=data.get('photo_url')
        )
        return jsonify({
            'id': step.id,
            'serial_number': step.serial_number,
            'message': 'Step added successfully'
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
