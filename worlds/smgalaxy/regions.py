from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld

from .Constants.Names import region_names as regname
from .Options import SMGOptions
from .locations import SMGLocation, locPC_table, base_stars_locations, SMGLocationData
from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import SMGWorld

class SMGRegionData(NamedTuple):
    type: str  # type of randomization for GER
    entrance_regions: Optional[list[str]] # Regions with entrances to this one
    exit_regions: Optional[list[str]] # Regions with entrances from this one
    ger_exits: Optional[list[str]] # connected exit regions that can be swapped during Entrance Rando
    default_access: Optional[dict[str, int]]

class SMGRegion(Region):
    game: str = "Super Mario Galaxy"
    region_data: SMGRegionData

    def __init__(self, region_name: str, region_data: SMGRegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

region_list: dict[str, SMGRegionData] = {
    regname.SHIP: SMGRegionData("Main", [],
                                [],
                                [regname.TERRACE, regname.LIBRARY, regname.KITCHEN, regname.GARDEN, regname.GATEWAY,
                                 regname.ENGINE, regname.BEDROOM, regname.FOUNTAIN, regname.COTU, regname.SWEETSWEET,
                                 regname.SLINGPOD, regname.DRIPDROP, regname.BIGMOUTH, regname.SANDSPIRAL,
                                 regname.SNOWCAP, regname.BOOBONE, regname.ROLLINGGIZ, regname.BUBBLEBLAST,
                                 regname.LOOPDEESWOOP, regname.FINALE], {}),
    regname.TERRACE: SMGRegionData("Dome", [regname.SHIP], [],
                                   [regname.GOODEGG, regname.HONEYHIVE, regname.LOOPDEELOOP, regname.FLIPSWITCH,
                                    regname.BOWJR1],
                                   {}),
    regname.FOUNTAIN: SMGRegionData("Dome", [regname.SHIP], [],
                                    [regname.SPACEJUNK, regname.ROLLINGGREEN, regname.BATTLEROCK, regname.HURRYSCUR,
                                     regname.BOWSER1],
                                    {"Grand Star": 1}),
    regname.ENGINE: SMGRegionData("Dome", [regname.SHIP], [],
                                  [regname.GOLDLEAF, regname.SEASLIDE, regname.TOYTIME, regname.BONEFIN,
                                   regname.BOWJR3],
                                    {"Grand Star": 4}),
    regname.KITCHEN: SMGRegionData("Dome", [regname.SHIP], [],
                                   [regname.BEACHBOWL, regname.BUBBLEBREEZE, regname.GHOSTLY, regname.BUOY,
                                    regname.BOWJR2],
                                    {"Grand Star": 2}),
    regname.BEDROOM: SMGRegionData("Dome",[regname.SHIP], [],
                                   [regname.GUSTY, regname.FREEZEFLAME, regname.DUSTY, regname.HONEYCLIMB,
                                    regname.BOWSER2],
                                    {"Grand Star": 3}),
    regname.GARDEN: SMGRegionData("Dome", [regname.SHIP], [],
                                  [regname.DEEPDARK, regname.DREADNOUGHT, regname.MATTER, regname.MELTY],
                                    {"Grand Star": 5}),
    regname.LIBRARY: SMGRegionData("Dome", [regname.SHIP], [], [], {}),
    regname.COTU: SMGRegionData("Dome", [regname.SHIP], [], [regname.BOWSER3], {"Grand Star": 5, "Power Star": 60}),
    regname.GATEWAY: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.SWEETSWEET: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.SLINGPOD: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.DRIPDROP: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.BIGMOUTH: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.SANDSPIRAL: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.SNOWCAP: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.BOOBONE: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.ROLLINGGIZ: SMGRegionData("Special", [regname.SHIP], [], [], {"Green Star": 1}),
    regname.LOOPDEESWOOP: SMGRegionData("Special", [regname.SHIP], [], [], {"Green Star": 1}),
    regname.BUBBLEBLAST: SMGRegionData("Special", [regname.SHIP], [], [], {"Green Star": 1}),
    regname.FINALE: SMGRegionData("Special", [regname.SHIP], [], [], {}),
    regname.BOWJR1: SMGRegionData("Boss", [regname.TERRACE], [], [], {}),
    regname.BOWJR2: SMGRegionData("Boss", [regname.KITCHEN], [], [], {}),
    regname.BOWJR3: SMGRegionData("Boss", [regname.ENGINE], [], [], {}),
    regname.BOWSER1: SMGRegionData("Boss", [regname.FOUNTAIN], [], [], {}),
    regname.BOWSER2: SMGRegionData("Boss", [regname.BEDROOM], [], [], {}),
    regname.BOWSER3: SMGRegionData("Goal", [regname.COTU], [], [], {}),
    regname.GOODEGG: SMGRegionData("Major", [regname.TERRACE], [], [], {}),
    regname.HONEYHIVE: SMGRegionData("Major", [regname.TERRACE], [], [], {}),
    regname.SPACEJUNK: SMGRegionData("Major", [regname.FOUNTAIN], [], [], {}),
    regname.BATTLEROCK: SMGRegionData("Major", [regname.FOUNTAIN], [], [], {}),
    regname.BEACHBOWL: SMGRegionData("Major", [regname.KITCHEN], [], [], {}),
    regname.GHOSTLY: SMGRegionData("Major", [regname.KITCHEN], [], [], {}),
    regname.GUSTY: SMGRegionData("Major", [regname.BEDROOM], [], [], {}),
    regname.FREEZEFLAME: SMGRegionData("Major", [regname.BEDROOM], [], [], {}),
    regname.DUSTY: SMGRegionData("Major", [regname.BEDROOM], [], [], {}),
    regname.GOLDLEAF: SMGRegionData("Major", [regname.ENGINE], [], [], {}),
    regname.SEASLIDE: SMGRegionData("Major", [regname.ENGINE], [], [], {}),
    regname.TOYTIME: SMGRegionData("Major", [regname.ENGINE], [], [], {}),
    regname.DEEPDARK: SMGRegionData("Major", [regname.GARDEN], [], [], {}),
    regname.DREADNOUGHT: SMGRegionData("Major", [regname.GARDEN], [], [], {}),
    regname.MELTY: SMGRegionData("Major", [regname.GARDEN], [], [], {}),
    regname.LOOPDEELOOP: SMGRegionData("Minor", [regname.TERRACE], [], [], {}),
    regname.FLIPSWITCH: SMGRegionData("Minor", [regname.TERRACE], [], [], {}),
    regname.ROLLINGGREEN: SMGRegionData("Minor", [regname.FOUNTAIN], [], [], {}),
    regname.HURRYSCUR: SMGRegionData("Minor", [regname.FOUNTAIN], [], [], {}),
    regname.BUBBLEBREEZE: SMGRegionData("Minor", [regname.KITCHEN], [], [], {}),
    regname.BUOY: SMGRegionData("Minor", [regname.KITCHEN], [], [], {}),
    regname.HONEYCLIMB: SMGRegionData("Minor", [regname.BEDROOM], [], [], {}),
    regname.BONEFIN: SMGRegionData("Minor", [regname.ENGINE], [], [], {}),
    regname.MATTER: SMGRegionData("Minor", [regname.GARDEN], [], [], {}),
}


def create_regions(world: "SMGWorld"):
    for region_name in region_list.keys():
        world.multiworld.regions.append(SMGRegion(region_name, region_list[region_name], world.player, world.multiworld))

    create_locations(base_stars_locations, world)

    if world.options.enable_purple_coin_stars.value == 0:
        gateway_purple: dict[str, SMGLocationData] = {"GG: Gateway's Purple coins": locPC_table["GG: Gateway's Purple coins"]}
        create_locations(gateway_purple, world)
    elif world.options.enable_purple_coin_stars.value == 1:
        create_locations(locPC_table, world)

def connect_regions(world: "SMGWorld", player: int, source: str, target: str, name: str, rule=None):
    sourceRegion = world.get_region(source)
    targetRegion = world.get_region(target)

    connection = Entrance(player, name, sourceRegion)
    if rule:
        add_rule(connection, rule, "and")

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, world: "SMGWorld") -> Region:
    return Region(name, world.player, world.multiworld, name)

def create_locations(locs: dict[str, SMGLocationData], world: "SMGWorld"):
    for name, data in locs.items():
        reg = world.get_region(data.region)
        location = SMGLocation(world.player, name, reg)
        if data.default_access:
            for item, count in data.default_access:
                rule = lambda state,i=item, c=count: state.has(i, world.player, count)
                add_rule(location, rule, "and")

        reg.locations += [location]

