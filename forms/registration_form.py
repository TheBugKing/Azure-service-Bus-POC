from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=30)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=5, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=12)],
                             render_kw={"placeholder": "password"})
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ], render_kw={"placeholder": "password"})
    submit = SubmitField('Submit')
