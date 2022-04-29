from app.models import db, BaseModel
# from app.models.division import Division


class Conference(BaseModel):
    __tablename__ = 'conferences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    shortname = db.Column(db.String(16), unique=True, nullable=False)

    # divisions = db.relationship('Division', back_populates='conference')
    divisions = db.relationship('Division')
