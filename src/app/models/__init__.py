from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    # "ck": "ck_%(table_name)s_%(constraint_name)s",
    # "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# flake8: noqa E402 F401
from .base_model import BaseModel
from .user import User
from .settings import Settings
from .player import Player
from .division import Division
from .conference import Conference
from .team import Team
from .pick import Pick
from .log import Log
from .status import Status
