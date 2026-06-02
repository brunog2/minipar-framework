"""Worker socket server — processo independente para teste de 3 máquinas."""

from __future__ import annotations

import json
import os
import socket


ROLE = os.environ.get("WORKER_ROLE", "quicksort")
PORT = int(os.environ.get("PORT", "9001"))


def run_quicksort() -> dict:
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = sorted(arr)
    return {
        "role": "quicksort",
        "machine": "PC1",
        "data": f"QuickSort: {arr} -> {sorted_arr}",
    }


def run_matrix() -> dict:
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result[i][j] += a[i][k] * b[k][j]
    return {
        "role": "matrix",
        "machine": "PC2",
        "data": f"Matriz 2x2: A={a} x B={b} = {result}",
    }


def run_factorial() -> dict:
    n = 10
    acc = 1
    for i in range(2, n + 1):
        acc *= i
    return {
        "role": "factorial",
        "machine": "PC3",
        "data": f"Fatorial({n}) = {acc}",
    }


HANDLERS = {
    "quicksort": run_quicksort,
    "matrix": run_matrix,
    "factorial": run_factorial,
}


def handle_client(conn: socket.socket) -> None:
    try:
        conn.recv(1024)
        handler = HANDLERS.get(ROLE)
        if not handler:
            payload = {"role": ROLE, "data": f"Unknown worker role: {ROLE}"}
        else:
            payload = handler()
        conn.sendall(json.dumps(payload).encode("utf-8") + b"\n")
    finally:
        conn.close()


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", PORT))
    sock.listen(5)
    print(f"Worker [{ROLE}] listening on port {PORT}", flush=True)
    while True:
        conn, addr = sock.accept()
        print(f"Worker [{ROLE}] connection from {addr}", flush=True)
        handle_client(conn)


if __name__ == "__main__":
    main()
