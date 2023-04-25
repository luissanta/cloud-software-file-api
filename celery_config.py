import os
from dotenv import load_dotenv

load_dotenv()

broker_url = 'redis://' + os.environ.get('REDIS_HOST') + ':' + os.environ.get('REDIS_PORT') + '/0'
result_backend = 'redis://' + os.environ.get('REDIS_HOST') + ':' + os.environ.get('REDIS_PORT') + '/0'
task_serializer = 'json'
result_serializer = 'json'
imports = (
    'app.tasks.file.tasks'
)
