import logging.config

from app.enums.file import ConverterStatusEnum
from app.factories import CompressorFactory
from app.repositories.file.bucket_file_storage import BucketFileStorage
from app.repositories.file.file_manager import FileManager
from ..models.sqlAlchemy.TaskFileModel import Task
from ..models.sqlAlchemy.declarative_base import Session

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


class FileConverter:
    file_manager = FileManager(BucketFileStorage())

    def converter_request(self, task_id: str, file_id: int, new_format: str) -> str:
        try:
            fetched_file_data, fetched_file_name = self.file_manager.get_file(file_id)
            compressor_factory = CompressorFactory()
            compresor_type = compressor_factory.get_compressor(new_format.upper())
            file_compress_data, file_compress_name = compresor_type.compress(
                fetched_file_data,
                fetched_file_name
            )
            self.file_manager.save_file(
                file_compress_name,
                file_compress_data,
                new_format
            )
            status = ConverterStatusEnum.PROCESSED.value
            return status

        except:
            status = ConverterStatusEnum.FAILED.value
            return status

        finally:
            self.update_status_task(task_id, status)

    def update_status_task(self, task_id, status):
        session = Session()
        try:
            task = session.query(Task).filter(Task.task_id == task_id).first()
            task.status = status
            session.add(task)
            session.commit()
        except Exception as e:
            logger.error("fail updating task: {task} with error: {error}".format(task=task_id, error=e))
        finally:
            session.close()
