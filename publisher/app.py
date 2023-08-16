import logging
from flask import Flask
from flask_migrate import Migrate

from extention import db, login_manager
from settings import DB_URL
from log.log import logger

from routes.login_route import login_bp
from routes.registration_route import register_bp
from routes.dashboard_route import dashboard_bp
from routes.publisher_route import publish_bp
from routes.root import root_bp


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'why_are_you_running'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'login_bp.login'

    app.register_blueprint(root_bp, url_prefix='/')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(publish_bp, url_prefix='/publish')

    with app.app_context():
        db.create_all()

    logger.info("Flask app created and configured.")
    return app


if __name__ == '__main__':
    logger.info("Starting the Flask app...")
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=80)
