# file-api

## Run Local

- `flask run` with debug off
- `python app.py` with debug
- `redis-server`
- `redis-cli`
- `celery -A app.tasks.file.tasks worker -l info --pool=solo -Q request`

## Run Server

- `flask run`
- `celery -A app.tasks.file.tasks worker -l info --pool=solo -Q request`


#### By Luis Santa