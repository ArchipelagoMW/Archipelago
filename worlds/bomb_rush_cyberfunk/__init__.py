from typing import Any, Dict
from BaseClasses import MultiWorld, Region, Location, Item, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table, BRCType
from .Locations import location_table, event_table
from .Regions import region_exits
from .Rules import rules
from .Options import BombRushCyberfunkOptions, StartStyle


class BombRushCyberfunkWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Bomb Rush Cyberfunk randomizer and connecting to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class BombRushCyberfunkWorld(World):
    """Bomb Rush Cyberfunk is 1 second per second of advanced funkstyle. Battle rival crews and dispatch militarized 
    police to conquer the five boroughs of New Amsterdam. Become All City."""

    game = "Bomb Rush Cyberfunk"
    web = BombRushCyberfunkWeb()

    item_name_to_id = {item["name"]: (base_id + index) for index, item in enumerate(item_table)}
    item_name_to_type = {item["name"]: item["type"] for item in item_table}
    location_name_to_id = {loc["name"]: (base_id + index) for index, loc in enumerate(location_table)}

    item_name_groups = group_table
    options_dataclass = BombRushCyberfunkOptions
    options: BombRushCyberfunkOptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super(BombRushCyberfunkWorld, self).__init__(multiworld, player)
        self.item_classification: Dict[BRCType, ItemClassification] = {
            BRCType.Music: ItemClassification.filler,
            BRCType.GraffitiM: ItemClassification.progression,
            BRCType.GraffitiL: ItemClassification.progression,
            BRCType.GraffitiXL: ItemClassification.progression,
            BRCType.Outfit: ItemClassification.filler,
            BRCType.Character: ItemClassification.progression,
            BRCType.REP: ItemClassification.progression_skip_balancing,
            BRCType.Camera: ItemClassification.progression
        }

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and "REP" in item.name:
            rep: int = int(item.name[0:len(item.name)-4])
            state.prog_items[item.player]["rep"] += rep
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and "REP" in item.name:
            rep: int = int(item.name[0:len(item.name)-4])
            state.prog_items[item.player]["rep"] -= rep
        return change

    def set_rules(self):
        rules(self)

    def get_item_classification(self, item_type: BRCType) -> ItemClassification:
        classification = ItemClassification.filler
        if item_type in self.item_classification.keys():
            classification = self.item_classification[item_type]

        return classification

    def create_item(self, name: str) -> "BombRushCyberfunkItem":
        item_id: int = self.item_name_to_id[name]
        item_type: BRCType = self.item_name_to_type[name]
        classification = self.get_item_classification(item_type)

        return BombRushCyberfunkItem(name, classification, item_id, self.player)

    def create_event(self, event: str) -> "BombRushCyberfunkItem":
        return BombRushCyberfunkItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        item = self.random.choice(item_table)

        while self.get_item_classification(item["type"]) == ItemClassification.progression:
            item = self.random.choice(item_table)

        return item["name"]

    def generate_early(self):
        if self.options.starting_movestyle == StartStyle.option_skateboard:
            self.item_classification[BRCType.Skateboard] = ItemClassification.filler
        else:
            self.item_classification[BRCType.Skateboard] = ItemClassification.progression

        if self.options.starting_movestyle == StartStyle.option_inline_skates:
            self.item_classification[BRCType.InlineSkates] = ItemClassification.filler
        else:
            self.item_classification[BRCType.InlineSkates] = ItemClassification.progression
        
        if self.options.starting_movestyle == StartStyle.option_bmx:
            self.item_classification[BRCType.BMX] = ItemClassification.filler
        else:
            self.item_classification[BRCType.BMX] = ItemClassification.progression

    def create_items(self):
        rep_locations: int = 87
        if self.options.skip_polo_photos:
            rep_locations -= 17

        self.options.total_rep.round_to_nearest_step()
        rep_counts = self.options.total_rep.get_rep_item_counts(self.random, rep_locations)
        #print(sum([8*rep_counts[0], 16*rep_counts[1], 24*rep_counts[2], 32*rep_counts[3], 48*rep_counts[4]]), \
        #    rep_counts)

        pool = []

        for item in item_table:
            if "REP" in item["name"]:
                count: int = 0

                if item["name"] == "8 REP":
                    count = rep_counts[0]
                elif item["name"] == "16 REP":
                    count = rep_counts[1]
                elif item["name"] == "24 REP":
                    count = rep_counts[2]
                elif item["name"] == "32 REP":
                    count = rep_counts[3]
                elif item["name"] == "48 REP":
                    count = rep_counts[4]

                if count > 0:
                    for _ in range(count):
                        pool.append(self.create_item(item["name"]))
            else:
                pool.append(self.create_item(item["name"]))

        self.multiworld.itempool += pool

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player

        menu = Region("Menu", player, multiworld)
        multiworld.regions.append(menu)

        for n in region_exits:
            multiworld.regions += [Region(n, player, multiworld)]

        menu.add_exits({"Hideout": "New Game"})

        for n in region_exits:
            self.get_region(n).add_exits(region_exits[n])

        for index, loc in enumerate(location_table):
            if self.options.skip_polo_photos and "Polo" in loc["game_id"]:
                continue
            stage: Region = self.get_region(loc["stage"])
            stage.add_locations({loc["name"]: base_id + index})

        for e in event_table:
            stage: Region = self.get_region(e["stage"])
            event = BombRushCyberfunkLocation(player, e["name"], None, stage)
            event.show_in_spoiler = False
            event.place_locked_item(self.create_event(e["item"]))
            stage.locations += [event]

        multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options

        slot_data: Dict[str, Any] = {
            "locations": {loc["game_id"]: (base_id + index) for index, loc in enumerate(location_table)},
            "logic": options.logic.value,
            "skip_intro": bool(options.skip_intro.value),
            "skip_dreams": bool(options.skip_dreams.value),
            "skip_statue_hands": bool(options.skip_statue_hands.value),
            "total_rep": options.total_rep.value,
            "extra_rep_required": bool(options.extra_rep_required.value),
            "starting_movestyle": options.starting_movestyle.value,
            "limited_graffiti": bool(options.limited_graffiti.value),
            "small_graffiti_uses": options.small_graffiti_uses.value,
            "skip_polo_photos": bool(options.skip_polo_photos.value),
            "dont_save_photos": bool(options.dont_save_photos.value),
            "score_difficulty": int(options.score_difficulty.value),
            "damage_multiplier": options.damage_multiplier.value,
            "death_link": bool(options.death_link.value)
        }

        return slot_data


class BombRushCyberfunkItem(Item):
    game: str = "Bomb Rush Cyberfunk"


class BombRushCyberfunkLocation(Location):
    game: str = "Bomb Rush Cyberfunk"
