import json
import logging.config
import os
from concurrent.futures._base import CancelledError
from concurrent.futures._base import TimeoutError
from datetime import datetime, timedelta

from flask_apscheduler import APScheduler
from google.cloud import pubsub_v1

from app.enums.file import ConverterStatusEnum
from app.factories import CompressorFactory
from app.repositories.file.bucket_file_storage import BucketFileStorage
from app.repositories.file.file_manager import FileManager
from ...models.sqlAlchemy.TaskFileModel import Task
from ...models.sqlAlchemy.declarative_base import Session
from ...utils.file_converter import FileConverter

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

file_manager = FileManager(BucketFileStorage())
scheduler = APScheduler()

publisher = pubsub_v1.PublisherClient()
subscriptor = os.getenv('GCP_SUBSCRIPTOR')
topic = os.getenv('GCP_TOPIC')
file_converter = FileConverter()

def callback(msg):
    try:
        data = json.loads(msg.data)
        logger.info("running schedule task: id {task_id}, msg: {msg}".format(task_id=data["task_id"], msg=data))
        file_converter.converter_request(data["task_id"], data["url"], data["new_format"])
        msg.ack()
    except Exception as e:
        logger.error("error processing message: error {error}".format(error=e))
        raise e


def process_msg():
    try:
        logger.info("aqui estoy ")
        with pubsub_v1.SubscriberClient() as subscriber:
            future = subscriber.subscribe(subscriptor, callback)
            future.result()
    except TimeoutError:
        logger.info("does not exist any message to process")
        future.cancel()
    except CancelledError as e:
        logger.error("message process was cancelled with error: {error}".format(error=e))
        future.cancel()
    except Exception as e:
        logger.error("failed to proccess message: error {error}".format(error=e))
        future.cancel()
    while True:
        pass


#scheduler.add_job(id="test", func=process_msg, trigger="date", run_date=datetime.now() + timedelta(minutes=1))
