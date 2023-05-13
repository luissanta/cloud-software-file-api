import json
import logging.config
import os
from concurrent.futures._base import CancelledError
from concurrent.futures._base import TimeoutError

from flask_apscheduler import APScheduler
from google.cloud import pubsub_v1

from app import db
from app.models import Task
from app.repositories.file.file_manager import FileManager
from app.repositories.file.bucket_file_storage import BucketFileStorage
from app.factories import CompressorFactory
from app.enums.file import ConverterStatusEnum

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

file_manager = FileManager(BucketFileStorage())
scheduler = APScheduler()

publisher = pubsub_v1.PublisherClient()
subscriptor = os.getenv('GCP_SUBSCRIPTOR')
topic = os.getenv('GCP_TOPIC')


def callback(msg):
    try:
        data = json.loads(msg.data)
        converter_request(data["task_id"], data["url"], data["new_format"])
        msg.ack()
    except Exception as e:
        logger.error("error processing message: error {error}".format(error=e))


def converter_request(task_id: str, file_id: int, new_format: str) -> str:
    status = ConverterStatusEnum.PROCESSED.value
    try:
        fetched_file_data, fetched_file_name = file_manager.get_file(file_id)
        compressor_factory = CompressorFactory()
        compresor_type = compressor_factory.get_compressor(new_format.upper())
        file_compress_data, file_compress_name = compresor_type.compress(
            fetched_file_data,
            fetched_file_name
        )
        file_manager.save_file(
            file_compress_name,
            file_compress_data,
            new_format
        )

    except:
        status = ConverterStatusEnum.FAILED.value
    finally:

        return status


def process_msg():
    try:
        logger.info("running schedule task")
        with pubsub_v1.SubscriberClient() as subscriber:
            future = subscriber.subscribe(subscriptor, callback)
            future.result()
    except TimeoutError:
        logger.info("does not exist any message to process")
    except CancelledError as e:
        logger.error("message process was cancelled with error: {error}".format(error=e))
    except Exception as e:
        logger.error("failed to proccess message: error {error}".format(error=e))
        future.cancel()


scheduler.add_job(id="test", func=process_msg, trigger="interval", seconds=20, max_instances=1)
