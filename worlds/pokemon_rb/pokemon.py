from copy import deepcopy
import typing

from worlds.Files import APTokenTypes

from . import poke_data, logic
from .rom_addresses import rom_addresses

if typing.TYPE_CHECKING:
    from . import PokemonRedBlueWorld
    from .rom import PokemonRedProcedurePatch, PokemonBlueProcedurePatch


def set_mon_palettes(world: "PokemonRedBlueWorld", patch: "PokemonRedProcedurePatch | PokemonBlueProcedurePatch"):
    if world.options.randomize_pokemon_palettes == "vanilla":
        return
    pallet_map = {
        "Poison": 0x0F,
        "Normal": 0x10,
        "Ice": 0x11,
        "Fire": 0x12,
        "Water": 0x13,
        "Ghost": 0x14,
        "Ground": 0x15,
        "Grass": 0x16,
        "Psychic": 0x17,
        "Electric": 0x18,
        "Rock": 0x19,
        "Dragon": 0x1F,
        "Flying": 0x20,
        "Fighting": 0x21,
        "Bug": 0x22
    }
    palettes = []
    for mon in poke_data.pokemon_data:
        if world.options.randomize_pokemon_palettes == "primary_type":
            pallet = pallet_map[world.local_poke_data[mon]["type1"]]
        elif (world.options.randomize_pokemon_palettes == "follow_evolutions" and mon in
              poke_data.evolves_from and poke_data.evolves_from[mon] != "Eevee"):
            pallet = palettes[-1]
        else:  # completely_random or follow_evolutions and it is not an evolved form (except eeveelutions)
            pallet = world.random.choice(list(pallet_map.values()))
        palettes.append(pallet)
    patch.write_token(APTokenTypes.WRITE, rom_addresses["Mon_Palettes"], bytes(palettes))


def choose_forced_type(chances, random):
    n = random.randint(1, 100)
    for chance in chances:
        if chance[0] >= n:
            return chance[1]
    return None


def filter_moves(local_move_data, moves, type, random):
    ret = []
    for move in moves:
        if local_move_data[move]["type"] == type or type is None:
            ret.append(move)
    random.shuffle(ret)
    return ret


def get_move(local_move_data, moves, chances, random, starting_move=False):
    type = choose_forced_type(chances, random)
    filtered_moves = filter_moves(local_move_data, moves, type, random)
    for move in filtered_moves:
        if (not starting_move) or (local_move_data[move]["accuracy"] > 80 and local_move_data[move]["power"] > 0):
            moves.remove(move)
            return move
    else:
        return get_move(local_move_data, moves, [], random, starting_move)


def move_power(move_data):
    power = move_data["power"]
    if move_data["effect"] in (29, 42):
        # 29: two-to-five attacks. 42: trapping effect, two-to-five turns.
        power *= 3
    elif move_data["effect"] in (77, 44):
        # 77: Twineedle. Two attacks and poison chance. 44: Just two attacks
        power *= 2
    elif move_data["effect"] == 48:
        # 25% recoil damage taken. Reduce power considered by that amount
        power *= 0.75
    elif move_data["effect"] == 3:
        # 50% absorb. Increase power considered by that amount
        power *= 1.5
    elif move_data["effect"] == 39 and move_data["id"] != 91:
        # Takes two turns while vulnerable. Dig uses this effect ID but is semi-invulnerable
        power *= 0.66
    elif move_data["effect"] == 7:
        # Faint user
        power *= 0.5
    elif move_data["id"] in (2, 75, 152, 163,):
        # High critical strike moves: Karate Chop, Razor Leaf, Crabhammer, Slash
        power *= 2
    return power


