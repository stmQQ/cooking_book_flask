from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
kitchen_bp = Blueprint('kitchen', __name__, url_prefix='/api/kitchens')
product_bp = Blueprint('product', __name__, url_prefix='/api/products')
recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/recipes')
user_bp = Blueprint('user', __name__, url_prefix='/api/users')
ingredient_step_bp = Blueprint('ingredient_step', __name__, url_prefix='/api/recipes')

__all__ = [
    'auth_bp', 'kitchen_bp', 'product_bp',
    'recipe_bp', 'user_bp', 'ingredient_step_bp'
]