FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-codegen-c/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-codegen-c/app ./app

ENV PORT=3004
EXPOSE 3004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3004"]
