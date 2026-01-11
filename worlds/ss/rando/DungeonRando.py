from typing import TYPE_CHECKING
from copy import deepcopy

from Options import OptionError
from Fill import FillError

from ..Locations import LOCATION_TABLE
from ..Items import ITEM_TABLE
from ..Options import SSOptions
from ..Constants import *

from ..logic.Logic import ALL_REQUIREMENTS

if TYPE_CHECKING:
    from .. import SSWorld


class DungeonRando:
    """
    Class handles required dungeons.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiword = world.multiworld

        self.required_dungeons: list[str] = []
        self.banned_dungeons: list[str] = []
        self.required_dungeon_checks: list[str] = []

        self.sky_keep_required: bool = False
        # Since `required_dungeons` and `banned_dungeons` only include the 6 main
        # dungeons, use this to determine if sky keep is required or not

        self.key_handler: DungeonKeyHandler = DungeonKeyHandler(self.world)

    def randomize_required_dungeons(self) -> None:
        """
        Randomize required dungeons based on player's options
        """

        self.num_required_dungeons = self.world.options.required_dungeon_count.value
        main_dungeons = list(DUNGEON_FINAL_CHECKS.keys())
        self.world.random.shuffle(main_dungeons)

        if self.num_required_dungeons > 6 or self.num_required_dungeons < 0:
            raise OptionError("Required dungeon count must be between 0 and 6.")

        # Randomize required dungeons
        self.required_dungeons.extend(
            self.world.random.sample(
                main_dungeons, k=self.num_required_dungeons
            )
        )
        self.required_dungeons = sorted(self.required_dungeons, key=lambda i: DUNGEON_LIST.index(i))

        self.required_dungeon_checks.extend(
            [
                chk
                for dun, chk in DUNGEON_FINAL_CHECKS.items()
                if dun in self.required_dungeons
            ]
        )
        
        self.banned_dungeons.extend(
            [
                dun
                for dun in main_dungeons
                if dun not in self.required_dungeons
            ]
        )

        self.sky_keep_required = self.world.options.triforce_required and self.world.options.triforce_shuffle != "anywhere"

        self.key_handler.set_progress_dungeons(self.required_dungeons)


class DungeonKeyHandler:
    """
    Class handles key placement for dungeon maps, small keys, and boss keys.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.all_maps: dict[str, str] = {}
        self.all_skeys: dict[str, list] = {}
        self.all_bkeys: dict[str, str] = {}

        self.start_maps: list[str] = []
        self.start_skeys: list[str] = []
        self.start_bkeys: list[str] = []

        self.map_placement: dict[str, str] = {}
        self.skey_placement: dict[str, str] = {}
        self.bkey_placement: dict[str, str] = {}

        for dun in DUNGEON_LIST:
            self.all_maps[dun] = f"{dun} Map"
            if dun != "Earth Temple":
                self.all_skeys[dun] = [f"{dun} Small Key"] * ITEM_TABLE[f"{dun} Small Key"].quantity
            if dun != "Sky Keep":
                self.all_bkeys[dun] = f"{dun} Boss Key"

    def set_progress_dungeons(self, req_dun) -> None:
        if self.world.options.empty_unrequired_dungeons:
            self.progression_dungeons = deepcopy(req_dun)
            if self.world.options.triforce_required and self.world.options.triforce_shuffle != "anywhere":
                self.progression_dungeons.append("Sky Keep")
        else:
            self.progression_dungeons = deepcopy(DUNGEON_LIST)

    def set_starting_keys(self) -> None:
        self.start_maps.extend([itm for itm in self.world.starting_items if ITEM_TABLE[itm].type == "Map"])
        self.start_skeys.extend([itm for itm in self.world.starting_items if ITEM_TABLE[itm].type == "Small Key"])
        self.start_bkeys.extend([itm for itm in self.world.starting_items if ITEM_TABLE[itm].type == "Boss Key"])
        
    def place_dungeon_maps(self) -> list[str]:
        """
        Places dungeon maps based on options.
        """
        placed = []
        locs_placeable = {}
        if self.world.options.map_mode == "start_with":
            raise FillError("Tried to place maps, but option is start with.")
        elif self.world.options.map_mode == "vanilla":
            for loc, data in LOCATION_TABLE.items():
                if data.vanilla_item is None:
                    continue
                if "Map" in data.vanilla_item:
                    if data.vanilla_item in self.start_maps:
                        continue
                    self.world.get_location(loc).place_locked_item(self.world.create_item(data.vanilla_item))
                    placed.append(data.vanilla_item)
            return placed
        elif self.world.options.map_mode == "own_dungeon_restricted":
            for dun in self.all_maps.keys():
                locs_placeable[dun] = []
                for loc in self.multiworld.get_locations(self.world.player):
                    if self.world.region_to_hint_region(loc.parent_region) == dun and loc.item is None:
                        if (
                            loc.name in DUNGEON_HC_CHECKS.values()
                            or loc.name in DUNGEON_FINAL_CHECKS.values()
                            or loc.name == "Skyview - Rupee on Spring Pillar"
                            or loc.item
                        ):
                            continue
                        locs_placeable[dun].append(tuple([loc.name, loc.player]))
        elif self.world.options.map_mode == "own_dungeon_unrestricted":
            for dun in self.all_maps.keys():
                locs_placeable[dun] = []
                for loc in self.multiworld.get_locations(self.world.player):
                    if self.world.region_to_hint_region(loc.parent_region) == dun and loc.item is None:
                        if loc.item:
                            continue
                        locs_placeable[dun].append(tuple([loc.name, loc.player]))
        elif self.world.options.map_mode == "anywhere":
            return []
        for dun, map_item in self.all_maps.items():
            if map_item in self.start_maps:
                continue
            if len(locs_placeable[dun]) == 0:
                raise FillError(f"Could not find a location to place map: {map_item}")
            loc_to_place = self.world.random.choice(locs_placeable[dun])
            self.world.get_location(loc_to_place[0]).place_locked_item(self.world.create_item(map_item))
            placed.append(map_item)

        return placed
    
    def place_small_keys(self) -> list[str]:
        """
        Places small keys based on options.
        """
        placed = []
        locs_placeable = {}
        if self.world.options.small_key_mode == "vanilla":
            for dun, skey_items in self.all_skeys.items():
                dun_start_skeys = self.start_skeys.count(skey_items[0])
                for i, skey in enumerate(skey_items):
                    if i < dun_start_skeys:
                        continue
                    locs_placeable = [
                        loc for loc in KEY_PLACEMENTS[dun][i]
                        if LOCATION_TABLE[loc].vanilla_item == skey
                        and self.world.get_location(loc).item is None
                    ]
                    self.world.get_location(locs_placeable.pop()).place_locked_item(self.world.create_item(skey))
                    placed.append(skey)
            return placed
        elif self.world.options.small_key_mode == "own_dungeon":
            locs_placeable = deepcopy(KEY_PLACEMENTS)
            for dun, keydata in locs_placeable.items():
                if dun in self.progression_dungeons:
                    for i, locs in keydata.items():
                        locs_placeable[dun][i] = [(loc, self.world.player) for loc in locs if loc not in self.world.nonprogress_locations and not self.world.get_location(loc).item]
                else:
                    for i, locs in keydata.items():
                        locs_placeable[dun][i] = [(loc, self.world.player) for loc in locs if not self.world.get_location(loc).item]
        elif self.world.options.small_key_mode == "anywhere":
            return []
        for dun, skey_items in self.all_skeys.items():
            dun_start_skeys = self.start_skeys.count(skey_items[0])
            if dun not in locs_placeable:
                if dun == "Lanayru Caves":
                    continue
                raise FillError(f"Tried to fill unknown dungeon with small keys: {dun}")
            for i, skey in enumerate(skey_items):
                if i < dun_start_skeys:
                    continue
                if len(locs_placeable[dun][i]) == 0:
                    raise FillError(f"Could not find a location to place small key: {skey}")
                loc_to_place = self.world.random.choice(locs_placeable[dun][i])
                self.world.get_location(loc_to_place[0]).place_locked_item(self.world.create_item(skey))
                for keyindex in locs_placeable[dun].keys():
                    # Only remove locations from pools including and after the current one
                    if keyindex < i:
                        continue
                    locs_placeable[dun][keyindex].remove(loc_to_place)
                placed.append(skey)

        return placed
    
    def place_caves_key(self) -> list[str]:
        """
        Places lanayru caves key based on options.
        """
        placed = []
        locs_placeable = []
        if self.world.options.lanayru_caves_small_key == "start_with":
            raise FillError("Tried to place caves key, but option is start with.")
        elif self.world.options.lanayru_caves_small_key == "caves":
            # Will also make sure that lanayru starting statue is not in sand sea
            locs_placeable.extend([
                loc for loc in ["Lanayru Caves - Chest", "Lanayru Caves - Golo's Gift"]
                if self.world.get_location(loc).item is None
            ])
        elif self.world.options.lanayru_caves_small_key == "lanayru":
            # Let's check to see where the starting statue is
            # We MUST place the small key on that side of caves
            if self.world.entrances.starting_statues["Lanayru Province"][0] in [
                "Lanayru Sand Sea Docks - Statue Entrance",
                "Pirate Stronghold - Statue Entrance",
                "Shipyard - Statue Entrance",
                "Skipper's Retreat - Statue Entrance",
            ]:
                # In this case, we must place the key in sand sea
                locs_placeable.extend([
                    loc for loc, data in LOCATION_TABLE.items()
                    if data.region in ["Lanayru Sand Sea"]
                    and self.world.get_location(loc).item is None
                ])
            else:
                # Otherwise, place the key anywhere except sand sea
                locs_placeable.extend([
                    loc for loc, data in LOCATION_TABLE.items()
                    if data.region in ["Lanayru Mine", "Lanayru Desert", "Lanayru Caves", "Lanayru Gorge"]
                    and self.world.get_location(loc).item is None
                ])
        elif self.world.options.lanayru_caves_small_key == "anywhere":
            return []
        
        if len(locs_placeable) == 0:
            raise FillError(f"Could not find a location to place lanayru caves small key")
        loc_to_place = self.world.random.choice(locs_placeable)
        self.world.get_location(loc_to_place).place_locked_item(self.world.create_item("Lanayru Caves Small Key"))
        placed.append("Lanayru Caves Small Key")
        
        return placed

    def place_boss_keys(self) -> list[str]:
        """
        Places boss keys based on options.
        """
        placed = []
        locs_placeable = {}
        if self.world.options.boss_key_mode == "vanilla":
            for loc, data in LOCATION_TABLE.items():
                if data.vanilla_item is None:
                    continue
                if "Boss Key" in data.vanilla_item:
                    if data.vanilla_item in self.start_bkeys:
                        continue
                    self.world.get_location(loc).place_locked_item(self.world.create_item(data.vanilla_item))
                    placed.append(data.vanilla_item)
            return placed
        elif self.world.options.boss_key_mode == "own_dungeon":
            for dun in self.all_bkeys.keys():
                locs_placeable[dun] = []
                for loc in self.multiworld.get_locations(self.world.player):
                    if self.world.region_to_hint_region(loc.parent_region) == dun and loc.item is None:
                        if (
                            loc.name in DUNGEON_HC_CHECKS.values()
                            or loc.name in DUNGEON_FINAL_CHECKS.values()
                            or loc.name == "Skyview - Rupee on Spring Pillar"
                            or loc.item
                        ):
                            continue
                        if dun in self.progression_dungeons and loc.name in self.world.nonprogress_locations:
                            continue
                        locs_placeable[dun].append(tuple([loc.name, loc.player]))
        elif self.world.options.boss_key_mode == "anywhere":
            return []
        for dun, bkey_item in self.all_bkeys.items():
            if bkey_item in self.start_bkeys:
                continue
            if len(locs_placeable[dun]) == 0:
                raise FillError(f"Could not find a location to place boss key: {bkey_item}")
            loc_to_place = self.world.random.choice(locs_placeable[dun])
            self.world.get_location(loc_to_place[0]).place_locked_item(self.world.create_item(bkey_item))
            placed.append(bkey_item)

        return placed

