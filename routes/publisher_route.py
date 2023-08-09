from flask import url_for, redirect, render_template, flash
from flask import Blueprint
from flask_login import current_user, login_required

from services import utils
from forms.publish_form import PublishForm

publish_bp = Blueprint('publish_bp', __name__)


@publish_bp.route('/', methods=['GET'])
@login_required
def publisher_home():
    data = utils.get_user_data(current_user.id)
    form = PublishForm()
    form.topic.choices = data['topics_subscribed']
    if not form.topic.choices:
        flash('you are not subscribed to any topic, click here to add subscriptions')
    return render_template('publish.html', data=data, form=form)


@publish_bp.route('/publish_post', methods=['POST'])
@login_required
def publish_article():
    form = PublishForm()
    form.topic.choices = utils.get_user_data(current_user.id)['topics_subscribed']
    if form.validate_on_submit():
        post = form.post.data
        topic = form.topic.data
        form.post.data = ''
        form.topic.data = ''
        flash(f"published successfully")
    else:
        for error in form.errors:
            flash(f"Error occurred: {error}")
    return render_template('publish.html',
                           data=utils.get_user_data(current_user.id),
                           form=form)
