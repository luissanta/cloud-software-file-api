from celery_app import celery
from app.repositories.file import get_detail_by_id, update
from app.models import File
from app.factories import CompressorFactory


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: int, new_format: str) -> None:
    fetched_file = get_detail_by_id(File(id=file_id))

    compressor_factory = CompressorFactory()
    compresor_type = compressor_factory.compress_file(new_format.upper())
    file_compress_data, file_compress_name = compresor_type.compress(
        fetched_file.original_data,
        fetched_file.original_name
    )
    update(File(id=file_id, compressed_data=file_compress_data, compressed_name=file_compress_name))

    status = 'processed'

    args = (task_id, status)
    converter_response.apply_async(args=args, queue='response')


@celery.task(name='converter.response')
def converter_response(task_id: str, status: str) -> None:
    pass
