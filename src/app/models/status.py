from app.models import db, BaseModel


class Status(BaseModel):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    k = db.Column(db.String(64), unique=True, nullable=False)
    v = db.Column(db.String(64))

    def __str__(self):
        return "<Status_{0}_{1}_{2}>".format(self.id, self.k, self.v)