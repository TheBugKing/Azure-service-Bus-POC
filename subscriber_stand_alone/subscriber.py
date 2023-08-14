import multiprocessing
import json
from azure.servicebus import ServiceBusClient

from send_email import send_mail
from setting import SERVICE_BUS_CON_STR
from log import logger


def process_message(message):
    """
    Process a received message.

    Args:
        message (Message): The received message from the service bus.
    """
    message_content = str(message)
    logger.info(f"Received message: {message_content}")
    try:
        message_data = json.loads(message_content)
        topic = message_data.get('topic')
        content = message_data.get('content')
        subscribed_users = message_data.get('subscribed_users', [])

        for user_name, user_email in subscribed_users:
            try:
                response = send_mail(receiver_email=user_email.strip(), subject=topic, message=content)
                logger.info(f"Email sent to: {user_email}")
                logger.info(f"status: {response}")
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                # Optionally, you could log the error for further analysis

    except json.JSONDecodeError:
        logger.warning("Invalid message format")


def process_topic(topic_name, subscription_name):
    """
    Process messages from a subscription within a topic.

    Args:
        topic_name (str): The name of the topic.
        subscription_name (str): The name of the subscription within the topic.
    """
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CON_STR) as client:
        with client.get_subscription_receiver(topic_name, subscription_name=subscription_name) as receiver:
            for message in receiver:
                try:
                    process_message(message)
                    receiver.complete_message(message)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    # Optionally, you could log the error for further analysis


def main():
    """
    Main function to start processing messages from different topics and subscriptions.
    """
    topic_to_subscription = {
        'esports': 'esports',
        'event': 'event',
        'marketing': 'marketing'
    }

    processes = []

    for topic_name, subscription_name in topic_to_subscription.items():
        process = multiprocessing.Process(target=process_topic, args=(topic_name, subscription_name))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    logger.info("Running....")
    main()
