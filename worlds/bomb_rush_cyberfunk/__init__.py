from typing import Any, Dict
from BaseClasses import MultiWorld, Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table, postgame_items, BRCType
from .Locations import location_table, event_table
from .Regions import region_names, region_exits, BRCStage
from .Rules import rules
from .Options import BombRushCyberfunkOptions, StartStyle


class BombRushCyberfunkWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guite to setting up Bomb Rush Cyberfunk randomizer and connecting to an Archipelago Multiworld",
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
            BRCType.Outfit: ItemClassification.filler,
            BRCType.Character: ItemClassification.progression,
            BRCType.REP: ItemClassification.progression_skip_balancing,
            BRCType.Camera: ItemClassification.progression
        }
        self.selectedM: str
        self.selectedL: str
        self.selectedXL: str


    def set_rules(self):
        rules(self)


    def get_item_classification(self, name: str, item_type: BRCType) -> ItemClassification:
        classification = ItemClassification.filler
        if item_type in self.item_classification.keys():
            classification = self.item_classification[item_type]
        elif name in group_table["girl"]:
            classification = ItemClassification.progression
        elif item_type == BRCType.GraffitiM:
            if name == self.selectedM or self.options.limited_graffiti:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
        elif item_type == BRCType.GraffitiL:
            if name == self.selectedL or self.options.limited_graffiti:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
        elif item_type == BRCType.GraffitiXL:
            if name == self.selectedXL or self.options.limited_graffiti:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler

        return classification


    def create_item(self, name: str) -> "BombRushCyberfunkItem":
        item_id: int = self.item_name_to_id[name]
        item_type: BRCType = self.item_name_to_type[name]
        classification = self.get_item_classification(name, item_type)

        return BombRushCyberfunkItem(name, classification, item_id, self.player)


    def create_event(self, event: str) -> "BombRushCyberfunkItem":
        return BombRushCyberfunkItem(event, ItemClassification.progression_skip_balancing, None, self.player)
    

    def get_filler_item_name(self) -> str:
        item = self.random.choice(item_table)

        while self.get_item_classification(item["name"], item["type"]) == ItemClassification.progression:
            item = self.random.choice(item_table)

        return item["name"]


    def generate_early(self):
        grafM = group_table["graffitim"]
        grafL = group_table["graffitil"]
        grafXL = group_table["graffitixl"]

        for item in postgame_items:
            if item in grafM:
                grafM.remove(item)
            elif item in grafL:
                grafL.remove(item)
            elif item in grafXL:
                grafXL.remove(item)

        self.selectedM = self.random.choice(grafM)
        self.selectedL = self.random.choice(grafL)
        self.selectedXL = self.random.choice(grafXL)

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
        self.options.total_rep.round_to_nearest_step()
        rep_counts = self.options.total_rep.get_rep_item_counts(self.multiworld.random, 87)
        #print(sum([8*rep_counts[0], 16*rep_counts[1], 24*rep_counts[2], 32*rep_counts[3], 48*rep_counts[4]]), \
        #    rep_counts)

        pool = []

        for item in item_table:
            if item["name"] in postgame_items:
                continue
            
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


    def get_stage(self, stage: BRCStage, player: int) -> Region:
        return self.multiworld.get_region(region_names[stage], player)


    def create_regions(self):
        world = self.multiworld
        player = self.player

        menu = Region("Menu", player, world)
        world.regions.append(menu)

        for _, n in region_names.items():
            world.regions += [Region(n, player, world)]

        menu.add_exits({"Hideout": "New Game"})

        for r, e in region_exits.items():
            exits = {region_names[ex] for ex in region_exits[r]}
            self.get_stage(r, player).add_exits(exits)

        for index, loc in enumerate(location_table):
            stage: Region = self.get_stage(loc["stage"], player)
            stage.add_locations({loc["name"]: base_id + index})
            if self.options.skip_polo_photos and "Polo" in loc["name"]:
                self.options.exclude_locations.value.add(loc["name"])

        for e in event_table:
            stage: Region = self.get_stage(loc["stage"], player)
            event = BombRushCyberfunkLocation(player, e["name"], None, stage)
            event.show_in_spoiler = False
            event.place_locked_item(self.create_event(e["item"]))
            stage.locations += [event]

        world.completion_condition[player] = lambda state: state.has("Victory", player)

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