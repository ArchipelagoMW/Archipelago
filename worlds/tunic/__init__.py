from typing import Dict, List, Any

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from .Items import item_name_to_id, item_table, item_name_groups, fool_tiers, filler_items, slot_data_item_names
from .Locations import location_table, location_name_groups, location_name_to_id, hexagon_locations
from .Rules import set_location_rules, set_region_rules, randomize_ability_unlocks, gold_hexagon
from .Regions import tunic_regions
from .Options import tunic_options
from worlds.AutoWorld import WebWorld, World
from decimal import Decimal, ROUND_HALF_UP


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
    option_definitions = tunic_options
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    ability_unlocks: Dict[str, int]
    slot_data_items: List[TunicItem]

    def create_item(self, name: str) -> TunicItem:
        item_data = item_table[name]
        return TunicItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        keys_behind_bosses = self.multiworld.keys_behind_bosses[self.player].value
        hexagon_quest = self.multiworld.hexagon_quest[self.player].value
        sword_progression = self.multiworld.sword_progression[self.player].value

        items: List[TunicItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        for money_fool in fool_tiers[self.multiworld.fool_traps[self.player].value]:
            items_to_create["Fool Trap"] += items_to_create[money_fool]
            items_to_create[money_fool] = 0

        if sword_progression:
            items_to_create["Stick"] = 0
            items_to_create["Sword"] = 0
        else:
            items_to_create["Sword Upgrade"] = 0

        if keys_behind_bosses:
            for rgb_hexagon, location in hexagon_locations.items():
                hex_item = self.create_item(gold_hexagon if hexagon_quest else rgb_hexagon)
                self.multiworld.get_location(location, self.player).place_locked_item(hex_item)
                self.slot_data_items.append(hex_item)
                items_to_create[rgb_hexagon] = 0
            items_to_create[gold_hexagon] -= 3

        if hexagon_quest:
            # Calculate number of hexagons in item pool
            hexagon_goal = self.multiworld.hexagon_goal[self.player].value
            extra_hexagons = self.multiworld.extra_hexagon_percentage[self.player].value
            items_to_create[gold_hexagon] += int((Decimal(100 + extra_hexagons) / 100 * hexagon_goal).to_integral_value(rounding=ROUND_HALF_UP))

            # Replace pages and normal hexagons with filler
            for replaced_item in list(filter(lambda item: "Pages" in item or item in hexagon_locations, items_to_create)):
                items_to_create[self.get_filler_item_name()] += items_to_create[replaced_item]
                items_to_create[replaced_item] = 0

            # Filler items that are still in the item pool to swap out
            available_filler: List[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
                                           item_table[filler].classification == ItemClassification.filler]

            # Remove filler to make room for extra hexagons
            for i in range(0, items_to_create[gold_hexagon]):
                fill = self.random.choice(available_filler)
                items_to_create[fill] -= 1
                if items_to_create[fill] == 0:
                    available_filler.remove(fill)

        for item, quantity in items_to_create.items():
            for i in range(0, quantity):
                tunic_item: TunicItem = self.create_item(item)
                if item in slot_data_item_names:
                    self.slot_data_items.append(tunic_item)
                items.append(tunic_item)

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        for region_name in tunic_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in tunic_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exits)

        for location_name, location_id in self.location_name_to_id.items():
            region = self.multiworld.get_region(location_table[location_name].region, self.player)
            location = TunicLocation(self.player, location_name, location_id, region)
            region.locations.append(location)

        victory_region = self.multiworld.get_region("Spirit Arena", self.player)
        victory_location = TunicLocation(self.player, "The Heir", None, victory_region)
        victory_location.place_locked_item(TunicItem("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        self.ability_unlocks = randomize_ability_unlocks(self.random, self.multiworld.hexagon_quest[self.player].value, self.multiworld.hexagon_goal[self.player].value)
        set_region_rules(self.multiworld, self.player, self.ability_unlocks)
        set_location_rules(self.multiworld, self.player, self.ability_unlocks)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "seed": self.random.randint(0, 2147483647),
            "start_with_sword": self.multiworld.start_with_sword[self.player].value,
            "keys_behind_bosses": self.multiworld.keys_behind_bosses[self.player].value,
            "sword_progression": self.multiworld.sword_progression[self.player].value,
            "ability_shuffling": self.multiworld.ability_shuffling[self.player].value,
            "hexagon_quest": self.multiworld.hexagon_quest[self.player].value,
            "fool_traps": self.multiworld.fool_traps[self.player].value,
            "Hexagon Quest Prayer": self.ability_unlocks["Pages 24-25 (Prayer)"],
            "Hexagon Quest Holy Cross": self.ability_unlocks["Pages 42-43 (Holy Cross)"],
            "Hexagon Quest Ice Rod": self.ability_unlocks["Pages 52-53 (Ice Rod)"],
            "Hexagon Quest Goal": self.multiworld.hexagon_goal[self.player].value,
        }

        for tunic_item in filter(lambda item: item.location is not None, self.slot_data_items):
            if tunic_item.name not in slot_data:
                slot_data[tunic_item.name] = []
            if tunic_item.name == gold_hexagon and len(slot_data[gold_hexagon]) >= 6:
                continue
            slot_data[tunic_item.name].extend([tunic_item.location.name, tunic_item.location.player])

        for start_item in self.multiworld.start_inventory_from_pool[self.player]:
            if start_item in slot_data_item_names:
                if start_item not in slot_data:
                    slot_data[start_item] = []
                for i in range(0, self.multiworld.start_inventory_from_pool[self.player][start_item]):
                    slot_data[start_item].extend(["Your Pocket", self.player])

        return slot_data
