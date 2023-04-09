from celery_app import celery
from app.repositories.file import get_detail_by_id, update
from app.models import File
from app.helpers.compressors.formats import GzCompressor, ZipCompressor
from app.data_transfer_objects.file import FileConverterDTO
from app.validators.file import validate_format_converter


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: int, new_format: str) -> None:
    validate_format_converter(FileConverterDTO(new_format=new_format))

    fetched_file = get_detail_by_id(File(id=file_id))
    # file_compress_data, file_compress_name = GzCompressor().compress(
    #     fetched_file.original_data,
    #     fetched_file.original_name
    # )
    file_compress_data, file_compress_name = ZipCompressor().compress(
        fetched_file.original_data,
        fetched_file.original_name
    )
    update(File(id=file_id, compressed_data=file_compress_data, compressed_name=file_compress_name))

    args = (task_id, 'processed')
    converter_response.apply_async(args=args, queue='response')


@celery.task(name='converter.response')
def converter_response(task_id: str, status: str) -> None:
    pass
