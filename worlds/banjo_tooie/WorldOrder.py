from worlds.banjo_tooie.Options import EggsBehaviour, GameLength, JamjarsSiloCosts, LogicType, ProgressiveEggAim, ProgressiveWaterTraining, RandomizeBKMoveList, OpenSilos

from .Names import itemName, regionName, locationName
from typing import TYPE_CHECKING, List
from .Locations import all_location_table

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld
else:
    BanjoTooieWorld = object

# Shamelessly Stolen from KH2 :D


def WorldRandomize(world: BanjoTooieWorld) -> None:
    # Universal Tracker Magic
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Banjo-Tooie" in world.multiworld.re_gen_passthrough:
            passthrough = world.multiworld.re_gen_passthrough["Banjo-Tooie"]
            world.randomize_worlds = passthrough["world_order"]
            world.randomize_order = passthrough["world_keys"]
            world.worlds_randomized = bool(passthrough["worlds"] == "true")
            world.starting_egg = passthrough["starting_egg"]
            world.starting_attack = passthrough["starting_attack"]
            world.single_silo = passthrough["first_silo"]
            world.jamjars_siloname_costs = passthrough["jamjars_siloname_costs"]
            world.loading_zones = passthrough["loading_zones"]
    else:
        randomize_level_order(world)
        set_level_costs(world)
        randomize_entrance_loading_zones(world)
        choose_unlocked_silos(world)
        handle_early_moves(world)
        generate_jamjars_costs(world)

def randomize_level_order(world: BanjoTooieWorld) -> None:
    world.worlds_randomized = world.options.randomize_worlds
    if not world.worlds_randomized:
        world.randomize_order = {
            regionName.MT:  1230944, #These ids stay in the same order, but the keys may switch order when randomized.
            regionName.GM:  1230945,
            regionName.WW:  1230946,
            regionName.JR:  1230947,
            regionName.TL:  1230948,
            regionName.GIO: 1230949,
            regionName.HP:  1230950,
            regionName.CC:  1230951,
            regionName.CK:  1230952
        }
    else:
        if world.options.randomize_world_loading_zone:
            randomizable_levels = [regionName.MT,regionName.GM,regionName.WW,regionName.JR,regionName.TL,regionName.GIO,regionName.HP,regionName.CC,regionName.CK]
            world_order = generate_world_order(world, randomizable_levels)

            world.randomize_order = {world_order[i]: i+1230944 for i in range(len(world_order))}
        else:
            randomizable_levels = [regionName.MT,regionName.GM,regionName.WW,regionName.JR,regionName.TL,regionName.GIO,regionName.HP,regionName.CC]
            world_order = generate_world_order(world, randomizable_levels)
            world.randomize_order = {world_order[i]: i+1230944 for i in range(len(world_order))}
            world.randomize_order.update({regionName.CK: 1230952})

def generate_world_order(world: BanjoTooieWorld, worlds: List[str]) -> List[str]:

    bad_first_worlds = set()
    # Fewer than 4 collectibles to get progressive Claw Clambers.
    if world.options.progressive_shoes:
        bad_first_worlds.add(regionName.CK)
    # Not enough collectibles in the overworld to get to Quag
    if world.options.randomize_bk_moves != RandomizeBKMoveList.option_all and world.options.open_silos == OpenSilos.option_none:
        bad_first_worlds.update([regionName.GIO, regionName.CK])
    # Without nests, reaching Wasteland might not be possible
    if world.options.randomize_bk_moves == RandomizeBKMoveList.option_mcjiggy_special and world.options.open_silos == OpenSilos.option_none\
        and not world.options.nestsanity:
        bad_first_worlds.update([regionName.CC, regionName.TL])

    world1 = world.random.choice([w for w in worlds if w not in bad_first_worlds])
    # The 2nd world needs to be not too hard to access from the first world.
    easy_2nd_worlds = {
        regionName.MT: [regionName.GM],
        regionName.GM: [regionName.MT, regionName.WW, regionName.JR, regionName.HP],
        regionName.WW: [regionName.MT, regionName.GM, regionName.TL, regionName.CC],
        regionName.JR: [regionName.MT, regionName.GM, regionName.HP],
        # GI is not easy when you need 3 progressive shoes.
        regionName.TL: [regionName.MT, regionName.GM, regionName.WW, regionName.CC] if world.options.progressive_shoes else [regionName.MT, regionName.GM, regionName.WW, regionName.GIO, regionName.CC],
        # Reaching CK is not easy when you need 4 progressive shoes.
        regionName.GIO: [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC] if world.options.progressive_shoes else [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC, regionName.CK],
        regionName.HP:  [regionName.MT, regionName.GM, regionName.JR],
        # Same thing with GI here.
        regionName.CC: [regionName.MT, regionName.GM, regionName.WW, regionName.TL] if world.options.progressive_shoes else [regionName.MT, regionName.GM, regionName.WW, regionName.GIO, regionName.TL],
        regionName.CK:  [regionName.MT, regionName.GM, regionName.GIO, regionName.TL, regionName.CC]
    }
    world2 = world.random.choice(easy_2nd_worlds[world1])
    left_worlds = [w for w in worlds if w not in [world1, world2]]
    world.random.shuffle(left_worlds)

    worlds = [world1] + [world2] + left_worlds

    return worlds

