from sqlalchemy import func
from flask_login import UserMixin

from extention import db
from models import TopicSubscription


class User(db.Model, UserMixin):
    """
    Represents a user model using SQLAlchemy and Flask-Login integration.

    Attributes:
        id (int): Primary key for the user.
        name (str): User's name.
        email (str): User's email (unique).
        hashed_password (str): Hashed password.
        created_at (datetime): Timestamp of user creation.
        subscribed_topics (str): Comma-separated string of subscribed topic names.
        topic_subscriptions (list): Relationship to associated topic subscriptions.
    """

    # Primary key for the user
    id = db.Column(db.Integer, primary_key=True)

    # User's name
    name = db.Column(db.String(50))

    # User's email (unique)
    email = db.Column(db.String(50), unique=True)

    # Hashed password
    hashed_password = db.Column(db.String(255))

    # Timestamp of user creation
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Comma-separated string of subscribed topic names
    subscribed_topics = db.Column(db.String)

    # Relationship to associated topic subscriptions
    topic_subscriptions = db.relationship(
        'TopicSubscription',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def subscribe_to_topic(self, topic_name):
        """
        Subscribe the user to a topic.

        Args:
            topic_name (str): The name of the topic to subscribe to.
        """
        topics = self.subscribed_topics.split(',') if self.subscribed_topics else []
        if topic_name not in topics:
            topics.append(topic_name)
            self.subscribed_topics = ','.join(topics)
            db.session.commit()

    def unsubscribe_from_topic(self, topic_name):
        """
        Unsubscribe the user from a topic.

        Args:
            topic_name (str): The name of the topic to unsubscribe from.
        """
        topics = self.subscribed_topics.split(',') if self.subscribed_topics else []
        if topic_name in topics:
            topics.remove(topic_name)
            self.subscribed_topics = ','.join(topics)

            subscription = TopicSubscription.query.filter_by(
                user_id=self.id,
                topic=topic_name
            ).first()
            if subscription:
                db.session.delete(subscription)
            db.session.commit()
