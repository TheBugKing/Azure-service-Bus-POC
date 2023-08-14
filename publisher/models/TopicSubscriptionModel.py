from extention import db


class TopicSubscription(db.Model):
    """
    Represents a topic subscription model using SQLAlchemy.

    Attributes:
        id (int): Primary key for the topic subscription.
        user_id (int): Foreign key referencing the associated user's id.
        topic (str): Name of the subscribed topic.
        user (User): Relationship to the associated user.
    """

    # Primary key for the topic subscription
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing the associated user's id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Name of the subscribed topic
    topic = db.Column(db.String)

    # Relationship to the associated user
    user = db.relationship('User', back_populates='topic_subscriptions')

    @classmethod
    def add_topic(cls, user, topic):
        """
        Add a topic subscription for the given user and topic.

        Args:
            user (User): The user to subscribe.
            topic (str): The topic to subscribe to.
        """
        existing_subscription = cls.query.filter_by(user_id=user.id, topic=topic).first()
        if not existing_subscription:
            new_subscription = cls(user=user, topic=topic)
            db.session.add(new_subscription)
            db.session.commit()
