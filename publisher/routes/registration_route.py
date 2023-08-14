from flask import render_template, redirect, url_for, flash, request
from flask import Blueprint
from werkzeug.security import generate_password_hash
from forms.registration_form import RegisterForm
from models.UserModel import User
from extention import db
from log.log import logger

register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/', methods=['GET', 'POST'])
def register_user():
    """
    Register user route.

    GET: Display the registration form.
    POST: Process the submitted form data for user registration.

    Returns:
        Response: Either the registration form or a redirection.
    """
    logger.info("Register user route accessed.")

    form = RegisterForm()

    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                hashed_password = generate_password_hash(form.password.data, method='sha256')

                user_exist = User.query.filter_by(email=email).first()
                if user_exist:
                    flash('Email already registered.')
                    logger.warning("Registration attempt with an existing email.")
                    return redirect(url_for('register_bp.register_user'))

                user = User(name=name, email=email, hashed_password=hashed_password)
                db.session.add(user)
                db.session.commit()

                flash('Registration successful. Please log in.')
                logger.info("User registered successfully.")
                return redirect(url_for('login_bp.login'))
    except Exception as e:
        logger.error("Error occurred during user registration: %s", e)
        flash('An error occurred during registration.')

    return render_template('register_user.html', form=form)
