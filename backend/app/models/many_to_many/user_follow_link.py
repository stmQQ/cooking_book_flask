from app.core.extensions import db


user_follow_link = db.Table('user_follow_link',
                            db.Column('follower_id', db.Integer, db.ForeignKey(
                                'users.id'), primary_key=True),
                            db.Column('following_id', db.Integer,
                                      db.ForeignKey('users.id'), primary_key=True)
                            )
