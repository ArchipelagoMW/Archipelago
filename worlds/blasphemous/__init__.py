from typing import Dict, TypedDict, List, Set, Any
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from worlds.generic.Rules import set_rule
from ..AutoWorld import World, WebWorld
from .Items import item_table, group_table, tears_set
from .Locations import location_table, shop_set
from .Exits import region_exit_table, exit_lookup_table
from .Rules import rules
from .Options import blasphemous_options
from . import Vanilla

import json
import os


class BlasphemousWeb(WebWorld):
    theme = ""
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Blasphemous randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class BlasphemousWorld(World):
    """
    description
    """

    game: str = "Blasphemous"
    web = BlasphemousWeb()
    base_id = 1909000
    data_version: 0

    item_name_to_id = {item["name"]: (1909000 + item_table.index(item)) for item in item_table}
    location_name_to_id = {loc["name"]: (1909000 + location_table.index(loc)) for loc in location_table}

    item_name_to_game_id = {item["name"]: item["game_id"] for item in item_table}
    location_name_to_game_id = {loc["name"]: loc["game_id"] for loc in location_table}

    item_name_groups = group_table
    option_definitions = blasphemous_options


    def set_rules(self):
        rules(self)


    def create_item(self, name: str) -> "BlasphemousItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - self.base_id

        return BlasphemousItem(name, item_table[id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return BlasphemousItem(event, ItemClassification.progression_skip_balancing, None, self.player)


    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(tears_set)

    
    def generate_basic(self):
        victory = Location(self.player, "His Holiness Escribar", None, self.multiworld.get_region("Deambulatory of His Holiness", self.player))
        victory.place_locked_item(self.create_event("Victory"))
        self.multiworld.get_region("Deambulatory of His Holiness", self.player).locations.append(victory)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


        pool = []

        for item in item_table:
            count = item["count"]
            if item["name"] in list(Vanilla.unrandomized_dict.values()):
                if item["name"] == "Verses Spun from Gold":
                    count -= 4
                else:
                    count -= 1
            if not self.multiworld.cherub_shuffle[self.player] and \
                item["name"] == "Child of Moonlight":
                    count = 0
            if not self.multiworld.life_shuffle[self.player] and \
                item["name"] == "Life Upgrade":
                    count = 0
            if not self.multiworld.fervour_shuffle[self.player] and \
                item["name"] == "Fervour Upgrade":
                    count = 0
            if not self.multiworld.sword_shuffle[self.player] and \
                item["name"] == "Mea Culpa Upgrade":
                    count = 0
            if not self.multiworld.blessing_shuffle[self.player] and \
                item["name"] in list(Vanilla.blessing_dict.values()):
                    count = 0
            if not self.multiworld.dungeon_shuffle[self.player] and \
                item["name"] in list(Vanilla.dungeon_dict.values()):
                    count -= 1
            if not self.multiworld.tirso_shuffle[self.player] and \
                item["name"] in list(Vanilla.tirso_dict.values()):
                    count -= 1
            if not self.multiworld.miriam_shuffle[self.player] and \
                item["name"] == "Cantina of the Blue Rose":
                    count = 0
            if not self.multiworld.redento_shuffle[self.player] and \
                item["name"] in list(Vanilla.redento_dict.values()):
                    count -= 1
            if not self.multiworld.jocinero_shuffle[self.player] and \
                item["name"] in list(Vanilla.jocinero_dict.values()):
                    count = 0
            if not self.multiworld.altasgracias_shuffle[self.player] and \
                item["name"] in list(Vanilla.altasgracias_dict.values()):
                    count = 0
            if not self.multiworld.tentudia_shuffle[self.player] and \
                item["name"] in list(Vanilla.tentudia_dict.values()):
                    count -= 1
            if not self.multiworld.gemino_shuffle[self.player] and \
                item["name"] in list(Vanilla.gemino_dict.values()):
                    count = 0
            if not self.multiworld.guilt_shuffle[self.player] and \
                item["name"] == "Weight of True Guilt":
                    count = 0
            if not self.multiworld.ossuary_shuffle[self.player] and \
                item["name"] in list(Vanilla.ossuary_dict.values()):
                    count -= 1
            if not self.multiworld.boss_shuffle[self.player] and \
                item["name"] in list(Vanilla.boss_dict.values()):
                    if item["name"] == "Tears of Atonement (18000)":
                        count -= 4
                    else:
                        count -= 1
            if not self.multiworld.wound_shuffle[self.player] and \
                item["name"] in list(Vanilla.wound_dict.values()):
                    count = 0
            if not self.multiworld.mask_shuffle[self.player] and \
                item["name"] in list(Vanilla.mask_dict.values()):
                    count = 0
            if not self.multiworld.herb_shuffle[self.player] and \
                item["name"] in list(Vanilla.herb_dict.values()):
                    count = 0
            if not self.multiworld.church_shuffle[self.player] and \
                item["name"] in list(Vanilla.church_dict.values()):
                    count = 0
            if not self.multiworld.shop_shuffle[self.player] and \
                item["name"] in list(Vanilla.shop_dict.values()):
                    count -= 1
            if not self.multiworld.thorn_shuffle[self.player] and \
                item["name"] == "Thorn":
                    count = 0
            if not self.multiworld.candle_shuffle[self.player] and \
                item["name"] in list(Vanilla.candle_dict.values()):
                    count = 0

            if count <= 0:
                continue
            else:
                for i in range(count):
                    pool.append(self.create_item(item["name"]))

        self.place_items_from_dict(Vanilla.unrandomized_dict)

        if not self.multiworld.cherub_shuffle[self.player]:
            self.place_items_from_set(Vanilla.cherub_set, "Child of Moonlight")

        if not self.multiworld.life_shuffle[self.player]:
            self.place_items_from_set(Vanilla.life_set, "Life Upgrade")

        if not self.multiworld.fervour_shuffle[self.player]:
            self.place_items_from_set(Vanilla.fervour_set, "Fervour Upgrade")

        if not self.multiworld.sword_shuffle[self.player]:
            self.place_items_from_set(Vanilla.sword_set, "Mea Culpa Upgrade")

        if not self.multiworld.blessing_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.blessing_dict)

        if not self.multiworld.dungeon_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.dungeon_dict)

        if not self.multiworld.tirso_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.tirso_dict)

        if not self.multiworld.miriam_shuffle[self.player]:
            self.multiworld.get_location("AtTotS: Miriam gift", self.player)\
                .place_locked_item(self.create_item("Cantina of the Blue Rose"))

        if not self.multiworld.redento_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.redento_dict)

        if not self.multiworld.jocinero_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.jocinero_dict)

        if not self.multiworld.altasgracias_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.altasgracias_dict)

        if not self.multiworld.tentudia_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.tentudia_dict)

        if not self.multiworld.gemino_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.gemino_dict)

        if not self.multiworld.guilt_shuffle[self.player]:
            self.multiworld.get_location("GotP: Guilt room", self.player)\
                .place_locked_item(self.create_item("Weight of True Guilt"))

        if not self.multiworld.ossuary_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.ossuary_dict)

        if not self.multiworld.boss_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.boss_dict)

        if not self.multiworld.wound_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.wound_dict)

        if not self.multiworld.mask_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.mask_dict)

        if not self.multiworld.herb_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.herb_dict)

        if not self.multiworld.church_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.church_dict)

        if not self.multiworld.shop_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.shop_dict)

        if not self.multiworld.thorn_shuffle[self.player]:
            self.place_items_from_set(Vanilla.thorn_set, "Thorn Upgrade")

        if not self.multiworld.candle_shuffle[self.player]:
            self.place_items_from_dict(Vanilla.candle_dict)

        self.multiworld.itempool += pool
        #for x in (range(len(self.multiworld.itempool))):
        #    print(self.multiworld.itempool[x])

    def place_items_from_set(self, location_set: Set[str], name: str):
        for loc in location_set:
            self.multiworld.get_location(loc, self.player)\
                .place_locked_item(self.create_item(name))

    
    def place_items_from_dict(self, option_dict: Dict[str, str]):
        for loc, item in option_dict.items():
            self.multiworld.get_location(loc, self.player)\
                .place_locked_item(self.create_item(item))


    def create_regions(self) -> None:
        
        type = RegionType.Generic
        player = self.player
        world = self.multiworld

        region_table: Dict[str, Region] = {
            "menu"    : Region("Menu", type, 
                            "Menu", player, world),
            "albero"  : Region("Albero", type, 
                            "Albero", player, world),
            "attots"  : Region("All the Tears of the Sea", type, 
                            "All the Tears of the Sea", player, world),
            "ar"      : Region("Archcathedral Rooftops", type, 
                            "Archcathedral Rooftops", player, world),
            "bottc"   : Region("Bridge of the Three Cavalries", type, 
                            "Bridge of the Three Cavalries", player, world),
            "botss"   : Region("Brotherhood of the Silent Sorrow", type, 
                            "Brotherhood of the Silent Sorrow", player, world),
            "coolotcv": Region("Convent of Our Lady of the Charred Visage", type, 
                            "Convent of Our Lady of the Charred Visage", player, world),
            "dohh"    : Region("Deambulatory of His Holiness", type, 
                            "Deambulatory of His Holiness", player, world),
            "dc"      : Region("Desecrated Cistern", type, 
                            "Desecrated Cistern", player, world),
            "eos"     : Region("Echoes of Salt", type, 
                            "Echoes of Salt", player, world),
            "ft"      : Region("Ferrous Tree", type,
                            "Ferrous Tree", player, world),
            "gotp"    : Region("Graveyard of the Peaks", type, 
                            "Graveyard of the Peaks", player, world),
            "ga"      : Region("Grievance Ascends", type, 
                            "Grievance Ascends", player, world),
            "hotd"    : Region("Hall of the Dawning", type, 
                            "Hall of the Dawning", player, world),
            "jondo"   : Region("Jondo", type, 
                            "Jondo", player, world),
            "kottw"   : Region("Knot of the Three Words", type, 
                            "Knot of the Three Words", player, world),
            "lotnw"   : Region("Library of the Negated Words", type, 
                            "Library of the Negated Words", player, world),
            "md"      : Region("Mercy Dreams", type, 
                            "Mercy Dreams", player, world),
            "mom"     : Region("Mother of Mothers", type, 
                            "Mother of Mothers", player, world),
            "moted"   : Region("Mountains of the Endless Dusk", type, 
                            "Mountains of the Endless Dusk", player, world),
            "mah"     : Region("Mourning and Havoc", type, 
                            "Mourning and Havoc", player, world),
            "potss"   : Region("Patio of the Silent Steps", type, 
                            "Patio of the Silent Steps", player, world),
            "petrous" : Region("Petrous", type, 
                            "Petrous", player, world),
            "thl"     : Region("The Holy Line", type, 
                            "The Holy Line", player, world),
            "trpots"  : Region("The Resting Place of the Sister", type, 
                            "The Resting Place of the Sister", player, world),
            "tsc"     : Region("The Sleeping Canvases", type, 
                            "The Sleeping Canvases", player, world),
            "wothp"   : Region("Wall of the Holy Prohibitions", type, 
                            "Wall of the Holy Prohibitions", player, world),
            "wotbc"   : Region("Wasteland of the Buried Churches", type, 
                            "Wasteland of the Buried Churches", player, world),
            "wotw"    : Region("Where Olive Trees Wither", type, 
                            "Where Olive Trees Wither", player, world),
            "dungeon" : Region("Dungeons", type,
                            "Dungeons", player, world)
        }

        room_table: Dict[str, Region] = {
            # Brotherhood of the Silent Sorrow
            "D17Z01S01": Region("BotSS: D17Z01S01", type, "BotSS: D17Z01S01", player, world),
            "D17Z01S02": Region("BotSS: D17Z01S02", type, "BotSS: D17Z01S02", player, world),
            "D17Z01S03": Region("BotSS: D17Z01S03", type, "BotSS: D17Z01S03", player, world),
            "D17Z01S04": Region("BotSS: D17Z01S04", type, "BotSS: D17Z01S04", player, world),
            "D17Z01S05": Region("BotSS: D17Z01S05", type, "BotSS: D17Z01S05", player, world),
            "D17Z01S06": Region("BotSS: D17Z01S06", type, "BotSS: D17Z01S06", player, world),
            "D17Z01S07": Region("BotSS: D17Z01S07", type, "BotSS: D17Z01S07", player, world),
            "D17Z01S08": Region("BotSS: D17Z01S08", type, "BotSS: D17Z01S08", player, world),
            "D17Z01S09": Region("BotSS: D17Z01S09", type, "BotSS: D17Z01S09", player, world),
            "D17Z01S10": Region("BotSS: D17Z01S10", type, "BotSS: D17Z01S10", player, world),
            "D17Z01S11": Region("BotSS: D17Z01S11", type, "BotSS: D17Z01S11", player, world),
            "D17Z01S12": Region("BotSS: D17Z01S12", type, "BotSS: D17Z01S12", player, world),
            "D17Z01S13": Region("BotSS: D17Z01S13", type, "BotSS: D17Z01S13", player, world),
            "D17Z01S14": Region("BotSS: D17Z01S14", type, "BotSS: D17Z01S14", player, world),
            "D17Z01S15": Region("BotSS: D17Z01S15", type, "BotSS: D17Z01S15", player, world),
            "D17BZ01S01[relic]": Region("BotSS: D17BZ01S01[relic]", type, "BotSS: D17BZ01S01[relic]", player, world),
            "D17BZ01S01[Front]": Region("BotSS: D17BZ01S01[Front]", type, "BotSS: D17BZ01S01[Front]", player, world),

            # The Holy Line
            "D01Z01S01": Region("THL: D01Z01S01", type, "THL: D01Z01S01", player, world),
            "D01Z01S02": Region("THL: D01Z01S02", type, "THL: D01Z01S02", player, world),
            "D01Z01S03": Region("THL: D01Z01S03", type, "THL: D01Z01S03", player, world),
            "D01Z01S07": Region("THL: D01Z01S07", type, "THL: D01Z01S07", player, world),

            # Albero
            "D01Z02S01": Region("Albero: D01Z02S01", type, "Albero: D01Z02S01", player, world),
            "D01Z02S02": Region("Albero: D01Z02S02", type, "Albero: D01Z02S02", player, world),
            "D01Z02S03": Region("Albero: D01Z02S03", type, "Albero: D01Z02S03", player, world),
            "D01Z02S04": Region("Albero: D01Z02S04", type, "Albero: D01Z02S04", player, world),
            "D01Z02S05": Region("Albero: D01Z02S05", type, "Albero: D01Z02S05", player, world),
            "D01Z02S06": Region("Albero: D01Z02S06", type, "Albero: D01Z02S06", player, world),
            "D01Z02S07": Region("Albero: D01Z02S07", type, "Albero: D01Z02S07", player, world),
            "D01BZ04S01": Region("Albero: D01BZ04S01", type, "Albero: D01BZ04S01", player, world),
            "D01BZ06S01": Region("Albero: D01BZ06S01", type, "Albero: D01BZ06S01", player, world),
            "D01BZ08S01": Region("Albero: D01BZ08S01", type, "Albero: D01BZ08S01", player, world),

            # Wasteland of the Buried Churches
            "D01Z03S01": Region("WotBC: D01Z03S01", type, "WotBC: D01Z03S01", player, world),
            "D01Z03S02": Region("WotBC: D01Z03S02", type, "WotBC: D01Z03S02", player, world),
            "D01Z03S03": Region("WotBC: D01Z03S03", type, "WotBC: D01Z03S03", player, world),
            "D01Z03S04": Region("WotBC: D01Z03S04", type, "WotBC: D01Z03S04", player, world),
            "D01Z03S05": Region("WotBC: D01Z03S05", type, "WotBC: D01Z03S05", player, world),
            "D01Z03S06": Region("WotBC: D01Z03S06", type, "WotBC: D01Z03S06", player, world),
            "D01Z03S07": Region("WotBC: D01Z03S07", type, "WotBC: D01Z03S07", player, world),

            # Mercy Dreams
            "D01Z04S01": Region("MD: D01Z04S01", type, "MD: D01Z04S01", player, world),
            "D01Z04S02": Region("MD: D01Z04S02", type, "MD: D01Z04S02", player, world),
            "D01Z04S03": Region("MD: D01Z04S03", type, "MD: D01Z04S03", player, world),
            "D01Z04S05": Region("MD: D01Z04S05", type, "MD: D01Z04S05", player, world),
            "D01Z04S06": Region("MD: D01Z04S06", type, "MD: D01Z04S06", player, world),
            "D01Z04S07": Region("MD: D01Z04S07", type, "MD: D01Z04S07", player, world),
            "D01Z04S08": Region("MD: D01Z04S08", type, "MD: D01Z04S08", player, world),
            "D01Z04S09": Region("MD: D01Z04S09", type, "MD: D01Z04S09", player, world),
            "D01Z04S10": Region("MD: D01Z04S10", type, "MD: D01Z04S10", player, world),
            "D01Z04S11": Region("MD: D01Z04S11", type, "MD: D01Z04S11", player, world),
            "D01Z04S12": Region("MD: D01Z04S12", type, "MD: D01Z04S12", player, world),
            "D01Z04S13": Region("MD: D01Z04S13", type, "MD: D01Z04S13", player, world),
            "D01Z04S14": Region("MD: D01Z04S14", type, "MD: D01Z04S14", player, world),
            "D01Z04S15": Region("MD: D01Z04S15", type, "MD: D01Z04S15", player, world),
            "D01Z04S16": Region("MD: D01Z04S16", type, "MD: D01Z04S16", player, world),
            "D01Z04S17": Region("MD: D01Z04S17", type, "MD: D01Z04S17", player, world),
            "D01Z04S18": Region("MD: D01Z04S18", type, "MD: D01Z04S18", player, world),
            "D01Z04S19": Region("MD: D01Z04S19", type, "MD: D01Z04S19", player, world),
            "D01BZ02S01": Region("MD: D01BZ02S01", type, "MD: D01BZ02S01", player, world),

            # Desecrated Cistern
            "D01Z05S01": Region("DC: D01Z05S01", type, "DC: D01Z05S01", player, world),
            "D01Z05S02": Region("DC: D01Z05S02", type, "DC: D01Z05S02", player, world),
            "D01Z05S03": Region("DC: D01Z05S03", type, "DC: D01Z05S03", player, world),
            "D01Z05S04": Region("DC: D01Z05S04", type, "DC: D01Z05S04", player, world),
            "D01Z05S05": Region("DC: D01Z05S05", type, "DC: D01Z05S05", player, world),
            "D01Z05S06": Region("DC: D01Z05S06", type, "DC: D01Z05S06", player, world),
            "D01Z05S07": Region("DC: D01Z05S07", type, "DC: D01Z05S07", player, world),
            "D01Z05S08": Region("DC: D01Z05S08", type, "DC: D01Z05S08", player, world),
            "D01Z05S09": Region("DC: D01Z05S09", type, "DC: D01Z05S09", player, world),
            "D01Z05S10": Region("DC: D01Z05S10", type, "DC: D01Z05S10", player, world),
            "D01Z05S11": Region("DC: D01Z05S11", type, "DC: D01Z05S11", player, world),
            "D01Z05S12": Region("DC: D01Z05S12", type, "DC: D01Z05S12", player, world),
            "D01Z05S13": Region("DC: D01Z05S13", type, "DC: D01Z05S13", player, world),
            "D01Z05S14": Region("DC: D01Z05S14", type, "DC: D01Z05S14", player, world),
            "D01Z05S15": Region("DC: D01Z05S15", type, "DC: D01Z05S15", player, world),
            "D01Z05S16": Region("DC: D01Z05S16", type, "DC: D01Z05S16", player, world),
            "D01Z05S17": Region("DC: D01Z05S17", type, "DC: D01Z05S17", player, world),
            "D01Z05S18": Region("DC: D01Z05S18", type, "DC: D01Z05S18", player, world),
            "D01Z05S19": Region("DC: D01Z05S19", type, "DC: D01Z05S19", player, world),
            "D01Z05S20": Region("DC: D01Z05S20", type, "DC: D01Z05S20", player, world),
            "D01Z05S21": Region("DC: D01Z05S21", type, "DC: D01Z05S21", player, world),
            "D01Z05S22": Region("DC: D01Z05S22", type, "DC: D01Z05S22", player, world),
            "D01Z05S23": Region("DC: D01Z05S23", type, "DC: D01Z05S23", player, world),
            "D01Z05S24": Region("DC: D01Z05S24", type, "DC: D01Z05S24", player, world),
            "D01Z05S25": Region("DC: D01Z05S25", type, "DC: D01Z05S25", player, world),
            "D01Z05S26": Region("DC: D01Z05S26", type, "DC: D01Z05S26", player, world),
            "D01Z05S27": Region("DC: D01Z05S27", type, "DC: D01Z05S27", player, world),
            "D01BZ05S01": Region("DC: D01BZ05S01", type, "DC: D01BZ05S01", player, world),

            # Petrous
            "D01Z06S01": Region("Petrous: D01Z06S01", type, "Petrous: D01Z06S01", player, world),
            "D01BZ07S01": Region("Petrous: D01BZ07S01", type, "Petrous: D01BZ07S01", player, world),

            # Where Olive Trees Wither
            "D02Z01S01": Region("WOTW: D02Z01S01", type, "WOTW: D02Z01S01", player, world),
            "D02Z01S02": Region("WOTW: D02Z01S02", type, "WOTW: D02Z01S02", player, world),
            "D02Z01S03": Region("WOTW: D02Z01S03", type, "WOTW: D02Z01S03", player, world),
            "D02Z01S04": Region("WOTW: D02Z01S04", type, "WOTW: D02Z01S04", player, world),
            "D02Z01S05": Region("WOTW: D02Z01S05", type, "WOTW: D02Z01S05", player, world),
            "D02Z01S06": Region("WOTW: D02Z01S06", type, "WOTW: D02Z01S06", player, world),
            "D02Z01S08": Region("WOTW: D02Z01S08", type, "WOTW: D02Z01S08", player, world),
            "D02Z01S09": Region("WOTW: D02Z01S09", type, "WOTW: D02Z01S09", player, world),

            # Graveyard of the Peaks
            "D02Z02S01": Region("GotP: D02Z02S01", type, "GotP: D02Z02S01", player, world),
            "D02Z02S02": Region("GotP: D02Z02S02", type, "GotP: D02Z02S02", player, world),
            "D02Z02S03": Region("GotP: D02Z02S03", type, "GotP: D02Z02S03", player, world),
            "D02Z02S04": Region("GotP: D02Z02S04", type, "GotP: D02Z02S04", player, world),
            "D02Z02S05": Region("GotP: D02Z02S05", type, "GotP: D02Z02S05", player, world),
            "D02Z02S06": Region("GotP: D02Z02S06", type, "GotP: D02Z02S06", player, world),
            "D02Z02S07": Region("GotP: D02Z02S07", type, "GotP: D02Z02S07", player, world),
            "D02Z02S08": Region("GotP: D02Z02S08", type, "GotP: D02Z02S08", player, world),
            "D02Z02S09": Region("GotP: D02Z02S09", type, "GotP: D02Z02S09", player, world),
            "D02Z02S10": Region("GotP: D02Z02S10", type, "GotP: D02Z02S10", player, world),
            "D02Z02S11": Region("GotP: D02Z02S11", type, "GotP: D02Z02S11", player, world),
            "D02Z02S12": Region("GotP: D02Z02S12", type, "GotP: D02Z02S12", player, world),
            "D02Z02S13": Region("GotP: D02Z02S13", type, "GotP: D02Z02S13", player, world),
            "D02Z02S14": Region("GotP: D02Z02S14", type, "GotP: D02Z02S14", player, world),
            "D02BZ02S01": Region("GotP: D02BZ02S01", type, "GotP: D02BZ02S01", player, world),

            # Convent of Our Lady of the Charred Visage
            "D02Z03S01": Region("CoOLotCV: D02Z03S01", type, "CoOLotCV: D02Z03S01", player, world),
            "D02Z03S02": Region("CoOLotCV: D02Z03S02", type, "CoOLotCV: D02Z03S02", player, world),
            "D02Z03S03": Region("CoOLotCV: D02Z03S03", type, "CoOLotCV: D02Z03S03", player, world),
            "D02Z03S05": Region("CoOLotCV: D02Z03S05", type, "CoOLotCV: D02Z03S05", player, world),
            "D02Z03S06": Region("CoOLotCV: D02Z03S06", type, "CoOLotCV: D02Z03S06", player, world),
            "D02Z03S07": Region("CoOLotCV: D02Z03S07", type, "CoOLotCV: D02Z03S07", player, world),
            "D02Z03S08": Region("CoOLotCV: D02Z03S08", type, "CoOLotCV: D02Z03S08", player, world),
            "D02Z03S09": Region("CoOLotCV: D02Z03S09", type, "CoOLotCV: D02Z03S09", player, world),
            "D02Z03S10": Region("CoOLotCV: D02Z03S10", type, "CoOLotCV: D02Z03S10", player, world),
            "D02Z03S11": Region("CoOLotCV: D02Z03S11", type, "CoOLotCV: D02Z03S11", player, world),
            "D02Z03S12": Region("CoOLotCV: D02Z03S12", type, "CoOLotCV: D02Z03S12", player, world),
            "D02Z03S13": Region("CoOLotCV: D02Z03S13", type, "CoOLotCV: D02Z03S13", player, world),
            "D02Z03S14": Region("CoOLotCV: D02Z03S14", type, "CoOLotCV: D02Z03S14", player, world),
            "D02Z03S15": Region("CoOLotCV: D02Z03S15", type, "CoOLotCV: D02Z03S15", player, world),
            "D02Z03S16": Region("CoOLotCV: D02Z03S16", type, "CoOLotCV: D02Z03S16", player, world),
            "D02Z03S17": Region("CoOLotCV: D02Z03S17", type, "CoOLotCV: D02Z03S17", player, world),
            "D02Z03S18": Region("CoOLotCV: D02Z03S18", type, "CoOLotCV: D02Z03S18", player, world),
            "D02Z03S19": Region("CoOLotCV: D02Z03S19", type, "CoOLotCV: D02Z03S19", player, world),
            "D02Z03S20": Region("CoOLotCV: D02Z03S20", type, "CoOLotCV: D02Z03S20", player, world),
            "D02Z03S21": Region("CoOLotCV: D02Z03S21", type, "CoOLotCV: D02Z03S21", player, world),
            "D02Z03S22": Region("CoOLotCV: D02Z03S22", type, "CoOLotCV: D02Z03S22", player, world),
            "D02Z03S23": Region("CoOLotCV: D02Z03S23", type, "CoOLotCV: D02Z03S23", player, world),
            "D02Z03S24": Region("CoOLotCV: D02Z03S24", type, "CoOLotCV: D02Z03S24", player, world),

            # Mountains of the Endless Dusk
            "D03Z01S01": Region("MotED: D03Z01S01", type, "MotED: D03Z01S01", player, world),
            "D03Z01S02": Region("MotED: D03Z01S02", type, "MotED: D03Z01S02", player, world),
            "D03Z01S03": Region("MotED: D03Z01S03", type, "MotED: D03Z01S03", player, world),
            "D03Z01S04": Region("MotED: D03Z01S04", type, "MotED: D03Z01S04", player, world),
            "D03Z01S05": Region("MotED: D03Z01S05", type, "MotED: D03Z01S05", player, world),
            "D03Z01S06": Region("MotED: D03Z01S06", type, "MotED: D03Z01S06", player, world),

            # Jondo
            "D03Z02S01": Region("Jondo: D03Z02S01", type, "Jondo: D03Z02S01", player, world),
            "D03Z02S02": Region("Jondo: D03Z02S02", type, "Jondo: D03Z02S02", player, world),
            "D03Z02S03": Region("Jondo: D03Z02S03", type, "Jondo: D03Z02S03", player, world),
            "D03Z02S04": Region("Jondo: D03Z02S04", type, "Jondo: D03Z02S04", player, world),
            "D03Z02S05": Region("Jondo: D03Z02S05", type, "Jondo: D03Z02S05", player, world),
            "D03Z02S06": Region("Jondo: D03Z02S06", type, "Jondo: D03Z02S06", player, world),
            "D03Z02S07": Region("Jondo: D03Z02S07", type, "Jondo: D03Z02S07", player, world),
            "D03Z02S08": Region("Jondo: D03Z02S08", type, "Jondo: D03Z02S08", player, world),
            "D03Z02S09": Region("Jondo: D03Z02S09", type, "Jondo: D03Z02S09", player, world),
            "D03Z02S10": Region("Jondo: D03Z02S10", type, "Jondo: D03Z02S10", player, world),
            "D03Z02S11": Region("Jondo: D03Z02S11", type, "Jondo: D03Z02S11", player, world),
            "D03Z02S12": Region("Jondo: D03Z02S12", type, "Jondo: D03Z02S12", player, world),
            "D03Z02S13": Region("Jondo: D03Z02S13", type, "Jondo: D03Z02S13", player, world),
            "D03Z02S14": Region("Jondo: D03Z02S14", type, "Jondo: D03Z02S14", player, world),
            "D03Z02S15": Region("Jondo: D03Z02S15", type, "Jondo: D03Z02S15", player, world),

            # Grievance Ascends
            "D03Z03S01": Region("GA: D03Z03S01", type, "GA: D03Z03S01", player, world),
            "D03Z03S02": Region("GA: D03Z03S02", type, "GA: D03Z03S02", player, world),
            "D03Z03S03": Region("GA: D03Z03S03", type, "GA: D03Z03S03", player, world),
            "D03Z03S04": Region("GA: D03Z03S04", type, "GA: D03Z03S04", player, world),
            "D03Z03S05": Region("GA: D03Z03S05", type, "GA: D03Z03S05", player, world),
            "D03Z03S06": Region("GA: D03Z03S06", type, "GA: D03Z03S06", player, world),
            "D03Z03S07": Region("GA: D03Z03S07", type, "GA: D03Z03S07", player, world),
            "D03Z03S08": Region("GA: D03Z03S08", type, "GA: D03Z03S08", player, world),
            "D03Z03S09": Region("GA: D03Z03S09", type, "GA: D03Z03S09", player, world),
            "D03Z03S10": Region("GA: D03Z03S10", type, "GA: D03Z03S10", player, world),
            "D03Z03S11": Region("GA: D03Z03S11", type, "GA: D03Z03S11", player, world),
            "D03Z03S12": Region("GA: D03Z03S12", type, "GA: D03Z03S12", player, world),
            "D03Z03S13": Region("GA: D03Z03S13", type, "GA: D03Z03S13", player, world),
            "D03Z03S14": Region("GA: D03Z03S14", type, "GA: D03Z03S14", player, world),
            "D03Z03S15": Region("GA: D03Z03S15", type, "GA: D03Z03S15", player, world),
            "D03Z03S16": Region("GA: D03Z03S16", type, "GA: D03Z03S16", player, world),
            "D03Z03S17": Region("GA: D03Z03S17", type, "GA: D03Z03S17", player, world),
            "D03Z03S18": Region("GA: D03Z03S18", type, "GA: D03Z03S18", player, world),
            "D03Z03S19": Region("GA: D03Z03S19", type, "GA: D03Z03S19", player, world),

            # Patio of the Silent Steps
            "D04Z01S01": Region("PotSS: D04Z01S01", type, "PotSS: D04Z01S01", player, world),
            "D04Z01S02": Region("PotSS: D04Z01S02", type, "PotSS: D04Z01S02", player, world),
            "D04Z01S03": Region("PotSS: D04Z01S03", type, "PotSS: D04Z01S03", player, world),
            "D04Z01S04": Region("PotSS: D04Z01S04", type, "PotSS: D04Z01S04", player, world),
            "D04Z01S05": Region("PotSS: D04Z01S05", type, "PotSS: D04Z01S05", player, world),
            "D04Z01S06": Region("PotSS: D04Z01S06", type, "PotSS: D04Z01S06", player, world),

            # Mother of Mothers
            "D04Z02S01": Region("MoM: D04Z02S01", type, "MoM: D04Z02S01", player, world),
            "D04Z02S02": Region("MoM: D04Z02S02", type, "MoM: D04Z02S02", player, world),
            "D04Z02S03": Region("MoM: D04Z02S03", type, "MoM: D04Z02S03", player, world),
            "D04Z02S04": Region("MoM: D04Z02S04", type, "MoM: D04Z02S04", player, world),
            "D04Z02S05": Region("MoM: D04Z02S05", type, "MoM: D04Z02S05", player, world),
            "D04Z02S06": Region("MoM: D04Z02S06", type, "MoM: D04Z02S06", player, world),
            "D04Z02S07": Region("MoM: D04Z02S07", type, "MoM: D04Z02S07", player, world),
            "D04Z02S08": Region("MoM: D04Z02S08", type, "MoM: D04Z02S08", player, world),
            "D04Z02S09": Region("MoM: D04Z02S09", type, "MoM: D04Z02S09", player, world),
            "D04Z02S10": Region("MoM: D04Z02S10", type, "MoM: D04Z02S10", player, world),
            "D04Z02S11": Region("MoM: D04Z02S11", type, "MoM: D04Z02S11", player, world),
            "D04Z02S12": Region("MoM: D04Z02S12", type, "MoM: D04Z02S12", player, world),
            "D04Z02S13": Region("MoM: D04Z02S13", type, "MoM: D04Z02S13", player, world),
            "D04Z02S14": Region("MoM: D04Z02S14", type, "MoM: D04Z02S14", player, world),
            "D04Z02S15": Region("MoM: D04Z02S15", type, "MoM: D04Z02S15", player, world),
            "D04Z02S16": Region("MoM: D04Z02S16", type, "MoM: D04Z02S16", player, world),
            "D04Z02S17": Region("MoM: D04Z02S17", type, "MoM: D04Z02S17", player, world),
            "D04Z02S19": Region("MoM: D04Z02S19", type, "MoM: D04Z02S19", player, world),
            "D04Z02S20": Region("MoM: D04Z02S20", type, "MoM: D04Z02S20", player, world),
            "D04Z02S21": Region("MoM: D04Z02S21", type, "MoM: D04Z02S21", player, world),
            "D04Z02S22": Region("MoM: D04Z02S22", type, "MoM: D04Z02S22", player, world),
            "D04Z02S23": Region("MoM: D04Z02S23", type, "MoM: D04Z02S23", player, world),
            "D04Z02S24": Region("MoM: D04Z02S24", type, "MoM: D04Z02S24", player, world),
            "D04Z02S25": Region("MoM: D04Z02S25", type, "MoM: D04Z02S25", player, world),
            "D04BZ02S01": Region("MoM: D04BZ02S01", type, "MoM: D04BZ02S01", player, world),

            # Knot of the Three Words
            "D04Z03S01": Region("KotTW: D04Z03S01", type, "KotTW: D04Z03S01", player, world),
            "D04Z03S02": Region("KotTW: D04Z03S02", type, "KotTW: D04Z03S02", player, world),

            # All the Tears of the Sea
            "D04Z04S01": Region("AtTotS: D04Z04S01", type, "AtTotS: D04Z04S01", player, world),
            "D04Z04S02": Region("AtTotS: D04Z04S02", type, "AtTotS: D04Z04S02", player, world),

            # Library of the Negated Words
            "D05Z01S01": Region("LotNW: D05Z01S01", type, "LotNW: D05Z01S01", player, world),
            "D05Z01S02": Region("LotNW: D05Z01S02", type, "LotNW: D05Z01S02", player, world),
            "D05Z01S03": Region("LotNW: D05Z01S03", type, "LotNW: D05Z01S03", player, world),
            "D05Z01S04": Region("LotNW: D05Z01S04", type, "LotNW: D05Z01S04", player, world),
            "D05Z01S05": Region("LotNW: D05Z01S05", type, "LotNW: D05Z01S05", player, world),
            "D05Z01S06": Region("LotNW: D05Z01S06", type, "LotNW: D05Z01S06", player, world),
            "D05Z01S07": Region("LotNW: D05Z01S07", type, "LotNW: D05Z01S07", player, world),
            "D05Z01S08": Region("LotNW: D05Z01S08", type, "LotNW: D05Z01S08", player, world),
            "D05Z01S09": Region("LotNW: D05Z01S09", type, "LotNW: D05Z01S09", player, world),
            "D05Z01S10": Region("LotNW: D05Z01S10", type, "LotNW: D05Z01S10", player, world),
            "D05Z01S11": Region("LotNW: D05Z01S11", type, "LotNW: D05Z01S11", player, world),
            "D05Z01S12": Region("LotNW: D05Z01S12", type, "LotNW: D05Z01S12", player, world),
            "D05Z01S13": Region("LotNW: D05Z01S13", type, "LotNW: D05Z01S13", player, world),
            "D05Z01S14": Region("LotNW: D05Z01S14", type, "LotNW: D05Z01S14", player, world),
            "D05Z01S15": Region("LotNW: D05Z01S15", type, "LotNW: D05Z01S15", player, world),
            "D05Z01S16": Region("LotNW: D05Z01S16", type, "LotNW: D05Z01S16", player, world),
            "D05Z01S17": Region("LotNW: D05Z01S17", type, "LotNW: D05Z01S17", player, world),
            "D05Z01S18": Region("LotNW: D05Z01S18", type, "LotNW: D05Z01S18", player, world),
            "D05Z01S19": Region("LotNW: D05Z01S19", type, "LotNW: D05Z01S19", player, world),
            "D05Z01S20": Region("LotNW: D05Z01S20", type, "LotNW: D05Z01S20", player, world),
            "D05Z01S21": Region("LotNW: D05Z01S21", type, "LotNW: D05Z01S21", player, world),
            "D05Z01S22": Region("LotNW: D05Z01S22", type, "LotNW: D05Z01S22", player, world),
            "D05Z01S23": Region("LotNW: D05Z01S23", type, "LotNW: D05Z01S23", player, world),
            "D05Z01S24": Region("LotNW: D05Z01S24", type, "LotNW: D05Z01S24", player, world),
            "D05BZ01S01": Region("LotNW: D05BZ01S01", type, "LotNW: D05BZ01S01", player, world),

            # The Sleeping Canvases
            "D05Z02S01": Region("TSC: D05Z02S01", type, "TSC: D05Z02S01", player, world),
            "D05Z02S02": Region("TSC: D05Z02S02", type, "TSC: D05Z02S02", player, world),
            "D05Z02S03": Region("TSC: D05Z02S03", type, "TSC: D05Z02S03", player, world),
            "D05Z02S04": Region("TSC: D05Z02S04", type, "TSC: D05Z02S04", player, world),
            "D05Z02S05": Region("TSC: D05Z02S05", type, "TSC: D05Z02S05", player, world),
            "D05Z02S06": Region("TSC: D05Z02S06", type, "TSC: D05Z02S06", player, world),
            "D05Z02S07": Region("TSC: D05Z02S07", type, "TSC: D05Z02S07", player, world),
            "D05Z02S08": Region("TSC: D05Z02S08", type, "TSC: D05Z02S08", player, world),
            "D05Z02S09": Region("TSC: D05Z02S09", type, "TSC: D05Z02S09", player, world),
            "D05Z02S10": Region("TSC: D05Z02S10", type, "TSC: D05Z02S10", player, world),
            "D05Z02S11": Region("TSC: D05Z02S11", type, "TSC: D05Z02S11", player, world),
            "D05Z02S12": Region("TSC: D05Z02S12", type, "TSC: D05Z02S12", player, world),
            "D05Z02S13": Region("TSC: D05Z02S13", type, "TSC: D05Z02S13", player, world),
            "D05Z02S14": Region("TSC: D05Z02S14", type, "TSC: D05Z02S14", player, world),
            "D05Z02S15": Region("TSC: D05Z02S15", type, "TSC: D05Z02S15", player, world),
            "D05BZ02S01": Region("TSC: D05BZ02S01", type, "TSC: D05BZ02S01", player, world),

            # Archcathedral Rooftops
            "D06Z01S01": Region("AR: D06Z01S01", type, "AR: D06Z01S01", player, world),
            "D06Z01S02": Region("AR: D06Z01S02", type, "AR: D06Z01S02", player, world),
            "D06Z01S03": Region("AR: D06Z01S03", type, "AR: D06Z01S03", player, world),
            "D06Z01S04": Region("AR: D06Z01S04", type, "AR: D06Z01S04", player, world),
            "D06Z01S05": Region("AR: D06Z01S05", type, "AR: D06Z01S05", player, world),
            "D06Z01S06": Region("AR: D06Z01S06", type, "AR: D06Z01S06", player, world),
            "D06Z01S07": Region("AR: D06Z01S07", type, "AR: D06Z01S07", player, world),
            "D06Z01S08": Region("AR: D06Z01S08", type, "AR: D06Z01S08", player, world),
            "D06Z01S09": Region("AR: D06Z01S09", type, "AR: D06Z01S09", player, world),
            "D06Z01S10": Region("AR: D06Z01S10", type, "AR: D06Z01S10", player, world),
            "D06Z01S11": Region("AR: D06Z01S11", type, "AR: D06Z01S11", player, world),
            "D06Z01S12": Region("AR: D06Z01S12", type, "AR: D06Z01S12", player, world),
            "D06Z01S13": Region("AR: D06Z01S13", type, "AR: D06Z01S13", player, world),
            "D06Z01S14": Region("AR: D06Z01S14", type, "AR: D06Z01S14", player, world),
            "D06Z01S15": Region("AR: D06Z01S15", type, "AR: D06Z01S15", player, world),
            "D06Z01S16": Region("AR: D06Z01S16", type, "AR: D06Z01S16", player, world),
            "D06Z01S17": Region("AR: D06Z01S17", type, "AR: D06Z01S17", player, world),
            "D06Z01S18": Region("AR: D06Z01S18", type, "AR: D06Z01S18", player, world),
            "D06Z01S19": Region("AR: D06Z01S19", type, "AR: D06Z01S19", player, world),
            "D06Z01S20": Region("AR: D06Z01S20", type, "AR: D06Z01S20", player, world),
            "D06Z01S21": Region("AR: D06Z01S21", type, "AR: D06Z01S21", player, world),
            "D06Z01S22": Region("AR: D06Z01S22", type, "AR: D06Z01S22", player, world),
            "D06Z01S23": Region("AR: D06Z01S23", type, "AR: D06Z01S23", player, world),
            "D06Z01S24": Region("AR: D06Z01S24", type, "AR: D06Z01S24", player, world),
            "D06Z01S25": Region("AR: D06Z01S25", type, "AR: D06Z01S25", player, world),
            "D06Z01S26": Region("AR: D06Z01S26", type, "AR: D06Z01S26", player, world),

            # Deambulatory of His Holiness
            "D07Z01S01": Region("DoHH: D07Z01S01", type, "DoHH: D07Z01S01", player, world),
            "D07Z01S02": Region("DoHH: D07Z01S02", type, "DoHH: D07Z01S02", player, world),
            "D07Z01S03": Region("DoHH: D07Z01S03", type, "DoHH: D07Z01S03", player, world),

            # Bridge of the Three Cavalries
            "D08Z01S01": Region("BotTC: D08Z01S01", type, "BotTC: D08Z01S01", player, world),
            "D08Z01S02": Region("BotTC: D08Z01S02", type, "BotTC: D08Z01S02", player, world),

            # Ferrous Tree
            "D08Z02S01": Region("FT: D08Z02S01", type, "FT: D08Z02S01", player, world),
            "D08Z02S02": Region("FT: D08Z02S02", type, "FT: D08Z02S02", player, world),
            "D08Z02S03": Region("FT: D08Z02S03", type, "FT: D08Z02S03", player, world),

            # Hall of the Dawning
            "D08Z03S01": Region("HotD: D08Z03S01", type, "HotD: D08Z03S01", player, world),
            "D08Z03S02": Region("HotD: D08Z03S02", type, "HotD: D08Z03S02", player, world),
            "D08Z03S03": Region("HotD: D08Z03S03", type, "HotD: D08Z03S03", player, world),

            # Wall of the Holy Prohibitions
            "D09Z01S01": Region("WotHP: D09Z01S01", type, "WotHP: D09Z01S01", player, world),
            "D09Z01S02": Region("WotHP: D09Z01S02", type, "WotHP: D09Z01S02", player, world),
            "D09Z01S03": Region("WotHP: D09Z01S03", type, "WotHP: D09Z01S03", player, world),
            "D09Z01S04": Region("WotHP: D09Z01S04", type, "WotHP: D09Z01S04", player, world),
            "D09Z01S05": Region("WotHP: D09Z01S05", type, "WotHP: D09Z01S05", player, world),
            "D09Z01S06": Region("WotHP: D09Z01S06", type, "WotHP: D09Z01S06", player, world),
            "D09Z01S07": Region("WotHP: D09Z01S07", type, "WotHP: D09Z01S07", player, world),
            "D09Z01S08": Region("WotHP: D09Z01S08", type, "WotHP: D09Z01S08", player, world),
            "D09Z01S09": Region("WotHP: D09Z01S09", type, "WotHP: D09Z01S09", player, world),
            "D09Z01S10": Region("WotHP: D09Z01S10", type, "WotHP: D09Z01S10", player, world),
            "D09Z01S11": Region("WotHP: D09Z01S11", type, "WotHP: D09Z01S11", player, world),
            "D09Z01S12": Region("WotHP: D09Z01S12", type, "WotHP: D09Z01S12", player, world),
            "D09BZ01S01[Cell1]": Region("WotHP: D09BZ01S01[Cell1]", type, "WotHP: D09BZ01S01[Cell1]", player, world),
            "D09BZ01S01[Cell2~3]": Region("WotHP: D09BZ01S01[Cell2~3]", type, "WotHP: D09BZ01S01[Cell2~3]", player, world),
            "D09BZ01S01[Cell4~5]": Region("WotHP: D09BZ01S01[Cell4~5]", type, "WotHP: D09BZ01S01[Cell4~5]", player, world),
            "D09BZ01S01[Cell6]": Region("WotHP: D09BZ01S01[Cell6]", type, "WotHP: D09BZ01S01[Cell6]", player, world),
            "D09BZ01S01[Cell7]": Region("WotHP: D09BZ01S01[Cell7]", type, "WotHP: D09BZ01S01[Cell7]", player, world),
            "D09BZ01S01[Cell8]": Region("WotHP: D09BZ01S01[Cell8]", type, "WotHP: D09BZ01S01[Cell8]", player, world),
            "D09BZ01S01[Cell9]": Region("WotHP: D09BZ01S01[Cell9]", type, "WotHP: D09BZ01S01[Cell9]", player, world),
            "D09BZ01S01[Cell10]": Region("WotHP: D09BZ01S01[Cell10]", type, "WotHP: D09BZ01S01[Cell10]", player, world),
            "D09BZ01S01[Cell11]": Region("WotHP: D09BZ01S01[Cell11]", type, "WotHP: D09BZ01S01[Cell11]", player, world),
            "D09BZ01S01[Cell12~13]": Region("WotHP: D09BZ01S01[Cell12~13]", type, "WotHP: D09BZ01S01[Cell12~13]", player, world),
            "D09BZ01S01[Cell14~15]": Region("WotHP: D09BZ01S01[Cell14~15]", type, "WotHP: D09BZ01S01[Cell14~15]", player, world),
            "D09BZ01S01[Cell16]": Region("WotHP: D09BZ01S01[Cell16]", type, "WotHP: D09BZ01S01[Cell16]", player, world),
            "D09BZ01S01[Cell17~18]": Region("WotHP: D09BZ01S01[Cell17~18]", type, "WotHP: D09BZ01S01[Cell17~18]", player, world),
            "D09BZ01S01[Cell19~20]": Region("WotHP: D09BZ01S01[Cell19~20]", type, "WotHP: D09BZ01S01[Cell19~20]", player, world),
            "D09BZ01S01[Cell21]": Region("WotHP: D09BZ01S01[Cell21]", type, "WotHP: D09BZ01S01[Cell21]", player, world),
            "D09BZ01S01[Cell22~23]": Region("WotHP: D09BZ01S01[Cell22~23]", type, "WotHP: D09BZ01S01[Cell22~23]", player, world),
            "D09BZ01S01[Cell24]": Region("WotHP: D09BZ01S01[Cell24]", type, "WotHP: D09BZ01S01[Cell24]", player, world),

            # Echoes of Salt
            "D20Z01S01": Region("EoS: D20Z01S01", type, "EoS: D20Z01S01", player, world),
            "D20Z01S02": Region("EoS: D20Z01S02", type, "EoS: D20Z01S02", player, world),
            "D20Z01S03": Region("EoS: D20Z01S03", type, "EoS: D20Z01S03", player, world),
            "D20Z01S04": Region("EoS: D20Z01S04", type, "EoS: D20Z01S04", player, world),
            "D20Z01S05": Region("EoS: D20Z01S05", type, "EoS: D20Z01S05", player, world),
            "D20Z01S06": Region("EoS: D20Z01S06", type, "EoS: D20Z01S06", player, world),
            "D20Z01S07": Region("EoS: D20Z01S07", type, "EoS: D20Z01S07", player, world),
            "D20Z01S08": Region("EoS: D20Z01S08", type, "EoS: D20Z01S08", player, world),
            "D20Z01S09": Region("EoS: D20Z01S09", type, "EoS: D20Z01S09", player, world),
            "D20Z01S10": Region("EoS: D20Z01S10", type, "EoS: D20Z01S10", player, world),
            "D20Z01S11": Region("EoS: D20Z01S11", type, "EoS: D20Z01S11", player, world),
            "D20Z01S12": Region("EoS: D20Z01S12", type, "EoS: D20Z01S12", player, world),
            "D20Z01S13": Region("EoS: D20Z01S13", type, "EoS: D20Z01S13", player, world),
            "D20Z01S14": Region("EoS: D20Z01S14", type, "EoS: D20Z01S14", player, world),

            # Mourning and Havoc
            "D20Z02S01": Region("MaH: D20Z02S01", type, "MaH: D20Z02S01", player, world),
            "D20Z02S02": Region("MaH: D20Z02S02", type, "MaH: D20Z02S02", player, world),
            "D20Z02S03": Region("MaH: D20Z02S03", type, "MaH: D20Z02S03", player, world),
            "D20Z02S04": Region("MaH: D20Z02S04", type, "MaH: D20Z02S04", player, world),
            "D20Z02S05": Region("MaH: D20Z02S05", type, "MaH: D20Z02S05", player, world),
            "D20Z02S06": Region("MaH: D20Z02S06", type, "MaH: D20Z02S06", player, world),
            "D20Z02S07": Region("MaH: D20Z02S07", type, "MaH: D20Z02S07", player, world),
            "D20Z02S08": Region("MaH: D20Z02S08", type, "MaH: D20Z02S08", player, world),
            "D20Z02S09": Region("MaH: D20Z02S09", type, "MaH: D20Z02S09", player, world),
            "D20Z02S10": Region("MaH: D20Z02S10", type, "MaH: D20Z02S10", player, world),
            "D20Z02S11": Region("MaH: D20Z02S11", type, "MaH: D20Z02S11", player, world),
            "D20Z02S12": Region("MaH: D20Z02S12", type, "MaH: D20Z02S12", player, world),

            # The Resting Place of the Sister
            "D20Z03S01": Region("TRPotS: D20Z03S01", type, "TRPotS: D20Z03S01", player, world),

            "dungeon": Region("Dungeons", type, "Dungeons", player, world),
        }

        for rname, reg in region_table.items():
            world.regions.append(reg)

            for ename, exits in region_exit_table.items():
                if ename == rname:
                    for i in exits:
                        ent = Entrance(player, i, reg)
                        reg.exits.append(ent)

                        for e, r in exit_lookup_table.items():
                            if i == e:
                                ent.connect(region_table[r])

        for loc in location_table:
            id = self.base_id + location_table.index(loc)
            region_table[loc["region"]].locations\
                .append(BlasphemousLocation(self.player, loc["name"], id, region_table[loc["region"]]))

    
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
        locations = []

        for loc in self.multiworld.get_filled_locations(self.player):
            if loc.name == "His Holiness Escribar":
                continue
            else:
                data = {
                    "id": self.location_name_to_game_id[loc.name],
                    "ap_id": loc.address,
                    "name": loc.item.name,
                    "player_name": self.multiworld.player_name[loc.item.player]
                }

                if loc.name in shop_set:
                    data["type"] = loc.item.classification.name

                locations.append(data)
    
        slot_data = {
            "locations": locations,
            "enemy_randomizer": self.multiworld.enemy_randomizer[self.player].value
        }
    
        return slot_data


    def generate_output(self, output_directory: str):
        slot_data: Dict[str, Any] = {}
        locations = []

        for loc in self.multiworld.get_filled_locations(self.player):
            if loc.name == "His Holiness Escribar":
                continue
            else:
                data = {
                    "id": self.location_name_to_game_id[loc.name],
                    "ap_id": loc.address,
                    "name": loc.item.name,
                    "player_name": self.multiworld.player_name[loc.item.player]
                }

                if loc.name in shop_set:
                    data["type"] = loc.item.classification.name

                locations.append(data)
    
        slot_data = {
            "locations": locations,
            "enemy_randomizer": self.multiworld.enemy_randomizer[self.player].value
        }
    
        filename = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.player_name[self.player]}.json"
        with open(os.path.join(output_directory, filename), 'w') as outfile:
            json.dump(slot_data, outfile)


class BlasphemousItem(Item):
    game: str = "Blasphemous"


class BlasphemousLocation(Location):
    game: str = "Blasphemous"