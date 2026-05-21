from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.extensions import db
from app.models import User


def get_user_by_id(user_id: int):
    """Получить пользователя по ID"""
    return User.query.get(user_id)


def get_user_by_email(email: str):
    """Получить пользователя по email"""
    return User.query.filter_by(email=email).first()


def create_user(email: str, password: str, full_name: str = None):
    """Создать нового пользователя"""
    if not email or not password:
        raise ValueError("Email and password are required")

    if get_user_by_email(email):
        raise ValueError("User with this email already exists")

    hashed_password = generate_password_hash(password)

    user = User(
        email=email.strip().lower(),
        hashed_password=hashed_password,
        full_name=full_name.strip() if full_name else None
    )

    try:
        db.session.add(user)
        db.session.commit()
        return user
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error creating user. Email may already be taken.")
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Unexpected error: {str(e)}")


def authenticate_user(email: str, password: str):
    """Аутентификация пользователя (для логина)"""
    user = get_user_by_email(email)
    if not user:
        return None

    if check_password_hash(user.hashed_password, password):
        return user
    return None


def update_user(user_id: int, full_name: str = None, email: str = None):
    """Обновить данные пользователя"""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    if full_name is not None:
        user.full_name = full_name.strip() if full_name else None

    if email is not None and email.strip().lower() != user.email:
        if get_user_by_email(email.strip().lower()):
            raise ValueError("Email already taken")
        user.email = email.strip().lower()

    try:
        db.session.commit()
        return user
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Update failed due to integrity error")


def change_password(user_id: int, old_password: str, new_password: str):
    """Сменить пароль пользователя"""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    if not check_password_hash(user.hashed_password, old_password):
        raise ValueError("Old password is incorrect")

    if len(new_password) < 6:
        raise ValueError("New password must be at least 6 characters long")

    user.hashed_password = generate_password_hash(new_password)

    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise ValueError("Failed to change password")


def delete_user(user_id: int):
    """Удалить пользователя"""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    # Проверка на наличие связанных рецептов (по желанию)
    if user.authored_recipes:
        raise ValueError("Cannot delete user with existing recipes")

    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise ValueError("Failed to delete user")