def process_move_data(world):
    world.local_move_data = deepcopy(poke_data.moves)

    if world.options.randomize_move_types:
        for move, data in world.local_move_data.items():
            if move == "No Move":
                continue
            # The chance of randomized moves choosing a normal type move is high, so we want to retain having a higher
            # rate of normal type moves
            data["type"] = world.random.choice(list(poke_data.type_ids) + (["Normal"] * 4))

    if world.options.move_balancing:
        world.local_move_data["Sing"]["accuracy"] = 30
        world.local_move_data["Sleep Powder"]["accuracy"] = 40
        world.local_move_data["Spore"]["accuracy"] = 50
        world.local_move_data["Sonicboom"]["effect"] = 0
        world.local_move_data["Sonicboom"]["power"] = 50
        world.local_move_data["Dragon Rage"]["effect"] = 0
        world.local_move_data["Dragon Rage"]["power"] = 80
        world.local_move_data["Horn Drill"]["effect"] = 0
        world.local_move_data["Horn Drill"]["power"] = 70
        world.local_move_data["Horn Drill"]["accuracy"] = 95
        world.local_move_data["Horn Drill"]["pp"] = 15
        world.local_move_data["Guillotine"]["effect"] = 0
        world.local_move_data["Guillotine"]["power"] = 70
        world.local_move_data["Guillotine"]["accuracy"] = 95
        world.local_move_data["Guillotine"]["pp"] = 15
        world.local_move_data["Fissure"]["effect"] = 0
        world.local_move_data["Fissure"]["power"] = 70
        world.local_move_data["Fissure"]["accuracy"] = 95
        world.local_move_data["Fissure"]["pp"] = 15
        world.local_move_data["Blizzard"]["accuracy"] = 70

    if world.options.no_trapping_moves:
        for move in world.local_move_data.values():
            if move["effect"] == 42:
                move["effect"] = 29

    if world.options.randomize_tm_moves:
        world.local_tms = world.random.sample([move for move in poke_data.moves.keys() if move not in
                                               ["No Move"] + poke_data.hm_moves], 50)
    else:
        world.local_tms = poke_data.tm_moves.copy()


