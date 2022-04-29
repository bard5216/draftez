from app import app
from app.models import db
from app.models.pick import Pick
from app.models.player import Player


def main():
    """
    for pick, player = db.session.query(Pick, Player).\
                                  filter(Pick.user_id==user_id).\
                                  filter(Pick.player_id==Player.id).\
                                  all():
    """
    q = db.session.query(Pick, Player).filter(Pick.user_id == 1).filter(Pick.player_id == Player.id).order_by(Pick.round)

    for pick, player in q.all():
        print("Round {0} selected {1}".format(pick.round, player.full_name))


if __name__ == '__main__':
    with app.app_context():
        main()
