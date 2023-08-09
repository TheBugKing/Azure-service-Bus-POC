from flask import render_template, redirect, url_for, flash, request
from flask import Blueprint
from werkzeug.security import generate_password_hash
from forms.registration_form import RegisterForm
from models.UserModel import User
from extention import db

register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/', methods=['GET', 'POST'])
def register_user():

    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            hashed_password = generate_password_hash(form.password.data, method='sha256')

            user_exist = User.query.filter_by(email=email).first()
            if user_exist:
                flash('email already registered')
                return redirect(url_for('register_bp.register_user'))

            user = User(name=name, email=email, hashed_password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successfully please login...')
            return redirect(url_for('login_bp.login'))

    return render_template('register_user.html', form=form)