def process_pokemon_data(self):

    local_poke_data = deepcopy(poke_data.pokemon_data)
    learnsets = deepcopy(poke_data.learnsets)
    tms_hms = self.local_tms + poke_data.hm_moves

    compat_hms = set()

    for mon, mon_data in local_poke_data.items():
        if self.options.randomize_pokemon_stats == "shuffle":
            stats = [mon_data["hp"], mon_data["atk"], mon_data["def"], mon_data["spd"], mon_data["spc"]]
            if mon in poke_data.evolves_from:
                stat_shuffle_map = local_poke_data[poke_data.evolves_from[mon]]["stat_shuffle_map"]
            else:
                stat_shuffle_map = self.random.sample(range(0, 5), 5)

            mon_data["stat_shuffle_map"] = stat_shuffle_map
            mon_data["hp"] = stats[stat_shuffle_map[0]]
            mon_data["atk"] = stats[stat_shuffle_map[1]]
            mon_data["def"] = stats[stat_shuffle_map[2]]
            mon_data["spd"] = stats[stat_shuffle_map[3]]
            mon_data["spc"] = stats[stat_shuffle_map[4]]
        elif self.options.randomize_pokemon_stats == "randomize":
            first_run = True
            while (mon_data["hp"] > 255 or mon_data["atk"] > 255 or mon_data["def"] > 255 or mon_data["spd"] > 255
                   or mon_data["spc"] > 255 or first_run):
                first_run = False
                total_stats = mon_data["hp"] + mon_data["atk"] + mon_data["def"] + mon_data["spd"] + mon_data["spc"]
                for stat in ("hp", "atk", "def", "spd", "spc"):
                    if mon in poke_data.evolves_from:
                        mon_data[stat] = local_poke_data[poke_data.evolves_from[mon]][stat]
                        total_stats -= mon_data[stat]
                    elif stat == "hp":
                        mon_data[stat] = 20
                        total_stats -= 20
                    else:
                        mon_data[stat] = 10
                        total_stats -= 10
                assert total_stats >= 0, f"Error distributing stats for {mon} for player {self.player}"
                dist = [self.random.randint(1, 101) / 100, self.random.randint(1, 101) / 100,
                        self.random.randint(1, 101) / 100, self.random.randint(1, 101) / 100,
                        self.random.randint(1, 101) / 100]
                total_dist = sum(dist)

                mon_data["hp"] += int(round(dist[0] / total_dist * total_stats))
                mon_data["atk"] += int(round(dist[1] / total_dist * total_stats))
                mon_data["def"] += int(round(dist[2] / total_dist * total_stats))
                mon_data["spd"] += int(round(dist[3] / total_dist * total_stats))
                mon_data["spc"] += int(round(dist[4] / total_dist * total_stats))
        if self.options.randomize_pokemon_types:
            if self.options.randomize_pokemon_types.value == 1 and mon in poke_data.evolves_from:
                type1 = local_poke_data[poke_data.evolves_from[mon]]["type1"]
                type2 = local_poke_data[poke_data.evolves_from[mon]]["type2"]
                if type1 == type2:
                    if self.options.secondary_type_chance.value == -1:
                        if mon_data["type1"] != mon_data["type2"]:
                            while type2 == type1:
                                type2 = self.random.choice(list(poke_data.type_names.values()))
                    elif self.random.randint(1, 100) <= self.options.secondary_type_chance.value:
                        type2 = self.random.choice(list(poke_data.type_names.values()))
            else:
                type1 = self.random.choice(list(poke_data.type_names.values()))
                type2 = type1
                if ((self.options.secondary_type_chance.value == -1 and mon_data["type1"]
                     != mon_data["type2"]) or self.random.randint(1, 100)
                        <= self.options.secondary_type_chance.value):
                    while type2 == type1:
                        type2 = self.random.choice(list(poke_data.type_names.values()))

            mon_data["type1"] = type1
            mon_data["type2"] = type2
        if self.options.randomize_pokemon_movesets:
            if self.options.randomize_pokemon_movesets == "prefer_types":
                if mon_data["type1"] == "Normal" and mon_data["type2"] == "Normal":
                    chances = [[75, "Normal"]]
                elif mon_data["type1"] == "Normal" or mon_data["type2"] == "Normal":
                    if mon_data["type1"] == "Normal":
                        second_type = mon_data["type2"]
                    else:
                        second_type = mon_data["type1"]
                    chances = [[30, "Normal"], [85, second_type]]
                elif mon_data["type1"] == mon_data["type2"]:
                    chances = [[60, mon_data["type1"]], [80, "Normal"]]
                else:
                    chances = [[50, mon_data["type1"]], [80, mon_data["type2"]], [85, "Normal"]]
            else:
                chances = []
            moves = list(poke_data.moves.keys())
            for move in ["No Move"] + poke_data.hm_moves:
                moves.remove(move)
            if self.options.confine_transform_to_ditto:
                moves.remove("Transform")
            if self.options.start_with_four_moves:
                num_moves = 4
            else:
                num_moves = len([i for i in [mon_data["start move 1"], mon_data["start move 2"],
                                             mon_data["start move 3"], mon_data["start move 4"]] if i != "No Move"])
            if mon in learnsets:
                num_moves += len(learnsets[mon])
            non_power_moves = []
            learnsets[mon] = []
            for i in range(num_moves):
                if i == 0 and mon == "Ditto" and self.options.confine_transform_to_ditto:
                    move = "Transform"
                else:
                    move = get_move(self.local_move_data, moves, chances, self.random)
                    while move == "Transform" and self.options.confine_transform_to_ditto:
                        move = get_move(self.local_move_data, moves, chances, self.random)
                if self.local_move_data[move]["power"] < 5:
                    non_power_moves.append(move)
                else:
                    learnsets[mon].append(move)
            learnsets[mon].sort(key=lambda move: move_power(self.local_move_data[move]))
            if learnsets[mon]:
                for move in non_power_moves:
                    learnsets[mon].insert(self.random.randint(1, len(learnsets[mon])), move)
            else:
                learnsets[mon] = non_power_moves
            for i in range(1, 5):
                if mon_data[f"start move {i}"] != "No Move" or self.options.start_with_four_moves:
                    mon_data[f"start move {i}"] = learnsets[mon].pop(0)

        if self.options.randomize_pokemon_catch_rates:
            mon_data["catch rate"] = self.random.randint(self.options.minimum_catch_rate.value, 255)
        else:
            mon_data["catch rate"] = max(self.options.minimum_catch_rate.value, mon_data["catch rate"])

        def roll_tm_compat(roll_move):
            if self.local_move_data[roll_move]["type"] in [mon_data["type1"], mon_data["type2"]]:
                if roll_move in poke_data.hm_moves:
                    if self.options.hm_same_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.random.randint(1, 100) <= self.options.hm_same_type_compatibility.value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.options.tm_same_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.random.randint(1, 100) <= self.options.tm_same_type_compatibility.value
            elif self.local_move_data[roll_move]["type"] == "Normal" and "Normal" not in [mon_data["type1"], mon_data["type2"]]:
                if roll_move in poke_data.hm_moves:
                    if self.options.hm_normal_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.random.randint(1, 100) <= self.options.hm_normal_type_compatibility.value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.options.tm_normal_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.random.randint(1, 100) <= self.options.tm_normal_type_compatibility.value
            else:
                if roll_move in poke_data.hm_moves:
                    if self.options.hm_other_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.random.randint(1, 100) <= self.options.hm_other_type_compatibility.value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.options.tm_other_type_compatibility.value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.random.randint(1, 100) <= self.options.tm_other_type_compatibility.value

        for flag, tm_move in enumerate(tms_hms):
            if mon in poke_data.evolves_from and self.options.inherit_tm_hm_compatibility:

                if local_poke_data[poke_data.evolves_from[mon]]["tms"][int(flag / 8)] & 1 << (flag % 8):
                    # always inherit learnable tms/hms
                    bit = 1
                else:
                    if self.local_move_data[tm_move]["type"] in [mon_data["type1"], mon_data["type2"]] and \
                            self.local_move_data[tm_move]["type"] not in [
                            local_poke_data[poke_data.evolves_from[mon]]["type1"],
                            local_poke_data[poke_data.evolves_from[mon]]["type2"]]:
                        # the tm/hm is for a move whose type matches current mon, but not pre-evolved form
                        # so this gets full chance roll
                        bit = roll_tm_compat(tm_move)
                    # otherwise 50% reduced chance to add compatibility over pre-evolved form
                    elif self.random.randint(1, 100) > 50 and roll_tm_compat(tm_move):
                        bit = 1
                    else:
                        bit = 0
            else:
                bit = roll_tm_compat(tm_move)
            if bit:
                mon_data["tms"][int(flag / 8)] |= 1 << (flag % 8)
            else:
                mon_data["tms"][int(flag / 8)] &= ~(1 << (flag % 8))

    hm_verify = ["Surf", "Strength"]
    if self.options.accessibility != "minimal" or ((not
            self.options.badgesanity) and max(self.options.elite_four_badges_condition,
            self.options.route_22_gate_condition, self.options.victory_road_condition)
            > 7) or (self.options.door_shuffle not in ("off", "simple")):
        hm_verify += ["Cut"]
    if (self.options.accessibility != "minimal" or (not self.options.dark_rock_tunnel_logic) and
            ((self.options.trainersanity or self.options.extra_key_items) or self.options.door_shuffle)):
        hm_verify += ["Flash"]
    # Fly does not need to be verified. Full/Insanity/Decoupled door shuffle connects reachable regions to unreachable
    # regions, so if Fly is available and can be learned, the towns you can fly to would be considered reachable for
    # door shuffle purposes, but if no Pokémon can learn it, that connection would just be out of logic and it would
    # ensure connections to those towns.

    for hm_move in hm_verify:
        if hm_move not in compat_hms:
            mon = self.random.choice([mon for mon in poke_data.pokemon_data if mon not in poke_data.legendary_pokemon])
            flag = tms_hms.index(hm_move)
            local_poke_data[mon]["tms"][int(flag / 8)] |= 1 << (flag % 8)

    self.local_poke_data = local_poke_data
    self.learnsets = learnsets


