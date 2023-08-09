from flask import url_for, redirect
from flask import Blueprint

root_bp = Blueprint('root_bp', __name__)


@root_bp.route('/', methods=['GET'])
def root():
    return redirect(url_for('login_bp.login'))
