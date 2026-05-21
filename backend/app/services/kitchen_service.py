from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.models import Kitchen


def get_all_kitchens():
    """Получить данные всех кухонь"""
    return Kitchen.query.all()


def get_kitchen_by_id(id: int):
    """Получить данные кухни по id"""
    return Kitchen.query.get(id)


def create_kitchen(title: str, desc: str, bg_url: str):
    """Создать новый экземпляр кухни"""
    if not title or not title.strip():
        raise ValueError("Kitchen title is required")

    kitchen = Kitchen(
        title=title.strip(),
        description=desc,
        background_url=bg_url
    )

    try:
        db.session.add(kitchen)
        db.session.commit()
        return kitchen
    except IntegrityError:
        db.session.rollback()
        raise ValueError("A kitchen with this title already exists")


# def delete_kitchen(id: int):
#     """Удалить экземпляр кухни"""
#     kitchen = Kitchen.query.get(id)

#     if not kitchen:
#         raise ValueError("Kitchen not found")
#     if kitchen.recipes:
#         raise ValueError("Kitchen has got attached recipes")

#     if kitchen.background_url:
#         delete_image(kitchen.background_url)

#     db.session.delete(kitchen)
#     db.session.commit()

#     return True
