from flask_sqlalchemy import SQLAlchemy

from app.core.extensions import db
from app.models.mixins import TimestampMixin


product_recipe_link = db.Table('product_recipe_link',
                               db.Column('product_id', db.Integer, db.ForeignKey(
                                   'products.id'), primary_key=True),
                               db.Column('recipe_id', db.Integer, db.ForeignKey(
                                   'recipes.id'), primary_key=True)
                               )

user_recipe_link = db.Table('user_recipe_link',
                            db.Column('user_id', db.Integer, db.ForeignKey(
                                'users.id'), primary_key=True),
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipes.id'), primary_key=True)
                            )


class Recipe(TimestampMixin, db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    duration = db.Column(db.Integer)
    portions = db.Column(db.Integer)
    likes = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default="not_moderated")

    kitchen_id = db.Column(db.Integer, db.ForeignKey(
        "kitchens.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    kitchen = db.relationship(
        "Kitchen", back_populates="recipes", lazy="selectin")
    author = db.relationship(
        "User", back_populates="authored_recipes", lazy="selectin")

    users = db.relationship(
        "User",
        secondary=user_recipe_link,
        back_populates="favorite_recipes",
        lazy="selectin"
    )

    products = db.relationship(
        "Product",
        secondary=product_recipe_link,
        back_populates="recipes",
        lazy="selectin"
    )

    recipe_steps = db.relationship(
        "RecipeStep",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    ingredients = db.relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
