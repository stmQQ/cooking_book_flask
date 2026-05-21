from flask import Blueprint

# Создаём blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
kitchen_bp = Blueprint('kitchen', __name__, url_prefix='/api/kitchens')
product_bp = Blueprint('product', __name__, url_prefix='/api/products')
recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/recipes')

__all__ = ['auth_bp', 'kitchen_bp', 'product_bp', 'recipe_bp']