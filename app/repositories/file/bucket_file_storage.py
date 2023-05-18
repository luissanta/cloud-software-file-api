import logging

from ...models.sqlAlchemy.declarative_base import Session
from ...models.sqlAlchemy.TaskFileModel import File
from .i_File import IFile
import os
from google.cloud import storage

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

path = os.path.join(os.getcwd(), os.environ.get('GCP_PATH'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
storage_client = storage.Client(path)
bucket = storage_client.get_bucket(os.environ.get('GCP_BUCKET'))


class BucketFileStorage(IFile):
    def get(self, file_id) -> tuple:
        session = Session()
        try:
            fetched_file = session.query(File).filter(File.id == file_id).first()
            temp_original_name = fetched_file.temporal_name + "." + fetched_file.original_name.split('.')[1]
            blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_ORIGINAL') + '/' + temp_original_name)
            data = blob.download_as_bytes()
            session.commit()
            return data, temp_original_name
        except Exception as e:
            logger.error("fail getting file from bucket: {file} whit error: {error} ".format(file=file_id, error={e}))
            raise e
        finally:
            session.close()

    def save(self, file_name, file_data, new_format) -> None:
        blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_COMPRESSED') + '/' + file_name)
        blob.upload_from_string(file_data)
