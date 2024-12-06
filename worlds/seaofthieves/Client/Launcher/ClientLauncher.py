from __future__ import annotations
import asyncio
from worlds.seaofthieves.Client.SotCustomClient import SOT_Context


async def main():
    ctx = SOT_Context()
    ctx.create_tasks()
    ctx.run_gui_and_cli()
    await ctx.application_exit()


def launch():
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
