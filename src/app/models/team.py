from app.models import db, BaseModel
# from app.models.player import Player
# from app.models.division import Division


class Team(BaseModel):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    shortname = db.Column(db.String(16), unique=True, nullable=False)
    abbrev = db.Column(db.String(3), unique=True, nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'), nullable=False)
    in_playoffs = db.Column(db.Boolean, nullable=False, default=1)

    division = db.relationship('Division', back_populates='teams')
    players = db.relationship('Player')

    def __str__(self):
        return "<Team#{0}_{1}>".format(self.id, self.shortname)