KEY_PLACEMENTS = {
    "Skyview": {
        0: [
            "Skyview - Chest on Tree Branch",
            "Skyview - Digging Spot in Crawlspace",
            "Skyview - Chest behind Two Eyes",
        ],
        1: [
            "Skyview - Chest on Tree Branch",
            "Skyview - Digging Spot in Crawlspace",
            "Skyview - Chest behind Two Eyes",
            "Skyview - Chest after Stalfos Fight",
            "Skyview - Item behind Bars",
            "Skyview - Rupee in Southeast Tunnel",
            "Skyview - Rupee in Southwest Tunnel",
            "Skyview - Rupee in East Tunnel",
            "Skyview - Chest behind Three Eyes",
        ],
    },
    "Earth Temple": {},
    "Lanayru Mining Facility": {
        0: [
            "Lanayru Mining Facility - Chest behind Bars",
            "Lanayru Mining Facility - First Chest in Hub Room",
            "Lanayru Mining Facility - Chest in First West Room",
            "Lanayru Mining Facility - Chest after Armos Fight",
            "Lanayru Mining Facility - Chest behind First Crawlspace",
            "Lanayru Mining Facility - Chest in Spike Maze",
            "Lanayru Mining Facility - Boss Key Chest",
            "Lanayru Mining Facility - Shortcut Chest in Main Hub",
        ],
    },
    "Ancient Cistern": {
        0: [
            "Ancient Cistern - Rupee in West Hand",
            "Ancient Cistern - Rupee in East Hand",
            "Ancient Cistern - First Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Second Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Third Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Rupee in East Part in Cubby",
            "Ancient Cistern - Rupee in East Part in Main Tunnel",
            "Ancient Cistern - Chest in East Part",
            "Ancient Cistern - Chest after Whip Hooks",
            "Ancient Cistern - Chest behind the Waterfall",
            "Ancient Cistern - Bokoblin",
        ],
        1: [
            "Ancient Cistern - Rupee in West Hand",
            "Ancient Cistern - Rupee in East Hand",
            "Ancient Cistern - First Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Second Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Third Rupee in East Part in Short Tunnel",
            "Ancient Cistern - Rupee in East Part in Cubby",
            "Ancient Cistern - Rupee in East Part in Main Tunnel",
            "Ancient Cistern - Chest in East Part",
            "Ancient Cistern - Chest after Whip Hooks",
            "Ancient Cistern - Chest behind the Waterfall",
            "Ancient Cistern - Bokoblin",
        ],
    },
    "Sandship": {
        0: [
            "Sandship - Chest at the Stern",
            "Sandship - Chest before 4-Door Corridor",
            "Sandship - Chest behind Combination Lock",
            "Sandship - Treasure Room First Chest",
            "Sandship - Treasure Room Second Chest",
            "Sandship - Treasure Room Third Chest",
            "Sandship - Treasure Room Fourth Chest",
            "Sandship - Treasure Room Fifth Chest",
            "Sandship - Robot in Brig's Reward",
        ],
        1: [
            "Sandship - Chest at the Stern",
            "Sandship - Chest before 4-Door Corridor",
            "Sandship - Chest behind Combination Lock",
            "Sandship - Treasure Room First Chest",
            "Sandship - Treasure Room Second Chest",
            "Sandship - Treasure Room Third Chest",
            "Sandship - Treasure Room Fourth Chest",
            "Sandship - Treasure Room Fifth Chest",
            "Sandship - Robot in Brig's Reward",
        ],
    },
    "Fire Sanctuary": {
        0: [
            "Fire Sanctuary - Chest in First Room",
        ],
        1: [
            "Fire Sanctuary - Chest in First Room",
            "Fire Sanctuary - Chest in Second Room",
            "Fire Sanctuary - Chest on Balcony",
            "Fire Sanctuary - Chest near First Trapped Mogma",
        ],
        2: [
            "Fire Sanctuary - Chest in First Room",
            "Fire Sanctuary - Chest in Second Room",
            "Fire Sanctuary - Chest on Balcony",
            "Fire Sanctuary - Chest near First Trapped Mogma",
            "Fire Sanctuary - First Chest in Water Fruit Room",
            "Fire Sanctuary - Second Chest in Water Fruit Room",
            "Fire Sanctuary - Rescue First Trapped Mogma",
            "Fire Sanctuary - Rescue Second Trapped Mogma",
            "Fire Sanctuary - Chest after Bombable Wall",
        ],
    },
    "Sky Keep": {
        0: [
            "Sky Keep - First Chest",
            "Sky Keep - Chest after Dreadfuse",
            "Sky Keep - Rupee in Fire Sanctuary Room in Alcove",
            "Sky Keep - Sacred Power of Din",
            "Sky Keep - Sacred Power of Nayru",
        ],
    },
}
