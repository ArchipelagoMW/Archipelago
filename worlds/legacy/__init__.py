from BaseClasses import Region, MultiWorld, Entrance, Item
from .Items import LegacyItem, item_table, item_frequencies
from .Locations import LegacyLocation, location_table
from .Options import legacy_options
from .Regions import create_regions
from ..AutoWorld import World
import random
import typing


class LegacyWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each
    time you die, your child will succeed you. Every child is unique. One child
    might be colorblind, another might have vertigo-- they could even be a
    dwarf. But that's OK, because no one is perfect, and you don't have to be to
    succeed.
    """

    game: str = "Rogue Legacy"
    options = legacy_options
    topology_present = False
    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            "initial_gender": self.world.initial_gender[self.player],
            "difficulty": self.world.difficulty[self.player],
            "stat_increase_pool": self.world.stat_increase_pool[self.player],
            "stat_increase_applies": self.world.stat_increase_applies[self.player],
            "early_vendors": self.world.early_vendors[self.player],
            "boss_shuffle": self.world.boss_shuffle[self.player],
            "children": self.world.children[self.player],
            "hereditary_blessings": self.world.hereditary_blessings[self.player],
            "enable_shop": self.world.enable_shop[self.player],
            "disable_charon": self.world.disable_charon[self.player],
            "death_link": self.world.death_link[self.player],
            "additional_children_names": self.world.additional_children_names[self.player],
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in legacy_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

            if option_name is "additional_children_names":
                slot_data[option_name] = option.value
            else:
                slot_data[option_name] = int(option.value)

        print(slot_data)
        return slot_data

    def generate_basic(self):
        itempool = []
        skillspool: typing.List[LegacyItem] = []

        # Pool the skills first.
        for name, data in skills_table.items():
            skillspool += [LegacyItem(name, self.player)] * item_frequencies[name]

        # Shuffle skills pool prior to combining stats.
        random.shuffle(skillspool)
        for i in range(0, 120):
            HP  = 0
            MP  = 0
            ATK = 0
            DEF = 0
            MAG = 0
            ARM = 0

            for j in range(0, 3):
                skill = skillspool.pop()
                if skill.name == "Health Up":
                    HP += 1
                elif skill.name == "Mana Up":
                    MP += 1
                elif skill.name == "Attack Up":
                    ATK += 1
                elif skill.name == "Armor Up":
                    DEF += 1
                elif skill.name == "Magic Damage Up":
                    MAG += 1
                else:
                    ARM += 1

            skill_name = ""
            is_double = False
            is_triple = False
            # Check Triples First
            if HP == 3:
                skill_name = "Triple Health Up"
                is_triple = True
            elif MP == 3:
                skill_name = "Triple Mana Up"
                is_triple = True
            elif ATK == 3:
                skill_name = "Triple Attack Up"
                is_triple = True
            elif DEF == 3:
                skill_name = "Triple Armor Up"
                is_triple = True
            elif MAG == 3:
                skill_name = "Triple Magic Damage Up"
                is_triple = True
            elif ARM == 3:
                skill_name = "Triple Equip Up"
                is_triple = True

            if is_triple:
                itempool += [LegacyItem(skill_name, self.player)]
                continue

            # Check Doubles
            if HP == 2:
                skill_name = "Double Health Up, "
                HP -= 2
                is_double = True
            elif MP == 2:
                skill_name = "Double Mana Up, "
                MP -= 2
                is_double = True
            elif ATK == 2:
                skill_name = "Double Attack Up, "
                ATK -= 2
                is_double = True
            elif DEF == 2:
                skill_name = "Double Armor Up, "
                DEF -= 2
                is_double = True
            elif MAG == 2:
                skill_name = "Double Magic Damage Up, "
                MAG -= 2
                is_double = True
            elif ARM == 2:
                skill_name = "Double Equip Up, "
                ARM -= 2
                is_double = True

            # Fill Remainder
            iterations = 1 if is_double else 3
            for j in range(0, iterations):
                if ATK >= 1:
                    skill_name += "Attack Up, "
                    ATK -= 1
                elif DEF >= 1:
                    skill_name += "Armor Up, "
                    DEF -= 1
                elif HP >= 1:
                    skill_name += "Health Up, "
                    HP -= 1
                elif MP >= 1:
                    skill_name += "Mana Up, "
                    MP -= 1
                elif MAG >= 1:
                    skill_name += "Magic Damage Up, "
                    MAG -= 1
                elif ARM >= 1:
                    skill_name += "Equip Up, "
                    ARM -= 1

            # Remove trailing digits
            skill_name = skill_name[:-2]
            itempool += [LegacyItem(skill_name, self.player)]

        # Add remaining skills to pool
        itempool += skillspool

        for name, data in base_item_table.items():
            # Exclude some packs depending on settings.
            # if name == "Haggle" and bool(self.world.disable_charon[self.player]) is True:
            #     continue

            # # Change the amount of increases dependant on settings.
            # if name == "Stat Increase":
            #     itempool += [LegacyItem(name, self.player)] * self.world.stat_increase_pool[self.player]
            #     continue

            # # If shop is disabled, add Armor Up to pool, otherwise do not.
            # if name == "Armor Up" and bool(self.world.enable_shop[self.player]) is False:
            #     itempool += [LegacyItem(name, self.player)] * 25
            #     continue
            # elif name == "Armor Up":
            #     continue

            # Add the rest of the items!
            if name in item_frequencies:
                itempool += [LegacyItem(name, self.player)] * item_frequencies[name]
            else:
                itempool += [LegacyItem(name, self.player)]

        self.world.itempool += itempool

    def create_regions(self):
        create_regions(self.world, self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        return LegacyItem(name, True, item_id, self.player)

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = LegacyLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret