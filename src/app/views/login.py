import logging
import datetime
from flask import (
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash
)
# from flask_login import login_user

from app.models import (
    db,
    User
)


login_bp = Blueprint("login", __name__, url_prefix="/login")
logger = logging.getLogger(__name__)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    When a user logs in successfully then a DraftUsersMessage needs to be
    sent to inform other users who logged in prior.
    """
    if request.method == 'POST':
        print("login request is")
        print(request.form)

        # authenticate request.form['email']
        user = User.query.filter(User.username == request.form['email'])
        if user.count() == 1:
            u = user.one()
            # login_user(u, remember=True)
            u.active = 1
            u.last_login = datetime.datetime.now()
            u.last_seen = u.last_login
            session['user'] = u.as_dict()
            db.session.add(u)
            db.session.commit()

            flash(f"{user.one().username} Logged In")
            next = request.args.get("next")
            return redirect(next or url_for('index.index'))
        else:
            flash("Invalid login")

        """
        if (user is not None):
            print("found user=",user)
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('index.index'))
        """

    return render_template("login_bulma.html")
    # return render_template("login_uikit.html")
