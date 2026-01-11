from typing import Dict, List, Any, NamedTuple, TYPE_CHECKING
from .entrances import global_entrances, EntranceData, EntGroup, innersea_entrances, town_entrances, \
    safe_entrances, safe_overworld_entrances_early, safe_overworld_entrances_west, \
    safe_entrances_overworld_only, titan_regions, internal_dungeons, internal_dungeons_ext, split_regions
from .data import entnames, regnames

if TYPE_CHECKING:
    from . import FF1pixelWorld, FF1pixelOptions

class EntranceShufflingData:
    def __init__(self, name, init_entrances, ow_shuffle = True, fill = True):
        self.name: str = name
        self.origin_entrances: List[EntranceData] = init_entrances
        self.entrances: List[EntranceData] = []
        self.stored_deadends: List[EntranceData] = []
        self.overworld_shuffle: bool = ow_shuffle
        self.allow_fill: bool = fill

    def early_candidate(self) -> bool:
        return self.overworld_shuffle and self.allow_fill and len(self.entrances) == 0

    def deadend_candidate(self) -> bool:
        return self.allow_fill and (len(self.origin_entrances) - len(self.stored_deadends)) > 0

def random_pop(world: "FF1pixelWorld", seq:List[Any]) -> Any:
    choice = world.random.choice(seq)
    seq.remove(choice)
    return choice

