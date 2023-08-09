from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=4, max=12)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
