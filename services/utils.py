import json

from flask_login import current_user

from models.UserModel import User
from settings import TOPIC_FILE_PATH


def read_json_file(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        return data


def read_topics():
    return read_json_file(TOPIC_FILE_PATH)


def get_subscribed_topics(user_id):
    user = User.query.get(user_id)
    if user:
        subscribed_topics = user.subscribed_topics.split(',') if user.subscribed_topics else []
        return subscribed_topics
    return []


def get_user_data(user_id):
    topics_subscribed = get_subscribed_topics(user_id)
    topics = read_json_file(TOPIC_FILE_PATH)
    data = {'username': current_user.name,
            'email': current_user.email,
            'topics_subscribed': topics_subscribed,
            'topics': topics
            }
    return data
