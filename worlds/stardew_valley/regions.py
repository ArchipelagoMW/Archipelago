from dataclasses import dataclass, field
from enum import IntFlag
from random import Random
from typing import Iterable, Dict, Protocol, Optional, List, Tuple

from BaseClasses import Region, Entrance
from . import options
from .data.region_data import SVRegion
from .options import StardewOptions


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0b0
    PELICAN_TOWN = 0b11111
    NON_PROGRESSION = 0b11110
    BUILDINGS = 0b11100
    EVERYTHING = 0b11000
    CHAOS = 0b10000


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    reverse: Optional[str] = None
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    def __post_init__(self):
        if self.reverse is None and " to " in self.name:
            origin, destination = self.name.split(" to ")
            super().__setattr__("reverse", f"{destination} to {origin}")


stardew_valley_regions = [
    RegionData(SVRegion.menu, ["To Stardew Valley"]),
    RegionData(SVRegion.stardew_valley, ["To Farmhouse"]),
    RegionData(SVRegion.farm_house, ["Outside to Farm", "Downstairs to Cellar"]),
    RegionData(SVRegion.cellar),
    RegionData(SVRegion.farm,
               ["Farm to Backwoods", "Farm to Bus Stop", "Farm to Forest", "Farm to Farmcave", "Enter Greenhouse",
                "Use Desert Obelisk", "Use Island Obelisk"]),
    RegionData(SVRegion.backwoods, ["Backwoods to Mountain"]),
    RegionData(SVRegion.bus_stop, ["Bus Stop to Town", "Take Bus to Desert", "Bus Stop to Tunnel Entrance"]),
    RegionData(SVRegion.forest, ["Forest to Town", "Enter Secret Woods", "Forest to Wizard Tower", "Forest to Marnie's Ranch",
                          "Forest to Leah's Cottage", "Forest to Sewers", "Talk to Traveling Merchant"]),
    RegionData(SVRegion.traveling_cart),
    RegionData(SVRegion.farm_cave),
    RegionData(SVRegion.greenhouse),
    RegionData(SVRegion.mountain,
               ["Mountain to Railroad", "Mountain to Tent", "Mountain to Carpenter Shop", "Mountain to The Mines",
                "Enter Quarry", "Mountain to Adventurer's Guild", "Mountain to Town"]),
    RegionData(SVRegion.tunnel_entrance, ["Enter Tunnel"]),
    RegionData(SVRegion.tunnel),
    RegionData(SVRegion.town, ["Town to Community Center", "Town to Beach", "Town to Hospital",
                        "Town to Pierre's General Store", "Town to Saloon", "Town to Alex's House", "Town to Trailer",
                        "Town to Mayor's Manor",
                        "Town to Sam's House", "Town to Haley's House", "Town to Sewers", "Town to Clint's Blacksmith",
                        "Town to Museum",
                        "Town to JojaMart"]),
    RegionData(SVRegion.beach, ["Beach to Willy's Fish Shop", "Enter Elliott's House", "Enter Tide Pools"]),
    RegionData(SVRegion.railroad, ["Enter Bathhouse Entrance", "Enter Witch Warp Cave"]),  # "Enter Perfection Cutscene Area"
    RegionData(SVRegion.ranch),
    RegionData(SVRegion.leah_house),
    RegionData(SVRegion.sewers, ["Enter Mutant Bug Lair"]),
    RegionData(SVRegion.mutant_bug_lair),
    RegionData(SVRegion.wizard_tower, ["Enter Wizard Basement"]),
    RegionData(SVRegion.wizard_basement),
    RegionData(SVRegion.tent),
    RegionData(SVRegion.carpenter, ["Enter Sebastian's Room"]),
    RegionData(SVRegion.sebastian_room),
    RegionData(SVRegion.adventurer_guild),
    RegionData(SVRegion.community_center,
               ["Access Crafts Room", "Access Pantry", "Access Fish Tank", "Access Boiler Room",
                "Access Bulletin Board",
                "Access Vault"]),
    RegionData(SVRegion.crafts_room),
    RegionData(SVRegion.pantry),
    RegionData(SVRegion.fish_tank),
    RegionData(SVRegion.boiler_room),
    RegionData(SVRegion.bulletin_board),
    RegionData(SVRegion.vault),
    RegionData(SVRegion.hospital, ["Enter Harvey's Room"]),
    RegionData(SVRegion.harvey_room),
    RegionData(SVRegion.pierre_store, ["Enter Sunroom"]),
    RegionData(SVRegion.sunroom),
    RegionData(SVRegion.saloon, ["Play Journey of the Prairie King", "Play Junimo Kart"]),
    RegionData(SVRegion.alex_house),
    RegionData(SVRegion.trailer),
    RegionData(SVRegion.mayor_house),
    RegionData(SVRegion.sam_house),
    RegionData(SVRegion.haley_house),
    RegionData(SVRegion.blacksmith),
    RegionData(SVRegion.museum),
    RegionData(SVRegion.jojamart),
    RegionData(SVRegion.fish_shop),
    RegionData(SVRegion.elliott_house),
    RegionData(SVRegion.tide_pools),
    RegionData(SVRegion.bathhouse_entrance, ["Enter Locker Room"]),
    RegionData(SVRegion.locker_room, ["Enter Public Bath"]),
    RegionData(SVRegion.public_bath),
    RegionData(SVRegion.witch_warp_cave, ["Enter Witch's Swamp"]),
    RegionData(SVRegion.witch_swamp),
    RegionData(SVRegion.quarry, ["Enter Quarry Mine Entrance"]),
    RegionData(SVRegion.quarry_mine_entrance, ["Enter Quarry Mine"]),
    RegionData(SVRegion.quarry_mine),
    RegionData(SVRegion.secret_woods),
    RegionData(SVRegion.desert, ["Enter Skull Cavern Entrance"]),
    RegionData(SVRegion.skull_cavern_entrance, ["Enter Skull Cavern"]),
    RegionData(SVRegion.skull_cavern, ["Mine to Skull Cavern Floor 100"]),
    RegionData(SVRegion.perfect_skull_cavern),
    RegionData(SVRegion.ginger_island),
    RegionData(SVRegion.jotpk_world_1, ["Reach JotPK World 2"]),
    RegionData(SVRegion.jotpk_world_2, ["Reach JotPK World 3"]),
    RegionData(SVRegion.jotpk_world_3),
    RegionData(SVRegion.junimo_kart_1, ["Reach Junimo Kart 2"]),
    RegionData(SVRegion.junimo_kart_2, ["Reach Junimo Kart 3"]),
    RegionData(SVRegion.junimo_kart_3),
    RegionData(SVRegion.mines, ["Dig to The Mines - Floor 5", "Dig to The Mines - Floor 10", "Dig to The Mines - Floor 15",
                             "Dig to The Mines - Floor 20", "Dig to The Mines - Floor 25",
                             "Dig to The Mines - Floor 30",
                             "Dig to The Mines - Floor 35", "Dig to The Mines - Floor 40",
                             "Dig to The Mines - Floor 45",
                             "Dig to The Mines - Floor 50", "Dig to The Mines - Floor 55",
                             "Dig to The Mines - Floor 60",
                             "Dig to The Mines - Floor 65", "Dig to The Mines - Floor 70",
                             "Dig to The Mines - Floor 75",
                             "Dig to The Mines - Floor 80", "Dig to The Mines - Floor 85",
                             "Dig to The Mines - Floor 90",
                             "Dig to The Mines - Floor 95", "Dig to The Mines - Floor 100",
                             "Dig to The Mines - Floor 105",
                             "Dig to The Mines - Floor 110", "Dig to The Mines - Floor 115",
                             "Dig to The Mines - Floor 120"]),
    RegionData(SVRegion.mines_floor_5),
    RegionData(SVRegion.mines_floor_10),
    RegionData(SVRegion.mines_floor_15),
    RegionData(SVRegion.mines_floor_20),
    RegionData(SVRegion.mines_floor_25),
    RegionData(SVRegion.mines_floor_30),
    RegionData(SVRegion.mines_floor_35),
    RegionData(SVRegion.mines_floor_40),
    RegionData(SVRegion.mines_floor_45),
    RegionData(SVRegion.mines_floor_50),
    RegionData(SVRegion.mines_floor_55),
    RegionData(SVRegion.mines_floor_60),
    RegionData(SVRegion.mines_floor_65),
    RegionData(SVRegion.mines_floor_70),
    RegionData(SVRegion.mines_floor_75),
    RegionData(SVRegion.mines_floor_80),
    RegionData(SVRegion.mines_floor_85),
    RegionData(SVRegion.mines_floor_90),
    RegionData(SVRegion.mines_floor_95),
    RegionData(SVRegion.mines_floor_100),
    RegionData(SVRegion.mines_floor_105),
    RegionData(SVRegion.mines_floor_110),
    RegionData(SVRegion.mines_floor_115),
    RegionData(SVRegion.mines_floor_120),
]

