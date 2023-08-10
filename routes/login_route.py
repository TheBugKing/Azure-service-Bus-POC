from flask import render_template, flash, request, redirect, url_for
from flask import Blueprint
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from forms.login_form import LoginForm
from models.UserModel import User
from extention import login_manager

login_bp = Blueprint('login_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember_me.data
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("user does not exists, please register")
            else:
                if check_password_hash(user.hashed_password, password, ):
                    login_user(user, remember=remember)
                    return redirect(url_for('dashboard_bp.dashboard_home'))
                else:
                    flash("email or password incorrect")
    print("login page")
    return render_template('login.html', form=form)


@login_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("user logged out !!")
    return redirect(url_for('login_bp.login', _method='GET'))
