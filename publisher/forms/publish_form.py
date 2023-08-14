from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, validators

from services.utils import read_topics


class PublishForm(FlaskForm):
    """
    Represents a form for publishing posts using Flask-WTF.

    Attributes:
        choices (list): List of topic choices for the SelectField.
        post (TextAreaField): Field for entering the post content.
        topic (SelectField): Dropdown for selecting the topic.
        submit (SubmitField): Button to submit the form.
    """

    # Load topic choices from a function
    choices = read_topics()['Topics']

    # Field for entering the post content
    post = TextAreaField('Post', validators=[validators.DataRequired()])

    # Dropdown for selecting the topic
    topic = SelectField('Topic', choices=choices, validators=[validators.DataRequired()])

    # Button to submit the form
    submit = SubmitField('Submit')
