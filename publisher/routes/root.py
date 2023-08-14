from flask import url_for, redirect
from flask import Blueprint
from log.log import logger

root_bp = Blueprint('root_bp', __name__)


@root_bp.route('/', methods=['GET'])
def root():
    logger.info("Redirecting to login page.")
    return redirect(url_for('login_bp.login'))
