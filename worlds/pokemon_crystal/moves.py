from collections.abc import Iterable
from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, LearnsetData, TMHMData, MoveCategory, TypeMatchup
from .options import RandomizeLearnsets, RandomizeMoveValues, PhysicalSpecialSplit, RandomizeTypeChart

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

MOVE_POWER_RATIO = {
    "BARRAGE": 3,
    "DOUBLESLAP": 3,
    "TRIPLE_KICK": 3,
    "BONEMERANG": 2,
    "COMET_PUNCH": 3,
    "DOUBLE_KICK": 2,
    "FURY_ATTACK": 3,
    "FURY_SWIPES": 3,
    "PIN_MISSILE": 3,
    "TWINEEDLE": 2,
    "SPIKE_CANNON": 3,
    "BONE_RUSH": 3,
    "ROLLOUT": 2
}

PHYSICAL_TYPES = {
    "NORMAL",
    "FIGHTING",
    "FLYING",
    "POISON",
    "GROUND",
    "ROCK",
    "BUG",
    "GHOST",
    "STEEL"
}

BAD_DAMAGING_MOVES = ["EXPLOSION", "SELFDESTRUCT", "STRUGGLE", "SNORE", "DREAM_EATER"]
DAMAGING_STATUS_MOVES = ["ZAP_CANNON", "DYNAMICPUNCH"]

HM_MOVES = ["CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL"]
HM_COMPAT_TMS = ["HEADBUTT", "ROCK_SMASH"]
LOGIC_MOVES = HM_MOVES + HM_COMPAT_TMS


def randomize_learnset(world: "PokemonCrystalWorld", pkmn_name: str, move_blocklist: Iterable[str]):
    pkmn_data = world.generated_pokemon[pkmn_name]
    learn_levels = []
    new_learnset = []
    for move in pkmn_data.learnset:
        if move.move != "NO_MOVE":
            learn_levels.append(move.level)
        elif world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            learn_levels.insert(0, 1)

    for level in learn_levels:
        if world.options.metronome_only:
            new_learnset.append(LearnsetData(level, "METRONOME"))
        else:
            move_type = None

            if world.options.learnset_type_bias > -1:  # checks if user put an option for Move Type bias (default is -1)
                pkmn_types = pkmn_data.types
                if world.random.randint(1, 100) <= world.options.learnset_type_bias:  # rolls for the chance
                    # chooses one of the pokemons types to give to move generation function
                    move_type = world.random.choice(pkmn_types)
                else:  # chooses one of the types other than the pokemons to give to move generation function
                    rem_types = [type for type in crystal_data.types if type not in pkmn_types]
                    move_type = world.random.choice(rem_types)
            new_learnset.append(
                LearnsetData(level,
                             get_random_move(world, move_blocklist, move_type=move_type, cur_learnset=new_learnset)))

    if not world.options.metronome_only:
        # All moves available at Lv.1 that do damage (and don't faint the user)
        start_attacking = [learnset for learnset in new_learnset if
                           world.generated_moves[learnset.move].power > 0
                           and learnset.move not in BAD_DAMAGING_MOVES
                           and learnset.level == 1]

        if not start_attacking:  # if there are no attacking moves at Lv.1, add one
            new_learnset[0] = LearnsetData(1, get_random_move(world,
                                                              move_blocklist,
                                                              attacking=True))  # overwrites whatever the 1st move is

    return new_learnset


def get_random_move(world: "PokemonCrystalWorld", blocklist: Iterable[str], move_type=None, attacking=None,
                    cur_learnset=None):
    if not cur_learnset:
        cur_learnset = []

    existing_moves = [entry.move for entry in cur_learnset]  # pulls the names of all the moves in current learnset

    move_pool = [move_name for move_name, move_data in world.generated_moves.items() if
                 not move_data.is_hm
                 # exclude beat up as it can softlock the game if an enemy trainer uses it
                 and move_name not in ("STRUGGLE", "BEAT_UP", "NO_MOVE")
                 and move_name not in existing_moves
                 and (not move_type or move_data.type == move_type)]

    if attacking is not None:
        move_pool = [move_name for move_name in move_pool if world.generated_moves[move_name].power > 0
                     and move_name not in BAD_DAMAGING_MOVES
                     and move_name not in existing_moves]

    # remove every move from move_pool that is in the blocklist
    if blocklist:
        move_pool = [move_name for move_name in move_pool if
                     move_name not in blocklist]

    if move_pool:
        return world.random.choice(move_pool)
    elif move_type:
        return get_random_move(world, blocklist=blocklist)
    else:
        return get_random_move(world, blocklist=[])


