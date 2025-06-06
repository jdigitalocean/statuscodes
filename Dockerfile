FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8080

USER nobody

CMD ["gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:8080"]