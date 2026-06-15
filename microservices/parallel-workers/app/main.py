"""Worker socket server — executa programas MiniPar nos workers."""

from __future__ import annotations

import json
import os
import socket
from pathlib import Path

from minipar_core.lexer import Lexer
from minipar_core.parser import Parser
from minipar_core.translation.interpreter import Interpreter

ROLE = os.environ.get("WORKER_ROLE", "quicksort")
PORT = int(os.environ.get("PORT", "9001"))
SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"

ROLE_FILES = {
    "quicksort": "worker_quicksort.minipar",
    "matrix": "worker_matrix.minipar",
    "factorial": "worker_factorial.minipar",
}

MACHINE_LABELS = {
    "quicksort": "PC1",
    "matrix": "PC2",
    "factorial": "PC3",
}


def load_source() -> str:
    filename = ROLE_FILES.get(ROLE, f"worker_{ROLE}.minipar")
    path = SOURCES_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return 'class Main { void run() { println("worker ok"); } }'


def run_minipar() -> dict:
    source = load_source()
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    output = interp.execute(program)
    hostname = socket.gethostname()
    return {
        "role": ROLE,
        "machine": MACHINE_LABELS.get(ROLE, ROLE.upper()),
        "ip": hostname,
        "port": PORT,
        "data": output.strip() or f"MiniPar worker {ROLE} ok",
    }


def handle_client(conn: socket.socket) -> None:
    try:
        conn.recv(1024)
        payload = run_minipar()
        conn.sendall(json.dumps(payload, ensure_ascii=False).encode("utf-8") + b"\n")
    finally:
        conn.close()


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", PORT))
    sock.listen(5)
    print(f"Worker [{ROLE}] MiniPar listening on port {PORT}", flush=True)
    while True:
        conn, addr = sock.accept()
        print(f"Worker [{ROLE}] connection from {addr}", flush=True)
        handle_client(conn)


if __name__ == "__main__":
    main()
