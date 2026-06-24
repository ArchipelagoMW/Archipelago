from BaseClasses import Item, ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from .items import filler_item_names, item_table, raw_item_table, trap_item_names
from .locations import location_table
from .options import ESSENTIAL_ITEMS, MAX_RESOURCE_UPGRADES, ShellipelagoOptions


__version__ = "1.8"


class ShellipelagoItem(Item):
    game = "Shellipelago"


class ShellipelagoLocation(Location):
    game = "Shellipelago"


class ShellipelagoWeb(WebWorld):
    theme = "ocean"
    game_info_languages = ["en"]
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Shellipelago for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["ethentianknight"],
        )
    ]


class ShellipelagoWorld(World):
    """A browser game about unlocking movement, checks, and graphics through Archipelago."""

    game = "Shellipelago"
    author = "ethentianknight"
    web = ShellipelagoWeb()
    options_dataclass = ShellipelagoOptions
    options: ShellipelagoOptions
    topology_present = False
    victory_location_name = "Final Boss Defeated"
    starting_item_counts = {
        "Progressive Room": 1,
    }

    item_name_to_id = {item_name: item_data["id"] for item_name, item_data in item_table.items()}
    location_name_to_id = {
        location_name: location_data["id"] for location_name, location_data in location_table.items()
    }

    item_name_groups = {
        "Progression": {
            item_name for item_name, item_data in item_table.items()
            if item_data["classification_name"] == "progression"
        },
        "Resources": {"Max HP", "Max Rounds"},
        "Linkable": {
            item_name for item_name, item_data in item_table.items()
            if item_data["classification_name"] != "trap" and item_data["key"] != "itemPool"
        },
        "Traps": set(trap_item_names),
    }
    location_name_groups = {
        "Checks": set(location_table.keys()),
        "Chests": {
            location_name for location_name, location_data in location_table.items()
            if location_data["category"] == "chest"
        },
        "Enemies": {
            location_name for location_name, location_data in location_table.items()
            if location_data["category"] == "enemy"
        },
        "Shops": {
            location_name for location_name, location_data in location_table.items()
            if location_data["category"] == "shop"
        },
        "Destructibles": {
            location_name for location_name, location_data in location_table.items()
            if location_data["category"] == "easy_destructible"
        },
    }

    def create_item(self, name: str) -> ShellipelagoItem:
        item_data = item_table[name]

        return ShellipelagoItem(name, item_data["classification"], item_data["id"], self.player)

    def create_event(self, name: str) -> ShellipelagoItem:
        return ShellipelagoItem(name, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    @staticmethod
    def option_set_contains(option, name: str) -> bool:
        return name in getattr(option, "value", set())

    def option_set_selected(self, local_option_name: str, remote_option_name: str, name: str) -> bool:
        return self.option_set_contains(getattr(self.options, local_option_name), name) or self.option_set_contains(
            getattr(self.options, remote_option_name), name
        )

    @staticmethod
    def requirement_met(state, player: int, requirement: dict) -> bool:
        item = requirement["item"]
        amount = requirement.get("amount", 1)

        if item == "Tank":
            return (
                state.has("Tank Treads", player)
                and state.has("Tank Chassis", player)
                and state.has("Tank Cannon", player)
            )

        return state.has(item, player, amount)

    @classmethod
    def requirements_met(cls, state, player: int, requirement_rows: list) -> bool:
        return all(
            any(cls.requirement_met(state, player, requirement) for requirement in requirement_row)
            for requirement_row in requirement_rows
        )

    @staticmethod
    def hint_trigger_key(location_data: dict) -> str:
        return (
            f"{location_data['room_x']},{location_data['room_y']}:"
            f"{location_data['tile_x']},{location_data['tile_y']}"
        )

    @staticmethod
    def has_tank(state, player: int) -> bool:
        return (
            state.has("Tank Treads", player)
            and state.has("Tank Chassis", player)
            and state.has("Tank Cannon", player)
        )

    @classmethod
    def has_final_run_access(cls, state, player: int) -> bool:
        return cls.has_tank(state, player) and state.has("Progressive Room", player, 5)

    @staticmethod
    def item_count(name: str) -> int:
        for item_data in raw_item_table:
            if item_data["name"] == name:
                return item_data.get("count", 1)

        return 1

    def location_enabled(self, location_data: dict) -> bool:
        category = location_data["category"]
        drop_name = location_data.get("drop_name", "")

        if category == "enemy":
            return bool(self.options.enemies_are_checks)

        if category == "easy_destructible":
            return bool(self.options.add_easy_destructible_checks)

        if category == "shop":
            if bool(self.options.shuffle_shops):
                return True

            return self.drop_can_shuffle_without_shop_shuffle(location_data)

        if location_data.get("item_pool"):
            return bool(self.options.other_players_can_find_item_pool_drops)

        if location_data.get("trap_location"):
            return bool(self.options.shuffle_essential_items)

        if location_data.get("resource_location"):
            return bool(self.options.shuffle_max_resource_upgrades) and self.option_set_selected(
                "max_resource_upgrades_in_my_world",
                "max_resource_upgrades_in_other_worlds",
                drop_name,
            )

        if location_data.get("essential_location"):
            return bool(self.options.shuffle_essential_items) and self.option_set_selected(
                "essential_items_in_my_world",
                "essential_items_in_other_worlds",
                drop_name,
            )

        return True

    def drop_can_shuffle_without_shop_shuffle(self, location_data: dict) -> bool:
        drop_name = location_data.get("drop_name", "")

        if location_data.get("resource_location"):
            return bool(self.options.shuffle_max_resource_upgrades) and self.option_set_selected(
                "max_resource_upgrades_in_my_world",
                "max_resource_upgrades_in_other_worlds",
                drop_name,
            )

        if location_data.get("essential_location"):
            return bool(self.options.shuffle_essential_items) and self.option_set_selected(
                "essential_items_in_my_world",
                "essential_items_in_other_worlds",
                drop_name,
            )

        return False

    def enabled_locations(self) -> list:
        return [
            location_data for location_data in location_table.values()
            if self.location_enabled(location_data)
        ]

    def should_place_location_drop_item(self, location_data: dict) -> bool:
        drop_name = location_data.get("drop_name", "")

        if not drop_name or drop_name not in item_table:
            return False

        if location_data.get("item_pool") or location_data.get("trap_location"):
            return False

        if location_data.get("resource_location") or location_data.get("essential_location"):
            return True

        return item_table[drop_name]["classification_name"] in {"progression", "useful"}

    def add_progression_items(self, item_pool: list, enabled_locations: list) -> None:
        skipped_starting_items = {
            item_name: 0 for item_name in self.starting_item_counts
        }

        for location_data in enabled_locations:
            if self.should_place_location_drop_item(location_data):
                drop_name = location_data["drop_name"]

                if skipped_starting_items.get(drop_name, 0) < self.starting_item_counts.get(drop_name, 0):
                    skipped_starting_items[drop_name] += 1
                    continue

                item_pool.append(self.create_item(location_data["drop_name"]))

    def add_trap_items(self, item_pool: list, remaining_slots: int) -> None:
        if not bool(self.options.add_traps_to_pool) or remaining_slots <= 0:
            return

        allowed_traps = [
            trap_name for trap_name in trap_item_names
            if self.option_set_contains(self.options.trap_pool_spawn, trap_name)
            and self.option_set_selected("trap_pool_in_my_world", "trap_pool_in_other_worlds", trap_name)
        ]

        while allowed_traps and remaining_slots > 0:
            item_pool.append(self.create_item(self.random.choice(allowed_traps)))
            remaining_slots -= 1

    def create_items(self) -> None:
        enabled_locations = self.enabled_locations()
        enabled_location_count = len(enabled_locations)
        item_pool = []
        precollected_item_counts = dict(self.starting_item_counts)

        if not bool(self.options.shuffle_essential_items):
            for item_name in ESSENTIAL_ITEMS:
                precollected_item_counts[item_name] = self.item_count(item_name)

        if not bool(self.options.shuffle_max_resource_upgrades):
            for item_name in MAX_RESOURCE_UPGRADES:
                precollected_item_counts[item_name] = self.item_count(item_name)

        for item_name, item_count_value in precollected_item_counts.items():
            for _ in range(item_count_value):
                self.multiworld.push_precollected(self.create_item(item_name))

        self.add_progression_items(item_pool, enabled_locations)
        self.add_trap_items(item_pool, enabled_location_count - len(item_pool))

        while len(item_pool) < enabled_location_count:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool[:enabled_location_count]

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        for location_data in self.enabled_locations():
            location = ShellipelagoLocation(self.player, location_data["name"], location_data["id"], menu_region)
            location.access_rule = lambda state, requirements=location_data["requirements"]: self.requirements_met(
                state, self.player, requirements
            )
            menu_region.locations.append(location)

        victory_location = ShellipelagoLocation(self.player, self.victory_location_name, None, menu_region)
        victory_location.access_rule = lambda state: self.has_final_run_access(state, self.player)
        victory_location.place_locked_item(self.create_event("Victory"))
        menu_region.locations.append(victory_location)

        self.multiworld.regions.append(menu_region)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def hint_trigger_data(self) -> dict:
        if not bool(self.options.enemies_are_hints):
            return {}

        hint_targets = []
        for location_data in self.enabled_locations():
            if location_data["category"] == "enemy":
                continue

            location = self.multiworld.get_location(location_data["name"], self.player)
            item = location.item
            if item and item.classification & (ItemClassification.progression | ItemClassification.useful):
                hint_targets.append(location_data["id"])

        hint_triggers = [
            location_data for location_data in location_table.values()
            if location_data["category"] == "enemy"
        ]

        self.random.shuffle(hint_targets)
        self.random.shuffle(hint_triggers)

        return {
            self.hint_trigger_key(location_data): hint_targets[index]
            for index, location_data in enumerate(hint_triggers[:len(hint_targets)])
        }

    def fill_slot_data(self) -> dict:
        shop_costs = {
            str(location_data["id"]): self.random.randint(1, 150)
            for location_data in self.enabled_locations()
            if location_data["category"] == "shop"
        }

        return {
            "show_essential_pickup_hints": bool(self.options.show_essential_pickup_hints),
            "add_easy_destructible_checks": bool(self.options.add_easy_destructible_checks),
            "enemies_are_checks": bool(self.options.enemies_are_checks),
            "hint_triggers": self.hint_trigger_data(),
            "shop_costs": shop_costs,
            "ring_link": bool(self.options.ring_link),
            "energy_link": bool(self.options.energy_link),
            "death_link": bool(self.options.death_link),
            "trap_link": bool(self.options.trap_link),
            "item_link": bool(self.options.item_link),
        }
