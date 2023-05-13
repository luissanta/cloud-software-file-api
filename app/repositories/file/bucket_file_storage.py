from ...models.sqlAlchemy.declarative_base import Session
from ...models.sqlAlchemy.TaskFileModel import File
from .i_File import IFile
import os
from google.cloud import storage

path = os.path.join(os.getcwd(), os.environ.get('GCP_PATH'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
storage_client = storage.Client(path)
bucket = storage_client.get_bucket(os.environ.get('GCP_BUCKET'))


class BucketFileStorage(IFile):
    def get(self, file_id) -> tuple:
        session = Session()
        fetched_file = session.query(File).filter(File.id == file_id).first()
        #fetched_file = File.query.get_or_404(file_id)
        temp_original_name = fetched_file.temporal_name + "." + fetched_file.original_name.split('.')[1]
        blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_ORIGINAL') + '/' + temp_original_name)
        data = blob.download_as_bytes()
        return data, temp_original_name

    def save(self, file_name, file_data, new_format) -> None:
        blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_COMPRESSED') + '/' + file_name)
        blob.upload_from_string(file_data)
