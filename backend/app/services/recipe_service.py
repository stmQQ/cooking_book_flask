from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.models import Recipe, RecipeStep, Ingredient, Kitchen, User


def get_recipe_by_id(id: int):
    return Recipe.query.get(id)


def get_all_recipes_by_kitchen(kitchen_id: int):
    return Kitchen.query.get(kitchen_id).recipes


def get_all_authored_recipes(user_id: int):
    return User.query.get(user_id).authored_recipes


def get_all_favorite_recipes(user_id: int):
    return User.query.get(user_id).favorite_recipes


def create_recipe(author_id: int):
    author = User.query.get(author_id)
    recipe = Recipe(title="Название")
    recipe.author = author
    try:
        db.session.add(recipe)
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Creating recipe failed")


def update_recipe(recipe_id, title=None, duration=None, portions=None, kitchen_id=None):
    """Добавляет рецепт"""
    recipe = Recipe.query.get(recipe_id)
    if title:
        recipe.title = title
    if duration:
        recipe.duration = duration
    if portions:
        recipe.portions = portions
    if kitchen_id:
        kitchen = Kitchen.query.get(kitchen_id)
        recipe.kitchen = kitchen
    try:
        db.session.add(recipe)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Updating recipe failed")
    return recipe


def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    try:
        db.session.delete(recipe)
    except IntegrityError:
        raise ValueError("Deleting recipe failed")
    
    return True
    

def add_recipe_to_favorite(recipe_id, user_id):
    recipe = Recipe.query.get(recipe_id)
    user = User.query.get(user_id)

    user.favorite_recipes.append(recipe)
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError: 
        db.session.rollback()
        raise ValueError("Adding to favorite failed")
    

def delete_recipe_from_favorite(recipe_id, user_id):
    recipe = Recipe.query.get(recipe_id)
    user = User.query.get(user_id)

    user.favorite_recipes.remove(recipe)
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError: 
        db.session.rollback()
        raise ValueError("Removing from favorite failed")

