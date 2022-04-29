import logging
# from app import db
from app.models import db
from datetime import datetime


logger = logging.getLogger(__name__)


class BaseModel(db.Model):
    __abstract__ = True
    __public_columns__ = None  # override with a list of column names

    def as_dict(self):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d = {}
        for c in self.__table__.columns:
            # logger.info(f"as_dict: c.name={c.name}")
            o = getattr(self, c.name)
            if isinstance(o, datetime):
                v = o.isoformat()
            else:
                v = o
            d[c.name] = v

        return d

    def as_dict_public(self):
        if getattr(self, '__public_columns__', None) is None:
            return self.as_dict()

        return {c: getattr(self, c) for c in self.__public_columns__}

    def __str__(self):
        return "<BaseModel_{0}>".format(0)

    def __repr__(self):
        return self.__str__()
