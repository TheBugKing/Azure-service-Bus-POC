from sqlalchemy import func
from flask_login import UserMixin

from extention import db
from . import TopicSubscriptionModel


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    hashed_password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    subscribed_topics = db.Column(db.String)  # Store topic names as a comma-separated string

    # topic_subscriptions = db.relationship(
    #     'TopicSubscription',
    #     back_populates='user',
    #     cascade='all, delete-orphan'
    # )

    def subscribe_to_topic(self, topic_name):
        topics = self.subscribed_topics.split(',') if self.subscribed_topics else []
        if topic_name not in topics:
            topics.append(topic_name)
            self.subscribed_topics = ','.join(topics)

    def unsubscribe_from_topic(self, topic_name):
        topics = self.subscribed_topics.split(',') if self.subscribed_topics else []
        if topic_name in topics:
            topics.remove(topic_name)
            self.subscribed_topics = ','.join(topics)
