from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from extention import db
from models import User
from models.TopicSubscriptionModel import TopicSubscription
from services import utils

dashboard_bp = Blueprint('dashboard_bp', __name__)

topics = utils.read_topics()


@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard_home():
    data = utils.get_user_data(current_user.id)
    return render_template('dashboard.html', data=data)


@dashboard_bp.route('/subscribe_topics', methods=['GET', 'POST'])
@login_required
def subscribe_topics():
    data = request.form.getlist('subscribe_topics[]')
    for topic in data:
        current_user.subscribe_to_topic(topic_name=topic)
        TopicSubscription.add_topic(user=current_user, topic=topic)
    return redirect(url_for('dashboard_bp.dashboard_home'))


@dashboard_bp.route('/unsubscribe_topics', methods=['GET', 'POST'])
@login_required
def unsubscribe_topics():
    print("here")
    data = request.form.getlist('subscribed_topics[]')
    for topic in data:
        current_user.unsubscribe_from_topic(topic_name=topic)
    return redirect(url_for('dashboard_bp.dashboard_home'))

