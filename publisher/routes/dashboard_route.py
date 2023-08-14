from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from models.TopicSubscriptionModel import TopicSubscription
from services import utils
from log.log import logger

dashboard_bp = Blueprint('dashboard_bp', __name__)

topics = utils.read_topics()


@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard_home():
    """
    Dashboard home route.

    Returns:
        Response: Rendered dashboard template.
    """
    logger.info("Dashboard home route accessed.")

    try:
        data = utils.get_user_data(current_user.id)
        return render_template('dashboard.html', data=data)
    except Exception as e:
        logger.error("Error occurred in dashboard_home: %s", e)
        return "An error occurred."


@dashboard_bp.route('/subscribe_topics', methods=['GET', 'POST'])
@login_required
def subscribe_topics():
    """
    Subscribe to topics route.

    Returns:
        Response: Redirection to the dashboard home page.
    """
    logger.info("Subscribe topics route accessed.")

    try:
        data = request.form.getlist('subscribe_topics[]')
        for topic in data:
            current_user.subscribe_to_topic(topic_name=topic)
            TopicSubscription.add_topic(user=current_user, topic=topic)
        return redirect(url_for('dashboard_bp.dashboard_home'))
    except Exception as e:
        logger.error("Error occurred in subscribe_topics: %s", e)
        return "An error occurred."


@dashboard_bp.route('/unsubscribe_topics', methods=['GET', 'POST'])
@login_required
def unsubscribe_topics():
    """
    Unsubscribe from topics route.

    Returns:
        Response: Redirection to the dashboard home page.
    """
    logger.info("Unsubscribe topics route accessed.")

    try:
        data = request.form.getlist('subscribed_topics[]')
        for topic in data:
            current_user.unsubscribe_from_topic(topic_name=topic)
        return redirect(url_for('dashboard_bp.dashboard_home'))
    except Exception as e:
        logger.error("Error occurred in unsubscribe_topics: %s", e)
        return "An error occurred."
