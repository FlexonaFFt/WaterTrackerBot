# Dockerfile for Django
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY config /app/

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
