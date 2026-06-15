FROM python:3.11-slim

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/parallel-workers/app ./app
COPY microservices/parallel-workers/sources ./sources

ENV PORT=9001
ENV WORKER_ROLE=quicksort

CMD ["python", "-m", "app.main"]