def set_level_costs(world: BanjoTooieWorld) -> None:
    normal_costs = [1,4,8,14,20,28,36,45,55]
    quick_costs = [1,3,6,10,15,21,28,35,44]
    long_costs = [1,8,16,25,34,43,52,60,70]
    level_cost_max = [1,10,20,30,50,60,70,80,90]
    custom_costs = world.options.custom_worlds.value.split(",")

    random_costs = [1,1,1,1,1,1,1,1,1]
    for i in range(len(random_costs)):
        random_costs[i] = world.random.randint(1, level_cost_max[i])

    if len(custom_costs) < 9:
        raise ValueError("Custom Costs has too few levels.")

    if len(custom_costs) > 9:
        raise ValueError("Custom Costs has too many levels.")

    for i in range(len(custom_costs)):
        try:
            int(custom_costs[i])
        except Exception:
            raise ValueError("Custom Cost for world "+str(i+1)+" must be a number.")
        custom_costs[i] = int(custom_costs[i])
        if custom_costs[i] == 0:
            raise ValueError("Custom Cost for world "+str(i+1)+" can't be 0.")
        if custom_costs[i] < 0:
            raise ValueError("Custom Cost for world "+str(i+1)+" can't be negative.")
        if custom_costs[i] > level_cost_max[i]:
            raise ValueError("Custom Cost for world "+str(i+1)+" is too high.")

    chosen_costs = []
    if world.options.game_length == GameLength.option_quick:
        chosen_costs = quick_costs
    elif world.options.game_length == GameLength.option_normal:
        chosen_costs = normal_costs
    elif world.options.game_length == GameLength.option_long:
        chosen_costs = long_costs
    elif world.options.game_length == GameLength.option_custom:
        chosen_costs = custom_costs
    elif world.options.game_length == GameLength.option_randomize:
        chosen_costs = random_costs

    world.randomize_worlds = {list(world.randomize_order.keys())[i]: chosen_costs[i] for i in range(len(list(world.randomize_order.keys())))}


def randomize_entrance_loading_zones(world: BanjoTooieWorld) -> None:
    randomizable_levels = list(world.randomize_worlds.keys()) # Gives the levels in the order that they open.
    if not world.options.randomize_world_loading_zone:
        world.loading_zones = {level: level for level in randomizable_levels}
    else:
        good_levels = [l for l in randomizable_levels if l not in [regionName.CK, regionName.GIO]]
        level1 = world.random.choice(good_levels)

        rest_levels = [l for l in randomizable_levels if l != level1]
        world.random.shuffle(rest_levels)

        randomized_levels = [level1] + rest_levels

        world.loading_zones = {randomizable_levels[i]: randomized_levels[i] for i in range(len(randomizable_levels))}


