from extention import db


class TopicSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String)

    user = db.relationship('User', back_populates='topic_subscriptions')

    @classmethod
    def add_topic(cls, user, topic):
        existing_subscription = cls.query.filter_by(user_id=user.id, topic=topic).first()
        if not existing_subscription:
            new_subscription = cls(user=user, topic=topic)
            db.session.add(new_subscription)
            db.session.commit()

