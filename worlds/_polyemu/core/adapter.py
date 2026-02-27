from __future__ import annotations

import abc
from typing import Any, ClassVar


__all__ = [
    "AutoAdapterRegister", "Adapter",
]


class AutoAdapterRegister(abc.ABCMeta):
    adapter_types: ClassVar[dict[str, Adapter]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoAdapterRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register request type
        if "name" in namespace:
            AutoAdapterRegister.adapter_types[namespace["name"]] = new_class

        return new_class

    @staticmethod
    def get_adapter(name: str) -> type[Adapter]:
        try:
            return AutoAdapterRegister.adapter_types[name]
        except KeyError:
            raise KeyError(f"Adapter type not registered: {name}")


class Adapter(abc.ABC, metaclass=AutoAdapterRegister):
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
