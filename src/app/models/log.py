from sqlalchemy import func
from app.models import db, BaseModel


class Log(BaseModel):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    # actions: "pick"
    action = db.Column(db.String(20), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # if action=="pick"
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    player = db.relationship("Player")
    user = db.relationship("User")

    def __str__(self):
        return "<Settings_{0}>".format(self.id)

