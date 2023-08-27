from BaseClasses import Location
from worlds.AutoWorld import World
from .Types import HatDLC, HatType
from typing import Optional, NamedTuple, List, Dict
from .Options import TasksanityCheckCount


class LocData(NamedTuple):
    id: int
    region: str
    required_hats: Optional[List[HatType]] = [HatType.NONE]
    required_tps: Optional[int] = 0
    hookshot: Optional[bool] = False
    dlc_flags: Optional[HatDLC] = HatDLC.none
    paintings: Optional[int] = 0  # Progressive paintings required for Subcon painting shuffle

    # For UmbrellaLogic setting
    umbrella: Optional[bool] = False  # Umbrella required for this check
    dweller_bell: Optional[int] = 0  # Dweller bell hit required, 1 means must hit bell, 2 means can bypass w/mask

    # Other
    act_complete_event: Optional[bool] = True  # Only used for event locations. Copy access rule from act completion
    nyakuza_thug: Optional[str] = ""  # Name of Nyakuza thug NPC (for metro shops)


class HatInTimeLocation(Location):
    game: str = "A Hat in Time"


def get_total_locations(world: World) -> int:
    total: int = 0

    for (name) in location_table.keys():
        if is_location_valid(world, name):
            total += 1

    if world.multiworld.EnableDLC1[world.player].value > 0 and world.multiworld.Tasksanity[world.player].value > 0:
        total += world.multiworld.TasksanityCheckCount[world.player].value

    return total


def location_dlc_enabled(world: World, location: str) -> bool:
    data = location_table.get(location) or event_locs.get(location)

    if data.dlc_flags == HatDLC.none:
        return True
    elif data.dlc_flags == HatDLC.dlc1 and world.multiworld.EnableDLC1[world.player].value > 0:
        return True
    elif data.dlc_flags == HatDLC.dlc2 and world.multiworld.EnableDLC2[world.player].value > 0:
        return True
    elif data.dlc_flags == HatDLC.death_wish and world.multiworld.EnableDeathWish[world.player].value > 0:
        return True

    return False


def is_location_valid(world: World, location: str) -> bool:
    if not location_dlc_enabled(world, location):
        return False

    if location in storybook_pages.keys() \
       and world.multiworld.ShuffleStorybookPages[world.player].value == 0:
        return False

    if location in shop_locations and location not in world.shop_locs:
        return False

    return True


def get_location_names() -> Dict[str, int]:
    names = {name: data.id for name, data in location_table.items()}
    id_start: int = 300204
    for i in range(TasksanityCheckCount.range_end):
        names.setdefault(format("Tasksanity Check %i") % (i+1), id_start+i)

    return names


