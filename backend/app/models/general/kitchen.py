from app.core.extensions import db
from ..mixins import TimestampMixin


class Kitchen(TimestampMixin, db.Model):
    __tablename__ = "kitchens"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    background_url = db.Column(db.String(500), nullable=True)

    recipes = db.relationship(
        "Recipe", back_populates="kitchen", lazy="selectin")

    popular_products = db.relationship(
        "Product",
        secondary="product_kitchen_link",
        back_populates="kitchens",
        lazy="selectin"
    )