# Exists and where they lead
mandatory_connections = [
    ConnectionData("To Stardew Valley", SVRegion.stardew_valley),
    ConnectionData("To Farmhouse", SVRegion.farm_house),
    ConnectionData("Outside to Farm", SVRegion.farm),
    ConnectionData("Downstairs to Cellar", SVRegion.cellar),
    ConnectionData("Farm to Backwoods", SVRegion.backwoods),
    ConnectionData("Farm to Bus Stop", SVRegion.bus_stop),
    ConnectionData("Farm to Forest", SVRegion.forest),
    ConnectionData("Farm to Farmcave", SVRegion.farm_cave, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Enter Greenhouse", SVRegion.greenhouse),
    ConnectionData("Use Desert Obelisk", SVRegion.desert),
    ConnectionData("Use Island Obelisk", SVRegion.ginger_island),
    ConnectionData("Backwoods to Mountain", SVRegion.mountain),
    ConnectionData("Bus Stop to Town", SVRegion.town),
    ConnectionData("Bus Stop to Tunnel Entrance", SVRegion.tunnel_entrance),
    ConnectionData("Take Bus to Desert", SVRegion.desert),
    ConnectionData("Enter Tunnel", SVRegion.tunnel),
    ConnectionData("Forest to Town", SVRegion.town),
    ConnectionData("Forest to Wizard Tower", SVRegion.wizard_tower, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Enter Wizard Basement", SVRegion.wizard_basement),
    ConnectionData("Forest to Marnie's Ranch", SVRegion.ranch, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Forest to Leah's Cottage", SVRegion.leah_house),
    ConnectionData("Enter Secret Woods", SVRegion.secret_woods),
    ConnectionData("Forest to Sewers", SVRegion.sewers),
    ConnectionData("Talk to Traveling Merchant", SVRegion.traveling_cart),
    ConnectionData("Town to Sewers", SVRegion.sewers),
    ConnectionData("Enter Mutant Bug Lair", SVRegion.mutant_bug_lair),
    ConnectionData("Mountain to Railroad", SVRegion.railroad),
    ConnectionData("Mountain to Tent", SVRegion.tent, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Mountain to Carpenter Shop", SVRegion.carpenter, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Enter Sebastian's Room", SVRegion.sebastian_room),
    ConnectionData("Mountain to Adventurer's Guild", SVRegion.adventurer_guild),
    ConnectionData("Enter Quarry", SVRegion.quarry),
    ConnectionData("Enter Quarry Mine Entrance", SVRegion.quarry_mine_entrance),
    ConnectionData("Enter Quarry Mine", SVRegion.quarry_mine),
    ConnectionData("Mountain to Town", SVRegion.town),
    ConnectionData("Town to Community Center", SVRegion.community_center, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Access Crafts Room", SVRegion.crafts_room),
    ConnectionData("Access Pantry", SVRegion.pantry),
    ConnectionData("Access Fish Tank", SVRegion.fish_tank),
    ConnectionData("Access Boiler Room", SVRegion.boiler_room),
    ConnectionData("Access Bulletin Board", SVRegion.bulletin_board),
    ConnectionData("Access Vault", SVRegion.vault),
    ConnectionData("Town to Hospital", SVRegion.hospital, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Enter Harvey's Room", SVRegion.harvey_room),
    ConnectionData("Town to Pierre's General Store", SVRegion.pierre_store, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Enter Sunroom", SVRegion.sunroom),
    ConnectionData("Town to Clint's Blacksmith", SVRegion.blacksmith, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Saloon", SVRegion.saloon, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Play Journey of the Prairie King", SVRegion.jotpk_world_1),
    ConnectionData("Reach JotPK World 2", SVRegion.jotpk_world_2),
    ConnectionData("Reach JotPK World 3", SVRegion.jotpk_world_3),
    ConnectionData("Play Junimo Kart", SVRegion.junimo_kart_1),
    ConnectionData("Reach Junimo Kart 2", SVRegion.junimo_kart_2),
    ConnectionData("Reach Junimo Kart 3", SVRegion.junimo_kart_3),
    ConnectionData("Town to Sam's House", SVRegion.sam_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Haley's House", SVRegion.haley_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Mayor's Manor", SVRegion.mayor_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Alex's House", SVRegion.alex_house, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Trailer", SVRegion.trailer, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Museum", SVRegion.museum, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to JojaMart", SVRegion.jojamart, flag=RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Beach", SVRegion.beach),
    ConnectionData("Enter Elliott's House", SVRegion.elliott_house),
    ConnectionData("Beach to Willy's Fish Shop", SVRegion.fish_shop, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Enter Tide Pools", SVRegion.tide_pools),
    ConnectionData("Mountain to The Mines", SVRegion.mines, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData("Dig to The Mines - Floor 5", SVRegion.mines_floor_5),
    ConnectionData("Dig to The Mines - Floor 10", SVRegion.mines_floor_10),
    ConnectionData("Dig to The Mines - Floor 15", SVRegion.mines_floor_15),
    ConnectionData("Dig to The Mines - Floor 20", SVRegion.mines_floor_20),
    ConnectionData("Dig to The Mines - Floor 25", SVRegion.mines_floor_25),
    ConnectionData("Dig to The Mines - Floor 30", SVRegion.mines_floor_30),
    ConnectionData("Dig to The Mines - Floor 35", SVRegion.mines_floor_35),
    ConnectionData("Dig to The Mines - Floor 40", SVRegion.mines_floor_40),
    ConnectionData("Dig to The Mines - Floor 45", SVRegion.mines_floor_45),
    ConnectionData("Dig to The Mines - Floor 50", SVRegion.mines_floor_50),
    ConnectionData("Dig to The Mines - Floor 55", SVRegion.mines_floor_55),
    ConnectionData("Dig to The Mines - Floor 60", SVRegion.mines_floor_60),
    ConnectionData("Dig to The Mines - Floor 65", SVRegion.mines_floor_65),
    ConnectionData("Dig to The Mines - Floor 70", SVRegion.mines_floor_70),
    ConnectionData("Dig to The Mines - Floor 75", SVRegion.mines_floor_75),
    ConnectionData("Dig to The Mines - Floor 80", SVRegion.mines_floor_80),
    ConnectionData("Dig to The Mines - Floor 85", SVRegion.mines_floor_85),
    ConnectionData("Dig to The Mines - Floor 90", SVRegion.mines_floor_90),
    ConnectionData("Dig to The Mines - Floor 95", SVRegion.mines_floor_95),
    ConnectionData("Dig to The Mines - Floor 100", SVRegion.mines_floor_100),
    ConnectionData("Dig to The Mines - Floor 105", SVRegion.mines_floor_105),
    ConnectionData("Dig to The Mines - Floor 110", SVRegion.mines_floor_110),
    ConnectionData("Dig to The Mines - Floor 115", SVRegion.mines_floor_115),
    ConnectionData("Dig to The Mines - Floor 120", SVRegion.mines_floor_120),
    ConnectionData("Enter Skull Cavern Entrance", SVRegion.skull_cavern_entrance),
    ConnectionData("Enter Skull Cavern", SVRegion.skull_cavern),
    ConnectionData("Mine to Skull Cavern Floor 100", SVRegion.perfect_skull_cavern),
    ConnectionData("Enter Witch Warp Cave", SVRegion.witch_warp_cave),
    ConnectionData("Enter Witch's Swamp", SVRegion.witch_swamp),
    ConnectionData("Enter Bathhouse Entrance", SVRegion.bathhouse_entrance),
    ConnectionData("Enter Locker Room", SVRegion.locker_room),
    ConnectionData("Enter Public Bath", SVRegion.public_bath),
]


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewOptions) -> Tuple[
    Iterable[Region], Dict[str, str]]:
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  stardew_valley_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    connections, randomized_data = randomize_connections(random, world_options)

    for connection in connections:
        if connection.name not in entrances:
            continue
        entrances[connection.name].connect(regions[connection.destination])

    return regions.values(), randomized_data


def randomize_connections(random: Random, world_options: StardewOptions) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize = []
    if world_options[options.EntranceRandomization] == options.EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connection for connection in mandatory_connections if
                                    RandomizationFlag.PELICAN_TOWN in connection.flag]
    elif world_options[options.EntranceRandomization] == options.EntranceRandomization.option_non_progression:
        connections_to_randomize = [connection for connection in mandatory_connections if
                                    RandomizationFlag.NON_PROGRESSION in connection.flag]
    random.shuffle(connections_to_randomize)

    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = []
    randomized_data = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections.append(ConnectionData(connection.name, destination.destination, destination.reverse))
        randomized_data[connection.name] = destination.name
        randomized_data[destination.reverse] = connection.reverse

    return mandatory_connections, randomized_data
