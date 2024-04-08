from typing import Dict, List, Any

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from .items import item_name_to_id, item_table, item_name_groups, fool_tiers, filler_items, slot_data_item_names
from .locations import location_table, location_name_groups, location_name_to_id, hexagon_locations
from .rules import set_location_rules, set_region_rules, randomize_ability_unlocks, gold_hexagon
from .er_rules import set_er_location_rules
from .regions import tunic_regions
from .er_scripts import create_er_regions
from .er_data import portal_mapping
from .options import TunicOptions
from worlds.AutoWorld import WebWorld, World
from decimal import Decimal, ROUND_HALF_UP


class TunicWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the TUNIC Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["SilentDestroyer"]
        )
    ]
    theme = "grassFlowers"
    game = "TUNIC"


class TunicItem(Item):
    game: str = "TUNIC"


class TunicLocation(Location):
    game: str = "TUNIC"


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "TUNIC"
    web = TunicWeb()

    options: TunicOptions
    options_dataclass = TunicOptions
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    ability_unlocks: Dict[str, int]
    slot_data_items: List[TunicItem]
    tunic_portal_pairs: Dict[str, str]
    er_portal_hints: Dict[int, str]

    def generate_early(self) -> None:
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "TUNIC" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["TUNIC"]
                self.options.start_with_sword.value = passthrough["start_with_sword"]
                self.options.keys_behind_bosses.value = passthrough["keys_behind_bosses"]
                self.options.sword_progression.value = passthrough["sword_progression"]
                self.options.ability_shuffling.value = passthrough["ability_shuffling"]
                self.options.logic_rules.value = passthrough["logic_rules"]
                self.options.lanternless.value = passthrough["lanternless"]
                self.options.maskless.value = passthrough["maskless"]
                self.options.hexagon_quest.value = passthrough["hexagon_quest"]
                self.options.entrance_rando.value = passthrough["entrance_rando"]
                self.options.shuffle_ladders.value = passthrough["shuffle_ladders"]

    def create_item(self, name: str) -> TunicItem:
        item_data = item_table[name]
        return TunicItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        keys_behind_bosses = self.options.keys_behind_bosses
        hexagon_quest = self.options.hexagon_quest
        sword_progression = self.options.sword_progression

        tunic_items: List[TunicItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        for money_fool in fool_tiers[self.options.fool_traps]:
            items_to_create["Fool Trap"] += items_to_create[money_fool]
            items_to_create[money_fool] = 0

        if self.options.start_with_sword:
            self.multiworld.push_precollected(self.create_item("Sword"))

        if sword_progression:
            items_to_create["Stick"] = 0
            items_to_create["Sword"] = 0
        else:
            items_to_create["Sword Upgrade"] = 0

        if self.options.laurels_location:
            laurels = self.create_item("Hero's Laurels")
            if self.options.laurels_location == "6_coins":
                self.multiworld.get_location("Coins in the Well - 6 Coins", self.player).place_locked_item(laurels)
            elif self.options.laurels_location == "10_coins":
                self.multiworld.get_location("Coins in the Well - 10 Coins", self.player).place_locked_item(laurels)
            elif self.options.laurels_location == "10_fairies":
                self.multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", self.player).place_locked_item(laurels)
            self.slot_data_items.append(laurels)
            items_to_create["Hero's Laurels"] = 0

        if keys_behind_bosses:
            for rgb_hexagon, location in hexagon_locations.items():
                hex_item = self.create_item(gold_hexagon if hexagon_quest else rgb_hexagon)
                self.multiworld.get_location(location, self.player).place_locked_item(hex_item)
                self.slot_data_items.append(hex_item)
                items_to_create[rgb_hexagon] = 0
            items_to_create[gold_hexagon] -= 3

        # Filler items in the item pool
        available_filler: List[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
                                       item_table[filler].classification == ItemClassification.filler]
        
        # Remove filler to make room for other items
        def remove_filler(amount: int):
            for _ in range(0, amount):
                if not available_filler:
                    fill = "Fool Trap"
                else:
                    fill = self.random.choice(available_filler)
                if items_to_create[fill] == 0:
                    raise Exception("No filler items left to accommodate options selected. Turn down fool trap amount.")
                items_to_create[fill] -= 1
                if items_to_create[fill] == 0:
                    available_filler.remove(fill)

        if self.options.shuffle_ladders:
            ladder_count = 0
            for item_name, item_data in item_table.items():
                if item_data.item_group == "ladders":
                    items_to_create[item_name] = 1
                    ladder_count += 1
            remove_filler(ladder_count)

        if hexagon_quest:
            # Calculate number of hexagons in item pool
            hexagon_goal = self.options.hexagon_goal
            extra_hexagons = self.options.extra_hexagon_percentage
            items_to_create[gold_hexagon] += int((Decimal(100 + extra_hexagons) / 100 * hexagon_goal).to_integral_value(rounding=ROUND_HALF_UP))
            
            # Replace pages and normal hexagons with filler
            for replaced_item in list(filter(lambda item: "Pages" in item or item in hexagon_locations, items_to_create)):
                filler_name = self.get_filler_item_name()
                items_to_create[filler_name] += items_to_create[replaced_item]
                if items_to_create[filler_name] >= 1 and filler_name not in available_filler:
                    available_filler.append(filler_name)
                items_to_create[replaced_item] = 0

            remove_filler(items_to_create[gold_hexagon])

        if self.options.maskless:
            mask_item = TunicItem("Scavenger Mask", ItemClassification.useful, self.item_name_to_id["Scavenger Mask"], self.player)
            tunic_items.append(mask_item)
            items_to_create["Scavenger Mask"] = 0

        if self.options.lanternless:
            lantern_item = TunicItem("Lantern", ItemClassification.useful, self.item_name_to_id["Lantern"], self.player)
            tunic_items.append(lantern_item)
            items_to_create["Lantern"] = 0

        for item, quantity in items_to_create.items():
            for i in range(0, quantity):
                tunic_item: TunicItem = self.create_item(item)
                if item in slot_data_item_names:
                    self.slot_data_items.append(tunic_item)
                tunic_items.append(tunic_item)

        self.multiworld.itempool += tunic_items

    def create_regions(self) -> None:
        self.tunic_portal_pairs = {}
        self.er_portal_hints = {}
        self.ability_unlocks = randomize_ability_unlocks(self.random, self.options)
        
        # stuff for universal tracker support, can be ignored for standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "TUNIC" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["TUNIC"]
                self.ability_unlocks["Pages 24-25 (Prayer)"] = passthrough["Hexagon Quest Prayer"]
                self.ability_unlocks["Pages 42-43 (Holy Cross)"] = passthrough["Hexagon Quest Holy Cross"]
                self.ability_unlocks["Pages 52-53 (Icebolt)"] = passthrough["Hexagon Quest Icebolt"]

        # ladder rando uses ER with vanilla connections, so that we're not managing more rules files
        if self.options.entrance_rando or self.options.shuffle_ladders:
            portal_pairs = create_er_regions(self)
            if self.options.entrance_rando:
                # these get interpreted by the game to tell it which entrances to connect
                for portal1, portal2 in portal_pairs.items():
                    self.tunic_portal_pairs[portal1.scene_destination()] = portal2.scene_destination()
        else:
            # for non-ER, non-ladders
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
        if self.options.entrance_rando or self.options.shuffle_ladders:
            set_er_location_rules(self, self.ability_unlocks)
        else:
            set_region_rules(self, self.ability_unlocks)
            set_location_rules(self, self.ability_unlocks)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.options.entrance_rando:
            hint_data.update({self.player: {}})
            # all state seems to have efficient paths
            all_state = self.multiworld.get_all_state(True)
            all_state.update_reachable_regions(self.player)
            paths = all_state.path
            portal_names = [portal.name for portal in portal_mapping]
            for location in self.multiworld.get_locations(self.player):
                # skipping event locations
                if not location.address:
                    continue
                path_to_loc = []
                previous_name = "placeholder"
                name, connection = paths[location.parent_region]
                while connection != ("Menu", None):
                    name, connection = connection
                    # for LS entrances, we just want to give the portal name
                    if "(LS)" in name:
                        name, _ = name.split(" (LS) ")
                    # was getting some cases like Library Grave -> Library Grave -> other place
                    if name in portal_names and name != previous_name:
                        previous_name = name
                        path_to_loc.append(name)
                hint_text = " -> ".join(reversed(path_to_loc))
                if hint_text:
                    hint_data[self.player][location.address] = hint_text

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "seed": self.random.randint(0, 2147483647),
            "start_with_sword": self.options.start_with_sword.value,
            "keys_behind_bosses": self.options.keys_behind_bosses.value,
            "sword_progression": self.options.sword_progression.value,
            "ability_shuffling": self.options.ability_shuffling.value,
            "hexagon_quest": self.options.hexagon_quest.value,
            "fool_traps": self.options.fool_traps.value,
            "logic_rules": self.options.logic_rules.value,
            "lanternless": self.options.lanternless.value,
            "maskless": self.options.maskless.value,
            "entrance_rando": int(bool(self.options.entrance_rando.value)),
            "shuffle_ladders": self.options.shuffle_ladders.value,
            "Hexagon Quest Prayer": self.ability_unlocks["Pages 24-25 (Prayer)"],
            "Hexagon Quest Holy Cross": self.ability_unlocks["Pages 42-43 (Holy Cross)"],
            "Hexagon Quest Icebolt": self.ability_unlocks["Pages 52-53 (Icebolt)"],
            "Hexagon Quest Goal": self.options.hexagon_goal.value,
            "Entrance Rando": self.tunic_portal_pairs
        }

        for tunic_item in filter(lambda item: item.location is not None and item.code is not None, self.slot_data_items):
            if tunic_item.name not in slot_data:
                slot_data[tunic_item.name] = []
            if tunic_item.name == gold_hexagon and len(slot_data[gold_hexagon]) >= 6:
                continue
            slot_data[tunic_item.name].extend([tunic_item.location.name, tunic_item.location.player])

        for start_item in self.options.start_inventory_from_pool:
            if start_item in slot_data_item_names:
                if start_item not in slot_data:
                    slot_data[start_item] = []
                for i in range(0, self.options.start_inventory_from_pool[start_item]):
                    slot_data[start_item].extend(["Your Pocket", self.player])

        for plando_item in self.multiworld.plando_items[self.player]:
            if plando_item["from_pool"]:
                items_to_find = set()
                for item_type in [key for key in ["item", "items"] if key in plando_item]:
                    for item in plando_item[item_type]:
                        items_to_find.add(item)
                for item in items_to_find:
                    if item in slot_data_item_names:
                        slot_data[item] = []
                        for item_location in self.multiworld.find_item_locations(item, self.player):
                            slot_data[item].extend([item_location.name, item_location.player])

        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
