from .Types import HatDLC, HatType, LocData, Difficulty, HitType
from typing import Dict, TYPE_CHECKING
from .Options import TasksanityCheckCount

if TYPE_CHECKING:
    from . import HatInTimeWorld

TASKSANITY_START_ID = 2000300204


def get_total_locations(world: "HatInTimeWorld") -> int:
    total = 0

    if not world.is_dw_only():
        for name in location_table.keys():
            if is_location_valid(world, name):
                total += 1

        if world.is_dlc1() and world.options.Tasksanity:
            total += world.options.TasksanityCheckCount

    if world.is_dw():
        if world.options.DWShuffle:
            total += len(world.dw_shuffle)
            if world.options.DWEnableBonus:
                total += len(world.dw_shuffle)
        else:
            total += 37
            if world.is_dlc2():
                total += 1

            if world.options.DWEnableBonus:
                total += 37
                if world.is_dlc2():
                    total += 1

    return total


def location_dlc_enabled(world: "HatInTimeWorld", location: str) -> bool:
    data = location_table.get(location) or event_locs.get(location)

    if data.dlc_flags == HatDLC.none:
        return True
    elif data.dlc_flags == HatDLC.dlc1 and world.is_dlc1():
        return True
    elif data.dlc_flags == HatDLC.dlc2 and world.is_dlc2():
        return True
    elif data.dlc_flags == HatDLC.death_wish and world.is_dw():
        return True
    elif data.dlc_flags == HatDLC.dlc1_dw and world.is_dlc1() and world.is_dw():
        return True
    elif data.dlc_flags == HatDLC.dlc2_dw and world.is_dlc2() and world.is_dw():
        return True

    return False


def is_location_valid(world: "HatInTimeWorld", location: str) -> bool:
    if not location_dlc_enabled(world, location):
        return False

    if not world.options.ShuffleStorybookPages and location in storybook_pages.keys():
        return False

    if not world.options.ShuffleActContracts and location in contract_locations.keys():
        return False

    if location not in world.shop_locs and location in shop_locations:
        return False

    data = location_table.get(location) or event_locs.get(location)
    if world.options.ExcludeTour and data.region == "Time Rift - Tour":
        return False

    # No need for all those event items if we're not doing candles
    if data.dlc_flags & HatDLC.death_wish:
        if world.options.DWExcludeCandles and location in event_locs.keys():
            return False

        if world.options.DWShuffle and data.region in death_wishes and data.region not in world.dw_shuffle:
            return False

        if location in zero_jumps:
            if world.options.DWShuffle and "Zero Jumps" not in world.dw_shuffle:
                return False

            difficulty: Difficulty = Difficulty(world.options.LogicDifficulty)
            if location in zero_jumps_hard and difficulty < Difficulty.HARD:
                return False

            if location in zero_jumps_expert and difficulty < Difficulty.EXPERT:
                return False

    return True


def get_location_names() -> Dict[str, int]:
    names = {name: data.id for name, data in location_table.items()}
    id_start: int = TASKSANITY_START_ID
    for i in range(TasksanityCheckCount.range_end):
        names.setdefault(f"Tasksanity Check {i+1}", id_start+i)

    for (key, loc_id) in death_wishes.items():
        names.setdefault(f"{key} - Main Objective", loc_id)
        names.setdefault(f"{key} - All Clear", loc_id+1)

    return names


