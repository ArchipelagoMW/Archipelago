import typing

from BaseClasses import Item, ItemClassification, Tutorial
from .Items import LegacyItem, ItemData, item_table, vendors_table, static_classes_table, progressive_classes_table, \
    skill_unlocks_table, blueprints_table, runes_table, misc_items_table
from .Locations import LegacyLocation, location_table, base_location_table
from .Options import legacy_options
from .Regions import create_regions
from .Rules import set_rules
from .Names import ItemName
from ..AutoWorld import World, WebWorld


class LegacyWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Rogue Legacy Randomizer software on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "rogue-legacy_en.md",
        "rogue-legacy/en",
        ["Phar"]
    )]


class LegacyWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game: str = "Rogue Legacy"
    option_definitions = legacy_options
    topology_present = False
    data_version = 3
    required_client_version = (0, 2, 3)
    web = LegacyWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            "starting_gender": self.world.starting_gender[self.player],
            "starting_class": self.world.starting_class[self.player],
            "new_game_plus": self.world.new_game_plus[self.player],
            "fairy_chests_per_zone": self.world.fairy_chests_per_zone[self.player],
            "chests_per_zone": self.world.chests_per_zone[self.player],
            "universal_fairy_chests": self.world.universal_fairy_chests[self.player],
            "universal_chests": self.world.universal_chests[self.player],
            "vendors": self.world.vendors[self.player],
            "architect_fee": self.world.architect_fee[self.player],
            "disable_charon": self.world.disable_charon[self.player],
            "require_purchasing": self.world.require_purchasing[self.player],
            "gold_gain_multiplier": self.world.gold_gain_multiplier[self.player],
            "number_of_children": self.world.number_of_children[self.player],
            "khidr": self.world.khidr[self.player],
            "alexander": self.world.alexander[self.player],
            "leon": self.world.leon[self.player],
            "herodotus": self.world.herodotus[self.player],
            "allow_default_names": self.world.allow_default_names[self.player],
            "additional_sir_names": self.world.additional_sir_names[self.player],
            "additional_lady_names": self.world.additional_lady_names[self.player],
            "death_link": self.world.death_link[self.player],
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in legacy_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[LegacyItem] = []
        total_required_locations = 64 + (self.world.chests_per_zone[self.player] * 4) + (self.world.fairy_chests_per_zone[self.player] * 4)

        # Fill item pool with all required items
        for item in {**skill_unlocks_table, **runes_table}:
            # if Haggling, do not add if Disable Charon.
            if item == ItemName.haggling and self.world.disable_charon[self.player] == 1:
                continue
            itempool += self._create_items(item)

        # Blueprints
        if self.world.progressive_blueprints[self.player]:
            itempool += [self.create_item(ItemName.progressive_blueprints)] * 15
        else:
            for item in blueprints_table:
                itempool += self._create_items(item)

        # Check Pool settings to add a certain amount of these items.
        itempool += [self.create_item(ItemName.health)] * int(self.world.health_pool[self.player])
        itempool += [self.create_item(ItemName.mana)] * int(self.world.mana_pool[self.player])
        itempool += [self.create_item(ItemName.attack)] * int(self.world.attack_pool[self.player])
        itempool += [self.create_item(ItemName.magic_damage)] * int(self.world.magic_damage_pool[self.player])
        itempool += [self.create_item(ItemName.armor)] * int(self.world.armor_pool[self.player])
        itempool += [self.create_item(ItemName.equip)] * int(self.world.equip_pool[self.player])
        itempool += [self.create_item(ItemName.crit_chance)] * int(self.world.crit_chance_pool[self.player])
        itempool += [self.create_item(ItemName.crit_damage)] * int(self.world.crit_damage_pool[self.player])

        classes = self.world.available_classes[self.player]
        if "Dragon" in classes:
            itempool.append(self.create_item(ItemName.dragon))
        if "Traitor" in classes:
            itempool.append(self.create_item(ItemName.traitor))
        if self.world.starting_class[self.player] == "knight":
            itempool.append(self.create_item(ItemName.progressive_knight))
        elif "Knight" in classes:
            itempool.extend(self._create_items(ItemName.progressive_knight))
        if self.world.starting_class[self.player] == "mage":
            itempool.append(self.create_item(ItemName.progressive_mage))
        elif "Mage" in classes:
            itempool.extend(self._create_items(ItemName.progressive_mage))
        if self.world.starting_class[self.player] == "barbarian":
            itempool.append(self.create_item(ItemName.progressive_barbarian))
        elif "Barbarian" in classes:
            itempool.extend(self._create_items(ItemName.progressive_barbarian))
        if self.world.starting_class[self.player] == "knave":
            itempool.append(self.create_item(ItemName.progressive_knave))
        elif "Knave" in classes:
            itempool.extend(self._create_items(ItemName.progressive_knave))
        if self.world.starting_class[self.player] == "shinobi":
            itempool.append(self.create_item(ItemName.progressive_shinobi))
        elif "Shinobi" in classes:
            itempool.extend(self._create_items(ItemName.progressive_shinobi))
        if self.world.starting_class[self.player] == "miner":
            itempool.append(self.create_item(ItemName.progressive_miner))
        elif "Miner" in classes:
            itempool.extend(self._create_items(ItemName.progressive_miner))
        if self.world.starting_class[self.player] == "lich":
            itempool.append(self.create_item(ItemName.progressive_lich))
        elif "Lich" in classes:
            itempool.extend(self._create_items(ItemName.progressive_lich))
        if self.world.starting_class[self.player] == "spellthief":
            itempool.append(self.create_item(ItemName.progressive_spellthief))
        elif "Spellthief" in classes:
            itempool.extend(self._create_items(ItemName.progressive_spellthief))

        # Check if we need to start with these vendors or put them in the pool.
        if self.world.vendors[self.player] == "start_unlocked":
            self.world.push_precollected(self.world.create_item(ItemName.blacksmith, self.player))
            self.world.push_precollected(self.world.create_item(ItemName.enchantress, self.player))
        else:
            itempool += [self.create_item(ItemName.blacksmith), self.create_item(ItemName.enchantress)]

        # Add Architect.
        if self.world.architect[self.player] == "start_unlocked":
            self.world.push_precollected(self.world.create_item(ItemName.architect, self.player))
        elif self.world.architect[self.player] != "disabled":
            itempool += [self.create_item(ItemName.architect)]

        # Fill item pool with the remaining
        for _ in range(len(itempool), total_required_locations):
            item = self.world.random.choice(list(misc_items_table.keys()))
            itempool += [self.create_item(item)]

        self.world.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(list(misc_items_table.keys()))

    def create_regions(self):
        create_regions(self.world, self.player)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return LegacyItem(name, ItemClassification.progression if data.progression else ItemClassification.filler, data.code, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)
