from celery_app import celery
from app.repositories.file import get_detail_by_id, update
from app.models import File
from app.helpers import compress_to_gz


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: str) -> None:
    fetched_file = get_detail_by_id(File(id=file_id))
    file_compress_data, file_compress_name = compress_to_gz(fetched_file.original_data, fetched_file.original_name)
    update(File(id=file_id, compressed_data=file_compress_data, compressed_name=file_compress_name))
    args = (task_id, file_id,)
    converter_response.apply_async(args=args, queue='request')


@celery.task(name='converter.response')
def converter_response(task_id, file_id) -> None:
    pass
