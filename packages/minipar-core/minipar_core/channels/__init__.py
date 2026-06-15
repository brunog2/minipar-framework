"""Canais de comunicação MiniPar — IPC exclusivamente via sockets TCP."""

from minipar_core.channels.socket_channel import (
    ChannelBroker,
    RemoteWorkerChannel,
    SocketChannelClient,
    get_or_start_broker,
)

__all__ = [
    "ChannelBroker",
    "RemoteWorkerChannel",
    "SocketChannelClient",
    "get_or_start_broker",
]
