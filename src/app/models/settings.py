from app.models import db, BaseModel


class Settings(BaseModel):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_count = db.Column(db.Integer)
    max_rounds = db.Column(db.Integer)
    current_round = db.Column(db.Integer)
    isopen = db.Column(db.Integer)
    site_password = db.Column(db.String(64))
    site_id = db.Column(db.Integer)
    invite_password = db.Column(db.String(64))

    def __str__(self):
        return "<Settings_{0}>".format(self.id)