FROM python:3.11-slim

WORKDIR /app

COPY microservices/parallel-workers/app ./app

ENV PORT=9001
ENV WORKER_ROLE=quicksort

CMD ["python", "-m", "app.main"]
