from celery_app import celery


@celery.task(name='converter.request')
def converter_request(filename: str) -> None:
    print(filename)
    pass
