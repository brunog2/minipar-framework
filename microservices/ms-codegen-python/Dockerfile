FROM python:3.11-slim

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-codegen-python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-codegen-python/app ./app

ENV PORT=3008
EXPOSE 3008

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3008"]
