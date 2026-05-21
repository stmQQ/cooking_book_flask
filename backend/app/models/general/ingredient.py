from app.core.extensions import db
from ..mixins import TimestampMixin


class Ingredient(TimestampMixin, db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    measure = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship(
        "Product", back_populates="ingredients", lazy="selectin")
