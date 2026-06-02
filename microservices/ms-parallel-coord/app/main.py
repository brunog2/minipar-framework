"""Coordenador de paralelismo distribuído — menu central via sockets."""

from __future__ import annotations

import json
import os
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="ms-parallel-coord", version="0.1.0")

WORKER_QUICKSORT_HOST = os.environ.get("WORKER_QUICKSORT_HOST", "worker-quicksort")
WORKER_MATRIX_HOST = os.environ.get("WORKER_MATRIX_HOST", "worker-matrix")
WORKER_FACTORIAL_HOST = os.environ.get("WORKER_FACTORIAL_HOST", "worker-factorial")

DEFAULT_HOSTS = [
    {"role": "quicksort", "host": WORKER_QUICKSORT_HOST, "port": 9001},
    {"role": "matrix", "host": WORKER_MATRIX_HOST, "port": 9002},
    {"role": "factorial", "host": WORKER_FACTORIAL_HOST, "port": 9003},
]


class HostSpec(BaseModel):
    role: str
    host: str
    port: int


class CoordinateRequest(BaseModel):
    ast: dict | None = None
    symbolTable: dict | None = None
    executionMode: str = "DISTRIBUTED_SOCKETS"
    hosts: list[HostSpec] | None = None


class WorkerResult(BaseModel):
    role: str
    data: str
    machine: str | None = None
    error: str | None = None


class CoordinateResponse(BaseModel):
    output: str
    results: list[WorkerResult]


def dispatch_worker(host: str, port: int, role: str, timeout: float = 15.0) -> WorkerResult:
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.sendall(b"RUN\n")
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
            payload: dict[str, Any] = json.loads(data.decode("utf-8").strip())
            return WorkerResult(
                role=payload.get("role", role),
                data=str(payload.get("data", "")),
                machine=payload.get("machine"),
            )
    except Exception as exc:
        return WorkerResult(role=role, data=f"Erro ao contactar {host}:{port}", error=str(exc))


@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-parallel-coord"}


@app.post("/coordinate", response_model=CoordinateResponse)
def coordinate(body: CoordinateRequest):
    hosts = body.hosts or [HostSpec(**h) for h in DEFAULT_HOSTS]
    results: list[WorkerResult] = []

    with ThreadPoolExecutor(max_workers=len(hosts)) as pool:
        futures = {
            pool.submit(dispatch_worker, h.host, h.port, h.role): h.role for h in hosts
        }
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda r: {"quicksort": 0, "matrix": 1, "factorial": 2}.get(r.role, 99))

    lines = [
        "=== Menu Coordenador — Paralelismo Real (3 Máquinas) ===",
        "Threads como processos independentes · comunicação via sockets TCP",
        "",
    ]
    labels = {
        "quicksort": "PC1 — QuickSort",
        "matrix": "PC2 — Multiplicação de Matrizes",
        "factorial": "PC3 — Fatorial",
    }
    for item in results:
        label = labels.get(item.role, item.role.upper())
        if item.error:
            lines.append(f"[{label}] ERRO: {item.error}")
        else:
            lines.append(f"[{label}] {item.data}")

    return CoordinateResponse(output="\n".join(lines), results=results)
