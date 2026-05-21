from app.core.extensions import db
from app.models.mixins import TimestampMixin


class RecipeStep(TimestampMixin, db.Model):
    __tablename__ = "recipe_steps"

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(500), nullable=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipes.id"), nullable=False)

    recipe = db.relationship(
        "Recipe", back_populates="recipe_steps", lazy="selectin")
