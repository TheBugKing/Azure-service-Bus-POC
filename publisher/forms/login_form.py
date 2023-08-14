from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators


class LoginForm(FlaskForm):
    """
    Represents a login form using Flask-WTF.

    Attributes:
        email (StringField): Field for entering the email.
        password (PasswordField): Field for entering the password.
        remember_me (BooleanField): Checkbox for remembering the user.
        submit (SubmitField): Button to submit the form.
    """

    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=12)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
