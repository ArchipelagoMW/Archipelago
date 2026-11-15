import asyncio
from dataclasses import dataclass, field
import logging
from functools import partial

from typing import Callable

import picklerpc
import Utils
import MultiServer as ms
import NetUtils


def emit_console_output(session: picklerpc.Session, text: str):
    Utils.async_start(session.notification("console_out", text))


class RemoteConsoleLogger(logging.Handler):
    session: picklerpc.Session

    def __init__(self, session: picklerpc.Session):
        super().__init__()
        self.session = session

    async def send_text(self, text: str):
        await self.session.notification("console_out", text)

    def emit(self, record: logging.LogRecord):
        Utils.async_start(self.session.notification("console_out", self.format(record)))


def rpc(name: str):
    def wrap(f):
        f.rpc_name = name
        return f

    return wrap


@dataclass
class Item:
    name: str
    location: str
    sent_by: str

    @staticmethod
    def from_network_item(
        ctx: ms.Context, game: str, ni: NetUtils.NetworkItem
    ) -> "Item":
        name = ctx.item_names[game][ni.item]
        if ni.player == 0:
            location = "Server"
        else:
            location = ctx.location_names[ctx.slot_info[ni.player].game][ni.location]
        sent_by = ctx.player_names[0, ni.player] if ni.player else "<Archipelago>"
        return Item(name=name, location=location, sent_by=sent_by)


@dataclass
class Inventory:
    game: str
    start_inventory: list[Item]
    received_items: list[Item]

    @staticmethod
    def from_network_items(
        ctx: ms.Context,
        game: str,
        start_inventory: list[NetUtils.NetworkItem],
        received_items: list[NetUtils.NetworkItem],
    ) -> "Inventory":
        return Inventory(
            game=game,
            start_inventory=list(
                Item.from_network_item(ctx, game, ni) for ni in start_inventory
            ),
            received_items=list(
                Item.from_network_item(ctx, game, ni) for ni in received_items
            ),
        )


@dataclass
class Session:
    session: picklerpc.Session
    ctx: ms.Context
    exit_callbacks: list[Callable[[], None]] = field(default_factory=list)

    @rpc("ping")
    async def ping(self) -> str:
        return "pong"

    @rpc("send_console_cmd")
    async def send_console_cmd(self, cmd: str) -> str:
        self.ctx.commandprocessor(cmd)
        return "ok"

    @rpc("inventory")
    async def inventory(self, player: int) -> Inventory:
        start_inventory = ms.get_start_inventory(self.ctx, player, True)
        received_items = ms.get_received_items(self.ctx, 0, player, True)
        game = self.ctx.slot_info[player].game
        return Inventory.from_network_items(
            self.ctx, game, start_inventory, received_items
        )

    @rpc("subscribe")
    async def subscribe(self) -> None:
        handler = RemoteConsoleLogger(self.session)
        rootlogger = logging.getLogger()
        rootlogger.addHandler(handler)
        remote_output = self.ctx.commandprocessor.register_remote_output(
            partial(emit_console_output, self.session)
        )

        def disconnect():
            rootlogger.removeHandler(handler)
            self.ctx.commandprocessor.unregister_remote_output(remote_output)
            logging.info("remote console disconnected")

        self.exit_callbacks.append(disconnect)
        logging.info("remote console connected")


    async def run_event_loop(self):
        try:
            await self.session.run_event_loop()
        finally:
            while self.exit_callbacks:
                self.exit_callbacks.pop()()

    def __post_init__(self):
        for attr in dir(type(self)):
            name = getattr(getattr(type(self), attr), "rpc_name", None)
            if name is not None:
                self.session.register_handler(name, getattr(self, attr))


async def handle_session(
    ctx: ms.Context, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    session = Session(picklerpc.spawn_session(reader, writer), ctx)

    logging.info("picklerpc session started")

    await session.run_event_loop()
