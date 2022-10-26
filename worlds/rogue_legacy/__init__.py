from typing import List

from BaseClasses import Tutorial
from .Items import RLItem, RLItemData, event_item_table, item_table, get_items_by_category
from .Locations import RLLocation, location_table
from .Options import rl_options
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld


class RLWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Rogue Legacy Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "rogue-legacy_en.md",
        "rogue-legacy/en",
        ["Phar"]
    )]


class RLWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game: str = "Rogue Legacy"
    option_definitions = rl_options
    topology_present = True
    data_version = 4
    required_client_version = (0, 3, 5)
    web = RLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    item_pool: List[RLItem] = []
    prefill_items: List[RLItem] = []

    def setting(self, name: str):
        return getattr(self.world, name)[self.player]

    def fill_slot_data(self) -> dict:
        slot_data = {}
        for option_name in rl_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_early(self):
        # Check validation of names.
        additional_lady_names = len(self.setting("additional_lady_names").value)
        additional_sir_names = len(self.setting("additional_sir_names").value)
        if not self.setting("allow_default_names"):
            # Check for max_quantity.
            if additional_lady_names < int(self.setting("number_of_children")):
                raise Exception(
                    f"allow_default_names is off, but not enough names are defined in additional_lady_names. "
                    f"Expected {int(self.setting('number_of_children'))}, Got {additional_lady_names}")

            if additional_sir_names < int(self.setting("number_of_children")):
                raise Exception(
                    f"allow_default_names is off, but not enough names are defined in additional_sir_names. "
                    f"Expected {int(self.setting('number_of_children'))}, Got {additional_sir_names}")

        if self.setting("vendors") == "early":
            self.prefill_items += [self.create_item("Blacksmith"), self.create_item("Enchantress")]

        if self.setting("architect") == "early":
            self.prefill_items += [self.create_item("Architect")]

    def generate_basic(self):
        # TODO: Remove hard code value here.
        total_required_locations = 64 + (self.world.chests_per_zone[self.player] * 4) + \
                                        (self.world.fairy_chests_per_zone[self.player] * 4)

        # Add items to item pool. Anything with a "continue" will not be added to the item pool.
        for name, data in item_table.items():
            quantity = data.max_quantity

            # Architect
            if name == "Architect":
                if self.setting("architect") == "disabled" or self.setting("architect") == "early":
                    continue
                if self.setting("architect") == "start_unlocked":
                    self.world.push_precollected(self.create_item(name))
                    continue

            # Blacksmith and Enchantress
            if name == "Blacksmith" or name == "Enchantress":
                if self.setting("vendors") == "start_unlocked":
                    self.world.push_precollected(self.create_item(name))
                    continue
                if self.setting("vendors") == "early":
                    continue

            # Haggling
            if name == "Haggling" and self.setting("disable_charon"):
                continue

            # Blueprints
            if data.category == "Blueprints":
                # No progressive blueprints if progressive_blueprints are disabled.
                if name == "Progressive Blueprints" and not self.setting("progressive_blueprints"):
                    continue
                # No distinct blueprints if progressive_blueprints are enabled.
                elif name != "Progressive Blueprints" and self.setting("progressive_blueprints"):
                    continue

            # Classes
            if data.category == "Classes":
                if name == "Progressive Knights" and "Knight" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Mages" and "Mage" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Barbarians" and "Barbarian" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Knaves" and "Knave" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Shinobis" and "Shinobi" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Miners" and "Miner" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Liches" and "Lich" not in self.setting("available_classes"):
                    continue
                if name == "Progressive Spellthieves" and "Spellthief" not in self.setting("available_classes"):
                    continue
                if name == "Dragons" and "Dragon" not in self.setting("available_classes"):
                    continue
                if name == "Traitors" and "Traitor" not in self.setting("available_classes"):
                    continue

            # Skills
            if name == "Health Up":
                quantity = self.setting("health_pool")
            elif name == "Mana Up":
                quantity = self.setting("mana_pool")
            elif name == "Attack Up":
                quantity = self.setting("attack_pool")
            elif name == "Magic Damage Up":
                quantity = self.setting("magic_damage_pool")
            elif name == "Armor Up":
                quantity = self.setting("armor_pool")
            elif name == "Equip Up":
                quantity = self.setting("equip_pool")
            elif name == "Crit Chance Up":
                quantity = self.setting("crit_chance_pool")
            elif name == "Crit Damage Up":
                quantity = self.setting("crit_damage_pool")

            # Ignore filler, it will be added in a later stage.
            if data.category == "Filler":
                continue

            self.item_pool += [self.create_item(name) for _ in range(0, quantity)]

        # Fill any empty locations with filler items.
        while len(self.item_pool) + len(self.prefill_items) < total_required_locations:
            self.item_pool.append(self.create_item(self.get_filler_item_name()))

        self.world.itempool += self.item_pool

    def pre_fill(self) -> None:
        reachable = [loc for loc in self.world.get_reachable_locations(player=self.player) if not loc.item]
        self.world.random.shuffle(reachable)
        items = self.prefill_items.copy()
        for item in items:
            reachable.pop().place_locked_item(item)

    def get_pre_fill_items(self) -> List[RLItem]:
        return self.prefill_items

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.world.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def create_item(self, name: str) -> RLItem:
        data = item_table[name]
        return RLItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> RLItem:
        data = event_item_table[name]
        return RLItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)