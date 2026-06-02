FROM python:3.11-slim

# rustc para compilar o código gerado (paridade com gcc no ms-codegen-c)
RUN apt-get update && apt-get install -y --no-install-recommends \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY packages/minipar-core /packages/minipar-core
RUN pip install --no-cache-dir /packages/minipar-core

COPY microservices/ms-codegen-rust/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-codegen-rust/app ./app

ENV PORT=3005
EXPOSE 3005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3005"]
