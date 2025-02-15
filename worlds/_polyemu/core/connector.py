from __future__ import annotations

import abc
from typing import Any, ClassVar


__all__ = [
    "AutoConnectorRegister", "Connector",
]


class AutoConnectorRegister(abc.ABCMeta):
    connector_types: ClassVar[dict[str, Connector]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoConnectorRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register request type
        if "name" in namespace:
            AutoConnectorRegister.connector_types[namespace["name"]] = new_class

        return new_class

    @staticmethod
    def get_connector(name: str) -> type[Connector]:
        try:
            return AutoConnectorRegister.connector_types[name]
        except KeyError:
            raise KeyError(f"Connector type not registered: {name}")


class Connector(abc.ABC, metaclass=AutoConnectorRegister):
    name: ClassVar[str]

    @abc.abstractmethod
    def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def connect(self) -> bool:
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        ...

    @abc.abstractmethod
    async def send_message(self, message: bytes) -> bytes:
        ...
