from celery import Celery

celery = Celery('celery_app')
celery.config_from_object('celery_config')
