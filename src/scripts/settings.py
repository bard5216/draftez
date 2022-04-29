from app import app
from app.models import db
from app.models.settings import Settings


def main():
    s = db.session.query(Settings).one_or_none()
    print(s)

    """
    for pick, player in q.all():
        print("Round {0} selected {1}".format(pick.round, player.full_name))
    """


if __name__ == '__main__':
    with app.app_context():
        main()
