from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class RegisterForm(FlaskForm):
    """
    Represents a registration form using Flask-WTF.

    Attributes:
        name (StringField): Field for entering the user's name.
        email (StringField): Field for entering the user's email.
        password (PasswordField): Field for entering the user's password.
        confirm_password (PasswordField): Field for confirming the user's password.
        submit (SubmitField): Button to submit the registration form.
    """

    # Field for entering the user's name
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=30)])

    # Field for entering the user's email
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=5, max=30)])

    # Field for entering the user's password
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=12)],
                             render_kw={"placeholder": "password"})

    # Field for confirming the user's password
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ], render_kw={"placeholder": "password"})

    # Button to submit the registration form
    submit = SubmitField('Submit')
