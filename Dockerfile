FROM python:3.10

WORKDIR /app_file

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5003", "-w", "1", "--threads", "1", "wsgi:app"]