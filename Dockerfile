# "Building"
FROM python:3.9-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Testing
FROM builder AS testing

COPY main.py /build/
COPY tests/ /build/tests/

RUN cd /build && pytest tests/

# Deploy
FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY main.py /app/

RUN adduser --disabled-password --gecos "" appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

CMD ["python", "main.py"]
