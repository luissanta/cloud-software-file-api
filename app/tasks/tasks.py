from celery_app import celery


@celery.task(name='converter.request')
def converter_request(message, hash) -> None:
    pass
