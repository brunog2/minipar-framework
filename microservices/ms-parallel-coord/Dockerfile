FROM python:3.11-slim

WORKDIR /app

COPY microservices/ms-parallel-coord/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/ms-parallel-coord/app ./app

ENV PORT=3006
ENV WORKER_QUICKSORT_HOST=worker-quicksort
ENV WORKER_MATRIX_HOST=worker-matrix
ENV WORKER_FACTORIAL_HOST=worker-factorial

EXPOSE 3006

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3006"]
