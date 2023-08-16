from flask import url_for, redirect, render_template, flash
from flask import Blueprint
from flask_login import current_user, login_required

from services import utils, publish_utils
from forms.publish_form import PublishForm
from log.log import logger

publish_bp = Blueprint('publish_bp', __name__)


@publish_bp.route('/', methods=['GET'])
@login_required
def publisher_home():
    """
    Display the publisher's home page.

    Returns:
        Response: The rendered template for the publisher's home page.
    """
    logger.info("Publisher home route accessed.")

    data = utils.get_user_data(current_user.id)
    form = PublishForm()
    form.topic.choices = data['topics_subscribed']
    if not form.topic.choices:
        flash('You are not subscribed to any topic. Click here to add subscriptions.')
    return render_template('publish.html', data=data, form=form)


@publish_bp.route('/publish_post', methods=['POST'])
@login_required
def publish_article():
    """
    Publish an article to a topic.

    Returns:
        Response: Redirection to the publisher's home page.
    """
    logger.info("Publish article route accessed.")

    form = PublishForm()
    try:
        form.topic.choices = utils.get_user_data(current_user.id)['topics_subscribed']
        if form.validate_on_submit():
            post = form.post.data
            topic = form.topic.data
            publish_utils.publish_to_azure_service_bus_topic(topic_name=topic, data=post)
            form.post.data = ''
            form.topic.data = ''
            flash("Published successfully.")
        else:
            for error in form.errors:
                flash(f"Error occurred: {error}")
        return redirect(url_for('publish_bp.publisher_home'))
    except Exception as e:
        logger.error("Error occurred while publishing article: %s", e)
        flash("An error occurred.")
        return render_template('publish.html', data=utils.get_user_data(current_user.id), form=form)
