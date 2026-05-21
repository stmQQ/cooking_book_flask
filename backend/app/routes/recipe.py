from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from app.services import recipe_service, ingredient_service, recipe_step_service

recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/recipes')


@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe(recipe_id):
    """Получить рецепт по ID"""
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'duration': recipe.duration,
        'portions': recipe.portions,
        'likes': recipe.likes,
        'rating': recipe.rating,
        'status': recipe.status,
        'kitchen_id': recipe.kitchen_id,
        'author_id': recipe.author_id,
    }), 200


@recipe_bp.route('/kitchen/<int:kitchen_id>', methods=['GET'])
@cross_origin()
def get_recipes_by_kitchen(kitchen_id):
    """Получить все рецепты кухни"""
    recipes = recipe_service.get_all_recipes_by_kitchen(kitchen_id)
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'duration': r.duration,
        'portions': r.portions
    } for r in recipes]), 200


@recipe_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    """Создать черновик рецепта"""
    user_id = get_jwt_identity()
    try:
        recipe = recipe_service.create_recipe(author_id=user_id)
        return jsonify({
            'id': recipe.id,
            'message': 'Recipe draft created successfully'
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@recipe_bp.route('/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """Обновить рецепт"""
    data = request.get_json(silent=True) or {}
    try:
        recipe = recipe_service.update_recipe(
            recipe_id=recipe_id,
            title=data.get('title'),
            duration=data.get('duration'),
            portions=data.get('portions'),
            kitchen_id=data.get('kitchen_id')
        )
        return jsonify({
            'id': recipe.id,
            'title': recipe.title,
            'message': 'Recipe updated successfully'
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@recipe_bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """Удалить рецепт"""
    try:
        recipe_service.delete_recipe(recipe_id)
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ====================== Избранное ======================

@recipe_bp.route('/<int:recipe_id>/favorite', methods=['POST'])
@jwt_required()
def add_to_favorites(recipe_id):
    """Добавить в избранное"""
    user_id = get_jwt_identity()
    try:
        recipe_service.add_recipe_to_favorite(recipe_id, user_id)
        return jsonify({"message": "Recipe added to favorites"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@recipe_bp.route('/<int:recipe_id>/favorite', methods=['DELETE'])
@jwt_required()
def remove_from_favorites(recipe_id):
    """Удалить из избранного"""
    user_id = get_jwt_identity()
    try:
        recipe_service.delete_recipe_from_favorite(recipe_id, user_id)
        return jsonify({"message": "Recipe removed from favorites"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400