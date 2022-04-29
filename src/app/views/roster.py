from flask import Blueprint, render_template, request


roster_bp = Blueprint("roster", __name__, url_prefix="/rosters")

rosters = {
    "barry": [
        {"team": "EDM", "player": "Connor McDavid"},
        {"team": "EDM", "player": "Leon Draisitl"},
        {"team": "TOR", "player": "Austen Matthews"},
        {"team": "WPG", "player": "Kyle Connor"},
    ],
    "brian": [
        {"team": "CAL", "player": "Milan Lucic"},
        {"team": "CAL", "player": "Milan Lucic"},
        {"team": "CAL", "player": "Milan Lucic"},
        {"team": "CAL", "player": "Milan Lucic"},
    ],
    "bill": [
        {"team": "VEG", "player": "Milan Lucic"},
        {"team": "VAN", "player": "Milan Lucic"},
        {"team": "COL", "player": "Milan Lucic"},
        {"team": "DAL", "player": "Milan Lucic"},
    ],
    "frazlo": [
        {"team": "STL", "player": "Milan Lucic"},
        {"team": "BOS", "player": "Milan Lucic"},
        {"team": "MON", "player": "Milan Lucic"},
        {"team": "COL", "player": "Milan Lucic"},
    ],
}

]
@roster_bp.route("/<user>")
def roster(user):
    return "foo"
