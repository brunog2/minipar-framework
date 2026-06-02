FROM python:3.11-slim

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-semantic/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-semantic/app ./app

ENV PORT=3002
EXPOSE 3002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3002"]
