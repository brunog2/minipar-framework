FROM python:3.11-slim

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-front-end/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-front-end/app ./app

ENV PORT=3001
EXPOSE 3001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
