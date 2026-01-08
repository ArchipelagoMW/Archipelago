import asyncio
import collections

import CommonClient
import NetUtils
import Utils

from typing import Any, Dict, List, Optional, Set

from BaseClasses import ItemClassification

from .data.item_data import KeymastersKeepItemData
from .data.location_data import KeymastersKeepLocationData
from .data.mapping_data import region_to_unlock_location_and_item

from .data_funcs import item_names_to_id, location_names_to_id, id_to_items, id_to_item_data, id_to_location_data

from .enums import (
    KeymastersKeepGoals,
    KeymastersKeepItems,
    KeymastersKeepRegions,
    KeymastersKeepShops,
    KeymastersKeepShopkeepers,
    KeymastersKeepTags,
)


class KeymastersKeepCommandProcessor(CommonClient.ClientCommandProcessor):
    pass


class KeymastersKeepContext(CommonClient.CommonContext):
    tags: Set[str] = {"AP"}
    game: str = "Keymaster's Keep"
    command_processor: CommonClient.ClientCommandProcessor = KeymastersKeepCommandProcessor
    items_handling: int = 0b111
    want_slot_data: bool = True

    item_name_to_id: Dict[str, int] = item_names_to_id()
    location_name_to_id: Dict[str, int] = location_names_to_id()

    id_to_items: Dict[int, KeymastersKeepItems] = id_to_items()
    id_to_item_data: Dict[int, KeymastersKeepItemData] = id_to_item_data()
    id_to_location_data: Dict[int, KeymastersKeepLocationData] = id_to_location_data()

    area_game_optional_constraints: Dict[str, List[str]]
    area_games: Dict[str, str]
    area_trial_game_objectives: Dict[str, str]
    area_trials: Dict[KeymastersKeepRegions, List[KeymastersKeepLocationData]]
    area_trials_maximum: int
    area_trials_minimum: int
    artifacts_of_resolve_required: int
    artifacts_of_resolve_total: int
    completed_locations_queue: collections.deque
    game_medley_mode: bool
    game_medley_percentage_chance: int
    goal: KeymastersKeepGoals
    goal_completed: bool
    goal_game: str
    goal_game_optional_constraints: List[str]
    goal_trial_game_objective: str
    hint_creation_queue: collections.deque
    hints_reveal_objectives: bool
    include_adult_only_or_unrated_games: bool
    include_difficult_objectives: bool
    include_modern_console_games: bool
    include_time_consuming_objectives: bool
    location_ids_checked: Set[int]
    lock_combinations: Dict[KeymastersKeepRegions, Optional[List[KeymastersKeepItems]]]
    lock_magic_keys_maximum: int
    lock_magic_keys_minimum: int
    magic_keys_required: int
    magic_keys_total: int
    selected_magic_keys: List[KeymastersKeepItems]
    shop_data: Dict[str, Dict[str, Any]]
    shop_hints: bool
    shop_items_minimum: int
    shop_items_maximum: int
    shop_items_progression_percentage_chance: int
    shops: bool
    shops_percentage_chance: int
    unlocked_areas: int
    used_magic_keys: List[KeymastersKeepItems]

    game_state: Dict[str, Any]
    is_game_state_initialized: bool

    controller_task: Optional[asyncio.Task]

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)

        self.game_state = dict()
        self.is_game_state_initialized = False

        self.completed_locations_queue = collections.deque()
        self.hint_creation_queue = collections.deque()

        self.goal_completed = False

        self.controller_task = None

    def run_gui(self) -> None:
        from .client_gui.client_gui import KeymastersKeepManager

        self.ui: KeymastersKeepManager = KeymastersKeepManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game_state = dict()
        self.is_game_state_initialized = False

        self.completed_locations_queue = collections.deque()
        self.hint_creation_queue = collections.deque()

        self.goal_completed = False

        self.ui.update_tabs()

        self.items_received = []
        self.locations_info = {}

        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, _args: Any) -> None:
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

            # Slot Data
            self.area_game_optional_constraints = _args["slot_data"]["area_game_optional_constraints"]
            self.area_games = _args["slot_data"]["area_games"]
            self.area_trial_game_objectives = _args["slot_data"]["area_trial_game_objectives"]

            self.area_trials = dict()

            area: str
            trials: List[str]
            for area, trials in _args["slot_data"]["area_trials"].items():
                trial: str
                self.area_trials[KeymastersKeepRegions(area)] = [
                    self.id_to_location_data[self.location_name_to_id[trial]] for trial in trials
                ]

            self.area_trials_maximum = _args["slot_data"]["area_trials_maximum"]
            self.area_trials_minimum = _args["slot_data"]["area_trials_minimum"]
            self.artifacts_of_resolve_required = _args["slot_data"]["artifacts_of_resolve_required"]
            self.artifacts_of_resolve_total = _args["slot_data"]["artifacts_of_resolve_total"]
            self.game_medley_mode = _args["slot_data"]["game_medley_mode"]
            self.game_medley_percentage_chance = _args["slot_data"]["game_medley_percentage_chance"]
            self.goal = KeymastersKeepGoals(_args["slot_data"]["goal"])
            self.goal_game = _args["slot_data"]["goal_game"]
            self.goal_game_optional_constraints = _args["slot_data"]["goal_game_optional_constraints"]
            self.goal_trial_game_objective = _args["slot_data"]["goal_trial_game_objective"]
            self.hints_reveal_objectives = _args["slot_data"]["hints_reveal_objectives"]
            self.include_adult_only_or_unrated_games = _args["slot_data"]["include_adult_only_or_unrated_games"]
            self.include_difficult_objectives = _args["slot_data"]["include_difficult_objectives"]
            self.include_modern_console_games = _args["slot_data"]["include_modern_console_games"]
            self.include_time_consuming_objectives = _args["slot_data"]["include_time_consuming_objectives"]

            self.lock_combinations = dict()

            area: str
            lock_combinations: Optional[List[str]]
            for area, lock_combinations in _args["slot_data"]["lock_combinations"].items():
                if lock_combinations is None:
                    self.lock_combinations[KeymastersKeepRegions(area)] = None
                    continue

                self.lock_combinations[KeymastersKeepRegions(area)] = [
                    KeymastersKeepItems(lock) for lock in lock_combinations
                ]

            self.lock_magic_keys_maximum = _args["slot_data"]["lock_magic_keys_maximum"]
            self.lock_magic_keys_minimum = _args["slot_data"]["lock_magic_keys_minimum"]
            self.magic_keys_required = _args["slot_data"]["magic_keys_required"]
            self.magic_keys_total = _args["slot_data"]["magic_keys_total"]

            self.selected_magic_keys = [KeymastersKeepItems(key) for key in _args["slot_data"]["selected_magic_keys"]]

            self.shop_data = dict()

            if "shop_data" in _args["slot_data"]:
                area: str
                data: Dict[str, Any]
                for area, data in _args["slot_data"]["shop_data"].items():
                    self.shop_data[KeymastersKeepRegions(area)] = {
                        "shop": KeymastersKeepShops(data["shop"]),
                        "shopkeeper": KeymastersKeepShopkeepers(data["shopkeeper"]),
                        "shop_items": dict(),
                    }

                    location_name: str
                    item_data: Any
                    for location_name, item_data in data["shop_items"].items():
                        self.shop_data[KeymastersKeepRegions(area)]["shop_items"][location_name] = {
                            "location_data": self.id_to_location_data[item_data["archipelago_id"]],
                            "relic": KeymastersKeepItems(item_data["relic"]["name"]),
                            "relic_data": self.id_to_item_data[item_data["relic"]["archipelago_id"]],
                            "item": {
                                "name": item_data["item"]["name"],
                                "classification": ItemClassification(item_data["item"]["classification"]),
                                "player": {
                                    "name": self.player_names[item_data["item"]["player"]],
                                    "game": self.slot_info[item_data["item"]["player"]].game,
                                }
                            }
                        }

            self.shop_hints = _args["slot_data"].get("shop_hints", False)
            self.shop_items_minimum = _args["slot_data"].get("shop_items_minimum", 2)
            self.shop_items_maximum = _args["slot_data"].get("shop_items_maximum", 5)

            self.shop_items_progression_percentage_chance = _args["slot_data"].get(
                "shop_items_progression_percentage_chance",
                100
            )

            self.shops = _args["slot_data"].get("shops", False)
            self.shops_percentage_chance = _args["slot_data"].get("shops_percentage_chance", 20)

            self.unlocked_areas = _args["slot_data"]["unlocked_areas"]
            self.used_magic_keys = [KeymastersKeepItems(key) for key in _args["slot_data"]["used_magic_keys"]]

            # Location IDs Checked
            self.location_ids_checked = set(_args["checked_locations"])

            # Game State
            self.game_state = self._initialize_game_state()
            self.is_game_state_initialized = True

            self._update_game_state()

            # Update UI Tabs
            self.ui.update_tabs()
        elif cmd == "ReceivedItems":
            self._update_game_state()
            self.ui.update_tabs()
        elif cmd == "RoomUpdate":
            # To handle collect / coop
            if "checked_locations" in _args:
                self.location_ids_checked |= set(_args["checked_locations"])

                self._update_game_state()
                self.ui.update_tabs()

    def create_hints_for(self, location_ids: List[int]) -> None:
        if self.shops and self.shop_hints:
            location_id: int
            for location_id in location_ids:
                self.hint_creation_queue.append(location_id)

    def complete_location(self, location_id: int) -> None:
        self.completed_locations_queue.append(location_id)

        self.location_ids_checked.add(location_id)

        self._update_game_state()
        self.ui.update_tabs()

    def complete_goal(self) -> None:
        self.goal_completed = True

        self._update_game_state()
        self.ui.update_tabs()

    async def controller(self):
        while not self.exit_event.is_set():
            await asyncio.sleep(0.1)

            # Network Operations
            if self.server and self.slot:
                # Create Hints
                hints_to_create: List[int] = list()

                while len(self.hint_creation_queue) > 0:
                    location_id: int = self.hint_creation_queue.popleft()
                    hints_to_create.append(location_id)

                if hints_to_create:
                    await self.send_msgs([
                        {
                            "cmd": "LocationScouts",
                            "locations": hints_to_create,
                            "create_as_hint": 2,
                        }
                    ])

                # Send Checked Locations
                checked_location_ids: List[int] = list()

                while len(self.completed_locations_queue) > 0:
                    location_id: int = self.completed_locations_queue.popleft()
                    checked_location_ids.append(location_id)

                if checked_location_ids:
                    await self.send_msgs([
                        {
                            "cmd": "LocationChecks",
                            "locations": checked_location_ids
                        }
                    ])

                # Check for Goal Completion
                if self.goal_completed:
                    await self.send_msgs([
                        {
                            "cmd": "StatusUpdate",
                            "status": CommonClient.ClientStatus.CLIENT_GOAL
                        }
                    ])

    def _initialize_game_state(self) -> Dict[str, Any]:
        game_state: Dict[str, Any] = {
            "areas_locked_by": dict(),
            "areas_unlocked": dict(),
            "artifact_of_resolve_received": 0,
            "goal_can_claim_victory": False,
            "goal_challenge_chamber_unlocked": False,
            "magic_keys": dict(),
            "magic_keys_received": 0,
            "relics": dict(),
            "shop_items_purchased": dict(),
            "trials_available": dict(),
            "trial_count": 0,
            "trial_count_total": 0,
        }

        # Magic Keys
        key_labels: List[str] = list()

        key: KeymastersKeepItems
        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            for key in self.used_magic_keys:
                key_labels.append(key.value)
        elif self.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
            for key in self.selected_magic_keys:
                key_labels.append(key.value)

        key_labels = sorted(key_labels)

        key_label: str
        for key_label in key_labels:
            key: KeymastersKeepItems = KeymastersKeepItems(key_label)
            game_state["magic_keys"][key] = False

        # Relics
        if self.shops:
            relics: List[KeymastersKeepItems] = [
                item for item in list(KeymastersKeepItems) if item.name.startswith("RELIC_")
            ]

            relic: KeymastersKeepItems
            for relic in relics:
                game_state["relics"][relic] = False

        # Areas
        area: KeymastersKeepRegions
        keys: Optional[List[KeymastersKeepItems]]
        for area, keys in self.lock_combinations.items():
            game_state["areas_locked_by"][area] = keys
            game_state["areas_unlocked"][area] = False

        # Trials Available
        area: KeymastersKeepRegions
        trials: List[KeymastersKeepLocationData]
        for area, trials in self.area_trials.items():
            game_state["trials_available"][area] = list()

            for _ in trials:
                game_state["trial_count_total"] += 1

        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            game_state["trial_count_total"] += 1

        # Shop Items Purchased
        if self.shops:
            data: Dict[str, Any]
            for data in self.shop_data.values():
                shop: KeymastersKeepShops = data["shop"]
                game_state["shop_items_purchased"][shop] = list()

        return game_state

    def _update_game_state(self) -> None:
        artifact_of_resolve_count: int = 0
        door_unlocks_received: List[KeymastersKeepItems] = list()
        magic_key_count: int = 0
        magic_keys_received: List[KeymastersKeepItems] = list()
        relics_received: List[KeymastersKeepItems] = list()
        trial_count: int = 0

        network_item: NetUtils.NetworkItem
        for network_item in self.items_received:
            item: KeymastersKeepItems = self.id_to_items[network_item.item]
            data: KeymastersKeepItemData = self.id_to_item_data[network_item.item]

            # Magic Keys
            if KeymastersKeepTags.KEYS in data.tags:
                magic_keys_received.append(item)
                magic_key_count += 1
            # Relics
            elif KeymastersKeepTags.RELICS in data.tags:
                relics_received.append(item)
            # Goal Challenge Chamber Unlock
            elif item == KeymastersKeepItems.UNLOCK_THE_KEYMASTERS_CHALLENGE_CHAMBER:
                self.game_state["goal_challenge_chamber_unlocked"] = True
            # Unlocks
            elif KeymastersKeepTags.DOOR_UNLOCKS in data.tags:
                door_unlocks_received.append(item)
            # Artifacts of Resolve
            elif item == KeymastersKeepItems.ARTIFACT_OF_RESOLVE:
                artifact_of_resolve_count += 1
            # Goal Can Claim Victory - Keymaster's Challenge
            elif item == KeymastersKeepItems.KEYMASTERS_KEEP_CHALLENGE_COMPLETE:
                trial_count += 1
                self.game_state["goal_can_claim_victory"] = True

        # Magic Keys
        self.game_state["magic_keys_received"] = magic_key_count

        if self.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
            if magic_key_count >= self.magic_keys_required:
                self.game_state["goal_can_claim_victory"] = True

        key: KeymastersKeepItems
        for key in magic_keys_received:
            if key in self.game_state["magic_keys"]:
                self.game_state["magic_keys"][key] = True

        # Relics
        if self.shops:
            relic: KeymastersKeepItems
            for relic in relics_received:
                if relic in self.game_state["relics"]:
                    self.game_state["relics"][relic] = True

        # Areas Locked By
        filtered_areas_locked_by: Dict[KeymastersKeepRegions, Optional[List[KeymastersKeepItems]]] = dict()

        area: KeymastersKeepRegions
        keys: Optional[List[KeymastersKeepItems]]
        for area, keys in self.game_state["areas_locked_by"].items():
            if keys is None:
                filtered_areas_locked_by[area] = None
                continue

            filtered_areas_locked_by[area] = [key for key in keys if key not in magic_keys_received] or None

        self.game_state["areas_locked_by"] = filtered_areas_locked_by

        # Areas Unlocked
        area: KeymastersKeepRegions
        for area in self.game_state["areas_unlocked"]:
            door_unlock_item: KeymastersKeepItems = region_to_unlock_location_and_item[area][1]

            if door_unlock_item in door_unlocks_received:
                self.game_state["areas_unlocked"][area] = True

        # Artifacts of Resolve
        self.game_state["artifact_of_resolve_received"] = artifact_of_resolve_count

        # Trials Available
        area: KeymastersKeepRegions
        trials: List[KeymastersKeepLocationData]
        for area, trials in self.area_trials.items():
            available_trials: List[int] = list()

            trial: KeymastersKeepLocationData
            for trial in self.area_trials[area]:
                if trial.archipelago_id not in self.location_ids_checked:
                    available_trials.append(trial.archipelago_id)
                else:
                    trial_count += 1

            self.game_state["trials_available"][area] = available_trials

        self.game_state["trial_count"] = trial_count

        # Shop Items Purchased
        if self.shops:
            data: Dict[str, Any]
            for data in self.shop_data.values():
                shop: KeymastersKeepShops = data["shop"]
                purchased_items: List[int] = list()

                for item_name, item_data in data["shop_items"].items():
                    if item_data["location_data"].archipelago_id in self.location_ids_checked:
                        purchased_items.append(item_data["location_data"].archipelago_id)

                self.game_state["shop_items_purchased"][shop] = purchased_items


def main() -> None:
    Utils.init_logging("KeymastersKeepClient", exception_logger="Client")

    async def _main():
        ctx: KeymastersKeepContext = KeymastersKeepContext(None, None)

        ctx.server_task = asyncio.create_task(CommonClient.server_loop(ctx), name="ServerLoop")
        ctx.controller_task = asyncio.create_task(ctx.controller(), name="KeymastersKeepController")

        if CommonClient.gui_enabled:
            ctx.run_gui()

        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())

    colorama.deinit()


if __name__ == "__main__":
    main()
