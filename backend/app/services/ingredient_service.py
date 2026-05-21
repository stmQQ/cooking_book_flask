from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.models import Ingredient, Product, Recipe


def get_ingredient_info(id: int):
    """Получить данные о ингредиенте"""
    return Ingredient.query.get(id)


def add_ingredient_to_recipe(recipe_id, product_id, measure, amount):
    """Создать и добавить к рецепту ингредиент"""
    product = Product.query.get(product_id)
    if not product:
        raise ValueError("Product not found")

    recipe = Recipe.query.get(recipe_id)

    ingredient = Ingredient(measure=measure, amount=amount)
    ingredient.product = product
    ingredient.recipe = recipe

    try:
        db.session.add(ingredient)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Adding ingredient failed")

    return ingredient
