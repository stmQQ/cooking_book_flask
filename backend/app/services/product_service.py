from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.models import Product


def get_product_by_id(id: int):
    return Product.query.get(id)


def create_product(title, type, manufacture, calories, proteins, fats, carbs, sugar, fiber):
    """Добавляет новый продукт"""
    product = Product(title, type, manufacture, calories,
                      proteins, fats, carbs, sugar, fiber)
    try:
        db.session.add(product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Adding product failed")
