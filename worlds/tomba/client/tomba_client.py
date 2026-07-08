import asyncio
import sys
from argparse import Namespace

from CommonClient import (
    CommonContext,
    server_loop,
)
from Utils import gui_enabled

from .. import constants


class TombaContext(CommonContext):
    game = constants.GAME

    client_loop: asyncio.Task[None]

    def __init__(
        self,
        server_address: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(server_address, password)

    async def apquest_loop(self) -> None:
        pass


async def main(args: Namespace) -> None:
    if not gui_enabled:
        raise RuntimeError("Tomba! cannot be played without gui.")

    ctx = TombaContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    ctx.run_gui()
    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(
        ctx.apquest_loop(), name="Client Loop"
    )

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args: str) -> None:
    from .launch import launch_tomba_client

    launch_tomba_client(*args)


if __name__ == "__main__":
    launch(*sys.argv[1:])