def choose_unlocked_silos(world: BanjoTooieWorld) -> None:
    if not world.options.randomize_bk_moves == RandomizeBKMoveList.option_all and world.options.open_silos == OpenSilos.option_none:
        world.single_silo = "NONE"

    elif world.options.randomize_bk_moves == RandomizeBKMoveList.option_all and\
        not world.options.randomize_worlds and world.options.open_silos == OpenSilos.option_none:
        world.single_silo = "NONE"

    elif world.options.open_silos == OpenSilos.option_all:
        world.single_silo = "ALL"

    elif world.options.randomize_bk_moves == RandomizeBKMoveList.option_all and world.options.randomize_worlds\
        or world.options.open_silos == OpenSilos.option_one:
        # One silo chosen or imposed.

        if list(world.randomize_order.keys())[0] == regionName.GIO:
            # GI is special. If loading zones are not randomized, the only way to make progress in the level is by riding the train into the level from Cliff Top.
            world.single_silo = regionName.IOHQM if world.options.randomize_world_loading_zone else regionName.IOHCT
        else:
            overworld_lookup = {
                regionName.MT: world.random.choice([regionName.IOHPL, regionName.IOHPG, regionName.IOHCT, regionName.IOHQM]), # You can already get there, so you get a bonus silo! (Nobody likes Mayahell anyway.)
                regionName.GM: regionName.IOHPL,
                regionName.WW: regionName.IOHPG,
                regionName.JR: regionName.IOHCT,
                regionName.TL: regionName.IOHWL,
                regionName.HP: regionName.IOHCT,
                regionName.CC: regionName.IOHWL,
                regionName.CK: regionName.IOHQM,
            }
            world.single_silo = overworld_lookup[list(world.randomize_order.keys())[0]]
    else:
        raise ValueError("These settings were not considered when randomizing loading zones. Please give us your settings so that we fix it.")

def handle_early_moves(world: BanjoTooieWorld) -> None:
    first_level = list(world.randomize_worlds.keys())[0]
    actual_first_level = world.loading_zones[first_level]

    # A silo to the first world is not given.
    if world.options.randomize_bk_moves != RandomizeBKMoveList.option_all and world.single_silo == "NONE":
        if  first_level != regionName.MT and world.options.logic_type != LogicType.option_easy_tricks:
            world.multiworld.early_items[world.player][itemName.GGRAB] = 1

            if first_level == regionName.WW:
                early_fire_eggs(world)
            if first_level == regionName.JR or first_level == regionName.HP:
                world.multiworld.early_items[world.player][itemName.SPLITUP] = 1
            if first_level == regionName.TL or first_level == regionName.CC:
                early_fire_eggs(world)
                early_torpedo(world)
            if first_level == regionName.CK: # CK can't be first if progressive shoes.
                world.multiworld.early_items[world.player][itemName.CLAWBTS] = 1

    if world.options.randomize_bk_moves == RandomizeBKMoveList.option_all: # Guaranteed silo to first level, but getting enough stuff in levels is still hard sometimes.
        # MT, GGM, WW Easy

        if actual_first_level == regionName.JR and not world.options.randomize_doubloons:
            move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.TTROT]
            move = world.random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

        # TDL Easy

        if first_level == regionName.GIO and not world.options.randomize_world_loading_zone: # Moves to enter the train.
            world.multiworld.early_items[world.player][itemName.CHUFFY] = 1
            world.multiworld.early_items[world.player][itemName.TRAINSWGI] = 1
            world.multiworld.early_items[world.player][itemName.CLIMB] = 1
            world.multiworld.early_items[world.player][itemName.TRAINSWIH] = 1
            world.multiworld.early_items[world.player][world.random.choice([itemName.FFLIP, itemName.TTROT, itemName.TJUMP])] = 1

        if actual_first_level == regionName.HP:
            move_lst = [itemName.TJUMP, itemName.FFLIP, itemName.TTROT]
            move = world.random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

        if actual_first_level == regionName.CC:
            if world.options.progressive_flight:
                move_lst = [itemName.SPLITUP, itemName.PFLIGHT]
            else:
                move_lst = [itemName.SPLITUP, itemName.FPAD]
            move = world.random.choice(move_lst)
            world.multiworld.early_items[world.player][move] = 1

        if first_level == regionName.CK: # CK can't be first if progressive shoes.
                world.multiworld.early_items[world.player][itemName.CLAWBTS] = 1


def early_fire_eggs(world: BanjoTooieWorld) -> None:
    world.multiworld.early_items[world.player][itemName.PEGGS if world.options.egg_behaviour == EggsBehaviour.option_progressive_eggs else itemName.FEGGS] = 1
    if world.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
        if world.options.progressive_egg_aiming == ProgressiveEggAim.option_basic:
            world.multiworld.early_items[world.player][itemName.PEGGAIM] = 2
        elif world.options.progressive_egg_aiming == ProgressiveEggAim.option_advanced:
            world.multiworld.early_items[world.player][itemName.PAEGGAIM] = 3
        else:
            world.multiworld.early_items[world.player][world.random.choice([itemName.EGGAIM, itemName.EGGSHOOT])] = 1

