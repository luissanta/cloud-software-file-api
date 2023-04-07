from celery_app import celery
from app.helpers import compress_gz, compress_zip


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: str) -> tuple:
    # todo: obtener archivo de bucket
    # file = bucket
    # compress_gz(file)
    # compress_zip(file)
    # todo: enviar archivo a bucket
    return task_id, file_id


@celery.task(name='converter.response')
def converter_response(task_id, file_id):
    pass
