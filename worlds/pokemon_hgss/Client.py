from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import colorama

from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)

from Utils import async_start

from .Items import GAME_NAME


EXPECTED_FORMAT_VERSION = 1


# -------------------------
# .aphgss file loading
# -------------------------

def load_aphgss_file(file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find .aphgss file: {file_path}")

    if file_path.suffix != ".aphgss":
        raise ValueError(
            f"Expected a .aphgss file, but got: {file_path.name}"
        )

    with file_path.open("r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    return data


def validate_aphgss_data(data: dict[str, Any]) -> None:
    format_version = data.get("format_version")

    if format_version != EXPECTED_FORMAT_VERSION:
        raise ValueError(
            "Unsupported .aphgss format version. "
            f"Expected {EXPECTED_FORMAT_VERSION}, got {format_version}."
        )

    required_fields = (
        "game",
        "player",
        "player_name",
        "options",
        "item_name_to_id",
        "location_name_to_id",
        "location_item_data",
    )

    missing_fields = [
        field_name
        for field_name in required_fields
        if field_name not in data
    ]

    if missing_fields:
        raise ValueError(
            "The .aphgss file is missing required fields: "
            f"{', '.join(missing_fields)}"
        )


def print_aphgss_summary(data: dict[str, Any]) -> None:
    location_item_data = data["location_item_data"]
    options = data["options"]

    normal_locations = [
        location_data
        for location_data in location_item_data
        if location_data["location_id"] is not None
    ]

    event_locations = [
        location_data
        for location_data in location_item_data
        if location_data["location_id"] is None
    ]

    print("Pokemon HGSS .aphgss file loaded successfully.")
    print(f"Game: {data['game']}")
    print(f"Player number: {data['player']}")
    print(f"Player name: {data['player_name']}")
    print(f"Goal option: {options['goal']}")
    print(
        "HM badge requirements: "
        f"{options['hm_badge_requirements']}"
    )
    print(f"Item IDs: {len(data['item_name_to_id'])}")
    print(f"Location IDs: {len(data['location_name_to_id'])}")
    print(f"Normal locations in output: {len(normal_locations)}")
    print(f"Event locations in output: {len(event_locations)}")

    print()
    print("First 5 location placements:")

    for location_data in location_item_data[:5]:
        print(
            "- "
            f"{location_data['location_name']} -> "
            f"{location_data['item_name']}"
        )


# -------------------------
# Archipelago client skeleton
# -------------------------

class PokemonHGSSCommandProcessor(ClientCommandProcessor):
    def _cmd_hgss(self) -> None:
        """Show basic Pokemon HGSS client status."""

        ctx = self.ctx

        self.output("Pokemon HGSS client status:")
        self.output(f"Game: {ctx.game}")
        self.output(f"Server address: {ctx.server_address or 'not connected'}")
        self.output(f"Authenticated slot: {ctx.auth or 'not authenticated'}")
        self.output(f"Received items: {len(ctx.items_received)}")

        if isinstance(ctx, PokemonHGSSContext):
            self.output(
                "Loaded .aphgss file: "
                f"{'yes' if ctx.aphgss_data else 'no'}"
            )
            self.output(
                "Received slot data: "
                f"{'yes' if ctx.slot_data else 'no'}"
            )


class PokemonHGSSContext(CommonContext):
    command_processor = PokemonHGSSCommandProcessor
    game = GAME_NAME

    # For this early client skeleton, receive all items the server sends for
    # this slot. We can adjust this later if HGSS needs different behaviour.
    items_handling = 0b111

    def __init__(
            self,
            server_address: str | None,
            password: str | None,
            aphgss_data: dict[str, Any] | None = None,
            test_check_name: str | None = None,
    ) -> None:
        super().__init__(server_address, password)

        self.aphgss_data = aphgss_data
        self.slot_data: dict[str, Any] = {}
        self.test_check_name = test_check_name
        self.test_check_sent = False

        if self.aphgss_data:
            self.auth = str(self.aphgss_data["player_name"])

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_location_id_by_name(self, location_name: str) -> int | None:
        location_name_to_id = {}

        if self.slot_data:
            location_name_to_id.update(
                self.slot_data.get("location_name_to_id", {})
            )

        if self.aphgss_data:
            location_name_to_id.update(
                self.aphgss_data.get("location_name_to_id", {})
            )

        location_id = location_name_to_id.get(location_name)

        if location_id is None:
            return None

        return int(location_id)

    async def send_test_location_check(self, location_name: str) -> None:
        location_id = self.get_location_id_by_name(location_name)

        if location_id is None:
            print(f"Could not find HGSS location: {location_name}")
            return

        self.locations_checked.add(location_id)

        await self.send_msgs(
            [
                {
                    "cmd": "LocationChecks",
                    "locations": [location_id],
                }
            ]
        )

        print(
            "Sent test location check: "
            f"{location_name} ({location_id})"
        )

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})

            print()
            print("Connected to Pokemon HeartGold SoulSilver slot.")

            if self.slot_data:
                print("Received HGSS slot data from server.")
                print(
                    "HM badge requirements: "
                    f"{self.slot_data.get('hm_badge_requirements')}"
                )
                print(f"Goal: {self.slot_data.get('goal')}")
                print(
                    "Known HGSS locations: "
                    f"{len(self.slot_data.get('location_name_to_id', {}))}"
                )
                print(
                    "Known HGSS items: "
                    f"{len(self.slot_data.get('item_name_to_id', {}))}"
                )

            if self.test_check_name and not self.test_check_sent:
                self.test_check_sent = True
                async_start(
                    self.send_test_location_check(self.test_check_name),
                    name="HGSS test location check",
                )

            else:
                print("No slot data was received.")

            print()

        if cmd == "ReceivedItems":
            print(
                "ReceivedItems packet received. "
                f"Total received items: {len(self.items_received)}"
            )