def verify_hm_moves(multiworld, world, player):
    def intervene(move, test_state):
        move_bit = pow(2, poke_data.hm_moves.index(move) + 2)
        viable_mons = [mon for mon in world.local_poke_data if world.local_poke_data[mon]["tms"][6] & move_bit]
        if world.options.randomize_pokemon_locations and viable_mons:
            accessible_slots = [loc for loc in multiworld.get_reachable_locations(test_state, player) if
                                loc.type == "Wild Encounter"]

            def number_of_zones(mon):
                zones = set()
                for loc in [slot for slot in accessible_slots if slot.item.name == mon]:
                    zones.add(loc.name.split(" - ")[0])
                return len(zones)

            placed_mons = [slot.item.name for slot in accessible_slots]

            if world.options.area_1_to_1_mapping:
                placed_mons.sort(key=lambda i: number_of_zones(i))
            else:
                # this sort method doesn't work if you reference the same list being sorted in the lambda
                placed_mons_copy = placed_mons.copy()
                placed_mons.sort(key=lambda i: placed_mons_copy.count(i))

            placed_mon = placed_mons.pop()
            replace_mon = world.random.choice(viable_mons)
            replace_slot = world.random.choice([slot for slot in accessible_slots if slot.item.name
                                                          == placed_mon])
            if world.options.area_1_to_1_mapping:
                zone = " - ".join(replace_slot.name.split(" - ")[:-1])
                replace_slots = [slot for slot in accessible_slots if slot.name.startswith(zone) and slot.item.name
                                 == placed_mon]
                for replace_slot in replace_slots:
                    replace_slot.item = world.create_item(replace_mon)
            else:
                replace_slot.item = world.create_item(replace_mon)
        else:
            tms_hms = world.local_tms + poke_data.hm_moves
            flag = tms_hms.index(move)
            mon_list = [mon for mon in poke_data.pokemon_data.keys() if test_state.has(mon, player)]
            world.random.shuffle(mon_list)
            mon_list.sort(key=lambda mon: world.local_move_data[move]["type"] not in
                          [world.local_poke_data[mon]["type1"], world.local_poke_data[mon]["type2"]])
            for mon in mon_list:
                if test_state.has(mon, player):
                    world.local_poke_data[mon]["tms"][int(flag / 8)] |= 1 << (flag % 8)
                    break

    last_intervene = None
    while True:
        intervene_move = None
        test_state = multiworld.get_all_state(False, True, False)
        if not logic.can_learn_hm(test_state, world, "Surf", player):
            intervene_move = "Surf"
        elif not logic.can_learn_hm(test_state, world, "Strength", player):
            intervene_move = "Strength"
        # cut may not be needed if accessibility is minimal, unless you need all 8 badges and badgesanity is off,
        # as you will require cut to access celadon gyn
        elif ((not logic.can_learn_hm(test_state, world, "Cut", player)) and
                (world.options.accessibility != "minimal" or ((not
                world.options.badgesanity) and max(
                world.options.elite_four_badges_condition,
                world.options.route_22_gate_condition,
                world.options.victory_road_condition)
                > 7) or (world.options.door_shuffle not in ("off", "simple")))):
            intervene_move = "Cut"
        elif ((not logic.can_learn_hm(test_state, world, "Flash", player))
               and world.options.dark_rock_tunnel_logic
               and (world.options.accessibility != "minimal"
                    or world.options.door_shuffle)):
            intervene_move = "Flash"
        # If no Pokémon can learn Fly, then during door shuffle it would simply not treat the free fly maps
        # as reachable, and if on no door shuffle or simple, fly is simply never necessary.
        # We only intervene if a Pokémon is able to learn fly but none are reachable, as that would have been
        # considered in door shuffle.
        elif ((not logic.can_learn_hm(test_state, world, "Fly", player))
                and world.options.door_shuffle not in
                ("off", "simple") and [world.fly_map, world.town_map_fly_map] != ["Pallet Town", "Pallet Town"]):
            intervene_move = "Fly"
        if intervene_move:
            if intervene_move == last_intervene:
                raise Exception(f"Caught in infinite loop attempting to ensure {intervene_move} is available to player {player}")
            intervene(intervene_move, test_state)
            last_intervene = intervene_move
        else:
            break
