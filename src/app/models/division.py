from app.models import db, BaseModel
# from app.models.conference import Conference
# from app.models.team import Team


class Division(BaseModel):
    __tablename__ = 'divisions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    shortname = db.Column(db.String(16), unique=True, nullable=False)
    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id'), nullable=True)
    conference = db.relationship('Conference', back_populates='divisions')
    teams = db.relationship('Team')
