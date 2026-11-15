import argparse
import asyncio
import dataclasses
import json

import ModuleUpdate

ModuleUpdate.requirements_files.add("requirements.txt")
ModuleUpdate.update()

import aioconsole
import picklerpc


async def ping(session: picklerpc.Session, _: argparse.Namespace):
    result = await session.request("ping")
    print(result)


async def send_console_cmd(session: picklerpc.Session, args: argparse.Namespace):
    cmd_text = " ".join(args.cmd_text)
    if not cmd_text:
        print("empty command?")
        return
    result = await session.request("send_console_cmd", cmd_text)
    print(result)


async def inventory(session: picklerpc.Session, args: argparse.Namespace):
    inv = await session.request("inventory", args.player)
    if args.json:
        print(json.dumps(dataclasses.asdict(inv), indent=2))
        return
    print(f"game: {inv.game}")
    for title, items in [
        ("start inventory", inv.start_inventory),
        ("received items", inv.received_items),
    ]:
        print(f"{title}:")
        print("\n".join(
            f"  {item.name} (from {item.sent_by}, at {item.location})" for item in items
        ))


async def console(session: picklerpc.Session, _: argparse.Namespace):
    session.register_handler("console_out", aioconsole.aprint)
    await session.request("subscribe")
    await asyncio.sleep(0)
    try:
        while True:
            line = await aioconsole.ainput("")
            if any(
                line.strip().startswith(prefix)
                for prefix in ["disconnect", "!disconnect", "/disconnect"]
            ):
                break
            await session.request("send_console_cmd", line)
    except (EOFError, asyncio.exceptions.CancelledError):
        pass


async def main(parser) -> None:
    args = parser.parse_args()
    reader, writer = await asyncio.open_unix_connection(args.socket)
    session = picklerpc.spawn_session(reader, writer)
    session.run_in_background(session.run_event_loop())
    await args.func(session, args)
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="AP MultiServer RPC client")
    parser.add_argument("socket", help="MultiServer RPC socket")
    subparsers = parser.add_subparsers(help="AP client admin", required=True)
    ping_parser = subparsers.add_parser("ping", help="ping")
    ping_parser.set_defaults(func=ping)
    send_console_cmd_parser = subparsers.add_parser(
        "send_command",
        help="send a console command to the multiserver",
        aliases=["send"],
    )
    send_console_cmd_parser.add_argument("cmd_text", nargs=argparse.REMAINDER)
    send_console_cmd_parser.set_defaults(func=send_console_cmd)
    inventory_parser = subparsers.add_parser(
        "inventory", help="list the items a player has received"
    )
    inventory_parser.add_argument("player", type=int, help="player slot number")
    inventory_parser.add_argument("--json", action="store_true", help="print as JSON")
    inventory_parser.set_defaults(func=inventory)
    console_parser = subparsers.add_parser(
        "console", help="connect to the running world's console"
    )
    console_parser.set_defaults(func=console)
    asyncio.run(main(parser))
