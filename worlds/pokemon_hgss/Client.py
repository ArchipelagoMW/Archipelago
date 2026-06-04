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
from .LocationTracker import LocationTracker
from .ReceivedItemTracker import ReceivedItemTracker
from .GameInterface import SimulatedHGSSInterface
from .GameChecks import get_event_key_for_location_name, get_location_name_for_event_key


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
# Archipelago client
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
            self.output(
                "Tracked checked locations: "
                f"{len(ctx.location_tracker.checked_location_ids)}"
            )


class PokemonHGSSContext(CommonContext):
    command_processor = PokemonHGSSCommandProcessor
    game = GAME_NAME
    items_handling = 0b111

    def __init__(
        self,
        server_address: str | None,
        password: str | None,
        aphgss_data: dict[str, Any] | None = None,
        test_check_names: list[str] | None = None,
        simulated_location_names: list[str] | None = None,
        simulation_delay: float = 2.0,
    ) -> None:
        super().__init__(server_address, password)

        self.aphgss_data = aphgss_data
        self.slot_data: dict[str, Any] = {}
        self.location_tracker = LocationTracker.from_seed_data(
            slot_data=None,
            aphgss_data=self.aphgss_data,
        )

        self.received_item_tracker = ReceivedItemTracker.from_seed_data(
            slot_data=None,
            aphgss_data=self.aphgss_data,
        )

        self.test_check_names = test_check_names or []
        self.test_checks_sent = False

        self.game_interface = SimulatedHGSSInterface(
            simulated_event_keys=simulated_location_names or [],
            delay_seconds=simulation_delay,
        )

        self.watcher_seen_event_keys: set[str] = set()

        if self.aphgss_data:
            self.auth = str(self.aphgss_data["player_name"])

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def rebuild_seed_trackers(self) -> None:
        self.location_tracker = LocationTracker.from_seed_data(
            slot_data=self.slot_data,
            aphgss_data=self.aphgss_data,
        )

        self.location_tracker.update_checked_locations(self.locations_checked)

        self.received_item_tracker.update_seed_data(
            slot_data=self.slot_data,
            aphgss_data=self.aphgss_data,
        )

    async def send_location_check_by_name(self, location_name: str) -> None:
        location_id, should_send = self.location_tracker.mark_location_checked(
            location_name
        )

        if location_id is None:
            print(f"Could not find HGSS location: {location_name}")
            return

        if not should_send:
            print(
                "Skipping already checked HGSS location: "
                f"{location_name} ({location_id})"
            )
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
            "Sent HGSS location check: "
            f"{location_name} ({location_id})"
        )

    async def send_test_location_checks(self) -> None:
        for location_name in self.test_check_names:
            await self.send_location_check_by_name(location_name)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})

            self.rebuild_seed_trackers()

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
            else:
                print("No slot data was received.")

            print(
                "Already checked locations from server/context: "
                f"{len(self.location_tracker.checked_location_ids)}"
            )
            print()

            if self.test_check_names and not self.test_checks_sent:
                self.test_checks_sent = True
                async_start(
                    self.send_test_location_checks(),
                    name="HGSS test location checks",
                )

        if cmd == "ReceivedItems":
            new_item_names = self.received_item_tracker.get_new_received_items(
                self.items_received
            )

            print(
                "ReceivedItems packet received. "
                f"Total received items: {len(self.items_received)}"
            )

            for item_name in new_item_names:
                print(f"New HGSS item received: {item_name}")


async def game_watcher(ctx: PokemonHGSSContext) -> None:
    """
    Temporary game watcher.

    Later this will read HGSS emulator memory.
    For now, it reads simulated HGSS event keys from SimulatedHGSSInterface.
    """

    while not ctx.exit_event.is_set():
        if not ctx.slot_data:
            await asyncio.sleep(1)
            continue

        completed_event_keys = (
            ctx.game_interface.get_completed_event_keys()
        )

        for event_key in completed_event_keys:
            if event_key in ctx.watcher_seen_event_keys:
                continue

            ctx.watcher_seen_event_keys.add(event_key)

            location_name = get_location_name_for_event_key(event_key)

            if location_name is None:
                print(
                    "Watcher detected unknown HGSS event key: "
                    f"{event_key}"
                )
                continue

            print(
                "Watcher detected completed HGSS event: "
                f"{event_key}"
            )
            print(
                "Mapped event to AP location: "
                f"{location_name}"
            )

            await ctx.send_location_check_by_name(location_name)

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
        args.simulate_event,
        args.simulation_delay,
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
        action="append",
        default=[],
        help=(
            "Development only: send one HGSS location check by name "
            "after connecting. Can be used multiple times."
        ),
    )

    parser.add_argument(
        "--simulate-event",
        action="append",
        default=[],
        help=(
            "Development only: simulate an HGSS event key becoming completed. "
            "Can be used multiple times."
        ),
    )

    parser.add_argument(
        "--simulation-delay",
        type=float,
        default=2.0,
        help=(
            "Seconds between simulated completed locations. "
            "Only used with --simulate-check."
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