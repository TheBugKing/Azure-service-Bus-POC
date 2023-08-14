from . import utils
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from settings import SERVICE_BUS_CON_STR
from log.log import logger


def publish_to_azure_service_bus_topic(topic_name, data):
    """
    Publish data to an Azure Service Bus topic.

    Args:
        topic_name (str): Name of the topic to publish to.
        data (dict): Data to be published.

    Returns:
        None
    """
    try:
        with ServiceBusClient.from_connection_string(SERVICE_BUS_CON_STR) as client:
            with client.get_topic_sender(topic_name) as sender:
                formatted_data = utils.format_publish_data(data=data, topic_name=topic_name)
                sender.send_messages(ServiceBusMessage(formatted_data))
                logger.info("Published to Azure Service Bus topic: %s", topic_name)
    except Exception as e:
        logger.error("Error occurred while publishing to Azure Service Bus: %s", e)
