from app.core.extensions import db


product_kitchen_link = db.Table('product_kitchen_link',
                                db.Column('product_id', db.Integer, db.ForeignKey(
                                    'products.id'), primary_key=True),
                                db.Column('kitchen_id', db.Integer, db.ForeignKey(
                                    'kitchens.id'), primary_key=True)
                                )
