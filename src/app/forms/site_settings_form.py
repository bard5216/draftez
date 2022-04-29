from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SiteSettingsForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired()])
    user_count = IntegerField('Maximum number of users')
    isopen = BooleanField('SiteOpen')
    # site_password
    # site_id
    current_round = IntegerField("Current round")
    max_rounds = IntegerField("Number of rounds")
    invite_password = StringField("Invite Password")

    submit = SubmitField('Save')
