FROM python:3.11-slim

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-interpreter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-interpreter/app ./app

ENV PORT=3003
EXPOSE 3003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3003"]