ahit_locations = {
    "Spaceship - Rumbi Abuse": LocData(301000, "Spaceship", required_tps=4, dweller_bell=1),
    # "Spaceship - Cooking Cat": LocData(301001, "Spaceship", required_tps=5),

    # 300000 range - Mafia Town/Batle of the Birds
    "Welcome to Mafia Town - Umbrella": LocData(301002, "Welcome to Mafia Town"),
    "Mafia Town - Old Man (Seaside Spaghetti)": LocData(303833, "Mafia Town Area"),
    "Mafia Town - Old Man (Steel Beams)": LocData(303832, "Mafia Town Area"),
    "Mafia Town - Blue Vault": LocData(302850, "Mafia Town Area"),
    "Mafia Town - Green Vault": LocData(302851, "Mafia Town Area"),
    "Mafia Town - Red Vault": LocData(302848, "Mafia Town Area"),
    "Mafia Town - Blue Vault Brewing Crate": LocData(305572, "Mafia Town Area", required_hats=[HatType.BREWING]),
    "Mafia Town - Plaza Under Boxes": LocData(304458, "Mafia Town Area"),
    "Mafia Town - Small Boat": LocData(304460, "Mafia Town Area"),
    "Mafia Town - Staircase Pon Cluster": LocData(304611, "Mafia Town Area"),
    "Mafia Town - Palm Tree": LocData(304609, "Mafia Town Area"),
    "Mafia Town - Port": LocData(305219, "Mafia Town Area"),
    "Mafia Town - Docks Chest": LocData(303534, "Mafia Town Area"),
    "Mafia Town - Ice Hat Cage": LocData(304831, "Mafia Town Area", required_hats=[HatType.ICE]),
    "Mafia Town - Hidden Buttons Chest": LocData(303483, "Mafia Town Area"),

    # These can be accessed from HUMT, the above locations can't be
    "Mafia Town - Dweller Boxes": LocData(304462, "Mafia Town Area (HUMT)"),
    "Mafia Town - Ledge Chest": LocData(303530, "Mafia Town Area (HUMT)"),
    "Mafia Town - Yellow Sphere Building Chest": LocData(303535, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beneath Scaffolding": LocData(304456, "Mafia Town Area (HUMT)"),
    "Mafia Town - On Scaffolding": LocData(304457, "Mafia Town Area (HUMT)"),
    "Mafia Town - Cargo Ship": LocData(304459, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beach Alcove": LocData(304463, "Mafia Town Area (HUMT)"),
    "Mafia Town - Wood Cage": LocData(304606, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beach Patio": LocData(304610, "Mafia Town Area (HUMT)"),
    "Mafia Town - Steel Beam Nest": LocData(304608, "Mafia Town Area (HUMT)"),
    "Mafia Town - Top of Ruined Tower": LocData(304607, "Mafia Town Area (HUMT)", required_hats=[HatType.ICE]),
    "Mafia Town - Hot Air Balloon": LocData(304829, "Mafia Town Area (HUMT)", required_hats=[HatType.ICE]),
    "Mafia Town - Camera Badge 1": LocData(302003, "Mafia Town Area (HUMT)"),
    "Mafia Town - Camera Badge 2": LocData(302004, "Mafia Town Area (HUMT)"),
    "Mafia Town - Chest Beneath Aqueduct": LocData(303489, "Mafia Town Area (HUMT)"),
    "Mafia Town - Secret Cave": LocData(305220, "Mafia Town Area (HUMT)", required_hats=[HatType.BREWING]),
    "Mafia Town - Crow Chest": LocData(303532, "Mafia Town Area (HUMT)"),
    "Mafia Town - Above Boats": LocData(305218, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Slip Slide Chest": LocData(303529, "Mafia Town Area (HUMT)"),
    "Mafia Town - Behind Faucet": LocData(304214, "Mafia Town Area (HUMT)"),
    "Mafia Town - Clock Tower Chest": LocData(303481, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Top of Lighthouse": LocData(304213, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Mafia Geek Platform": LocData(304212, "Mafia Town Area (HUMT)"),
    "Mafia Town - Behind HQ Chest": LocData(303486, "Mafia Town Area (HUMT)"),

    "Mafia HQ - Hallway Brewing Crate": LocData(305387, "Down with the Mafia!", required_hats=[HatType.BREWING]),
    "Mafia HQ - Freezer Chest": LocData(303241, "Down with the Mafia!"),
    "Mafia HQ - Secret Room": LocData(304979, "Down with the Mafia!", required_hats=[HatType.ICE]),
    "Mafia HQ - Bathroom Stall Chest": LocData(303243, "Down with the Mafia!"),

    "Dead Bird Studio - Up the Ladder": LocData(304874, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Red Building Top": LocData(305024, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Behind Water Tower": LocData(305248, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Side of House": LocData(305247, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - DJ Grooves Sign Chest": LocData(303901, "Dead Bird Studio", umbrella=True),
    "Dead Bird Studio - Tightrope Chest": LocData(303898, "Dead Bird Studio", umbrella=True),
    "Dead Bird Studio - Tepee Chest": LocData(303899, "Dead Bird Studio", umbrella=True),
    "Dead Bird Studio - Conductor Chest": LocData(303900, "Dead Bird Studio", umbrella=True),

    "Murder on the Owl Express - Cafeteria": LocData(305313, "Murder on the Owl Express"),
    "Murder on the Owl Express - Luggage Room Top": LocData(305090, "Murder on the Owl Express"),
    "Murder on the Owl Express - Luggage Room Bottom": LocData(305091, "Murder on the Owl Express"),

    "Murder on the Owl Express - Raven Suite Room": LocData(305701, "Murder on the Owl Express",
                                                            required_hats=[HatType.BREWING]),

    "Murder on the Owl Express - Raven Suite Top": LocData(305312, "Murder on the Owl Express"),
    "Murder on the Owl Express - Lounge Chest": LocData(303963, "Murder on the Owl Express"),

    "Picture Perfect - Behind Badge Seller": LocData(304307, "Picture Perfect"),
    "Picture Perfect - Hats Buy Building": LocData(304530, "Picture Perfect"),

    "Dead Bird Studio Basement - Window Platform": LocData(305432, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Cardboard Conductor": LocData(305059, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Above Conductor Sign": LocData(305057, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Logo Wall": LocData(305207, "Dead Bird Studio Basement"),
    "Dead Bird Studio Basement - Disco Room": LocData(305061, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Small Room": LocData(304813, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Vent Pipe": LocData(305430, "Dead Bird Studio Basement"),
    "Dead Bird Studio Basement - Tightrope": LocData(305058, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Cameras": LocData(305431, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Locked Room": LocData(305819, "Dead Bird Studio Basement", hookshot=True),

    # 320000 range - Subcon Forest
    "Contractual Obligations - Cherry Bomb Bone Cage": LocData(324761, "Contractual Obligations"),
    "Subcon Village - Tree Top Ice Cube": LocData(325078, "Subcon Forest Area"),
    "Subcon Village - Graveyard Ice Cube": LocData(325077, "Subcon Forest Area"),
    "Subcon Village - House Top": LocData(325471, "Subcon Forest Area"),
    "Subcon Village - Ice Cube House": LocData(325469, "Subcon Forest Area"),
    "Subcon Village - Snatcher Statue Chest": LocData(323730, "Subcon Forest Area", paintings=1),
    "Subcon Village - Stump Platform Chest": LocData(323729, "Subcon Forest Area"),
    "Subcon Forest - Giant Tree Climb": LocData(325470, "Subcon Forest Area"),
    
    "Subcon Forest - Swamp Gravestone": LocData(326296, "Subcon Forest Area",
                                                required_hats=[HatType.BREWING],
                                                paintings=1),
    
    "Subcon Forest - Swamp Near Well": LocData(324762, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree A": LocData(324763, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree B": LocData(324764, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Ice Wall": LocData(324706, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Treehouse": LocData(325468, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree Chest": LocData(323728, "Subcon Forest Area", paintings=1),
    
    "Subcon Forest - Dweller Stump": LocData(324767, "Subcon Forest Area", 
                                             required_hats=[HatType.DWELLER],
                                             paintings=3),
    
    "Subcon Forest - Dweller Floating Rocks": LocData(324464, "Subcon Forest Area",
                                                      required_hats=[HatType.DWELLER],
                                                      paintings=3),
    
    "Subcon Forest - Dweller Platforming Tree A": LocData(324709, "Subcon Forest Area", paintings=3),
    
    "Subcon Forest - Dweller Platforming Tree B": LocData(324855, "Subcon Forest Area", 
                                                          required_hats=[HatType.DWELLER],
                                                          paintings=3),
    
    "Subcon Forest - Giant Time Piece": LocData(325473, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Gallows": LocData(325472, "Subcon Forest Area", paintings=1),
    
    "Subcon Forest - Green and Purple Dweller Rocks": LocData(325082, "Subcon Forest Area",
                                                              required_hats=[HatType.DWELLER],
                                                              paintings=3),
    
    "Subcon Forest - Dweller Shack": LocData(324463, "Subcon Forest Area",
                                             required_hats=[HatType.DWELLER],
                                             paintings=1),
    
    "Subcon Forest - Tall Tree Hookshot Swing": LocData(324766, "Subcon Forest Area",
                                                        paintings=3,
                                                        required_hats=[HatType.DWELLER],
                                                        hookshot=True),
    
    "Subcon Forest - Burning House": LocData(324710, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Tree Climb": LocData(325079, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Stump Chest": LocData(323731, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Forest Treehouse": LocData(325467, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Spider Bone Cage A": LocData(324462, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Spider Bone Cage B": LocData(325080, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Triple Spider Bounce": LocData(324765, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Noose Treehouse": LocData(324856, "Subcon Forest Area", hookshot=True, paintings=2),
    "Subcon Forest - Ice Cube Shack": LocData(324465, "Subcon Forest Area", paintings=1),
    
    "Subcon Forest - Long Tree Climb Chest": LocData(323734, "Subcon Forest Area",
                                                     required_hats=[HatType.DWELLER],
                                                     paintings=2),
    
    "Subcon Forest - Boss Arena Chest": LocData(323735, "Subcon Forest Area"),
    "Subcon Forest - Manor Rooftop": LocData(325466, "Subcon Forest Area", dweller_bell=2, paintings=1),
    
    "Subcon Forest - Infinite Yarn Bush": LocData(325478, "Subcon Forest Area", 
                                                  required_hats=[HatType.BREWING],
                                                  paintings=2),
    
    "Subcon Forest - Magnet Badge Bush": LocData(325479, "Subcon Forest Area",
                                                 required_hats=[HatType.BREWING],
                                                 paintings=3),
    
    "Subcon Well - Hookshot Badge Chest": LocData(324114, "The Subcon Well", dweller_bell=1, paintings=1),
    "Subcon Well - Above Chest": LocData(324612, "The Subcon Well", dweller_bell=1, paintings=1),
    "Subcon Well - On Pipe": LocData(324311, "The Subcon Well", hookshot=True, dweller_bell=1, paintings=1),
    "Subcon Well - Mushroom": LocData(325318, "The Subcon Well", dweller_bell=1, paintings=1),
    
    "Queen Vanessa's Manor - Cellar": LocData(324841, "Queen Vanessa's Manor", dweller_bell=2, paintings=1),
    "Queen Vanessa's Manor - Bedroom Chest": LocData(323808, "Queen Vanessa's Manor", dweller_bell=2, paintings=1),
    "Queen Vanessa's Manor - Hall Chest": LocData(323896, "Queen Vanessa's Manor", dweller_bell=2, paintings=1),
    "Queen Vanessa's Manor - Chandelier": LocData(325546, "Queen Vanessa's Manor", dweller_bell=2, paintings=1),

    # 330000 range - Alpine Skyline
    "Alpine Skyline - Goat Village: Below Hookpoint": LocData(334856, "Goat Village"),
    "Alpine Skyline - Goat Village: Hidden Branch": LocData(334855, "Goat Village"),
    "Alpine Skyline - Goat Refinery": LocData(333635, "Alpine Skyline Area"),
    "Alpine Skyline - Bird Pass Fork": LocData(335911, "Alpine Skyline Area"),
    "Alpine Skyline - Yellow Band Hills": LocData(335756, "Alpine Skyline Area", required_hats=[HatType.BREWING]),
    "Alpine Skyline - The Purrloined Village: Horned Stone": LocData(335561, "Alpine Skyline Area"),
    "Alpine Skyline - The Purrloined Village: Chest Reward": LocData(334831, "Alpine Skyline Area"),
    "Alpine Skyline - The Birdhouse: Triple Crow Chest": LocData(334758, "The Birdhouse"),

    "Alpine Skyline - The Birdhouse: Dweller Platforms Relic": LocData(336497, "The Birdhouse",
                                                                       required_hats=[HatType.DWELLER]),

    "Alpine Skyline - The Birdhouse: Brewing Crate House": LocData(336496, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Hay Bale": LocData(335885, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Alpine Crow Mini-Gauntlet": LocData(335886, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Outer Edge": LocData(335492, "The Birdhouse"),

    "Alpine Skyline - Mystifying Time Mesa: Zipline": LocData(337058, "Alpine Skyline Area"),
    "Alpine Skyline - Mystifying Time Mesa: Gate Puzzle": LocData(336052, "Alpine Skyline Area"),
    "Alpine Skyline - Ember Summit": LocData(336311, "Alpine Skyline Area"),
    "Alpine Skyline - The Lava Cake: Center Fence Cage": LocData(335448, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Outer Island Chest": LocData(334291, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Dweller Pillars": LocData(335417, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Top Cake": LocData(335418, "The Lava Cake"),
    "Alpine Skyline - The Twilight Path": LocData(334434, "Alpine Skyline Area", required_hats=[HatType.DWELLER]),
    "Alpine Skyline - The Twilight Bell: Wide Purple Platform": LocData(336478, "The Twilight Bell"),
    "Alpine Skyline - The Twilight Bell: Ice Platform": LocData(335826, "The Twilight Bell"),
    "Alpine Skyline - Goat Outpost Horn": LocData(334760, "Alpine Skyline Area"),
    "Alpine Skyline - Windy Passage": LocData(334776, "Alpine Skyline Area"),
    "Alpine Skyline - The Windmill: Inside Pon Cluster": LocData(336395, "The Windmill"),
    "Alpine Skyline - The Windmill: Entrance": LocData(335783, "The Windmill"),
    "Alpine Skyline - The Windmill: Dropdown": LocData(335815, "The Windmill"),
    "Alpine Skyline - The Windmill: House Window": LocData(335389, "The Windmill"),

    "The Finale - Frozen Item": LocData(304108, "The Finale"),

    "Bon Voyage! - Lamp Post Top": LocData(305321, "Bon Voyage!", dlc_flags=HatDLC.dlc1),
    "Bon Voyage! - Mafia Cargo Ship": LocData(304313, "Bon Voyage!", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Toilet": LocData(305109, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Bar": LocData(304251, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Dive Board Ledge": LocData(304254, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Top Balcony": LocData(304255, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Octopus Room": LocData(305253, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Octopus Room Top": LocData(304249, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Laundry Room": LocData(304250, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Ship Side": LocData(304247, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Silver Ring": LocData(305252, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Reception Room - Suitcase": LocData(304045, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Reception Room - Under Desk": LocData(304047, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Lamp Post": LocData(304048, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Iceberg Top": LocData(304046, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Post Captain Rescue": LocData(304049, "Rock the Boat", dlc_flags=HatDLC.dlc1),

    "Nyakuza Metro - Main Station Dining Area": LocData(304105, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),
    "Nyakuza Metro - Top of Ramen Shop": LocData(304104, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),

    "Nyakuza Metro - Yellow Overpass Station Crate": LocData(305413, "Yellow Overpass Station",
                                                             dlc_flags=HatDLC.dlc2,
                                                             required_hats=[HatType.BREWING]),

    "Nyakuza Metro - Bluefin Tunnel Cat Vacuum": LocData(305111, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),

    "Nyakuza Metro - Pink Paw Station Cat Vacuum": LocData(305110, "Pink Paw Station",
                                                           dlc_flags=HatDLC.dlc2,
                                                           hookshot=True,
                                                           required_hats=[HatType.DWELLER]),

    "Nyakuza Metro - Pink Paw Station Behind Fan": LocData(304106, "Pink Paw Station",
                                                           dlc_flags=HatDLC.dlc2,
                                                           hookshot=True,
                                                           required_hats=[HatType.TIME_STOP, HatType.DWELLER]),
}

act_completions = {
    # 310000 range - Act Completions
    "Act Completion (Time Rift - Gallery)": LocData(312758, "Time Rift - Gallery", required_hats=[HatType.BREWING]),
    "Act Completion (Time Rift - The Lab)": LocData(312838, "Time Rift - The Lab"),

    "Act Completion (Welcome to Mafia Town)": LocData(311771, "Welcome to Mafia Town"),
    "Act Completion (Barrel Battle)": LocData(311958, "Barrel Battle"),
    "Act Completion (She Came from Outer Space)": LocData(312262, "She Came from Outer Space"),
    "Act Completion (Down with the Mafia!)": LocData(311326, "Down with the Mafia!"),
    "Act Completion (Cheating the Race)": LocData(312318, "Cheating the Race"),
    "Act Completion (Heating Up Mafia Town)": LocData(311481, "Heating Up Mafia Town", umbrella=True),
    "Act Completion (The Golden Vault)": LocData(312250, "The Golden Vault"),
    "Act Completion (Time Rift - Bazaar)": LocData(312465, "Time Rift - Bazaar"),
    "Act Completion (Time Rift - Sewers)": LocData(312484, "Time Rift - Sewers"),
    "Act Completion (Time Rift - Mafia of Cooks)": LocData(311855, "Time Rift - Mafia of Cooks"),

    "Act Completion (Dead Bird Studio)": LocData(311383, "Dead Bird Studio", umbrella=True),
    "Act Completion (Murder on the Owl Express)": LocData(311544, "Murder on the Owl Express"),
    "Act Completion (Picture Perfect)": LocData(311587, "Picture Perfect"),
    "Act Completion (Train Rush)": LocData(312481, "Train Rush", hookshot=True),
    "Act Completion (The Big Parade)": LocData(311157, "The Big Parade", umbrella=True),
    "Act Completion (Award Ceremony)": LocData(311488, "Award Ceremony"),
    "Act Completion (Dead Bird Studio Basement)": LocData(312253, "Dead Bird Studio Basement", hookshot=True),
    "Act Completion (Time Rift - The Owl Express)": LocData(312807, "Time Rift - The Owl Express"),
    "Act Completion (Time Rift - The Moon)": LocData(312785, "Time Rift - The Moon"),
    "Act Completion (Time Rift - Dead Bird Studio)": LocData(312577, "Time Rift - Dead Bird Studio"),

    "Act Completion (Contractual Obligations)": LocData(312317, "Contractual Obligations", paintings=1),
    "Act Completion (The Subcon Well)": LocData(311160, "The Subcon Well", hookshot=True, umbrella=True, paintings=1),
    "Act Completion (Toilet of Doom)": LocData(311984, "Toilet of Doom", hookshot=True, paintings=1),
    "Act Completion (Queen Vanessa's Manor)": LocData(312017, "Queen Vanessa's Manor", umbrella=True, paintings=1),
    "Act Completion (Mail Delivery Service)": LocData(312032, "Mail Delivery Service", required_hats=[HatType.SPRINT]),
    "Act Completion (Your Contract has Expired)": LocData(311390, "Your Contract has Expired", umbrella=True),
    "Act Completion (Time Rift - Pipe)": LocData(313069, "Time Rift - Pipe", hookshot=True),
    "Act Completion (Time Rift - Village)": LocData(313056, "Time Rift - Village"),
    "Act Completion (Time Rift - Sleepy Subcon)": LocData(312086, "Time Rift - Sleepy Subcon"),

    "Act Completion (The Birdhouse)": LocData(311428, "The Birdhouse"),
    "Act Completion (The Lava Cake)": LocData(312509, "The Lava Cake"),
    "Act Completion (The Twilight Bell)": LocData(311540, "The Twilight Bell"),
    "Act Completion (The Windmill)": LocData(312263, "The Windmill"),
    "Act Completion (The Illness has Spread)": LocData(312022, "The Illness has Spread", hookshot=True),
    
    "Act Completion (Time Rift - The Twilight Bell)": LocData(312399, "Time Rift - The Twilight Bell",
                                                              required_hats=[HatType.DWELLER]),
    
    "Act Completion (Time Rift - Curly Tail Trail)": LocData(313335, "Time Rift - Curly Tail Trail",
                                                             required_hats=[HatType.ICE]),
    
    "Act Completion (Time Rift - Alpine Skyline)": LocData(311777, "Time Rift - Alpine Skyline"),

    "Act Completion (The Finale)": LocData(311872, "The Finale", hookshot=True, required_hats=[HatType.DWELLER]),
    "Act Completion (Time Rift - Tour)": LocData(311803, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),

    "Act Completion (Bon Voyage!)": LocData(311520, "Bon Voyage!", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Act Completion (Ship Shape)": LocData(311451, "Ship Shape", dlc_flags=HatDLC.dlc1),
    "Act Completion (Rock the Boat)": LocData(311437, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Act Completion (Time Rift - Balcony)": LocData(312226, "Time Rift - Balcony", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Act Completion (Time Rift - Deep Sea)": LocData(312434, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),

    "Act Completion (Nyakuza Metro Intro)": LocData(311138, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),

    "Act Completion (Yellow Overpass Station)": LocData(311206, "Yellow Overpass Station",
                                                        dlc_flags=HatDLC.dlc2,
                                                        hookshot=True),

    "Act Completion (Yellow Overpass Manhole)": LocData(311387, "Yellow Overpass Manhole",
                                                        dlc_flags=HatDLC.dlc2,
                                                        required_hats=[HatType.ICE]),

    "Act Completion (Green Clean Station)": LocData(311207, "Green Clean Station", dlc_flags=HatDLC.dlc2),

    "Act Completion (Green Clean Manhole)": LocData(311388, "Green Clean Manhole",
                                                    dlc_flags=HatDLC.dlc2,
                                                    required_hats=[HatType.ICE, HatType.DWELLER]),

    "Act Completion (Bluefin Tunnel)": LocData(311208, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),

    "Act Completion (Pink Paw Station)": LocData(311209, "Pink Paw Station",
                                                 dlc_flags=HatDLC.dlc2,
                                                 hookshot=True,
                                                 required_hats=[HatType.DWELLER]),

    "Act Completion (Pink Paw Manhole)": LocData(311389, "Pink Paw Manhole",
                                                 dlc_flags=HatDLC.dlc2,
                                                 required_hats=[HatType.ICE]),

    "Act Completion (Rush Hour)": LocData(311210, "Rush Hour",
                                          dlc_flags=HatDLC.dlc2,
                                          hookshot=True,
                                          required_hats=[HatType.ICE, HatType.BREWING]),

    "Act Completion (Rumbi Factory)": LocData(312736, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
}

storybook_pages = {
    "Mafia of Cooks - Page: Fish Pile": LocData(345091, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Trash Mound": LocData(345090, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Beside Red Building": LocData(345092, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Behind Shipping Containers": LocData(345095, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Top of Boat": LocData(345093, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Below Dock": LocData(345094, "Time Rift - Mafia of Cooks"),

    "Dead Bird Studio (Rift) - Page: Behind Cardboard Planet": LocData(345449, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Near Time Rift Gate": LocData(345447, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Top of Metal Bar": LocData(345448, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Lava Lamp": LocData(345450, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Above Horse Picture": LocData(345451, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Green Screen": LocData(345452, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: In The Corner": LocData(345453, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Above TV Room": LocData(345445, "Time Rift - Dead Bird Studio"),

    "Sleepy Subcon - Page: Behind Entrance Area": LocData(345373, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Near Wrecking Ball": LocData(345327, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind Crane": LocData(345371, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Wrecked Treehouse": LocData(345326, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind 2nd Rift Gate": LocData(345372, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Rotating Platform": LocData(345328, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind 3rd Rift Gate": LocData(345329, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Frozen Tree": LocData(345330, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Secret Library": LocData(345370, "Time Rift - Sleepy Subcon"),

    "Alpine Skyline (Rift) - Page: Entrance Area Hidden Ledge": LocData(345016, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Windmill Island Ledge": LocData(345012, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Waterfall Wooden Pillar": LocData(345015, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Lonely Birdhouse Top": LocData(345014, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Below Aqueduct": LocData(345013, "Time Rift - Alpine Skyline"),

    "Deep Sea - Page: Starfish": LocData(346454, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),
    "Deep Sea - Page: Mini Castle": LocData(346452, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),
    "Deep Sea - Page: Urchins": LocData(346449, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),
    "Deep Sea - Page: Big Castle": LocData(346450, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Deep Sea - Page: Castle Top Chest": LocData(304850, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Deep Sea - Page: Urchin Ledge": LocData(346451, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Deep Sea - Page: Hidden Castle Chest": LocData(304849, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Deep Sea - Page: Falling Platform": LocData(346456, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Deep Sea - Page: Lava Starfish": LocData(346453, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1, hookshot=True),

    "Tour - Page: Mafia Town - Ledge": LocData(345038, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Mafia Town - Beach": LocData(345039, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Dead Bird Studio - C.A.W. Agents": LocData(345040, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Dead Bird Studio - Fragile Box": LocData(345041, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Subcon Forest - Giant Frozen Tree": LocData(345042, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Subcon Forest - Top of Pillar": LocData(345043, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Alpine Skyline - Birdhouse": LocData(345044, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Alpine Skyline - Behind Lava Isle": LocData(345047, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: The Finale - Near Entrance": LocData(345087, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),

    "Rumbi Factory - Page: Manhole": LocData(345891, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Shutter Doors": LocData(345888, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Toxic Waste Dispenser": LocData(345892, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: 3rd Area Ledge": LocData(345889, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Green Box Assembly Line": LocData(345884, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Broken Window": LocData(345885, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Money Vault": LocData(345890, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Warehouse Boxes": LocData(345887, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Glass Shelf": LocData(345886, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Last Area": LocData(345883, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
}

contract_locations = {
    "Snatcher's Contract - The Subcon Well": LocData(300200, "Contractual Obligations"),
    "Snatcher's Contract - Toilet of Doom": LocData(300201, "Subcon Forest Area"),
    "Snatcher's Contract - Queen Vanessa's Manor": LocData(300202, "Subcon Forest Area"),
    "Snatcher's Contract - Mail Delivery Service": LocData(300203, "Subcon Forest Area"),
}

shop_locations = {
    "Badge Seller - Item 1": LocData(301003, "Badge Seller"),
    "Badge Seller - Item 2": LocData(301004, "Badge Seller"),
    "Badge Seller - Item 3": LocData(301005, "Badge Seller"),
    "Badge Seller - Item 4": LocData(301006, "Badge Seller"),
    "Badge Seller - Item 5": LocData(301007, "Badge Seller"),
    "Badge Seller - Item 6": LocData(301008, "Badge Seller"),
    "Badge Seller - Item 7": LocData(301009, "Badge Seller"),
    "Badge Seller - Item 8": LocData(301010, "Badge Seller"),
    "Badge Seller - Item 9": LocData(301011, "Badge Seller"),
    "Badge Seller - Item 10": LocData(301012, "Badge Seller"),
    "Mafia Boss Shop Item": LocData(301013, "Spaceship", required_tps=12),

    "Yellow Overpass Station - Yellow Ticket Booth": LocData(301014, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2),
    "Green Clean Station - Green Ticket Booth": LocData(301015, "Green Clean Station", dlc_flags=HatDLC.dlc2),
    "Bluefin Tunnel - Blue Ticket Booth": LocData(301016, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),
    "Pink Paw Station - Pink Ticket Booth": LocData(301017, "Pink Paw Station", dlc_flags=HatDLC.dlc2),

    "Main Station Thug A - Item 1": LocData(301048, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 2": LocData(301049, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 3": LocData(301050, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 4": LocData(301051, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 5": LocData(301052, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),

    "Main Station Thug B - Item 1": LocData(301053, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 2": LocData(301054, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 3": LocData(301055, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 4": LocData(301056, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 5": LocData(301057, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),

    "Main Station Thug C - Item 1": LocData(301058, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 2": LocData(301059, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 3": LocData(301060, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 4": LocData(301061, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 5": LocData(301062, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),

    "Yellow Overpass Thug A - Item 1": LocData(301018, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 2": LocData(301019, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 3": LocData(301020, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 4": LocData(301021, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 5": LocData(301022, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),

    "Yellow Overpass Thug B - Item 1": LocData(301043, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 2": LocData(301044, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 3": LocData(301045, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 4": LocData(301046, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 5": LocData(301047, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),

    "Yellow Overpass Thug C - Item 1": LocData(301063, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 2": LocData(301064, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 3": LocData(301065, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 4": LocData(301066, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 5": LocData(301067, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),

    "Green Clean Station Thug A - Item 1": LocData(301033, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 2": LocData(301034, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 3": LocData(301035, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 4": LocData(301036, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 5": LocData(301037, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),

    # This guy requires either the yellow ticket or the Ice Hat
    "Green Clean Station Thug B - Item 1": LocData(301028, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 2": LocData(301029, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 3": LocData(301030, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 4": LocData(301031, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 5": LocData(301032, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),

    "Bluefin Tunnel Thug - Item 1": LocData(301023, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 2": LocData(301024, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 3": LocData(301025, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 4": LocData(301026, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 5": LocData(301027, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),

    "Pink Paw Station Thug - Item 1": LocData(301038, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 2": LocData(301039, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 3": LocData(301040, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 4": LocData(301041, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 5": LocData(301042, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),

}

# Don't put any of the locations from peaks here, the rules for their entrances are set already
zipline_unlocks = {
    "Alpine Skyline - Bird Pass Fork":                          "Zipline Unlock - The Birdhouse Path",
    "Alpine Skyline - Yellow Band Hills":                       "Zipline Unlock - The Birdhouse Path",
    "Alpine Skyline - The Purrloined Village: Horned Stone":    "Zipline Unlock - The Birdhouse Path",
    "Alpine Skyline - The Purrloined Village: Chest Reward":    "Zipline Unlock - The Birdhouse Path",

    "Alpine Skyline - Mystifying Time Mesa: Zipline":       "Zipline Unlock - The Lava Cake Path",
    "Alpine Skyline - Mystifying Time Mesa: Gate Puzzle":   "Zipline Unlock - The Lava Cake Path",
    "Alpine Skyline - Ember Summit":                        "Zipline Unlock - The Lava Cake Path",

    "Alpine Skyline - Goat Outpost Horn":   "Zipline Unlock - The Windmill Path",
    "Alpine Skyline - Windy Passage":       "Zipline Unlock - The Windmill Path",

    "Alpine Skyline - The Twilight Path":   "Zipline Unlock - The Twilight Bell Path",
}

# Locations in Alpine that are available in The Illness has Spread
# Goat Village locations don't need to be put here
tihs_locations = [
    "Alpine Skyline - Bird Pass Fork",
    "Alpine Skyline - Yellow Band Hills",
    "Alpine Skyline - Ember Summit",
    "Alpine Skyline - Goat Outpost Horn",
    "Alpine Skyline - Windy Passage",
]

event_locs = {
    "Birdhouse Cleared": LocData(0, "The Birdhouse"),
    "Lava Cake Cleared": LocData(0, "The Lava Cake"),
    "Windmill Cleared": LocData(0, "The Windmill"),
    "Twilight Bell Cleared": LocData(0, "The Twilight Bell"),
    "Time Piece Cluster": LocData(0, "The Finale"),

    # not really an act
    "Nyakuza Intro Cleared": LocData(0, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2, act_complete_event=False),

    "Yellow Overpass Station Cleared": LocData(0, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2),
    "Green Clean Station Cleared": LocData(0, "Green Clean Station", dlc_flags=HatDLC.dlc2),
    "Bluefin Tunnel Cleared": LocData(0, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),
    "Pink Paw Station Cleared": LocData(0, "Pink Paw Station", dlc_flags=HatDLC.dlc2),
    "Yellow Overpass Manhole Cleared": LocData(0, "Yellow Overpass Manhole", dlc_flags=HatDLC.dlc2),
    "Green Clean Manhole Cleared": LocData(0, "Green Clean Manhole", dlc_flags=HatDLC.dlc2),
    "Pink Paw Manhole Cleared": LocData(0, "Pink Paw Manhole", dlc_flags=HatDLC.dlc2),
    "Rush Hour Cleared": LocData(0, "Rush Hour", dlc_flags=HatDLC.dlc2),
}

location_table = {
    **ahit_locations,
    **act_completions,
    **storybook_pages,
    **contract_locations,
    **shop_locations,
}
