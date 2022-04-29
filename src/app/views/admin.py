from flask import (
    Blueprint,
    render_template,
    request
)
# from flask_login import login_required, current_user

from app.forms.site_settings_form import SiteSettingsForm
from app.helpers.session import current_user, login_required
from app.models import (
    db,
    User,
    Settings
)
# from app.models.settings import Settings
# from app.helpers.auth import is_admin
# from werkzeug.security import check_password_hash


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

admin_routes = [
    {
        "title": "Settings",
        "view": "admin.settings",
        "description": "Draftdodger app settings"
    },
    {
        "title": "Users",
        "view": "admin.users",
        "description": "User administration."
    }
]


@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SiteSettingsForm()

    print("settings")
    print("request method=", request.method)
    print("isopen=", form.isopen)
    if form.validate_on_submit():
        s = db.session.query(Settings).one_or_none()
        s.user_count = form.user_count.data
        s.isopen = form.isopen.data
        s.current_round = form.current_round.data
        s.max_rounds = form.max_rounds.data
        s.invite_password = form.invite_password.data
        db.session.commit()

    s = db.session.query(Settings).one_or_none()
    if s is None:
        s = Settings()
        db.session.add(s)
        db.session.commit()
        s = db.session.query(Settings).one_or_none()
        if s is None:
            raise Exception("Settings cannot be None")

    return render_template("admin/settings.html",
                           form=form,
                           current_user=current_user, settings=s)


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
def users():
    users = User.query.all()
    return render_template("/admin/users.html", users=users, current_user=current_user)


@admin_bp.route("/", methods=["GET", "POST"])
# @login_required
def admin():
    return render_template("admin/bulma_index.html", routes=admin_routes, current_user=current_user)
