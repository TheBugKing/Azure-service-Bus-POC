import json

from flask_login import current_user

from models.TopicSubscriptionModel import TopicSubscription
from models.UserModel import User
from settings import TOPIC_FILE_PATH
from log.log import logger


def read_json_file(file):
    """
    Read and parse JSON data from a file.

    Args:
        file (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        logger.error("Error occurred while reading JSON file: %s", e)
        return {}


def read_topics():
    """
    Read and return topic data from a JSON file.

    Returns:
        dict: Topic data.
    """
    return read_json_file(TOPIC_FILE_PATH)


def get_subscribed_topics(user_id):
    """
    Get the list of topics subscribed by a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        list: List of subscribed topics.
    """
    try:
        user = User.query.get(user_id)
        if user:
            subscribed_topics = user.subscribed_topics.split(',') if user.subscribed_topics else []
            return subscribed_topics
        return []
    except Exception as e:
        logger.error("Error occurred while getting subscribed topics: %s", e)
        return []


def get_user_data(user_id):
    """
    Get user-related data for rendering the dashboard.

    Args:
        user_id (int): ID of the user.

    Returns:
        dict: User-related data.
    """
    try:
        topics_subscribed = get_subscribed_topics(user_id)
        topics = read_json_file(TOPIC_FILE_PATH)
        data = {'username': current_user.name,
                'email': current_user.email,
                'topics_subscribed': topics_subscribed,
                'topics': topics
                }
        return data
    except Exception as e:
        logger.error("Error occurred while getting user data: %s", e)
        return {}


def get_subscribed_topic_users(topic_name):
    """
    Get a list of users subscribed to a specific topic.

    Args:
        topic_name (str): Name of the topic.

    Returns:
        list: List of subscribed user names and emails.
    """
    try:
        subscribed_users = User.query.join(TopicSubscription).filter(TopicSubscription.topic == topic_name).all()
        return [(user.name, user.email) for user in subscribed_users]
    except Exception as e:
        logger.error("Error occurred while getting subscribed topic users: %s", e)
        return []


def format_publish_data(data, topic_name):
    """
    Format data to be published to a topic.

    Args:
        data (dict): Data to be published.
        topic_name (str): Name of the topic.

    Returns:
        str: Formatted JSON data.
    """
    try:
        data_to_send = {'topic': topic_name,
                        'content': data,
                        'subscribed_users': get_subscribed_topic_users(topic_name),
                        'publisher_info': {
                            'publisher_name': current_user.name,
                            'publisher_id': current_user.id,
                            'publisher_email': current_user.email
                        }
                        }
        return json.dumps(data_to_send, indent=1)
    except Exception as e:
        logger.error("Error occurred while formatting publish data: %s", e)
        return ""
