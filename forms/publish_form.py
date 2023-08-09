from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, TextAreaField, SelectField
from flask_login import current_user
from services.utils import read_topics


class PublishForm(FlaskForm):
    choices = read_topics()['Topics']
    post = TextAreaField('Post', validators=[validators.DataRequired()])
    topic = SelectField('Topic', choices=choices, validators=[validators.DataRequired()])
    submit = SubmitField('Submit')
