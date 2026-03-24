"""Minimal fake BizHawk connector used for protocol-level integration tests."""

from __future__ import annotations

import asyncio
import base64
import json
from dataclasses import dataclass, field


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


@dataclass
class FakeBizHawkConnector:
    system: str = "GBA"
    rom_hash: str = "fake-kirbyam-hash"
    script_version: int = 5
    host: str = "127.0.0.1"
    port: int = 0
    _server: asyncio.AbstractServer | None = field(init=False, default=None)
    _memory: dict[str, dict[int, int]] = field(init=False, default_factory=dict)
    request_log: list[dict[str, object]] = field(init=False, default_factory=list)

    def set_bytes(self, domain: str, address: int, data: bytes) -> None:
        bank = self._memory.setdefault(domain, {})
        for offset, value in enumerate(data):
            bank[address + offset] = value

    def get_bytes(self, domain: str, address: int, size: int) -> bytes:
        bank = self._memory.setdefault(domain, {})
        return bytes(bank.get(address + offset, 0) for offset in range(size))

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle_client, self.host, self.port)
        sockets = self._server.sockets or []
        if not sockets:
            raise RuntimeError("FakeBizHawkConnector failed to bind a listening socket")
        self.port = int(sockets[0].getsockname()[1])

    async def close(self) -> None:
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            while True:
                raw_line = await reader.readline()
                if not raw_line:
                    break

                line = raw_line.decode("utf-8").strip()
                if line == "VERSION":
                    writer.write(f"{self.script_version}\n".encode("utf-8"))
                    await writer.drain()
                    continue

                try:
                    req_list = json.loads(line)
                    if not isinstance(req_list, list):
                        raise ValueError("Request payload must be a JSON list")
                except Exception as exc:
                    writer.write(json.dumps([{"type": "ERROR", "err": f"invalid request: {exc}"}]).encode("utf-8") + b"\n")
                    await writer.drain()
                    continue

                responses: list[dict[str, object]] = []
                for req in req_list:
                    if isinstance(req, dict):
                        self.request_log.append(dict(req))
                        responses.append(self._handle_request(req))
                    else:
                        responses.append({"type": "ERROR", "err": "request entry must be an object"})

                writer.write(json.dumps(responses).encode("utf-8") + b"\n")
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    def _handle_request(self, req: dict[str, object]) -> dict[str, object]:
        req_type = str(req.get("type", ""))

        if req_type == "PING":
            return {"type": "PONG"}
        if req_type == "SYSTEM":
            return {"type": "SYSTEM_RESPONSE", "value": self.system}
        if req_type == "HASH":
            return {"type": "HASH_RESPONSE", "value": self.rom_hash}
        if req_type == "PREFERRED_CORES":
            return {"type": "PREFERRED_CORES_RESPONSE", "value": {}}
        if req_type == "LOCK":
            return {"type": "LOCKED"}
        if req_type == "UNLOCK":
            return {"type": "UNLOCKED"}
        if req_type == "DISPLAY_MESSAGE":
            return {"type": "DISPLAY_MESSAGE_RESPONSE"}
        if req_type == "SET_MESSAGE_INTERVAL":
            return {"type": "SET_MESSAGE_INTERVAL_RESPONSE"}

        if req_type == "MEMORY_SIZE":
            domain = str(req.get("domain", "ROM"))
            bank = self._memory.setdefault(domain, {})
            if bank:
                return {"type": "MEMORY_SIZE_RESPONSE", "value": max(bank.keys()) + 1}
            return {"type": "MEMORY_SIZE_RESPONSE", "value": 0x200000}

        if req_type == "READ":
            domain = str(req.get("domain", "ROM"))
            address = int(req.get("address", 0))
            size = int(req.get("size", 0))
            return {"type": "READ_RESPONSE", "value": _b64(self.get_bytes(domain, address, size))}

        if req_type == "WRITE":
            domain = str(req.get("domain", "ROM"))
            address = int(req.get("address", 0))
            value = base64.b64decode(str(req.get("value", "")))
            self.set_bytes(domain, address, value)
            return {"type": "WRITE_RESPONSE"}

        if req_type == "GUARD":
            domain = str(req.get("domain", "ROM"))
            address = int(req.get("address", 0))
            expected = base64.b64decode(str(req.get("expected_data", "")))
            actual = self.get_bytes(domain, address, len(expected))
            return {"type": "GUARD_RESPONSE", "value": actual == expected}

        return {"type": "ERROR", "err": f"Unsupported request type: {req_type}"}
