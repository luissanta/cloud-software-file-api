from app.repositories.file.file_manager import FileManager
from app.repositories.file.bucket_file_storage import BucketFileStorage
from celery_app import celery
from app.models import File
from app.factories import CompressorFactory
from app.enums.file import ConverterStatusEnum
from app.repositories.file import get_detail_by_id

file_manager = FileManager(BucketFileStorage())


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: int, new_format: str) -> None:
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
        args = (task_id, status)
        converter_response.apply_async(args=args, queue='response')


@celery.task(name='converter.response')
def converter_response(task_id: str, status: str) -> None:
    # This is a queue
    pass
