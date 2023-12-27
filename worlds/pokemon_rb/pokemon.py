from copy import deepcopy
from . import poke_data
from .rom_addresses import rom_addresses


def set_mon_palettes(self, random, data):
    if self.multiworld.randomize_pokemon_palettes[self.player] == "vanilla":
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
        if self.multiworld.randomize_pokemon_palettes[self.player] == "primary_type":
            pallet = pallet_map[self.local_poke_data[mon]["type1"]]
        elif (self.multiworld.randomize_pokemon_palettes[self.player] == "follow_evolutions" and mon in
              poke_data.evolves_from and poke_data.evolves_from[mon] != "Eevee"):
            pallet = palettes[-1]
        else:  # completely_random or follow_evolutions and it is not an evolved form (except eeveelutions)
            pallet = random.choice(list(pallet_map.values()))
        palettes.append(pallet)
    address = rom_addresses["Mon_Palettes"]
    for pallet in palettes:
        data[address] = pallet
        address += 1


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


def process_move_data(self):
    self.local_move_data = deepcopy(poke_data.moves)

    if self.multiworld.randomize_move_types[self.player]:
        for move, data in self.local_move_data.items():
            if move == "No Move":
                continue
            # The chance of randomized moves choosing a normal type move is high, so we want to retain having a higher
            # rate of normal type moves
            data["type"] = self.multiworld.random.choice(list(poke_data.type_ids) + (["Normal"] * 4))

    if self.multiworld.move_balancing[self.player]:
        self.local_move_data["Sing"]["accuracy"] = 30
        self.local_move_data["Sleep Powder"]["accuracy"] = 40
        self.local_move_data["Spore"]["accuracy"] = 50
        self.local_move_data["Sonicboom"]["effect"] = 0
        self.local_move_data["Sonicboom"]["power"] = 50
        self.local_move_data["Dragon Rage"]["effect"] = 0
        self.local_move_data["Dragon Rage"]["power"] = 80
        self.local_move_data["Horn Drill"]["effect"] = 0
        self.local_move_data["Horn Drill"]["power"] = 70
        self.local_move_data["Horn Drill"]["accuracy"] = 90
        self.local_move_data["Guillotine"]["effect"] = 0
        self.local_move_data["Guillotine"]["power"] = 70
        self.local_move_data["Guillotine"]["accuracy"] = 90
        self.local_move_data["Fissure"]["effect"] = 0
        self.local_move_data["Fissure"]["power"] = 70
        self.local_move_data["Fissure"]["accuracy"] = 90
        self.local_move_data["Blizzard"]["accuracy"] = 70
    if self.multiworld.randomize_tm_moves[self.player]:
        self.local_tms = self.multiworld.random.sample([move for move in poke_data.moves.keys() if move not in
                                                        ["No Move"] + poke_data.hm_moves], 50)
    else:
        self.local_tms = poke_data.tm_moves.copy()


