from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import RLItem, RLItemData, event_item_table, get_items_by_category, item_table
from .Locations import RLLocation, location_table
from .Options import rl_options
from .Presets import rl_options_presets
from .Regions import create_regions
from .Rules import set_rules


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
    bug_report_page = "https://github.com/ThePhar/RogueLegacyRandomizer/issues/new?assignees=&labels=bug&template=" \
                      "report-an-issue---.md&title=%5BIssue%5D"
    options_presets = rl_options_presets


class RLWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game = "Rogue Legacy"
    option_definitions = rl_options
    topology_present = True
    data_version = 4
    required_client_version = (0, 3, 5)
    web = RLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    # TODO: Replace calls to this function with "options-dict", once that PR is completed and merged.
    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {option_name: self.get_setting(option_name).value for option_name in rl_options}

    def generate_early(self):
        # Check validation of names.
        additional_lady_names = len(self.get_setting("additional_lady_names").value)
        additional_sir_names = len(self.get_setting("additional_sir_names").value)
        if not self.get_setting("allow_default_names"):
            if additional_lady_names < int(self.get_setting("number_of_children")):
                raise Exception(
                    f"allow_default_names is off, but not enough names are defined in additional_lady_names. "
                    f"Expected {int(self.get_setting('number_of_children'))}, Got {additional_lady_names}")

            if additional_sir_names < int(self.get_setting("number_of_children")):
                raise Exception(
                    f"allow_default_names is off, but not enough names are defined in additional_sir_names. "
                    f"Expected {int(self.get_setting('number_of_children'))}, Got {additional_sir_names}")

    def create_items(self):
        item_pool: List[RLItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            quantity = data.max_quantity

            # Architect
            if name == "Architect":
                if self.get_setting("architect") == "disabled":
                    continue
                if self.get_setting("architect") == "start_unlocked":
                    self.multiworld.push_precollected(self.create_item(name))
                    continue
                if self.get_setting("architect") == "early":
                    self.multiworld.local_early_items[self.player]["Architect"] = 1

            # Blacksmith and Enchantress
            if name == "Blacksmith" or name == "Enchantress":
                if self.get_setting("vendors") == "start_unlocked":
                    self.multiworld.push_precollected(self.create_item(name))
                    continue
                if self.get_setting("vendors") == "early":
                    self.multiworld.local_early_items[self.player]["Blacksmith"] = 1
                    self.multiworld.local_early_items[self.player]["Enchantress"] = 1

            # Haggling
            if name == "Haggling" and self.get_setting("disable_charon"):
                continue

            # Blueprints
            if data.category == "Blueprints":
                # No progressive blueprints if progressive_blueprints are disabled.
                if name == "Progressive Blueprints" and not self.get_setting("progressive_blueprints"):
                    continue
                # No distinct blueprints if progressive_blueprints are enabled.
                elif name != "Progressive Blueprints" and self.get_setting("progressive_blueprints"):
                    continue

            # Classes
            if data.category == "Classes":
                if name == "Progressive Knights":
                    if "Knight" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "knight":
                        quantity = 1
                if name == "Progressive Mages":
                    if "Mage" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "mage":
                        quantity = 1
                if name == "Progressive Barbarians":
                    if "Barbarian" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "barbarian":
                        quantity = 1
                if name == "Progressive Knaves":
                    if "Knave" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "knave":
                        quantity = 1
                if name == "Progressive Miners":
                    if "Miner" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "miner":
                        quantity = 1
                if name == "Progressive Shinobis":
                    if "Shinobi" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "shinobi":
                        quantity = 1
                if name == "Progressive Liches":
                    if "Lich" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "lich":
                        quantity = 1
                if name == "Progressive Spellthieves":
                    if "Spellthief" not in self.get_setting("available_classes"):
                        continue

                    if self.get_setting("starting_class") == "spellthief":
                        quantity = 1
                if name == "Dragons":
                    if "Dragon" not in self.get_setting("available_classes"):
                        continue
                if name == "Traitors":
                    if "Traitor" not in self.get_setting("available_classes"):
                        continue

            # Skills
            if name == "Health Up":
                quantity = self.get_setting("health_pool")
            elif name == "Mana Up":
                quantity = self.get_setting("mana_pool")
            elif name == "Attack Up":
                quantity = self.get_setting("attack_pool")
            elif name == "Magic Damage Up":
                quantity = self.get_setting("magic_damage_pool")
            elif name == "Armor Up":
                quantity = self.get_setting("armor_pool")
            elif name == "Equip Up":
                quantity = self.get_setting("equip_pool")
            elif name == "Crit Chance Up":
                quantity = self.get_setting("crit_chance_pool")
            elif name == "Crit Damage Up":
                quantity = self.get_setting("crit_damage_pool")

            # Ignore filler, it will be added in a later stage.
            if data.category == "Filler":
                continue

            item_pool += [self.create_item(name) for _ in range(0, quantity)]

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def create_item(self, name: str) -> RLItem:
        data = item_table[name]
        return RLItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> RLItem:
        data = event_item_table[name]
        return RLItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)
        self._place_events()

    def _place_events(self):
        # Fountain
        self.multiworld.get_location("Fountain Room", self.player).place_locked_item(
            self.create_event("Defeat The Fountain"))

        # Khidr / Neo Khidr
        if self.get_setting("khidr") == "vanilla":
            self.multiworld.get_location("Castle Hamson Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Khidr"))
        else:
            self.multiworld.get_location("Castle Hamson Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Neo Khidr"))

        # Alexander / Alexander IV
        if self.get_setting("alexander") == "vanilla":
            self.multiworld.get_location("Forest Abkhazia Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Alexander"))
        else:
            self.multiworld.get_location("Forest Abkhazia Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Alexander IV"))

        # Ponce de Leon / Ponce de Freon
        if self.get_setting("leon") == "vanilla":
            self.multiworld.get_location("The Maya Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Ponce de Leon"))
        else:
            self.multiworld.get_location("The Maya Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Ponce de Freon"))

        # Herodotus / Astrodotus
        if self.get_setting("herodotus") == "vanilla":
            self.multiworld.get_location("Land of Darkness Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Herodotus"))
        else:
            self.multiworld.get_location("Land of Darkness Boss Room", self.player).place_locked_item(
                self.create_event("Defeat Astrodotus"))
