from app.models import db, BaseModel

# import pytz
from sqlalchemy.sql import func


class Pick(BaseModel):
    __tablename__ = 'picks'

    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    elapsed_secs = db.Column(db.Integer)

    player = db.relationship("Player")
    user = db.relationship("User")

    def __str__(self):
        return "<Pick_{0}:{1}_{2}>".format(self.id, self.round, self.user_id)