def get_tmhm_compatibility(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    tm_value = world.options.tm_compatibility.value
    hm_value = world.options.hm_compatibility.value
    tmhms = []
    for tm_name, tm_data in sorted(world.generated_tms.items(), key=lambda x: x[0]):
        use_value = hm_value if tm_data.is_hm or tm_name in HM_COMPAT_TMS else tm_value
        # if the value is -1, use vanilla compatibility
        if use_value == -1:
            if tm_name in pkmn_data.tm_hm:
                tmhms.append(tm_name)
                continue
        # double chance if types match
        if tm_data.type in pkmn_data.types:
            use_value = use_value * 2
        if world.random.randint(0, 99) < use_value:
            tmhms.append(tm_name)
    return tmhms


def apply_tm_plando(world: "PokemonCrystalWorld") -> dict[int, str]:
    move_friendly_to_ids = {move_data.name.title(): move_id for move_id, move_data in world.generated_moves.items()}
    plando_data = {tm_num: move_friendly_to_ids[move] for tm_num, move in world.options.tm_plando.value.items()}
    for tm_name, tm_data in sorted(world.generated_tms.items(), key=lambda x: x[0]):
        if tm_data.is_hm or tm_data.tm_num not in plando_data:
            continue
        move = world.generated_moves[plando_data[tm_data.tm_num]]
        world.generated_tms[tm_name] = TMHMData(move.id, tm_data.tm_num, move.type, False, move.rom_id)
    return plando_data


def randomize_tms(world: "PokemonCrystalWorld"):
    plandoed_tms = dict()
    if world.options.tm_plando and not world.options.metronome_only:
        plandoed_tms = apply_tm_plando(world)
    if not world.options.randomize_tm_moves and not world.options.metronome_only: return

    plandoed_tms[2] = "HEADBUTT"
    plandoed_tms[8] = "ROCK_SMASH"
    if (world.options.dexsanity or world.options.dexcountsanity) and "SWEET_SCENT" not in plandoed_tms.values():
        plandoed_tms[12] = "SWEET_SCENT"
    ignored_moves = ["NO_MOVE", "STRUGGLE"] + list(plandoed_tms.values())
    global_move_pool = [move_data for move_name, move_data in world.generated_moves.items() if
                        not move_data.is_hm
                        and move_name not in ignored_moves]

    blocked_tm_moves = moves_convert_friendly_to_ids(world, world.options.tm_blocklist)
    filtered_move_pool = [move for move in global_move_pool if move.id not in blocked_tm_moves]

    world.random.shuffle(global_move_pool)
    world.random.shuffle(filtered_move_pool)

    for tm_name, tm_data in world.generated_tms.items():
        if tm_data.is_hm or tm_data.tm_num in plandoed_tms:
            continue
        if world.options.metronome_only:
            new_move = world.generated_moves["METRONOME"]
        elif not filtered_move_pool:
            new_move = global_move_pool.pop()
        else:
            new_move = filtered_move_pool.pop()
            global_move_pool.remove(new_move)
        world.generated_tms[tm_name] = TMHMData(new_move.id, tm_data.tm_num, new_move.type, False, new_move.rom_id)


def get_random_move_from_learnset(world: "PokemonCrystalWorld", pokemon: str, level: int):
    move_pool = [learn_move.move for learn_move in world.generated_pokemon[pokemon].learnset if
                 learn_move.level <= level and learn_move.move != "NO_MOVE"]
    # double learnset pool to dilute HMs slightly
    # exclude beat up as it can softlock the game if an enemy trainer uses it
    move_pool.extend(world.generated_tms[tm].id for tm in world.generated_pokemon[pokemon].tm_hm if
                     world.generated_tms[tm].id != "BEAT_UP")
    return world.random.choice(move_pool)


def randomize_move_values(world: "PokemonCrystalWorld"):
    if world.options.randomize_move_values:

        acc100 = 70  # Moves have a 70% chance to get 100% accuracy
        for move_name, move_data in world.generated_moves.items():
            if move_name in ("NO_MOVE", "CURSE", "DRAGON_RAGE", "SONICBOOM"):
                continue
            new_power = move_data.power
            new_acc = move_data.accuracy
            new_pp = move_data.pp
            if new_power > 1:
                if world.options.randomize_move_values == RandomizeMoveValues.option_restricted:
                    new_power = int(new_power * (world.random.random() + 0.5))
                    if new_power > 255: new_power = 255
                    new_pp = new_pp + world.random.choice((-10, -5, 0, 5, 10))
                    if new_pp < 5: new_pp = 5
                    if new_pp > 40: new_pp = 40
                else:
                    new_power = world.random.randint(20, 150)
                    new_power //= MOVE_POWER_RATIO.get(move_name, 1)
                    new_pp = world.random.randint(5, 40)

                if world.options.randomize_move_values == RandomizeMoveValues.option_full:
                    if world.random.randint(1, 100) <= acc100:
                        new_acc = 100
                    else:
                        # 30 is 76,5 so actual lowest accuracy is a bit lower than 30
                        new_acc = world.random.randint(30, 100)

                if move_name in DAMAGING_STATUS_MOVES and new_acc > 75:
                    new_acc = 75

            world.generated_moves[move_name] = replace(
                world.generated_moves[move_name],
                power=new_power,
                accuracy=new_acc,
                pp=new_pp
            )

    if world.options.physical_special_split == PhysicalSpecialSplit.option_vanilla:
        physical_types = PHYSICAL_TYPES
    elif world.options.physical_special_split == PhysicalSpecialSplit.option_random_by_type:
        physical_types = {type for type in crystal_data.types if world.random.randint(0, 1)}
    else:
        physical_types = set()

    if world.options.physical_special_split in (PhysicalSpecialSplit.option_vanilla,
                                                PhysicalSpecialSplit.option_random_by_type):
        for move_name, move_data in world.generated_moves.items():
            if move_data.category is MoveCategory.Status: continue

            if move_data.type in physical_types:
                new_category = MoveCategory.Physical
            else:
                new_category = MoveCategory.Special

            world.generated_moves[move_name] = replace(move_data, category=new_category)

    elif world.options.physical_special_split == PhysicalSpecialSplit.option_random_by_move:
        for move_name, move_data in world.generated_moves.items():
            if move_data.category is MoveCategory.Status: continue

            new_category = MoveCategory.Physical if world.random.randint(0, 1) else MoveCategory.Special

            world.generated_moves[move_name] = replace(move_data, category=new_category)


def cap_hm_move_power(world: "PokemonCrystalWorld"):
    if world.options.hm_power_cap.value == world.options.hm_power_cap.range_end: return

    cap = world.options.hm_power_cap.value
    for move_name in LOGIC_MOVES:
        if world.generated_moves.get(move_name).power > cap:
            world.generated_moves[move_name] = replace(
                world.generated_moves[move_name],
                power=cap
            )


def randomize_move_types(world: "PokemonCrystalWorld"):
    if not world.options.randomize_move_types: return

    all_types = list(crystal_data.types.keys())

    for move_name, move_data in world.generated_moves.items():
        if move_name in ("NO_MOVE", "CURSE"):
            continue
        new_type = world.random.choice(all_types)
        world.generated_moves[move_name] = replace(
            world.generated_moves[move_name],
            type=new_type
        )


def randomize_type_chart(world: "PokemonCrystalWorld"):
    if not world.options.randomize_type_chart: return

    if world.options.randomize_type_chart == RandomizeTypeChart.option_shuffle:
        matchup_pool = [
            matchup for _, type_data in world.generated_types.items() for _, matchup in type_data.matchups.items()
        ]
        world.random.shuffle(matchup_pool)
    else:
        all_matchups = list(TypeMatchup)
        matchup_pool = [world.random.choice(all_matchups) for _ in
                        range(len(crystal_data.types) * len(crystal_data.types))]

    for type_id, type_data in world.generated_types.items():
        world.generated_types[type_id] = replace(type_data,
                                                 matchups={matchup_type: matchup_pool.pop() for matchup_type in
                                                           type_data.matchups.keys()})


def moves_convert_friendly_to_ids(world: "PokemonCrystalWorld", moves: Iterable[str]) -> set[str]:
    return {move_id for move_id, move_data in world.generated_moves.items() if move_data.name.title() in moves}
