FROM python:3.10

WORKDIR /app_file

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["celery", "-A", "app.tasks.file.tasks", "worker", "-l", "info", "--pool=solo", "-Q", "request"]