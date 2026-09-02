FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN mkdir -p /data

ENV RESOLVEAI_DB_PATH=/data/resolveai.db
ENV RESOLVEAI_CORS_ORIGINS=http://localhost:3000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