def early_torpedo(world: BanjoTooieWorld) -> None:
    if world.options.randomize_bk_moves != RandomizeBKMoveList.option_none:
        if world.options.progressive_water_training == ProgressiveWaterTraining.option_basic:
            world.multiworld.early_items[world.player][itemName.PSWIM] = 1
            world.multiworld.early_items[world.player][itemName.TTORP] = 1
        elif world.options.progressive_water_training == ProgressiveWaterTraining.option_advanced:
            world.multiworld.early_items[world.player][itemName.PASWIM] = 3
        else:
            world.multiworld.early_items[world.player][itemName.DIVE] = 1
            world.multiworld.early_items[world.player][itemName.TTORP] = 1


def generate_jamjars_costs(world: BanjoTooieWorld) -> None:
    if world.options.jamjars_silo_costs == JamjarsSiloCosts.option_vanilla:
        world.jamjars_siloname_costs = {
            locationName.FEGGS: 45,
            locationName.GEGGS: 110,
            locationName.IEGGS: 200,
            locationName.CEGGS: 315,
            locationName.EGGAIM: 25,
            locationName.BBLASTER: 30,
            locationName.GGRAB: 35,
            locationName.BDRILL: 85,
            locationName.BBAYONET: 95,
            locationName.SPLITUP: 160,
            locationName.PACKWH: 170,
            locationName.AIREAIM: 180,
            locationName.WWHACK: 265,
            locationName.AUQAIM: 275,
            locationName.TTORP: 290,
            locationName.SPRINGB: 390,
            locationName.TAXPACK: 405,
            locationName.HATCH: 420,
            locationName.CLAWBTS: 505,
            locationName.SNPACK: 525,
            locationName.LSPRING: 545,
            locationName.SHPACK: 640,
            locationName.GLIDE: 660,
            locationName.SAPACK: 765,
        }
    elif world.options.jamjars_silo_costs == JamjarsSiloCosts.option_randomize:
        silo_locations = [
            locationName.FEGGS,
            locationName.GEGGS,
            locationName.IEGGS,
            locationName.CEGGS,
            locationName.EGGAIM,
            locationName.BBLASTER,
            locationName.GGRAB,
            locationName.BDRILL,
            locationName.BBAYONET,
            locationName.SPLITUP,
            locationName.PACKWH,
            locationName.AIREAIM,
            locationName.WWHACK,
            locationName.AUQAIM,
            locationName.TTORP,
            locationName.SPRINGB,
            locationName.TAXPACK,
            locationName.HATCH,
            locationName.CLAWBTS,
            locationName.SNPACK,
            locationName.LSPRING,
            locationName.SHPACK,
            locationName.GLIDE,
            locationName.SAPACK,
        ]

        for location in silo_locations:
            world.jamjars_siloname_costs.update({location: world.random.randint(0, 160)*5})

    elif world.options.jamjars_silo_costs == JamjarsSiloCosts.option_progressive:
        # We have no control over overworld progression, so those stay vanilla.
        world.jamjars_siloname_costs = {
            locationName.FEGGS: 45,
            locationName.GEGGS: 110,
            locationName.IEGGS: 200,
            locationName.CEGGS: 315
        }

        # In decreasing order so that pop removes the lowest.
        move_costs = [765, 660, 640, 545, 525, 505, 420, 405, 390, 290, 275, 265, 180, 170, 160, 95, 85, 35, 30, 25]
        moves_per_world = {
            regionName.MT: [
                locationName.EGGAIM,
                locationName.BBLASTER,
                locationName.GGRAB,
                ],
            regionName.GM: [
                locationName.BDRILL,
                locationName.BBAYONET,
            ],
            regionName.WW: [
                locationName.SPLITUP,
                locationName.PACKWH,
                locationName.AIREAIM,
            ],
            regionName.JR: [
                locationName.WWHACK,
                locationName.AUQAIM,
                locationName.TTORP,
            ],
            regionName.TL: [
                locationName.SPRINGB,
                locationName.TAXPACK,
                locationName.HATCH,
            ],
            regionName.GIO: [
                locationName.CLAWBTS,
                locationName.SNPACK,
                locationName.LSPRING,
            ],
            regionName.HP: [
                locationName.SHPACK,
                locationName.GLIDE,
            ],
            regionName.CC: [
                locationName.SAPACK,
            ],
            regionName.CK: []
        }

        for world_entrance in world.randomize_order:
            actual_level = world.loading_zones[world_entrance]
            for silo in moves_per_world[actual_level]:
                world.jamjars_siloname_costs.update({silo: move_costs.pop()})

    for name, value in world.jamjars_siloname_costs.items():
        world.jamjars_silo_costs[all_location_table[name].btid] = value
