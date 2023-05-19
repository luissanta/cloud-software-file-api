import json
import logging.config
import os

from google.cloud import pubsub_v1

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


class PubSubTopic:

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic = os.getenv('GCP_TOPIC')

    def send_message(self, msg: dict) -> bool:
        try:
            future = self.publisher.publish(topic=self.topic, data=json.dumps(msg).encode("utf-8"), timeout=1)
            future.result()
        except Exception as e:
            logger.error("error sending message to topic: {topic} - error: {error}".format(topic=self.topic, error=e.__cause__))

