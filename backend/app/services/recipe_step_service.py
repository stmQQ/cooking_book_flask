from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.models import RecipeStep
from app.models.general.recipe import Recipe


def add_step_to_recipe(recipe_id, serial_number, text, photo_url):
    """Добавляет шаг к рецепту"""
    step = RecipeStep(serial_number=serial_number,
                      text=text, photo_url=photo_url)

    recipe = Recipe.query.get(recipe_id)
    step.recipe = recipe
    try:
        db.session.add(step)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Adding recipe step failed")
    return step