async def game_watcher(ctx: PokemonHGSSContext) -> None:
    """
    Placeholder watcher.

    Later this is where emulator memory reading will happen.
    For now, it simply keeps the client alive while connected.
    """

    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)


async def run_client(args) -> None:
    aphgss_data = None

    if args.aphgss:
        aphgss_data = load_aphgss_file(args.aphgss)
        validate_aphgss_data(aphgss_data)
        print_aphgss_summary(aphgss_data)

        logger.info(
            "Using player name from .aphgss file: "
            f"{aphgss_data['player_name']}"
        )

    ctx = PokemonHGSSContext(
        args.connect,
        args.password,
        aphgss_data,
        args.test_check,
    )

    if not args.connect:
        logger.info(
            "No server address supplied. "
            "Client skeleton loaded successfully."
        )
        logger.info(
            "To connect later, use something like: "
            "py -3.13 -m worlds.pokemon_hgss.Client --connect localhost:38281"
        )
        return

    ctx.server_task = asyncio.create_task(
        server_loop(ctx),
        name="server loop",
    )

    if gui_enabled:
        ctx.run_gui()

    ctx.run_cli()

    watcher_task = asyncio.create_task(
        game_watcher(ctx),
        name="PokemonHGSSGameWatcher",
    )

    try:
        await ctx.exit_event.wait()
    finally:
        ctx.server_address = None

        watcher_task.cancel()

        try:
            await watcher_task
        except asyncio.CancelledError:
            pass

        await ctx.shutdown()


def main() -> None:
    parser = get_base_parser(
        description="Pokemon HeartGold SoulSilver Archipelago Client"
    )

    parser.add_argument(
        "--aphgss",
        type=Path,
        default=None,
        help="Path to a generated PokemonHGSS_PlayerX.aphgss file.",
    )

    parser.add_argument(
        "--test-check",
        type=str,
        default=None,
        help=(
            "Development only: send one HGSS location check by name "
            "after connecting."
        ),
    )

    args, _ = parser.parse_known_args()

    colorama.init()

    try:
        asyncio.run(run_client(args))
    finally:
        colorama.deinit()


if __name__ == "__main__":
    main()