def process_pokemon_data(self):

    local_poke_data = deepcopy(poke_data.pokemon_data)
    learnsets = deepcopy(poke_data.learnsets)
    tms_hms = self.local_tms + poke_data.hm_moves


    compat_hms = set()

    for mon, mon_data in local_poke_data.items():
        if self.multiworld.randomize_pokemon_stats[self.player] == "shuffle":
            stats = [mon_data["hp"], mon_data["atk"], mon_data["def"], mon_data["spd"], mon_data["spc"]]
            if mon in poke_data.evolves_from:
                stat_shuffle_map = local_poke_data[poke_data.evolves_from[mon]]["stat_shuffle_map"]
            else:
                stat_shuffle_map = self.multiworld.random.sample(range(0, 5), 5)

            mon_data["stat_shuffle_map"] = stat_shuffle_map
            mon_data["hp"] = stats[stat_shuffle_map[0]]
            mon_data["atk"] = stats[stat_shuffle_map[1]]
            mon_data["def"] = stats[stat_shuffle_map[2]]
            mon_data["spd"] = stats[stat_shuffle_map[3]]
            mon_data["spc"] = stats[stat_shuffle_map[4]]
        elif self.multiworld.randomize_pokemon_stats[self.player] == "randomize":
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
                dist = [self.multiworld.random.randint(1, 101) / 100, self.multiworld.random.randint(1, 101) / 100,
                        self.multiworld.random.randint(1, 101) / 100, self.multiworld.random.randint(1, 101) / 100,
                        self.multiworld.random.randint(1, 101) / 100]
                total_dist = sum(dist)

                mon_data["hp"] += int(round(dist[0] / total_dist * total_stats))
                mon_data["atk"] += int(round(dist[1] / total_dist * total_stats))
                mon_data["def"] += int(round(dist[2] / total_dist * total_stats))
                mon_data["spd"] += int(round(dist[3] / total_dist * total_stats))
                mon_data["spc"] += int(round(dist[4] / total_dist * total_stats))
        if self.multiworld.randomize_pokemon_types[self.player]:
            if self.multiworld.randomize_pokemon_types[self.player].value == 1 and mon in poke_data.evolves_from:
                type1 = local_poke_data[poke_data.evolves_from[mon]]["type1"]
                type2 = local_poke_data[poke_data.evolves_from[mon]]["type2"]
                if type1 == type2:
                    if self.multiworld.secondary_type_chance[self.player].value == -1:
                        if mon_data["type1"] != mon_data["type2"]:
                            while type2 == type1:
                                type2 = self.multiworld.random.choice(list(poke_data.type_names.values()))
                    elif self.multiworld.random.randint(1, 100) <= self.multiworld.secondary_type_chance[self.player].value:
                        type2 = self.multiworld.random.choice(list(poke_data.type_names.values()))
            else:
                type1 = self.multiworld.random.choice(list(poke_data.type_names.values()))
                type2 = type1
                if ((self.multiworld.secondary_type_chance[self.player].value == -1 and mon_data["type1"]
                     != mon_data["type2"]) or self.multiworld.random.randint(1, 100)
                        <= self.multiworld.secondary_type_chance[self.player].value):
                    while type2 == type1:
                        type2 = self.multiworld.random.choice(list(poke_data.type_names.values()))

            mon_data["type1"] = type1
            mon_data["type2"] = type2
        if self.multiworld.randomize_pokemon_movesets[self.player]:
            if self.multiworld.randomize_pokemon_movesets[self.player] == "prefer_types":
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
            if self.multiworld.confine_transform_to_ditto[self.player]:
                moves.remove("Transform")
            if self.multiworld.start_with_four_moves[self.player]:
                num_moves = 4
            else:
                num_moves = len([i for i in [mon_data["start move 1"], mon_data["start move 2"],
                                             mon_data["start move 3"], mon_data["start move 4"]] if i != "No Move"])
            if mon in learnsets:
                num_moves += len(learnsets[mon])
            non_power_moves = []
            learnsets[mon] = []
            for i in range(num_moves):
                if i == 0 and mon == "Ditto" and self.multiworld.confine_transform_to_ditto[self.player]:
                    move = "Transform"
                else:
                    move = get_move(self.local_move_data, moves, chances, self.multiworld.random)
                    while move == "Transform" and self.multiworld.confine_transform_to_ditto[self.player]:
                        move = get_move(self.local_move_data, moves, chances, self.multiworld.random)
                if self.local_move_data[move]["power"] < 5:
                    non_power_moves.append(move)
                else:
                    learnsets[mon].append(move)
            learnsets[mon].sort(key=lambda move: move_power(self.local_move_data[move]))
            if learnsets[mon]:
                for move in non_power_moves:
                    learnsets[mon].insert(self.multiworld.random.randint(1, len(learnsets[mon])), move)
            else:
                learnsets[mon] = non_power_moves
            for i in range(1, 5):
                if mon_data[f"start move {i}"] != "No Move" or self.multiworld.start_with_four_moves[self.player]:
                    mon_data[f"start move {i}"] = learnsets[mon].pop(0)

        if self.multiworld.randomize_pokemon_catch_rates[self.player]:
            mon_data["catch rate"] = self.multiworld.random.randint(self.multiworld.minimum_catch_rate[self.player],
                                                                    255)
        else:
            mon_data["catch rate"] = max(self.multiworld.minimum_catch_rate[self.player], mon_data["catch rate"])

        def roll_tm_compat(roll_move):
            if self.local_move_data[roll_move]["type"] in [mon_data["type1"], mon_data["type2"]]:
                if roll_move in poke_data.hm_moves:
                    if self.multiworld.hm_same_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.multiworld.random.randint(1, 100) <= self.multiworld.hm_same_type_compatibility[self.player].value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.multiworld.tm_same_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.multiworld.random.randint(1, 100) <= self.multiworld.tm_same_type_compatibility[self.player].value
            elif self.local_move_data[roll_move]["type"] == "Normal" and "Normal" not in [mon_data["type1"], mon_data["type2"]]:
                if roll_move in poke_data.hm_moves:
                    if self.multiworld.hm_normal_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.multiworld.random.randint(1, 100) <= self.multiworld.hm_normal_type_compatibility[self.player].value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.multiworld.tm_normal_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.multiworld.random.randint(1, 100) <= self.multiworld.tm_normal_type_compatibility[self.player].value
            else:
                if roll_move in poke_data.hm_moves:
                    if self.multiworld.hm_other_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    r = self.multiworld.random.randint(1, 100) <= self.multiworld.hm_other_type_compatibility[self.player].value
                    if r and mon not in poke_data.legendary_pokemon:
                        compat_hms.add(roll_move)
                    return r
                else:
                    if self.multiworld.tm_other_type_compatibility[self.player].value == -1:
                        return mon_data["tms"][int(flag / 8)] & 1 << (flag % 8)
                    return self.multiworld.random.randint(1, 100) <= self.multiworld.tm_other_type_compatibility[self.player].value

        for flag, tm_move in enumerate(tms_hms):
            if mon in poke_data.evolves_from and self.multiworld.inherit_tm_hm_compatibility[self.player]:

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
                    elif self.multiworld.random.randint(1, 100) > 50 and roll_tm_compat(tm_move):
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
    if self.multiworld.accessibility[self.player] == "locations" or ((not
            self.multiworld.badgesanity[self.player]) and max(self.multiworld.elite_four_badges_condition[self.player],
            self.multiworld.route_22_gate_condition[self.player], self.multiworld.victory_road_condition[self.player])
            > 7) or (self.multiworld.door_shuffle[self.player] not in ("off", "simple")):
        hm_verify += ["Cut"]
    if self.multiworld.accessibility[self.player] == "locations" or (not
            self.multiworld.dark_rock_tunnel_logic[self.player]) and ((self.multiworld.trainersanity[self.player] or
                                                                       self.multiworld.extra_key_items[self.player])
                                                                      or self.multiworld.door_shuffle[self.player]):
        hm_verify += ["Flash"]
    # Fly does not need to be verified. Full/Insanity door shuffle connects reachable regions to unreachable regions,
    # so if Fly is available and can be learned, the towns you can fly to would be reachable, but if no Pokémon can
    # learn it this simply would not occur

    for hm_move in hm_verify:
        if hm_move not in compat_hms:
            mon = self.multiworld.random.choice([mon for mon in poke_data.pokemon_data if mon not in
                                                 poke_data.legendary_pokemon])
            flag = tms_hms.index(hm_move)
            local_poke_data[mon]["tms"][int(flag / 8)] |= 1 << (flag % 8)

    self.local_poke_data = local_poke_data
    self.learnsets = learnsets
