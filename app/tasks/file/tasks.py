from app.repositories.file.manager_repository import FileManager, NetworkFileStorage
from celery_app import celery
from app.models import File
from app.factories import CompressorFactory
from app.enums.file import ConverterStatusEnum

file_manager = FileManager(NetworkFileStorage())


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: int, new_format: str) -> None:
    status = ConverterStatusEnum.PROCESSED.value
    try:
        fetched_file = file_manager.get_file(File(id=file_id))

        compressor_factory = CompressorFactory()
        compresor_type = compressor_factory.get_compressor(new_format.upper())
        file_compress_data, file_compress_name = compresor_type.compress(
            fetched_file.original_data,
            fetched_file.original_name
        )
        # file_manager.save_file(new_format, File(
        #     id=file_id,
        #     compressed_data=file_compress_data,
        #     compressed_name=file_compress_name,
        #     temporal_name=fetched_file.temporal_name
        # ))

    except:
        status = ConverterStatusEnum.FAILED.value

    finally:
        args = (task_id, status)
        converter_response.apply_async(args=args, queue='response')


@celery.task(name='converter.response')
def converter_response(task_id: str, status: str) -> None:
    # This is a queue
    pass
