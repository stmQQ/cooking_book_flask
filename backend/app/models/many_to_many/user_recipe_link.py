from app.core.extensions import db


user_recipe_link = db.Table('user_recipe_link',
                            db.Column('user_id', db.Integer, db.ForeignKey(
                                'users.id'), primary_key=True),
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipes.id'), primary_key=True)
                            )