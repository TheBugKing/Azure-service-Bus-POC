from extention import db


class TopicSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String)

    user = db.relationship('User', back_populates='topic_subscriptions')

    @classmethod
    def remove_subscription(cls, user, topic):
        subscription = cls.query.filter_by(user_id=user.id, topic_id=topic.id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()

    @classmethod
    def get_subscriptions_by_user(cls, user):
        return cls.query.filter_by(user_id=user.id).all()

    @classmethod
    def get_subscriptions_by_topic(cls, topic):
        return cls.query.filter_by(topic_id=topic.id).all()