def shuffle_entrances(world: "FF1pixelWorld") -> None:
    options = world.options
    ow_is_shuffled = options.shuffle_overworld or options.shuffle_entrances == 3

    new_entrances: List[EntranceData] = []

    def connect_entrance(connect_pool: EntranceShufflingData, target_entrance: EntranceData) -> None:
        origin_entrance = world.random.choice(connect_pool.origin_entrances)
        connect_pool.origin_entrances.remove(origin_entrance)
        new_entrances.append(
            EntranceData(origin_entrance.name, origin_entrance.region, target_entrance.target_point,
                         target_entrance.target_region, target_entrance.type, target_entrance.group,
                         target_entrance.deadend, target_entrance.access_req))
        if origin_entrance.target_point != target_entrance.target_point:
            world.result_entrances[origin_entrance.name] = target_entrance.target_point
        if not target_entrance.deadend:
            connect_pool.origin_entrances += [e for e in global_entrances if e.region == target_entrance.target_region]

    def place_entrance_rng(pools: List[EntranceShufflingData], entrance: EntranceData, disable_fill: bool = False) -> None:
        if len(pools) == 0:
            print("Placing: Error, couldn't place " + entrance.name + " in any pool.")
        place_pool = world.random.choice(pools)
        #print("Placing: " + entrance.name + " in " + place_pool.name)
        place_pool.entrances.append(entrance)
        if entrance in all_entrances:
            all_entrances.remove(entrance)
        if disable_fill:
            place_pool.allow_fill = False
        connect_entrance(place_pool, entrance)

    def place_entrance(single_pool: EntranceShufflingData, entrance: EntranceData, disable_fill: bool = False) -> None:
        #print("Placing: " + entrance.name + " in " + single_pool.name)
        place_pool = single_pool
        place_pool.entrances.append(entrance)
        if entrance in all_entrances:
            all_entrances.remove(entrance)
        if disable_fill:
            place_pool.allow_fill = False
        connect_entrance(place_pool, entrance)

    # 1. Process Town Options
    town_option = options.shuffle_towns
    if town_option == 3 and options.shuffle_entrances < 3:
        town_option = 2

    if town_option == 2 and not options.shuffle_overworld:
        town_option = 1

    # 2. Initial Pools + Add special pools
    ow_entrances = [e for e in global_entrances if e.type == EntGroup.OverworldDungeon or e.type == EntGroup.OverworldTown]
    ow_town_entrances = [e for e in global_entrances if e.type == EntGroup.OverworldTown]
    ow_pools = {e.name: EntranceShufflingData(e.name,[e]) for e in ow_entrances}

    ow_pools["Sunken Shrine"] = EntranceShufflingData("Sunken Shrine",
                                                             [e for e in global_entrances
                                                              if e.region == regnames.sunken_shrine_3f_split],
                                                             False,
                                                             options.shuffle_entrances > 0)

    ow_pools["Chaos Shrine Right"] = EntranceShufflingData("Chaos Shrine Right",
                                                            [e for e in global_entrances
                                                             if e.name == entnames.chaos_shrine_1f_entrance_right_stairs],
                                                            False,
                                                            False)
    ow_pools["Chaos Shrine Left"] = EntranceShufflingData("Chaos Shrine Left",
                                                            [e for e in global_entrances
                                                             if e.name == entnames.chaos_shrine_1f_entrance_left_stairs],
                                                            False,
                                                            False)

    # 3. Set Entrances to be shuffled
    all_entrances = []

    if ow_is_shuffled:
        all_entrances = ow_entrances

    dungeon_entrances = []
    if 0 < options.shuffle_entrances < 3:
        if options.shuffle_entrances == 1:
            dungeon_entrances = internal_dungeons
        else:
            dungeon_entrances = internal_dungeons_ext

        for dungeon in dungeon_entrances:
            all_entrances += [e for e in global_entrances if e.group == dungeon and e.type != EntGroup.Fixed and e not in all_entrances]
    elif options.shuffle_entrances == 3:
        all_entrances += [e for e in global_entrances if e.type == EntGroup.InnerDungeon]

    # Maybe a list
    shallow_entrances = [e for e in global_entrances if e.name == entnames.overworld_chaos_shrine]

    # 4. Process Towns
    if options.early_progression == 0:
        pravoka_towns = [e for e in ow_town_entrances if e.name == entnames.overworld_pravoka]
        if len(pravoka_towns) > 0:
            place_entrance(ow_pools[pravoka_towns[0].name], pravoka_towns[0], True)
            ow_town_entrances.remove(pravoka_towns[0])

    if town_option == 0:
        for town in ow_town_entrances:
            all_entrances = [e for e in all_entrances if e != town]
            ow_pools[town.name].entrances.append(town)
            ow_pools[town.name].allow_fill = False
    elif town_option == 1:
        town_pools = [p for p in ow_pools.values() if p.name in [t.name for t in ow_town_entrances]]
        for pool in town_pools:
            picked_entrance =  world.random.choice(ow_town_entrances)
            place_entrance(pool, picked_entrance, True)
            ow_town_entrances.remove(picked_entrance)
    elif town_option == 2:
        shallow_entrances += ow_town_entrances

    # 5. Process Special Entrances
    # Safe Entrance
    if ow_is_shuffled:
        if options.shuffle_entrances == 3:
            candidate_safe_entrances = safe_entrances
        else:
            candidate_safe_entrances = safe_entrances_overworld_only
        safe_entrance = world.random.choice([e for e in all_entrances if e.name in candidate_safe_entrances])
        if options.early_progression == 0:
            safe_ow_entrances = safe_overworld_entrances_early
        else:
            safe_ow_entrances = safe_overworld_entrances_west
        safe_pools = [p for p in ow_pools.values() if p.name in safe_ow_entrances and p.early_candidate()]
        place_entrance_rng(safe_pools, safe_entrance, True)

    # Titan
    if ow_is_shuffled:
        titan_entrances = [e for e in all_entrances if e.target_region == regnames.giants_cavern]

        new_titan_regions: Dict[str, List[EntranceShufflingData]] = {}
        for region, region_entrances in titan_regions.items():
            valid_entrances = [p for p in ow_pools.values()
                            if len([e for e in p.origin_entrances if not e.access_req]) > 0
                            and p.early_candidate()
                            and p.name in region_entrances]
            if len(valid_entrances) > 0:
                new_titan_regions[region] = valid_entrances

        for titan_entrance in titan_entrances:
            picked_region = new_titan_regions.pop(world.random.choice([r for r in new_titan_regions.keys()]), None)
            place_entrance_rng(picked_region, titan_entrance, True)

    # Mount Duergar (Prevent Canal softlock)
    if ow_is_shuffled:
        dwarf_entrance = [e for e in all_entrances if e.target_region == regnames.mount_duergar][0]

        dwarf_pools = [p for p in ow_pools.values()
                        if p.name in innersea_entrances
                        and p.early_candidate()]

        if options.shuffle_entrances < 3:
            place_entrance_rng(dwarf_pools, dwarf_entrance, options.shuffle_entrances < 3)
        else:
            dwarf_pool = world.random.choice(dwarf_pools)
            dwarf_pool.stored_deadends.append(dwarf_entrance)
            dwarf_pool.entrances.append(dwarf_entrance)
            all_entrances.remove(dwarf_entrance)

    # Prevent Onrac getting placed in Sunken Shrine
    if options.shuffle_entrances == 3 and options.shuffle_towns == 3:
        onrac_town = [e for e in all_entrances if e.target_region == regnames.onrac][0]
        onrac_pools = [p for p in ow_pools.values()
                        if p.name != "Sunken Shrine"
                        and p.early_candidate()]

        onrac_pool = world.random.choice(onrac_pools)
        onrac_pool.stored_deadends.append(onrac_town)
        onrac_pool.entrances.append(onrac_town)
        all_entrances.remove(onrac_town)

    # Shallow Entrances
    if ow_is_shuffled:
        for e in [s for s in shallow_entrances if s in all_entrances]:
            shallow_pools = [p for p in ow_pools.values() if p.early_candidate()]
            place_entrance_rng(shallow_pools, e, True)

    # Chaos Shrine
    if options.shuffle_entrances > 0:
        chaos_entrances = [e for e in global_entrances if e.group == "Chaos Shrine"]

        lute_entrance = [e for e in chaos_entrances if e.name == entnames.chaos_shrine_2f_corridor_right_stairs][0]
        final_entrance = [e for e in chaos_entrances if e.name == entnames.chaos_shrine_b4_right_stairs][0]
        b1_deadeand_entrance = [e for e in chaos_entrances if e.name == entnames.chaos_shrine_1f_entrance_left_stairs][0]
        chaos_entrances.remove(lute_entrance)
        chaos_entrances.remove(final_entrance)
        chaos_entrances.remove(b1_deadeand_entrance)

        chaos_entrances_groups = [[lute_entrance, final_entrance], [b1_deadeand_entrance]]

        while len(chaos_entrances) > 0:
            picked_group = world.random.choice(chaos_entrances_groups)
            picked_entrance = world.random.choice(chaos_entrances)
            picked_group.append(picked_entrance)
            chaos_entrances.remove(picked_entrance)

        chaos_entrances_group = world.random.choice(chaos_entrances_groups)
        chaos_entrances_groups.remove(chaos_entrances_group)

        chaos_entrances_prog = [e for e in chaos_entrances_group if not e.deadend]
        chaos_entrances_dead = [e for e in chaos_entrances_group if e.deadend]

        while len(chaos_entrances_prog) > 0:
            chaos_entrance = random_pop(world, chaos_entrances_prog)
            place_entrance(ow_pools["Chaos Shrine Right"], chaos_entrance)

        while len(chaos_entrances_dead) > 0:
            chaos_entrance = random_pop(world, chaos_entrances_dead)
            place_entrance(ow_pools["Chaos Shrine Right"], chaos_entrance)

        chaos_entrances_group = world.random.choice(chaos_entrances_groups)
        chaos_entrances_groups.remove(chaos_entrances_group)

        chaos_entrances_prog = [e for e in chaos_entrances_group if not e.deadend]
        chaos_entrances_dead = [e for e in chaos_entrances_group if e.deadend]

        while len(chaos_entrances_prog) > 0:
            chaos_entrance = random_pop(world, chaos_entrances_prog)
            place_entrance(ow_pools["Chaos Shrine Left"], chaos_entrance)

        while len(chaos_entrances_dead) > 0:
            chaos_entrance = random_pop(world, chaos_entrances_dead)
            place_entrance(ow_pools["Chaos Shrine Left"], chaos_entrance)

    # 6. Place everything else
    prog_mixed_entrances = [e for e in all_entrances if not e.deadend]
    deadend_mixed_entrances = [e for e in all_entrances if e.deadend]

    # Process Internal dungeon pool
    dungeon_pools: Dict[str: EntranceShufflingData] = {}

    if 0 < options.shuffle_entrances < 3:
        dungeon_pools: Dict[str: EntranceShufflingData] = {"Sunken Shrine": ow_pools["Sunken Shrine"]}
        #ow_pools["Sunken Shrine"].allow_fill = False

        for group in dungeon_entrances:
            if group not in dungeon_pools.keys():
                if options.shuffle_overworld:
                    select_pool = world.random.choice(
                        [p for p in ow_pools.values() if p.early_candidate() and p not in dungeon_pools.values()])
                else:
                    select_pool = ow_pools[group]
                dungeon_pools[group] = select_pool

    # Place Progression entrances
    while len(prog_mixed_entrances) > 0:
        select_entrance = random_pop(world, prog_mixed_entrances)

        #print("Progress: Placing entrance " + select_entrance.name + " in group " + select_entrance_group)
        if options.shuffle_overworld and options.shuffle_entrances == 0:
            place_entrance_rng([p for p in ow_pools.values() if p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 1:
            if select_entrance.group in dungeon_pools.keys():
                place_entrance(dungeon_pools[select_entrance.group], select_entrance)
            else:
                place_entrance_rng([p for p in ow_pools.values() if p not in dungeon_pools.values() and p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 2:
            if select_entrance.group in dungeon_pools.keys():
                place_entrance_rng([p for p in dungeon_pools.values()], select_entrance)
            else:
                place_entrance_rng([p for p in ow_pools.values() if p not in dungeon_pools.values() and p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 3:
            place_entrance_rng([p for p in ow_pools.values() if p.allow_fill], select_entrance)
        else:
            print("Option error, what are we doing here???")
            place_entrance_rng([p for p in ow_pools.values() if p.allow_fill], select_entrance)

    # Place Deadend entrances
    while len(deadend_mixed_entrances) > 0:
        select_entrance = random_pop(world, deadend_mixed_entrances)

        #print("Deadends: Placing entrance " + select_entrance.name + " in group " + select_entrance_group)
        if options.shuffle_overworld and options.shuffle_entrances == 0:
            place_entrance_rng([p for p in ow_pools.values() if p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 1:
            if select_entrance.group in dungeon_pools.keys():
                place_entrance(dungeon_pools[select_entrance.group], select_entrance)
            else:
                place_entrance_rng([p for p in ow_pools.values() if p not in dungeon_pools.values() and p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 2:
            if select_entrance.group in dungeon_pools.keys():
                place_entrance_rng([p for p in dungeon_pools.values() if p.deadend_candidate()], select_entrance)
                #for d in dungeon_pools.values():
                #    print("> " + d.name + "; dead: " + str(len(d.initial_entrances)))
            else:
                place_entrance_rng([p for p in ow_pools.values() if p not in dungeon_pools.values() and p.early_candidate()], select_entrance)
        elif options.shuffle_entrances == 3:
            place_entrance_rng([p for p in ow_pools.values() if p.deadend_candidate()], select_entrance)
        else:
            print("Option error, what are we doing here???")
            place_entrance_rng([p for p in ow_pools.values() if p.deadend_candidate()], select_entrance)

    # 8. Build filled locations and connect entrances
    #new_entrances: List[EntranceData] = []
    for p in ow_pools.values():
        for deadend in p.stored_deadends:
            place_entrance(p, deadend)

    print("Add Entrances to regions dictionary")
    new_entrances_names = [n.name for n in new_entrances]
    fixed_entrances = [e for e in global_entrances if e.name not in new_entrances_names]

    for data in new_entrances:
        world.region_dict[data.region][data.target_region] = data.name
    for data in fixed_entrances:
        world.region_dict[data.region][data.target_region] = data.name

    for key, final_entrances in world.region_dict.items():
        region = world.get_region(key)
        region.add_exits(final_entrances)