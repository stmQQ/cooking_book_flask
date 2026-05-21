from app.core.extensions import db
from app.models.many_to_many import product_kitchen_link, product_recipe_link
from ..mixins import TimestampMixin


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    manufacture = db.Column(db.String(255), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)

    recipes = db.relationship(
        "Recipe",
        secondary=product_recipe_link,
        back_populates="products",
        lazy="selectin"
    )

    kitchens = db.relationship(
        "Kitchen",
        secondary=product_kitchen_link,
        back_populates="popular_products",
        lazy="selectin"
    )
