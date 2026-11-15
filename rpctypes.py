# Intentionally does not import anything from Archipelago. Clients will be able
# import this file as a standalone.

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    name: str
    location: str
    sent_by: str


@dataclass
class Inventory:
    game: str
    start_inventory: list[Item]
    received_items: list[Item]


@dataclass
class Player:
    slot: int
    name: str
    game: str
    finished: bool


@dataclass
class ServerInfo:
    port: int
    # the join password, not the admin `server_password`.
    password: Optional[str]
