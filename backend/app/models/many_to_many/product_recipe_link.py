from app.core.extensions import db


product_recipe_link = db.Table('product_recipe_link',
                               db.Column('product_id', db.Integer, db.ForeignKey(
                                   'products.id'), primary_key=True),
                               db.Column('recipe_id', db.Integer, db.ForeignKey(
                                   'recipes.id'), primary_key=True)
                               )
