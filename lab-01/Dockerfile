
# Stage 1: install application dependencies
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: production image
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create an unprivileged user and prepare writable data directory
RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app --no-create-home app \
    && mkdir -p /data \
    && chown -R app:app /app /data

# Copy only installed dependencies from the builder
COPY --from=builder /install/ /usr/local/

# Copy application code
COPY --chown=app:app app.py .

# Remove pip because it is not needed at runtime
RUN python -m pip uninstall -y pip \
    && rm -rf /usr/local/lib/python3.12/ensurepip

# Run as an unprivileged user
USER app

EXPOSE 8080

CMD ["python", "app.py"]
