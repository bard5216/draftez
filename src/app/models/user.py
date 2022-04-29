from sqlalchemy import func
# from flask_login import UserMixin
from app.models import db, BaseModel


# class User(db.Model, UserMixin):
class User(BaseModel):
    __tablename__ = 'users'
    __public_columns__ = ['id', 'username', 'display_name', 'pos']

    id = db.Column(db.Integer, primary_key=True)
    # Username should be an email-addr
    username = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), unique=True, nullable=False)
    # 80 char password to accommodate sha256 hash
    password = db.Column(db.String(80))
    pos = db.Column(db.Integer, nullable=False, default=0)
    admin = db.Column(db.Integer, nullable=False, default=0)
    registered = db.Column(db.Integer, nullable=False, default=0)
    # logged in - and not timed-out
    active = db.Column(db.Integer, nullable=False, default=0)
    last_seen = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())

    def is_selecting(self):
        """
        Currently draft selecting.
        """
        return True

    def __str__(self):
        return "<User_{0}:{1}>".format(self.id, self.username)
