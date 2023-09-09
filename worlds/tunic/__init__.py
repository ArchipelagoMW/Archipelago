from typing import Dict

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from .Items import filler_items, item_table, item_name_groups
from .Locations import location_table, location_name_groups
from .Rules import set_location_rules, set_region_rules, hexagon_quest_abilities, set_abilities
from .Regions import tunic_regions
from .Options import tunic_options
from ..AutoWorld import WebWorld, World


class TunicWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the TUNIC Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="guide/en",
            authors=["SilentDestroyer"]
        )
    ]
    theme = "grassFlowers"
    game = "Tunic"


class TunicItem(Item):
    game: str = "Tunic"


class TunicLocation(Location):
    game: str = "Tunic"


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "Tunic"
    web = TunicWeb()

    data_version = 1
    tunic_items = item_table
    tunic_locations = location_table
    option_definitions = tunic_options
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = {}
    location_name_to_id = {}
    item_base_id = 509342400
    location_base_id = 509342400

    for item_name, item_data in item_table.items():
        item_name_to_id[item_name] = item_base_id + item_data.item_id_offset

    for location_name, location_data in location_table.items():
        location_name_to_id[location_name] = location_base_id
        location_base_id += 1

    def create_item(self, name: str) -> TunicItem:
        item_data = item_table[name]
        return TunicItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        hexagon_locations: Dict[str, str] = {
            "Red Hexagon": "Fortress Arena - Siege Engine/Vault Key Pickup",
            "Green Hexagon": "Librarian - Hexagon Green",
            "Blue Hexagon": "Rooted Ziggurat Lower - Hexagon Blue"
        }

        fool_tiers = [
            [],
            ["Money x1", "Money x10", "Money x15", "Money x16"],
            ["Money x1", "Money x10", "Money x15", "Money x16", "Money x20"],
            ["Money x1", "Money x10", "Money x15", "Money x16", "Money x20", "Money x25", "Money x30"]
        ]

        items = []
        for item_name in item_table:
            item_data = item_table[item_name]

            if item_name in fool_tiers[self.multiworld.fool_traps[self.player].value]:
                for i in range(item_data.quantity_in_item_pool):
                    items.append(self.create_item("Fool Trap"))
                continue

            if item_name == "Gold Hexagon":
                # if hexagon quest is on, add the gold hexagons in
                if self.multiworld.hexagon_quest[self.player].value:
                    # if keys are behind bosses, place 3 manually
                    gold_hexes = item_data.quantity_in_item_pool
                    if self.multiworld.keys_behind_bosses[self.player].value:
                        for location in hexagon_locations.values():
                            self.multiworld.get_location(location, self.player)\
                                .place_locked_item(self.create_item("Gold Hexagon"))
                        gold_hexes -= 3

                    for i in range(0, gold_hexes):
                        items.append(self.create_item(item_name))
                    # adding a money x1 or fool trap to even out the pool with this option
                    if self.multiworld.fool_traps[self.player].value == 0:
                        items.append(self.create_item("Money x1"))
                    else:
                        items.append(self.create_item("Fool Trap"))
                else:
                    # if not doing hexagon quest, just skip the gold hexagons
                    continue
            elif self.multiworld.hexagon_quest[self.player].value and \
                    ("Pages" in item_name or item_name in hexagon_locations.keys()):
                continue
            elif self.multiworld.keys_behind_bosses[self.player].value and item_name in hexagon_locations.keys():
                self.multiworld.get_location(hexagon_locations[item_name], self.player)\
                    .place_locked_item(self.create_item(item_name))
            elif (item_name == "Sword Upgrade" and not self.multiworld.sword_progression[self.player].value)\
                    or (item_name in ["Stick", "Sword"] and self.multiworld.sword_progression[self.player].value):
                continue
            else:
                for i in range(0, item_data.quantity_in_item_pool):
                    items.append(self.create_item(item_name))

        self.multiworld.itempool += items

    def create_regions(self):
        for region_name in tunic_regions.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name in tunic_regions.keys():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(tunic_regions[region_name])

        for location_name in self.location_name_to_id:
            region = self.multiworld.get_region(location_table[location_name].region, self.player)
            location = TunicLocation(self.player, location_name, self.location_name_to_id[location_name], region)
            region.locations.append(location)

        victory_region = self.multiworld.get_region("Spirit Arena", self.player)
        victory_location = TunicLocation(self.player, "The Heir", None, victory_region)
        victory_location.place_locked_item(TunicItem("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        set_abilities(self.multiworld, self.player, self.random)
        set_region_rules(self.multiworld, self.player)
        set_location_rules(self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def fill_slot_data(self) -> Dict[str, any]:
        slot_data: Dict[str, any] = {
            "seed": self.random.randint(0, 2147483647),
            "start_with_sword": self.multiworld.start_with_sword[self.player].value,
            "keys_behind_bosses": self.multiworld.keys_behind_bosses[self.player].value,
            "sword_progression": self.multiworld.sword_progression[self.player].value,
            "ability_shuffling": self.multiworld.ability_shuffling[self.player].value,
            "hexagon_quest": self.multiworld.hexagon_quest[self.player].value,
            "fool_traps": self.multiworld.fool_traps[self.player].value
        }

        removed_item = ["Your Pocket", self.player]

        items = [
            "Magic Dagger",
            "Magic Wand",
            "Magic Orb",
            "Hero's Laurels",
            "Lantern",
            "Shotgun",
            "Scavenger Mask",
            "Shield",
            "Dath Stone",
            "Hourglass",
            "Old House Key",
            "Fortress Vault Key",
            "Hero Relic - ATT",
            "Hero Relic - DEF",
            "Hero Relic - POTION",
            "Hero Relic - HP",
            "Hero Relic - SP",
            "Hero Relic - MP",
        ]

        if self.multiworld.sword_progression[self.player].value:
            items.append("Sword Upgrade")
        else:
            items.extend(["Stick", "Sword"])

        if self.multiworld.hexagon_quest[self.player].value:
            golden_hexagons = self.multiworld.find_item_locations("Gold Hexagon", self.player, False)
            self.random.shuffle(golden_hexagons)
            hexagon_gold = golden_hexagons.pop()
            hexagon_gold2 = golden_hexagons.pop()
            hexagon_gold3 = golden_hexagons.pop()
            slot_data["Gold Hexagon"] = [hexagon_gold.name, hexagon_gold.player, hexagon_gold2.name,
                                         hexagon_gold2.player, hexagon_gold3.name, hexagon_gold3.player]
            if self.multiworld.ability_shuffling[self.player].value:
                slot_data["Hexagon Quest Prayer"] = hexagon_quest_abilities["prayer"]
                slot_data["Hexagon Quest Holy Cross"] = hexagon_quest_abilities["holy_cross"]
                slot_data["Hexagon Quest Ice Rod"] = hexagon_quest_abilities["ice_rod"]
        else:
            items.extend(["Red Hexagon", "Green Hexagon", "Blue Hexagon"])

        if self.multiworld.ability_shuffling[self.player].value and not self.multiworld.hexagon_quest[self.player].value:
            items.extend(["Pages 24-25 (Prayer)", "Pages 42-43 (Holy Cross)", "Pages 52-53 (Ice Rod)"])

        for start_item in self.multiworld.start_inventory_from_pool[self.player]:
            # If not all swords or sword upgrades are placed in start inventory, leave remaining ones for slot data
            if (start_item == "Sword" and self.multiworld.start_inventory_from_pool[self.player][start_item] < 3) or \
                    (start_item == "Sword Upgrade" and self.multiworld.start_inventory_from_pool[self.player][start_item] < 4):
                continue
            if start_item in items:
                items.remove(start_item)
                slot_data[start_item] = removed_item

        for item in items:
            data = []
            for found_item in self.multiworld.find_item_locations(item, self.player, False):
                data.append(found_item.item.location.name)
                data.append(found_item.item.location.player)
            slot_data[item] = data

        return slot_data
