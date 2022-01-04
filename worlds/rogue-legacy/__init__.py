import typing

from BaseClasses import Item, MultiWorld
from .Items import LegacyItem, ItemData, item_table, vendors_table, static_classes_table, progressive_classes_table, \
    skill_unlocks_table, blueprints_table, runes_table, misc_items_table
from .Locations import LegacyLocation, location_table, base_location_table
from .Options import legacy_options
from .Regions import create_regions
from .Rules import set_rules
from .Names import ItemName
from ..AutoWorld import World


class LegacyWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game: str = "Rogue Legacy"
    options = legacy_options
    topology_present = False
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            "starting_gender": self.world.starting_gender[self.player],
            "starting_class": self.world.starting_class[self.player],
            "new_game_plus": self.world.new_game_plus[self.player],
            "fairy_chests_per_zone": self.world.fairy_chests_per_zone[self.player],
            "chests_per_zone": self.world.chests_per_zone[self.player],
            "vendors": self.world.vendors[self.player],
            "disable_charon": self.world.disable_charon[self.player],
            "require_purchasing": self.world.require_purchasing[self.player],
            "gold_gain_multiplier": self.world.gold_gain_multiplier[self.player],
            "number_of_children": self.world.number_of_children[self.player],
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
        total_required_locations = 61 + (self.world.chests_per_zone[self.player] * 4) + (self.world.fairy_chests_per_zone[self.player] * 4)

        # Fill item pool with all required items
        for item in {**skill_unlocks_table, **blueprints_table, **runes_table}:
            # if Haggling, do not add if Disable Charon.
            if item == ItemName.haggling and self.world.disable_charon[self.player] == 1:
                continue
            itempool += self._create_items(item)
            
        # Add specific classes into the pool. Eventually, will be able to shuffle the starting ones, but until then...
        itempool += [
            self.create_item(ItemName.paladin),
            self.create_item(ItemName.archmage),
            self.create_item(ItemName.barbarian_king),
            self.create_item(ItemName.assassin),
            self.create_item(ItemName.dragon),
            self.create_item(ItemName.traitor),
            *self._create_items(ItemName.progressive_shinobi),
            *self._create_items(ItemName.progressive_miner),
            *self._create_items(ItemName.progressive_lich),
            *self._create_items(ItemName.progressive_spellthief),
        ]

        # Check if we need to start with these vendors or put them in the pool.
        if self.world.vendors[self.player] == "start_unlocked":
            self.world.push_precollected(self.world.create_item(ItemName.blacksmith, self.player))
            self.world.push_precollected(self.world.create_item(ItemName.enchantress, self.player))
        else:
            itempool += [self.create_item(ItemName.blacksmith), self.create_item(ItemName.enchantress)]

        # Add Arcitect.
        itempool += [self.create_item(ItemName.architect)]
            
        # Fill item pool with the remaining
        for _ in range(len(itempool), total_required_locations):
            item = self.world.random.choice(list(misc_items_table.keys()))
            itempool += [self.create_item(item)]

        self.world.itempool += itempool

    def create_regions(self):
        create_regions(self.world, self.player)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return LegacyItem(name, data.progression, data.code, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)
