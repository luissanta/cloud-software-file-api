broker_url = 'redis://local.redis:6379/0'
result_backend = 'redis://local.redis:6379/0'
task_serializer = 'json'
result_serializer = 'json'
imports = (
    'app.tasks.file.tasks'
)
