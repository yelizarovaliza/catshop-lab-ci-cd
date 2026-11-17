FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    COUNTER_FILE=/data/visits.txt

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
