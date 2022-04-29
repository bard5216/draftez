from app.models import db, BaseModel


class Player(BaseModel):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    position = db.Column(db.String(16), nullable=False)

    season = db.Column(db.String(16), nullable=True)
    games = db.Column(db.Integer, nullable=True)
    goals = db.Column(db.Integer, nullable=True)
    assists = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=True)

    team = db.relationship('Team', back_populates='players')

    def __str__(self):
        return "<Player_{0}:{1}>".format(self.id, self.full_name)