ahit_locations = {
    "Spaceship - Rumbi Abuse": LocData(2000301000, "Spaceship", hit_type=HitType.umbrella_or_brewing),

    # 300000 range - Mafia Town/Battle of the Birds
    "Welcome to Mafia Town - Umbrella": LocData(2000301002, "Welcome to Mafia Town"),
    "Mafia Town - Old Man (Seaside Spaghetti)": LocData(2000303833, "Mafia Town Area"),
    "Mafia Town - Old Man (Steel Beams)": LocData(2000303832, "Mafia Town Area"),
    "Mafia Town - Blue Vault": LocData(2000302850, "Mafia Town Area"),
    "Mafia Town - Green Vault": LocData(2000302851, "Mafia Town Area"),
    "Mafia Town - Red Vault": LocData(2000302848, "Mafia Town Area"),
    "Mafia Town - Blue Vault Brewing Crate": LocData(2000305572, "Mafia Town Area", required_hats=[HatType.BREWING]),
    "Mafia Town - Plaza Under Boxes": LocData(2000304458, "Mafia Town Area"),
    "Mafia Town - Small Boat": LocData(2000304460, "Mafia Town Area"),
    "Mafia Town - Staircase Pon Cluster": LocData(2000304611, "Mafia Town Area"),
    "Mafia Town - Palm Tree": LocData(2000304609, "Mafia Town Area"),
    "Mafia Town - Port": LocData(2000305219, "Mafia Town Area"),
    "Mafia Town - Docks Chest": LocData(2000303534, "Mafia Town Area"),
    "Mafia Town - Ice Hat Cage": LocData(2000304831, "Mafia Town Area", required_hats=[HatType.ICE]),
    "Mafia Town - Hidden Buttons Chest": LocData(2000303483, "Mafia Town Area"),

    # These can be accessed from HUMT, the above locations can't be
    "Mafia Town - Dweller Boxes": LocData(2000304462, "Mafia Town Area (HUMT)"),
    "Mafia Town - Ledge Chest": LocData(2000303530, "Mafia Town Area (HUMT)"),
    "Mafia Town - Yellow Sphere Building Chest": LocData(2000303535, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beneath Scaffolding": LocData(2000304456, "Mafia Town Area (HUMT)"),
    "Mafia Town - On Scaffolding": LocData(2000304457, "Mafia Town Area (HUMT)"),
    "Mafia Town - Cargo Ship": LocData(2000304459, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beach Alcove": LocData(2000304463, "Mafia Town Area (HUMT)"),
    "Mafia Town - Wood Cage": LocData(2000304606, "Mafia Town Area (HUMT)"),
    "Mafia Town - Beach Patio": LocData(2000304610, "Mafia Town Area (HUMT)"),
    "Mafia Town - Steel Beam Nest": LocData(2000304608, "Mafia Town Area (HUMT)"),
    "Mafia Town - Top of Ruined Tower": LocData(2000304607, "Mafia Town Area (HUMT)", required_hats=[HatType.ICE]),
    "Mafia Town - Hot Air Balloon": LocData(2000304829, "Mafia Town Area (HUMT)", required_hats=[HatType.ICE]),
    "Mafia Town - Camera Badge 1": LocData(2000302003, "Mafia Town Area (HUMT)"),
    "Mafia Town - Camera Badge 2": LocData(2000302004, "Mafia Town Area (HUMT)"),
    "Mafia Town - Chest Beneath Aqueduct": LocData(2000303489, "Mafia Town Area (HUMT)"),
    "Mafia Town - Secret Cave": LocData(2000305220, "Mafia Town Area (HUMT)", required_hats=[HatType.BREWING]),
    "Mafia Town - Crow Chest": LocData(2000303532, "Mafia Town Area (HUMT)"),
    "Mafia Town - Above Boats": LocData(2000305218, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Slip Slide Chest": LocData(2000303529, "Mafia Town Area (HUMT)"),
    "Mafia Town - Behind Faucet": LocData(2000304214, "Mafia Town Area (HUMT)"),
    "Mafia Town - Clock Tower Chest": LocData(2000303481, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Top of Lighthouse": LocData(2000304213, "Mafia Town Area (HUMT)", hookshot=True),
    "Mafia Town - Mafia Geek Platform": LocData(2000304212, "Mafia Town Area (HUMT)"),
    "Mafia Town - Behind HQ Chest": LocData(2000303486, "Mafia Town Area (HUMT)"),

    "Mafia HQ - Hallway Brewing Crate": LocData(2000305387, "Down with the Mafia!", required_hats=[HatType.BREWING]),
    "Mafia HQ - Freezer Chest": LocData(2000303241, "Down with the Mafia!"),
    "Mafia HQ - Secret Room": LocData(2000304979, "Down with the Mafia!", required_hats=[HatType.ICE]),
    "Mafia HQ - Bathroom Stall Chest": LocData(2000303243, "Down with the Mafia!"),

    "Dead Bird Studio - Up the Ladder": LocData(2000304874, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Red Building Top": LocData(2000305024, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Behind Water Tower": LocData(2000305248, "Dead Bird Studio - Elevator Area"),
    "Dead Bird Studio - Side of House": LocData(2000305247, "Dead Bird Studio - Elevator Area"),

    "Dead Bird Studio - DJ Grooves Sign Chest": LocData(2000303901, "Dead Bird Studio - Post Elevator Area",
                                                        hit_type=HitType.umbrella_or_brewing),

    "Dead Bird Studio - Tightrope Chest": LocData(2000303898, "Dead Bird Studio - Post Elevator Area",
                                                  hit_type=HitType.umbrella_or_brewing),

    "Dead Bird Studio - Tepee Chest": LocData(2000303899, "Dead Bird Studio - Post Elevator Area",
                                              hit_type=HitType.umbrella_or_brewing),

    "Dead Bird Studio - Conductor Chest": LocData(2000303900, "Dead Bird Studio - Post Elevator Area",
                                                  hit_type=HitType.umbrella_or_brewing),

    "Murder on the Owl Express - Cafeteria": LocData(2000305313, "Murder on the Owl Express"),
    "Murder on the Owl Express - Luggage Room Top": LocData(2000305090, "Murder on the Owl Express"),
    "Murder on the Owl Express - Luggage Room Bottom": LocData(2000305091, "Murder on the Owl Express"),

    "Murder on the Owl Express - Raven Suite Room": LocData(2000305701, "Murder on the Owl Express",
                                                            required_hats=[HatType.BREWING]),

    "Murder on the Owl Express - Raven Suite Top": LocData(2000305312, "Murder on the Owl Express"),
    "Murder on the Owl Express - Lounge Chest": LocData(2000303963, "Murder on the Owl Express"),

    "Picture Perfect - Behind Badge Seller": LocData(2000304307, "Picture Perfect"),
    "Picture Perfect - Hats Buy Building": LocData(2000304530, "Picture Perfect"),

    "Dead Bird Studio Basement - Window Platform": LocData(2000305432, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Cardboard Conductor": LocData(2000305059, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Above Conductor Sign": LocData(2000305057, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Logo Wall": LocData(2000305207, "Dead Bird Studio Basement"),
    "Dead Bird Studio Basement - Disco Room": LocData(2000305061, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Small Room": LocData(2000304813, "Dead Bird Studio Basement"),
    "Dead Bird Studio Basement - Vent Pipe": LocData(2000305430, "Dead Bird Studio Basement"),
    "Dead Bird Studio Basement - Tightrope": LocData(2000305058, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Cameras": LocData(2000305431, "Dead Bird Studio Basement", hookshot=True),
    "Dead Bird Studio Basement - Locked Room": LocData(2000305819, "Dead Bird Studio Basement", hookshot=True),

    # Subcon Forest
    "Contractual Obligations - Cherry Bomb Bone Cage": LocData(2000324761, "Contractual Obligations"),
    "Subcon Village - Tree Top Ice Cube": LocData(2000325078, "Subcon Forest Area"),
    "Subcon Village - Graveyard Ice Cube": LocData(2000325077, "Subcon Forest Area"),
    "Subcon Village - House Top": LocData(2000325471, "Subcon Forest Area"),
    "Subcon Village - Ice Cube House": LocData(2000325469, "Subcon Forest Area"),
    "Subcon Village - Snatcher Statue Chest": LocData(2000323730, "Subcon Forest Area", paintings=1),
    "Subcon Village - Stump Platform Chest": LocData(2000323729, "Subcon Forest Area"),
    "Subcon Forest - Giant Tree Climb": LocData(2000325470, "Subcon Forest Area"),

    "Subcon Forest - Ice Cube Shack": LocData(2000324465, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Gravestone": LocData(2000326296, "Subcon Forest Area",
                                                required_hats=[HatType.BREWING], paintings=1),

    "Subcon Forest - Swamp Near Well": LocData(2000324762, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree A": LocData(2000324763, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree B": LocData(2000324764, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Ice Wall": LocData(2000324706, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Treehouse": LocData(2000325468, "Subcon Forest Area", paintings=1),
    "Subcon Forest - Swamp Tree Chest": LocData(2000323728, "Subcon Forest Area", paintings=1),

    "Subcon Forest - Burning House": LocData(2000324710, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Tree Climb": LocData(2000325079, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Stump Chest": LocData(2000323731, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Burning Forest Treehouse": LocData(2000325467, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Spider Bone Cage A": LocData(2000324462, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Spider Bone Cage B": LocData(2000325080, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Triple Spider Bounce": LocData(2000324765, "Subcon Forest Area", paintings=2),
    "Subcon Forest - Noose Treehouse": LocData(2000324856, "Subcon Forest Area", hookshot=True, paintings=2),

    "Subcon Forest - Long Tree Climb Chest": LocData(2000323734, "Subcon Forest Area",
                                                     required_hats=[HatType.DWELLER], paintings=2),

    "Subcon Forest - Boss Arena Chest": LocData(2000323735, "Subcon Forest Area"),

    "Subcon Forest - Manor Rooftop": LocData(2000325466, "Subcon Forest Area",
                                             hit_type=HitType.dweller_bell, paintings=1),

    "Subcon Forest - Infinite Yarn Bush": LocData(2000325478, "Subcon Forest Area",
                                                  required_hats=[HatType.BREWING], paintings=2),

    "Subcon Forest - Magnet Badge Bush": LocData(2000325479, "Subcon Forest Area",
                                                 required_hats=[HatType.BREWING], paintings=3),

    "Subcon Forest - Dweller Stump": LocData(2000324767, "Subcon Forest Area",
                                             required_hats=[HatType.DWELLER], paintings=3),

    "Subcon Forest - Dweller Floating Rocks": LocData(2000324464, "Subcon Forest Area",
                                                      required_hats=[HatType.DWELLER], paintings=3),

    "Subcon Forest - Dweller Platforming Tree A": LocData(2000324709, "Subcon Forest Area", paintings=3),

    "Subcon Forest - Dweller Platforming Tree B": LocData(2000324855, "Subcon Forest Area",
                                                          required_hats=[HatType.DWELLER], paintings=3),

    "Subcon Forest - Giant Time Piece": LocData(2000325473, "Subcon Forest Area", paintings=3),
    "Subcon Forest - Gallows": LocData(2000325472, "Subcon Forest Area", paintings=3),

    "Subcon Forest - Green and Purple Dweller Rocks": LocData(2000325082, "Subcon Forest Area", paintings=3),

    "Subcon Forest - Dweller Shack": LocData(2000324463, "Subcon Forest Area",
                                             required_hats=[HatType.DWELLER], paintings=3),

    "Subcon Forest - Tall Tree Hookshot Swing": LocData(2000324766, "Subcon Forest Area",
                                                        hookshot=True,
                                                        paintings=3),

    "Subcon Well - Hookshot Badge Chest": LocData(2000324114, "The Subcon Well",
                                                  hit_type=HitType.umbrella_or_brewing, paintings=1),

    "Subcon Well - Above Chest": LocData(2000324612, "The Subcon Well",
                                         hit_type=HitType.umbrella_or_brewing, paintings=1),

    "Subcon Well - On Pipe": LocData(2000324311, "The Subcon Well", hookshot=True,
                                     hit_type=HitType.umbrella_or_brewing, paintings=1),

    "Subcon Well - Mushroom": LocData(2000325318, "The Subcon Well",
                                      hit_type=HitType.umbrella_or_brewing, paintings=1),

    "Queen Vanessa's Manor - Cellar": LocData(2000324841, "Queen Vanessa's Manor",
                                              hit_type=HitType.dweller_bell, paintings=1),

    "Queen Vanessa's Manor - Bedroom Chest": LocData(2000323808, "Queen Vanessa's Manor",
                                                     hit_type=HitType.dweller_bell, paintings=1),

    "Queen Vanessa's Manor - Hall Chest": LocData(2000323896, "Queen Vanessa's Manor",
                                                  hit_type=HitType.dweller_bell, paintings=1),

    "Queen Vanessa's Manor - Chandelier": LocData(2000325546, "Queen Vanessa's Manor",
                                                  hit_type=HitType.dweller_bell, paintings=1),

    # Alpine Skyline
    "Alpine Skyline - Goat Village: Below Hookpoint": LocData(2000334856, "Alpine Skyline Area (TIHS)"),
    "Alpine Skyline - Goat Village: Hidden Branch": LocData(2000334855, "Alpine Skyline Area (TIHS)"),
    "Alpine Skyline - Goat Refinery": LocData(2000333635, "Alpine Skyline Area (TIHS)", hookshot=True),
    "Alpine Skyline - Bird Pass Fork": LocData(2000335911, "Alpine Skyline Area (TIHS)", hookshot=True),

    "Alpine Skyline - Yellow Band Hills": LocData(2000335756, "Alpine Skyline Area (TIHS)", hookshot=True,
                                                  required_hats=[HatType.BREWING]),

    "Alpine Skyline - The Purrloined Village: Horned Stone": LocData(2000335561, "Alpine Skyline Area"),
    "Alpine Skyline - The Purrloined Village: Chest Reward": LocData(2000334831, "Alpine Skyline Area"),
    "Alpine Skyline - The Birdhouse: Triple Crow Chest": LocData(2000334758, "The Birdhouse"),

    "Alpine Skyline - The Birdhouse: Dweller Platforms Relic": LocData(2000336497, "The Birdhouse",
                                                                       required_hats=[HatType.DWELLER]),

    "Alpine Skyline - The Birdhouse: Brewing Crate House": LocData(2000336496, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Hay Bale": LocData(2000335885, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Alpine Crow Mini-Gauntlet": LocData(2000335886, "The Birdhouse"),
    "Alpine Skyline - The Birdhouse: Outer Edge": LocData(2000335492, "The Birdhouse"),

    "Alpine Skyline - Mystifying Time Mesa: Zipline": LocData(2000337058, "Alpine Skyline Area"),
    "Alpine Skyline - Mystifying Time Mesa: Gate Puzzle": LocData(2000336052, "Alpine Skyline Area"),
    "Alpine Skyline - Ember Summit": LocData(2000336311, "Alpine Skyline Area (TIHS)", hookshot=True),
    "Alpine Skyline - The Lava Cake: Center Fence Cage": LocData(2000335448, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Outer Island Chest": LocData(2000334291, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Dweller Pillars": LocData(2000335417, "The Lava Cake"),
    "Alpine Skyline - The Lava Cake: Top Cake": LocData(2000335418, "The Lava Cake"),
    "Alpine Skyline - The Twilight Path": LocData(2000334434, "Alpine Skyline Area", required_hats=[HatType.DWELLER]),
    "Alpine Skyline - The Twilight Bell: Wide Purple Platform": LocData(2000336478, "The Twilight Bell"),
    "Alpine Skyline - The Twilight Bell: Ice Platform": LocData(2000335826, "The Twilight Bell"),
    "Alpine Skyline - Goat Outpost Horn": LocData(2000334760, "Alpine Skyline Area (TIHS)", hookshot=True),
    "Alpine Skyline - Windy Passage": LocData(2000334776, "Alpine Skyline Area (TIHS)", hookshot=True),
    "Alpine Skyline - The Windmill: Inside Pon Cluster": LocData(2000336395, "The Windmill"),
    "Alpine Skyline - The Windmill: Entrance": LocData(2000335783, "The Windmill"),
    "Alpine Skyline - The Windmill: Dropdown": LocData(2000335815, "The Windmill"),
    "Alpine Skyline - The Windmill: House Window": LocData(2000335389, "The Windmill"),

    "The Finale - Frozen Item": LocData(2000304108, "The Finale"),

    "Bon Voyage! - Lamp Post Top": LocData(2000305321, "Bon Voyage!", dlc_flags=HatDLC.dlc1),
    "Bon Voyage! - Mafia Cargo Ship": LocData(2000304313, "Bon Voyage!", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Toilet": LocData(2000305109, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Bar": LocData(2000304251, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Dive Board Ledge": LocData(2000304254, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Top Balcony": LocData(2000304255, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Octopus Room": LocData(2000305253, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Octopus Room Top": LocData(2000304249, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Laundry Room": LocData(2000304250, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Ship Side": LocData(2000304247, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "The Arctic Cruise - Silver Ring": LocData(2000305252, "Cruise Ship", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Reception Room - Suitcase": LocData(2000304045, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Reception Room - Under Desk": LocData(2000304047, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Lamp Post": LocData(2000304048, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Iceberg Top": LocData(2000304046, "Rock the Boat", dlc_flags=HatDLC.dlc1),
    "Rock the Boat - Post Captain Rescue": LocData(2000304049, "Rock the Boat", dlc_flags=HatDLC.dlc1,
                                                   required_hats=[HatType.ICE]),

    "Nyakuza Metro - Main Station Dining Area": LocData(2000304105, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),
    "Nyakuza Metro - Top of Ramen Shop": LocData(2000304104, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),

    "Yellow Overpass Station - Brewing Crate": LocData(2000305413, "Yellow Overpass Station",
                                                       dlc_flags=HatDLC.dlc2,
                                                       required_hats=[HatType.BREWING]),

    "Bluefin Tunnel - Cat Vacuum": LocData(2000305111, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),

    "Pink Paw Station - Cat Vacuum": LocData(2000305110, "Pink Paw Station",
                                             dlc_flags=HatDLC.dlc2,
                                             hookshot=True,
                                             required_hats=[HatType.DWELLER]),

    "Pink Paw Station - Behind Fan": LocData(2000304106, "Pink Paw Station",
                                             dlc_flags=HatDLC.dlc2,
                                             hookshot=True,
                                             required_hats=[HatType.TIME_STOP, HatType.DWELLER]),
}

act_completions = {
    "Act Completion (Time Rift - Gallery)": LocData(2000312758, "Time Rift - Gallery", required_hats=[HatType.BREWING]),
    "Act Completion (Time Rift - The Lab)": LocData(2000312838, "Time Rift - The Lab"),

    "Act Completion (Welcome to Mafia Town)": LocData(2000311771, "Welcome to Mafia Town"),
    "Act Completion (Barrel Battle)": LocData(2000311958, "Barrel Battle"),
    "Act Completion (She Came from Outer Space)": LocData(2000312262, "She Came from Outer Space"),
    "Act Completion (Down with the Mafia!)": LocData(2000311326, "Down with the Mafia!"),
    "Act Completion (Cheating the Race)": LocData(2000312318, "Cheating the Race", required_hats=[HatType.TIME_STOP]),
    "Act Completion (Heating Up Mafia Town)": LocData(2000311481, "Heating Up Mafia Town", hit_type=HitType.umbrella),
    "Act Completion (The Golden Vault)": LocData(2000312250, "The Golden Vault"),
    "Act Completion (Time Rift - Bazaar)": LocData(2000312465, "Time Rift - Bazaar"),
    "Act Completion (Time Rift - Sewers)": LocData(2000312484, "Time Rift - Sewers"),
    "Act Completion (Time Rift - Mafia of Cooks)": LocData(2000311855, "Time Rift - Mafia of Cooks"),

    "Act Completion (Dead Bird Studio)": LocData(2000311383, "Dead Bird Studio",
                                                 hit_type=HitType.umbrella_or_brewing),

    "Act Completion (Murder on the Owl Express)": LocData(2000311544, "Murder on the Owl Express"),
    "Act Completion (Picture Perfect)": LocData(2000311587, "Picture Perfect"),
    "Act Completion (Train Rush)": LocData(2000312481, "Train Rush", hookshot=True),
    "Act Completion (The Big Parade)": LocData(2000311157, "The Big Parade", hit_type=HitType.umbrella),
    "Act Completion (Award Ceremony)": LocData(2000311488, "Award Ceremony"),
    "Act Completion (Dead Bird Studio Basement)": LocData(2000312253, "Dead Bird Studio Basement", hookshot=True),
    "Act Completion (Time Rift - The Owl Express)": LocData(2000312807, "Time Rift - The Owl Express"),
    "Act Completion (Time Rift - The Moon)": LocData(2000312785, "Time Rift - The Moon"),
    "Act Completion (Time Rift - Dead Bird Studio)": LocData(2000312577, "Time Rift - Dead Bird Studio"),

    "Act Completion (Contractual Obligations)": LocData(2000312317, "Contractual Obligations", paintings=1),

    "Act Completion (The Subcon Well)": LocData(2000311160, "The Subcon Well",
                                                hookshot=True, hit_type=HitType.umbrella_or_brewing, paintings=1),

    "Act Completion (Toilet of Doom)": LocData(2000311984, "Toilet of Doom",
                                               hit_type=HitType.umbrella_or_brewing, hookshot=True, paintings=1),

    "Act Completion (Queen Vanessa's Manor)": LocData(2000312017, "Queen Vanessa's Manor",
                                                      hit_type=HitType.dweller_bell, paintings=1),

    "Act Completion (Mail Delivery Service)": LocData(2000312032, "Mail Delivery Service",
                                                      required_hats=[HatType.SPRINT]),

    "Act Completion (Your Contract has Expired)": LocData(2000311390, "Your Contract has Expired",
                                                          hit_type=HitType.umbrella),

    "Act Completion (Time Rift - Pipe)": LocData(2000313069, "Time Rift - Pipe", hookshot=True),
    "Act Completion (Time Rift - Village)": LocData(2000313056, "Time Rift - Village"),
    "Act Completion (Time Rift - Sleepy Subcon)": LocData(2000312086, "Time Rift - Sleepy Subcon"),

    "Act Completion (The Birdhouse)": LocData(2000311428, "The Birdhouse"),
    "Act Completion (The Lava Cake)": LocData(2000312509, "The Lava Cake"),
    "Act Completion (The Twilight Bell)": LocData(2000311540, "The Twilight Bell"),
    "Act Completion (The Windmill)": LocData(2000312263, "The Windmill"),
    "Act Completion (The Illness has Spread)": LocData(2000312022, "The Illness has Spread", hookshot=True),

    "Act Completion (Time Rift - The Twilight Bell)": LocData(2000312399, "Time Rift - The Twilight Bell",
                                                              required_hats=[HatType.DWELLER]),

    "Act Completion (Time Rift - Curly Tail Trail)": LocData(2000313335, "Time Rift - Curly Tail Trail",
                                                             required_hats=[HatType.ICE]),

    "Act Completion (Time Rift - Alpine Skyline)": LocData(2000311777, "Time Rift - Alpine Skyline"),

    "Act Completion (The Finale)": LocData(2000311872, "The Finale", hookshot=True, required_hats=[HatType.DWELLER]),
    "Act Completion (Time Rift - Tour)": LocData(2000311803, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),

    "Act Completion (Bon Voyage!)": LocData(2000311520, "Bon Voyage!", dlc_flags=HatDLC.dlc1, hookshot=True),
    "Act Completion (Ship Shape)": LocData(2000311451, "Ship Shape", dlc_flags=HatDLC.dlc1),

    "Act Completion (Rock the Boat)": LocData(2000311437, "Rock the Boat", dlc_flags=HatDLC.dlc1,
                                              required_hats=[HatType.ICE]),

    "Act Completion (Time Rift - Balcony)": LocData(2000312226, "Time Rift - Balcony", dlc_flags=HatDLC.dlc1,
                                                    hookshot=True),

    "Act Completion (Time Rift - Deep Sea)": LocData(2000312434, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                                     hookshot=True, required_hats=[HatType.DWELLER, HatType.ICE]),

    "Act Completion (Nyakuza Metro Intro)": LocData(2000311138, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),

    "Act Completion (Yellow Overpass Station)": LocData(2000311206, "Yellow Overpass Station",
                                                        dlc_flags=HatDLC.dlc2,
                                                        hookshot=True),

    "Act Completion (Yellow Overpass Manhole)": LocData(2000311387, "Yellow Overpass Manhole",
                                                        dlc_flags=HatDLC.dlc2,
                                                        required_hats=[HatType.ICE]),

    "Act Completion (Green Clean Station)": LocData(2000311207, "Green Clean Station", dlc_flags=HatDLC.dlc2),

    "Act Completion (Green Clean Manhole)": LocData(2000311388, "Green Clean Manhole",
                                                    dlc_flags=HatDLC.dlc2,
                                                    required_hats=[HatType.ICE, HatType.DWELLER]),

    "Act Completion (Bluefin Tunnel)": LocData(2000311208, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),

    "Act Completion (Pink Paw Station)": LocData(2000311209, "Pink Paw Station",
                                                 dlc_flags=HatDLC.dlc2,
                                                 hookshot=True,
                                                 required_hats=[HatType.DWELLER]),

    "Act Completion (Pink Paw Manhole)": LocData(2000311389, "Pink Paw Manhole",
                                                 dlc_flags=HatDLC.dlc2,
                                                 required_hats=[HatType.ICE]),

    "Act Completion (Rush Hour)": LocData(2000311210, "Rush Hour",
                                          dlc_flags=HatDLC.dlc2,
                                          hookshot=True,
                                          required_hats=[HatType.ICE, HatType.BREWING]),

    "Act Completion (Time Rift - Rumbi Factory)": LocData(2000312736, "Time Rift - Rumbi Factory",
                                                          dlc_flags=HatDLC.dlc2),
}

storybook_pages = {
    "Mafia of Cooks - Page: Fish Pile": LocData(2000345091, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Trash Mound": LocData(2000345090, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Beside Red Building": LocData(2000345092, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Behind Shipping Containers": LocData(2000345095, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Top of Boat": LocData(2000345093, "Time Rift - Mafia of Cooks"),
    "Mafia of Cooks - Page: Below Dock": LocData(2000345094, "Time Rift - Mafia of Cooks"),

    "Dead Bird Studio (Rift) - Page: Behind Cardboard Planet": LocData(2000345449, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Near Time Rift Gate": LocData(2000345447, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Top of Metal Bar": LocData(2000345448, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Lava Lamp": LocData(2000345450, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Above Horse Picture": LocData(2000345451, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Green Screen": LocData(2000345452, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: In The Corner": LocData(2000345453, "Time Rift - Dead Bird Studio"),
    "Dead Bird Studio (Rift) - Page: Above TV Room": LocData(2000345445, "Time Rift - Dead Bird Studio"),

    "Sleepy Subcon - Page: Behind Entrance Area": LocData(2000345373, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Near Wrecking Ball": LocData(2000345327, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind Crane": LocData(2000345371, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Wrecked Treehouse": LocData(2000345326, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind 2nd Rift Gate": LocData(2000345372, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Rotating Platform": LocData(2000345328, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Behind 3rd Rift Gate": LocData(2000345329, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Frozen Tree": LocData(2000345330, "Time Rift - Sleepy Subcon"),
    "Sleepy Subcon - Page: Secret Library": LocData(2000345370, "Time Rift - Sleepy Subcon"),

    "Alpine Skyline (Rift) - Page: Entrance Area Hidden Ledge": LocData(2000345016, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Windmill Island Ledge": LocData(2000345012, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Waterfall Wooden Pillar": LocData(2000345015, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Lonely Birdhouse Top": LocData(2000345014, "Time Rift - Alpine Skyline"),
    "Alpine Skyline (Rift) - Page: Below Aqueduct": LocData(2000345013, "Time Rift - Alpine Skyline"),

    "Deep Sea - Page: Starfish": LocData(2000346454, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),
    "Deep Sea - Page: Mini Castle": LocData(2000346452, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),
    "Deep Sea - Page: Urchins": LocData(2000346449, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1),

    "Deep Sea - Page: Big Castle": LocData(2000346450, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                           hookshot=True),

    "Deep Sea - Page: Castle Top Chest": LocData(2000304850, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                                 hookshot=True),

    "Deep Sea - Page: Urchin Ledge": LocData(2000346451, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                             hookshot=True),

    "Deep Sea - Page: Hidden Castle Chest": LocData(2000304849, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                                    hookshot=True),

    "Deep Sea - Page: Falling Platform": LocData(2000346456, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                                 hookshot=True),

    "Deep Sea - Page: Lava Starfish": LocData(2000346453, "Time Rift - Deep Sea", dlc_flags=HatDLC.dlc1,
                                              hookshot=True),

    "Tour - Page: Mafia Town - Ledge": LocData(2000345038, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Mafia Town - Beach": LocData(2000345039, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Dead Bird Studio - C.A.W. Agents": LocData(2000345040, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Dead Bird Studio - Fragile Box": LocData(2000345041, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Subcon Forest - Giant Frozen Tree": LocData(2000345042, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Subcon Forest - Top of Pillar": LocData(2000345043, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Alpine Skyline - Birdhouse": LocData(2000345044, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: Alpine Skyline - Behind Lava Isle": LocData(2000345047, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),
    "Tour - Page: The Finale - Near Entrance": LocData(2000345087, "Time Rift - Tour", dlc_flags=HatDLC.dlc1),

    "Rumbi Factory - Page: Manhole": LocData(2000345891, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Shutter Doors": LocData(2000345888, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),

    "Rumbi Factory - Page: Toxic Waste Dispenser": LocData(2000345892, "Time Rift - Rumbi Factory",
                                                           dlc_flags=HatDLC.dlc2),

    "Rumbi Factory - Page: 3rd Area Ledge": LocData(2000345889, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),

    "Rumbi Factory - Page: Green Box Assembly Line": LocData(2000345884, "Time Rift - Rumbi Factory",
                                                             dlc_flags=HatDLC.dlc2),

    "Rumbi Factory - Page: Broken Window": LocData(2000345885, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Money Vault": LocData(2000345890, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Warehouse Boxes": LocData(2000345887, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Glass Shelf": LocData(2000345886, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
    "Rumbi Factory - Page: Last Area": LocData(2000345883, "Time Rift - Rumbi Factory", dlc_flags=HatDLC.dlc2),
}

shop_locations = {
    "Badge Seller - Item 1": LocData(2000301003, "Badge Seller"),
    "Badge Seller - Item 2": LocData(2000301004, "Badge Seller"),
    "Badge Seller - Item 3": LocData(2000301005, "Badge Seller"),
    "Badge Seller - Item 4": LocData(2000301006, "Badge Seller"),
    "Badge Seller - Item 5": LocData(2000301007, "Badge Seller"),
    "Badge Seller - Item 6": LocData(2000301008, "Badge Seller"),
    "Badge Seller - Item 7": LocData(2000301009, "Badge Seller"),
    "Badge Seller - Item 8": LocData(2000301010, "Badge Seller"),
    "Badge Seller - Item 9": LocData(2000301011, "Badge Seller"),
    "Badge Seller - Item 10": LocData(2000301012, "Badge Seller"),
    "Mafia Boss Shop Item": LocData(2000301013, "Spaceship"),

    "Yellow Overpass Station - Yellow Ticket Booth": LocData(2000301014, "Yellow Overpass Station",
                                                             dlc_flags=HatDLC.dlc2),

    "Green Clean Station - Green Ticket Booth": LocData(2000301015, "Green Clean Station", dlc_flags=HatDLC.dlc2),
    "Bluefin Tunnel - Blue Ticket Booth": LocData(2000301016, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2),

    "Pink Paw Station - Pink Ticket Booth": LocData(2000301017, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                                    hookshot=True, required_hats=[HatType.DWELLER]),

    "Main Station Thug A - Item 1": LocData(2000301048, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 2": LocData(2000301049, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 3": LocData(2000301050, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 4": LocData(2000301051, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),
    "Main Station Thug A - Item 5": LocData(2000301052, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_0"),

    "Main Station Thug B - Item 1": LocData(2000301053, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 2": LocData(2000301054, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 3": LocData(2000301055, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 4": LocData(2000301056, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),
    "Main Station Thug B - Item 5": LocData(2000301057, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_1"),

    "Main Station Thug C - Item 1": LocData(2000301058, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 2": LocData(2000301059, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 3": LocData(2000301060, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 4": LocData(2000301061, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),
    "Main Station Thug C - Item 5": LocData(2000301062, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_2"),

    "Yellow Overpass Thug A - Item 1": LocData(2000301018, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 2": LocData(2000301019, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 3": LocData(2000301020, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 4": LocData(2000301021, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),
    "Yellow Overpass Thug A - Item 5": LocData(2000301022, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_13"),

    "Yellow Overpass Thug B - Item 1": LocData(2000301043, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 2": LocData(2000301044, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 3": LocData(2000301045, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 4": LocData(2000301046, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),
    "Yellow Overpass Thug B - Item 5": LocData(2000301047, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_5"),

    "Yellow Overpass Thug C - Item 1": LocData(2000301063, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 2": LocData(2000301064, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 3": LocData(2000301065, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 4": LocData(2000301066, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),
    "Yellow Overpass Thug C - Item 5": LocData(2000301067, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2,
                                               nyakuza_thug="Hat_NPC_NyakuzaShop_14"),

    "Green Clean Station Thug A - Item 1": LocData(2000301033, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 2": LocData(2000301034, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 3": LocData(2000301035, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 4": LocData(2000301036, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),
    "Green Clean Station Thug A - Item 5": LocData(2000301037, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   nyakuza_thug="Hat_NPC_NyakuzaShop_4"),

    # This guy requires either the yellow ticket or the Ice Hat
    "Green Clean Station Thug B - Item 1": LocData(2000301028, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 2": LocData(2000301029, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 3": LocData(2000301030, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 4": LocData(2000301031, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),
    "Green Clean Station Thug B - Item 5": LocData(2000301032, "Green Clean Station", dlc_flags=HatDLC.dlc2,
                                                   required_hats=[HatType.ICE], nyakuza_thug="Hat_NPC_NyakuzaShop_6"),

    "Bluefin Tunnel Thug - Item 1": LocData(2000301023, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 2": LocData(2000301024, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 3": LocData(2000301025, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 4": LocData(2000301026, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),
    "Bluefin Tunnel Thug - Item 5": LocData(2000301027, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2,
                                            nyakuza_thug="Hat_NPC_NyakuzaShop_7"),

    "Pink Paw Station Thug - Item 1": LocData(2000301038, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 2": LocData(2000301039, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 3": LocData(2000301040, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 4": LocData(2000301041, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),
    "Pink Paw Station Thug - Item 5": LocData(2000301042, "Pink Paw Station", dlc_flags=HatDLC.dlc2,
                                              required_hats=[HatType.DWELLER], hookshot=True,
                                              nyakuza_thug="Hat_NPC_NyakuzaShop_12"),

}

contract_locations = {
    "Snatcher's Contract - The Subcon Well": LocData(2000300200, "Contractual Obligations"),
    "Snatcher's Contract - Toilet of Doom": LocData(2000300201, "Subcon Forest Area", paintings=1),
    "Snatcher's Contract - Queen Vanessa's Manor": LocData(2000300202, "Subcon Forest Area", paintings=1),
    "Snatcher's Contract - Mail Delivery Service": LocData(2000300203, "Subcon Forest Area", paintings=1),
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

# act completion rules should be set automatically as these are all event items
zero_jumps_hard = {
    "Time Rift - Sewers (Zero Jumps)": LocData(0, "Time Rift - Sewers",
                                               required_hats=[HatType.ICE], dlc_flags=HatDLC.death_wish),

    "Time Rift - Bazaar (Zero Jumps)": LocData(0, "Time Rift - Bazaar",
                                               required_hats=[HatType.ICE], dlc_flags=HatDLC.death_wish),

    "The Big Parade (Zero Jumps)": LocData(0, "The Big Parade",
                                           hit_type=HitType.umbrella,
                                           required_hats=[HatType.ICE],
                                           dlc_flags=HatDLC.death_wish),

    "Time Rift - Pipe (Zero Jumps)": LocData(0, "Time Rift - Pipe", hookshot=True, dlc_flags=HatDLC.death_wish),

    "Time Rift - Curly Tail Trail (Zero Jumps)": LocData(0, "Time Rift - Curly Tail Trail",
                                                         required_hats=[HatType.ICE], dlc_flags=HatDLC.death_wish),

    "Time Rift - The Twilight Bell (Zero Jumps)": LocData(0, "Time Rift - The Twilight Bell",
                                                          required_hats=[HatType.ICE, HatType.DWELLER],
                                                          hit_type=HitType.umbrella_or_brewing,
                                                          dlc_flags=HatDLC.death_wish),

    "The Illness has Spread (Zero Jumps)": LocData(0, "The Illness has Spread",
                                                   required_hats=[HatType.ICE], hookshot=True,
                                                   hit_type=HitType.umbrella_or_brewing, dlc_flags=HatDLC.death_wish),

    "The Finale (Zero Jumps)": LocData(0, "The Finale",
                                       required_hats=[HatType.ICE, HatType.DWELLER],
                                       hookshot=True,
                                       dlc_flags=HatDLC.death_wish),

    "Pink Paw Station (Zero Jumps)": LocData(0, "Pink Paw Station",
                                             required_hats=[HatType.ICE],
                                             hookshot=True,
                                             dlc_flags=HatDLC.dlc2_dw),
}

zero_jumps_expert = {
    "The Birdhouse (Zero Jumps)": LocData(0, "The Birdhouse",
                                          required_hats=[HatType.ICE],
                                          dlc_flags=HatDLC.death_wish),

    "The Lava Cake (Zero Jumps)": LocData(0, "The Lava Cake", dlc_flags=HatDLC.death_wish),

    "The Windmill (Zero Jumps)": LocData(0, "The Windmill",
                                         required_hats=[HatType.ICE],
                                         misc_required=["No Bonk Badge"],
                                         dlc_flags=HatDLC.death_wish),
    "The Twilight Bell (Zero Jumps)": LocData(0, "The Twilight Bell",
                                              required_hats=[HatType.ICE, HatType.DWELLER],
                                              hit_type=HitType.umbrella_or_brewing,
                                              misc_required=["No Bonk Badge"],
                                              dlc_flags=HatDLC.death_wish),

    "Sleepy Subcon (Zero Jumps)": LocData(0, "Time Rift - Sleepy Subcon", required_hats=[HatType.ICE],
                                          dlc_flags=HatDLC.death_wish),

    "Ship Shape (Zero Jumps)": LocData(0, "Ship Shape", required_hats=[HatType.ICE], dlc_flags=HatDLC.dlc1_dw),
}

zero_jumps = {
    **zero_jumps_hard,
    **zero_jumps_expert,
    "Welcome to Mafia Town (Zero Jumps)": LocData(0, "Welcome to Mafia Town", dlc_flags=HatDLC.death_wish),

    "Down with the Mafia! (Zero Jumps)": LocData(0, "Down with the Mafia!",
                                                 required_hats=[HatType.ICE],
                                                 dlc_flags=HatDLC.death_wish),

    "Cheating the Race (Zero Jumps)": LocData(0, "Cheating the Race",
                                              required_hats=[HatType.TIME_STOP],
                                              dlc_flags=HatDLC.death_wish),

    "The Golden Vault (Zero Jumps)": LocData(0, "The Golden Vault",
                                             required_hats=[HatType.ICE],
                                             dlc_flags=HatDLC.death_wish),

    "Dead Bird Studio (Zero Jumps)": LocData(0, "Dead Bird Studio",
                                             required_hats=[HatType.ICE],
                                             hit_type=HitType.umbrella_or_brewing,
                                             dlc_flags=HatDLC.death_wish),

    "Murder on the Owl Express (Zero Jumps)": LocData(0, "Murder on the Owl Express",
                                                      required_hats=[HatType.ICE],
                                                      dlc_flags=HatDLC.death_wish),

    "Picture Perfect (Zero Jumps)": LocData(0, "Picture Perfect", dlc_flags=HatDLC.death_wish),

    "Train Rush (Zero Jumps)": LocData(0, "Train Rush",
                                       required_hats=[HatType.ICE],
                                       hookshot=True,
                                       dlc_flags=HatDLC.death_wish),

    "Contractual Obligations (Zero Jumps)": LocData(0, "Contractual Obligations",
                                                    paintings=1,
                                                    dlc_flags=HatDLC.death_wish),

    "Your Contract has Expired (Zero Jumps)": LocData(0, "Your Contract has Expired",
                                                      hit_type=HitType.umbrella,
                                                      dlc_flags=HatDLC.death_wish),

    # No ice hat/painting required in Expert
    "Toilet of Doom (Zero Jumps)": LocData(0, "Toilet of Doom",
                                           hookshot=True,
                                           hit_type=HitType.umbrella_or_brewing,
                                           required_hats=[HatType.ICE],
                                           paintings=1,
                                           dlc_flags=HatDLC.death_wish),

    "Mail Delivery Service (Zero Jumps)": LocData(0, "Mail Delivery Service",
                                                  required_hats=[HatType.SPRINT],
                                                  dlc_flags=HatDLC.death_wish),

    "Time Rift - Alpine Skyline (Zero Jumps)": LocData(0, "Time Rift - Alpine Skyline",
                                                       required_hats=[HatType.ICE],
                                                       hookshot=True,
                                                       dlc_flags=HatDLC.death_wish),

    "Time Rift - The Lab (Zero Jumps)": LocData(0, "Time Rift - The Lab",
                                                required_hats=[HatType.ICE],
                                                dlc_flags=HatDLC.death_wish),

    "Yellow Overpass Station (Zero Jumps)": LocData(0, "Yellow Overpass Station",
                                                    required_hats=[HatType.ICE],
                                                    hookshot=True,
                                                    dlc_flags=HatDLC.dlc2_dw),

    "Green Clean Station (Zero Jumps)": LocData(0, "Green Clean Station",
                                                required_hats=[HatType.ICE],
                                                dlc_flags=HatDLC.dlc2_dw),
}

snatcher_coins = {
    "Snatcher Coin - Top of HQ (DWTM)": LocData(0, "Down with the Mafia!", snatcher_coin="Snatcher Coin - Top of HQ",
                                                dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of HQ (CTR)": LocData(0, "Cheating the Race", snatcher_coin="Snatcher Coin - Top of HQ",
                                               dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of HQ (HUMT)": LocData(0, "Heating Up Mafia Town", snatcher_coin="Snatcher Coin - Top of HQ",
                                                hit_type=HitType.umbrella, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of HQ (TGV)": LocData(0, "The Golden Vault", snatcher_coin="Snatcher Coin - Top of HQ",
                                               dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of HQ (DW: BTH)": LocData(0, "Beat the Heat", snatcher_coin="Snatcher Coin - Top of HQ",
                                                   hit_type=HitType.umbrella, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Tower": LocData(0, "Mafia Town Area (HUMT)", snatcher_coin="Snatcher Coin - Top of Tower",
                                            dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Tower (DW: BTH)": LocData(0, "Beat the Heat", snatcher_coin="Snatcher Coin - Top of Tower",
                                                      dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Tower (DW: CAT)": LocData(0, "Collect-a-thon", snatcher_coin="Snatcher Coin - Top of Tower",
                                                      dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Tower (SSFOS)": LocData(0, "She Speedran from Outer Space",
                                                    snatcher_coin="Snatcher Coin - Top of Tower",
                                                    dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Tower (DW: MJ)": LocData(0, "Mafia's Jumps", snatcher_coin="Snatcher Coin - Top of Tower",
                                                     dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Under Ruined Tower": LocData(0, "Mafia Town Area",
                                                  snatcher_coin="Snatcher Coin - Under Ruined Tower",
                                                  dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Under Ruined Tower (DW: CAT)": LocData(0, "Collect-a-thon",
                                                            snatcher_coin="Snatcher Coin - Under Ruined Tower",
                                                            dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Under Ruined Tower (DW: SSFOS)": LocData(0, "She Speedran from Outer Space",
                                                              snatcher_coin="Snatcher Coin - Under Ruined Tower",
                                                              dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Red House (DBS)": LocData(0, "Dead Bird Studio - Elevator Area",
                                                      snatcher_coin="Snatcher Coin - Top of Red House",
                                                      dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Top of Red House (DW: SB)": LocData(0, "Security Breach",
                                                         snatcher_coin="Snatcher Coin - Top of Red House",
                                                         dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Train Rush": LocData(0, "Train Rush", snatcher_coin="Snatcher Coin - Train Rush",
                                          hookshot=True, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Train Rush (10 Seconds)": LocData(0, "10 Seconds until Self-Destruct",
                                                       snatcher_coin="Snatcher Coin - Train Rush",
                                                       hookshot=True, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Picture Perfect": LocData(0, "Picture Perfect", snatcher_coin="Snatcher Coin - Picture Perfect",
                                               dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Swamp Tree": LocData(0, "Subcon Forest Area", snatcher_coin="Snatcher Coin - Swamp Tree",
                                          hookshot=True, paintings=1,
                                          dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Swamp Tree (Speedrun Well)": LocData(0, "Speedrun Well",
                                                          snatcher_coin="Snatcher Coin - Swamp Tree",
                                                          hookshot=True, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Manor Roof": LocData(0, "Subcon Forest Area", snatcher_coin="Snatcher Coin - Manor Roof",
                                          hit_type=HitType.dweller_bell, paintings=1,
                                          dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Giant Time Piece": LocData(0, "Subcon Forest Area",
                                                snatcher_coin="Snatcher Coin - Giant Time Piece",
                                                paintings=3, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Goat Village Top": LocData(0, "Alpine Skyline Area (TIHS)",
                                                snatcher_coin="Snatcher Coin - Goat Village Top",
                                                dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Goat Village Top (Illness Speedrun)": LocData(0, "The Illness has Speedrun",
                                                                   snatcher_coin="Snatcher Coin - Goat Village Top",
                                                                   dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Lava Cake": LocData(0, "The Lava Cake", snatcher_coin="Snatcher Coin - Lava Cake",
                                         dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Windmill": LocData(0, "The Windmill", snatcher_coin="Snatcher Coin - Windmill",
                                        dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Windmill (DW: WUW)": LocData(0, "Wound-Up Windmill", snatcher_coin="Snatcher Coin - Windmill",
                                                  hookshot=True, dlc_flags=HatDLC.death_wish),

    "Snatcher Coin - Green Clean Tower": LocData(0, "Green Clean Station",
                                                 snatcher_coin="Snatcher Coin - Green Clean Tower",
                                                 dlc_flags=HatDLC.dlc2_dw),

    "Snatcher Coin - Bluefin Cat Train": LocData(0, "Bluefin Tunnel",
                                                 snatcher_coin="Snatcher Coin - Bluefin Cat Train",
                                                 dlc_flags=HatDLC.dlc2_dw),

    "Snatcher Coin - Pink Paw Fence": LocData(0, "Pink Paw Station",
                                              snatcher_coin="Snatcher Coin - Pink Paw Fence",
                                              dlc_flags=HatDLC.dlc2_dw),
}

event_locs = {
    **zero_jumps,
    **snatcher_coins,
    "HUMT Access": LocData(0, "Heating Up Mafia Town"),
    "TOD Access": LocData(0, "Toilet of Doom"),
    "YCHE Access": LocData(0, "Your Contract has Expired"),
    "AFR Access": LocData(0, "Alpine Free Roam"),
    "TIHS Access": LocData(0, "The Illness has Spread"),

    "Birdhouse Cleared": LocData(0, "The Birdhouse", act_event=True),
    "Lava Cake Cleared": LocData(0, "The Lava Cake", act_event=True),
    "Windmill Cleared": LocData(0, "The Windmill", act_event=True),
    "Twilight Bell Cleared": LocData(0, "The Twilight Bell", act_event=True),
    "Time Piece Cluster": LocData(0, "The Finale", act_event=True),

    # not really an act
    "Nyakuza Intro Cleared": LocData(0, "Nyakuza Free Roam", dlc_flags=HatDLC.dlc2),

    "Yellow Overpass Station Cleared": LocData(0, "Yellow Overpass Station", dlc_flags=HatDLC.dlc2, act_event=True),
    "Green Clean Station Cleared": LocData(0, "Green Clean Station", dlc_flags=HatDLC.dlc2, act_event=True),
    "Bluefin Tunnel Cleared": LocData(0, "Bluefin Tunnel", dlc_flags=HatDLC.dlc2, act_event=True),
    "Pink Paw Station Cleared": LocData(0, "Pink Paw Station", dlc_flags=HatDLC.dlc2, act_event=True),
    "Yellow Overpass Manhole Cleared": LocData(0, "Yellow Overpass Manhole", dlc_flags=HatDLC.dlc2, act_event=True),
    "Green Clean Manhole Cleared": LocData(0, "Green Clean Manhole", dlc_flags=HatDLC.dlc2, act_event=True),
    "Pink Paw Manhole Cleared": LocData(0, "Pink Paw Manhole", dlc_flags=HatDLC.dlc2, act_event=True),
    "Rush Hour Cleared": LocData(0, "Rush Hour", dlc_flags=HatDLC.dlc2, act_event=True),
}

# DO NOT ALTER THE ORDER OF THIS LIST
death_wishes = {
    "Beat the Heat": 2000350000,
    "Snatcher's Hit List": 2000350002,
    "So You're Back From Outer Space": 2000350004,
    "Collect-a-thon": 2000350006,
    "Rift Collapse: Mafia of Cooks": 2000350008,
    "She Speedran from Outer Space": 2000350010,
    "Mafia's Jumps": 2000350012,
    "Vault Codes in the Wind": 2000350014,
    "Encore! Encore!": 2000350016,
    "Snatcher Coins in Mafia Town": 2000350018,

    "Security Breach": 2000350020,
    "The Great Big Hootenanny": 2000350022,
    "Rift Collapse: Dead Bird Studio": 2000350024,
    "10 Seconds until Self-Destruct": 2000350026,
    "Killing Two Birds": 2000350028,
    "Snatcher Coins in Battle of the Birds": 2000350030,
    "Zero Jumps": 2000350032,

    "Speedrun Well": 2000350034,
    "Rift Collapse: Sleepy Subcon": 2000350036,
    "Boss Rush": 2000350038,
    "Quality Time with Snatcher": 2000350040,
    "Breaching the Contract": 2000350042,
    "Snatcher Coins in Subcon Forest": 2000350044,

    "Bird Sanctuary": 2000350046,
    "Rift Collapse: Alpine Skyline": 2000350048,
    "Wound-Up Windmill": 2000350050,
    "The Illness has Speedrun": 2000350052,
    "Snatcher Coins in Alpine Skyline": 2000350054,
    "Camera Tourist": 2000350056,

    "The Mustache Gauntlet": 2000350058,
    "No More Bad Guys": 2000350060,

    "Seal the Deal": 2000350062,
    "Rift Collapse: Deep Sea": 2000350064,
    "Cruisin' for a Bruisin'": 2000350066,

    "Community Rift: Rhythm Jump Studio": 2000350068,
    "Community Rift: Twilight Travels": 2000350070,
    "Community Rift: The Mountain Rift": 2000350072,
    "Snatcher Coins in Nyakuza Metro": 2000350074,
}

location_table = {
    **ahit_locations,
    **act_completions,
    **storybook_pages,
    **contract_locations,
    **shop_locations,
}
