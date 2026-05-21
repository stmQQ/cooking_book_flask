from app.core.extensions import db
from app.models.many_to_many import user_follow_link, user_recipe_link
from ..mixins import TimestampMixin


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)

    authored_recipes = db.relationship(
        "Recipe", back_populates="author", lazy="selectin")

    favorite_recipes = db.relationship(
        "Recipe",
        secondary=user_recipe_link,
        back_populates="users",
        lazy="selectin"
    )
    following = db.relationship(
        "User",
        secondary=user_follow_link,
        primaryjoin=(user_follow_link.c.follower_id == id),
        secondaryjoin=(user_follow_link.c.following_id == id),
        back_populates="followers"
    )
    followers = db.relationship(
        "User",
        secondary=user_follow_link,
        primaryjoin=(user_follow_link.c.following_id == id),
        secondaryjoin=(user_follow_link.c.follower_id == id),
        back_populates="following"
    )
