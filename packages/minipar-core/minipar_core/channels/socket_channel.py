"""Broker e clientes de canal MiniPar — comunicação somente via sockets TCP."""

from __future__ import annotations

import json
import multiprocessing
import socket
import threading
from typing import Any, Dict, Optional

_BROKER: Optional["ChannelBroker"] = None
_BROKER_LOCK = threading.Lock()


def _frame_message(payload: dict) -> bytes:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return f"MSG {len(body)}\n".encode("ascii") + body


def _read_message(sock: socket.socket) -> dict:
    header = b""
    while b"\n" not in header:
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Channel broker connection closed")
        header += chunk
    line = header.decode("ascii").strip()
    if not line.startswith("MSG "):
        raise ValueError(f"Invalid channel frame: {line!r}")
    length = int(line.split()[1])
    body = b""
    while len(body) < length:
        chunk = sock.recv(length - len(body))
        if not chunk:
            raise ConnectionError("Channel broker truncated message")
        body += chunk
    return json.loads(body.decode("utf-8"))


def _broker_main(host: str, port: int, authkey: bytes) -> None:
    """Processo do broker — filas nomeadas acessíveis só via TCP."""
    from multiprocessing.managers import BaseManager

    class QueueManager(BaseManager):
        pass

    queues: Dict[str, list] = {}

    class BrokerAPI:
        def register_channel(self, name: str, channel_type: str) -> None:
            if name not in queues:
                queues[name] = []

        def send(self, name: str, value: Any) -> None:
            if name not in queues:
                queues[name] = []
            queues[name].append(value)

        def receive(self, name: str, timeout: float = 120.0) -> Any:
            import time

            deadline = time.time() + timeout
            while time.time() < deadline:
                if name in queues and queues[name]:
                    return queues[name].pop(0)
                time.sleep(0.01)
            raise TimeoutError(f"Channel receive timeout: {name}")

    QueueManager.register("api", callable=BrokerAPI)
    manager = QueueManager(address=(host, port), authkey=authkey)
    server = manager.get_server()
    server.serve_forever()


class ChannelBroker:
    """Broker local para canais s_channel/c_channel (IPC via socket)."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self._authkey = b"minipar-channel-broker"
        self._process: Optional[multiprocessing.Process] = None
        self._api = None

    def start(self) -> tuple[str, int]:
        if self._process and self._process.is_alive():
            return self.host, self.port

        from multiprocessing.managers import BaseManager

        class QueueManager(BaseManager):
            pass

        class BrokerAPI:
            def __init__(self):
                self._queues: Dict[str, list] = {}

            def register_channel(self, name: str, channel_type: str) -> None:
                self._queues.setdefault(name, [])

            def send(self, name: str, value: Any) -> None:
                self._queues.setdefault(name, []).append(value)

            def receive(self, name: str, timeout: float = 120.0) -> Any:
                import time

                deadline = time.time() + timeout
                while time.time() < deadline:
                    q = self._queues.setdefault(name, [])
                    if q:
                        return q.pop(0)
                    time.sleep(0.01)
                raise TimeoutError(f"Channel receive timeout: {name}")

        QueueManager.register("api", BrokerAPI)
        manager = QueueManager(address=(self.host, self.port), authkey=self._authkey)
        manager.start()
        self._api = manager.api()
        self.port = manager.address[1]
        self.host = manager.address[0]
        return self.host, self.port

    def register(self, name: str, channel_type: str) -> None:
        if self._api is None:
            self.start()
        self._api.register_channel(name, channel_type)

    def send(self, name: str, value: Any) -> None:
        if self._api is None:
            self.start()
        self._api.send(name, value)

    def receive(self, name: str, timeout: float = 120.0) -> Any:
        if self._api is None:
            self.start()
        return self._api.receive(name, timeout=timeout)


def get_or_start_broker() -> ChannelBroker:
    global _BROKER
    with _BROKER_LOCK:
        if _BROKER is None:
            _BROKER = ChannelBroker()
            _BROKER.start()
        return _BROKER


class SocketChannelClient:
    """Cliente de canal — todas as operações via conexão ao broker (socket)."""

    def __init__(self, broker_host: str, broker_port: int, channel_name: str):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.channel_name = channel_name

    def send(self, value: Any) -> None:
        broker = get_or_start_broker()
        if broker.host == self.broker_host and broker.port == self.broker_port:
            broker.send(self.channel_name, value)
            return
        with socket.create_connection(
            (self.broker_host, self.broker_port), timeout=30
        ) as sock:
            sock.sendall(
                _frame_message(
                    {"op": "send", "channel": self.channel_name, "value": value}
                )
            )

    def receive(self, timeout: float = 120.0) -> Any:
        broker = get_or_start_broker()
        if broker.host == self.broker_host and broker.port == self.broker_port:
            return broker.receive(self.channel_name, timeout=timeout)
        with socket.create_connection(
            (self.broker_host, self.broker_port), timeout=30
        ) as sock:
            sock.sendall(
                _frame_message(
                    {"op": "receive", "channel": self.channel_name, "timeout": timeout}
                )
            )
            return _read_message(sock).get("value")


class RemoteWorkerChannel:
    """c_channel(host, port) — comunicação com worker MiniPar via socket TCP."""

    def __init__(self, host: str, port: int, role: str = "worker"):
        self.host = host
        self.port = int(port)
        self.role = role

    def run_remote(self) -> dict:
        with socket.create_connection((self.host, self.port), timeout=30) as sock:
            sock.sendall(b"RUN\n")
            data = b""
            while not data.endswith(b"\n"):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
        return json.loads(data.decode("utf-8").strip())

    def send(self, value: Any) -> None:
        raise RuntimeError("RemoteWorkerChannel does not support send; use receive()")

    def receive(self, timeout: float = 120.0) -> Any:
        payload = self.run_remote()
        ip = payload.get("ip", self.host)
        port = payload.get("port", self.port)
        machine = payload.get("machine", "")
        role = payload.get("role", self.role)
        data = payload.get("data", "")
        return f"[{machine} {ip}:{port} {role}] {data}"
