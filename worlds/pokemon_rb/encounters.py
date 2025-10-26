from copy import deepcopy
from . import poke_data
from .locations import location_data

non_randomized_catch_em_all_candidate_slots = [
    "Route 4 Pokemon Center - Pokemon For Sale",
    "Underground Path Route 5 - Spot Trade",
    "Route 11 Gate 2F - Terry Trade",
    "Cinnabar Lab Fossil Room - Sailor Trade",
    "Cinnabar Lab Trade Room - Crinkles Trade",
    "Cinnabar Lab Trade Room - Doris Trade",
    *[f"Celadon Prize Corner - Pokemon Prize - {i}" for i in range(1, 3)]
]


def get_encounter_slots(world, types):
    encounter_slots = deepcopy([location for location in location_data if location.type in types])

    i = [True, False][world.options.game_version.value]
    for location in encounter_slots:
        if isinstance(location.original_item, list):
            if world.options.catch_em_all and not world.options.randomize_pokemon_locations and location.name in (
                    "Celadon Prize Corner - Pokemon Prize - 4", "Celadon Prize Corner - Pokemon Prize - 5"):
                location.original_item = location.original_item[world.options.game_version.value]
            else:
                location.original_item = location.original_item[i]
                if world.options.catch_em_all and not world.options.randomize_pokemon_locations:
                    i = not i

    return encounter_slots


def get_base_stat_total(mon):
    return (poke_data.pokemon_data[mon]["atk"] + poke_data.pokemon_data[mon]["def"]
            + poke_data.pokemon_data[mon]["hp"] + poke_data.pokemon_data[mon]["spd"]
            + poke_data.pokemon_data[mon]["spc"])


def randomize_pokemon(self, mon, mons_list, randomize_type, random):
    if randomize_type in [1, 3]:
        type_mons = [pokemon for pokemon in mons_list if any([poke_data.pokemon_data[mon][
             "type1"] in [self.local_poke_data[pokemon]["type1"], self.local_poke_data[pokemon]["type2"]],
             poke_data.pokemon_data[mon]["type2"] in [self.local_poke_data[pokemon]["type1"],
                                                      self.local_poke_data[pokemon]["type2"]]])]
        if not type_mons:
            type_mons = mons_list.copy()
        if randomize_type == 3:
            stat_base = get_base_stat_total(mon)
            type_mons.sort(key=lambda mon: abs(get_base_stat_total(mon) - stat_base))
        mon = type_mons[round(random.triangular(0, len(type_mons) - 1, 0))]
    if randomize_type == 2:
        stat_base = get_base_stat_total(mon)
        mons_list.sort(key=lambda mon: abs(get_base_stat_total(mon) - stat_base))
        mon = mons_list[round(random.triangular(0, 50, 0))]
    elif randomize_type == 4:
        mon = random.choice(mons_list)
    return mon


def process_trainer_data(world):
    mons_list = [pokemon for pokemon in poke_data.pokemon_data.keys() if pokemon not in poke_data.legendary_pokemon
                 or world.options.trainer_legendaries.value]
    unevolved_mons = [pokemon for pokemon in poke_data.first_stage_pokemon if pokemon not in poke_data.legendary_pokemon
                      or world.options.randomize_legendary_pokemon.value == 3]
    evolved_mons = [mon for mon in mons_list if mon not in unevolved_mons]
    rival_map = {
        "Charmander": world.multiworld.get_location("Oak's Lab - Starter 1", world.player).item.name[9:],  # strip the
        "Squirtle": world.multiworld.get_location("Oak's Lab - Starter 2", world.player).item.name[9:],  # 'Missable'
        "Bulbasaur": world.multiworld.get_location("Oak's Lab - Starter 3", world.player).item.name[9:],  # from the name
    }

    def add_evolutions():
        for a, b in rival_map.copy().items():
            if a in poke_data.evolves_to and poke_data.evolves_to[a] not in rival_map:
                if b in poke_data.evolves_to:
                    rival_map[poke_data.evolves_to[a]] = poke_data.evolves_to[b]
                else:
                    rival_map[poke_data.evolves_to[a]] = b
    add_evolutions()
    add_evolutions()
    parties_objs = [location for location in world.multiworld.get_locations(world.player)
                    if location.type == "Trainer Parties"]
    # Process Rival parties in order                                     "Route 22 " is not a typo
    parties_objs.sort(key=lambda i: 0 if "Oak's Lab" in i.name else 1 if "Route 22 " in i.name else 2 if "Cerulean City"
                      in i.name else 3 if "Anne" in i.name else 4 if "Pokemon Tower" in i.name else 5 if "Silph" in
                      i.name else 6 if "Route 22-F" in i.name else 7 if "Champion" in i.name else 8)
    for parties in parties_objs:
        parties_data = parties.party_data
        for party in parties_data:
            if party["party"] and isinstance(party["party"][0], list):
                # only for Rival parties
                for rival_party in party["party"]:
                    for i, mon in enumerate(rival_party):
                        if mon in ("Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
                                   "Squirtle", "Wartortle", "Blastoise"):
                            if world.options.randomize_pokemon_locations:
                                rival_party[i] = rival_map[mon]
                        elif world.options.randomize_trainer_parties:
                            if mon in rival_map:
                                rival_party[i] = rival_map[mon]
                            else:
                                new_mon = randomize_pokemon(world, mon,
                                                            unevolved_mons if mon in unevolved_mons else evolved_mons,
                                                            world.options.randomize_trainer_parties.value,
                                                            world.random)
                                rival_map[mon] = new_mon
                                rival_party[i] = new_mon
                            add_evolutions()
            else:
                if world.options.randomize_trainer_parties:
                    for i, mon in enumerate(party["party"]):
                        party["party"][i] = randomize_pokemon(world, mon, mons_list,
                                                              world.options.randomize_trainer_parties.value,
                                                              world.random)


def process_pokemon_locations(self):
    starter_slots = get_encounter_slots(self, ["Starter Pokemon"])
    legendary_slots = get_encounter_slots(self, ["Legendary Pokemon"])
    static_slots = get_encounter_slots(self, ["Static Pokemon", "Static Repeatable Pokemon", "Missable Pokemon"])
    legendary_mons = deepcopy([slot.original_item for slot in legendary_slots])

    static_placed_mons = {pokemon: 0 for pokemon in poke_data.pokemon_data.keys()}
    placed_mons = {pokemon: 0 for pokemon in poke_data.pokemon_data.keys()}

    mons_list = [pokemon for pokemon in poke_data.first_stage_pokemon if pokemon not in poke_data.legendary_pokemon
                 or self.options.randomize_legendary_pokemon.value == 3]
    if self.options.randomize_legendary_pokemon == "vanilla":
        for slot in legendary_slots:
            location = self.multiworld.get_location(slot.name, self.player)
            location.place_locked_item(self.create_item("Static " + slot.original_item))
    elif self.options.randomize_legendary_pokemon == "shuffle":
        self.random.shuffle(legendary_mons)
        for slot in legendary_slots:
            location = self.multiworld.get_location(slot.name, self.player)
            mon = legendary_mons.pop()
            location.place_locked_item(self.create_item("Static " + mon))
            static_placed_mons[mon] += 1
    elif self.options.randomize_legendary_pokemon == "static":
        static_slots = static_slots + legendary_slots
        self.random.shuffle(static_slots)
        static_slots.sort(key=lambda s: s.name != "Pokemon Tower 6F - Restless Soul"
                          and "Fake Pokeball" not in s.name)
        while legendary_slots:
            swap_slot = legendary_slots.pop()
            slot = static_slots.pop()
            prepend = ""
            if slot.type in ("Legendary Pokemon", "Static Pokemon"):
                prepend = "Static "
                static_placed_mons[swap_slot.original_item] += 1
            else:
                placed_mons[swap_slot.original_item] += 1
            location = self.multiworld.get_location(slot.name, self.player)
            location.place_locked_item(self.create_item(prepend + swap_slot.original_item))
            swap_slot.original_item = slot.original_item
            
    elif self.options.randomize_legendary_pokemon == "any":
        static_slots = static_slots + legendary_slots

    non_randomized_catch_em_all_mons = ["Bulbasaur", "Charmander", "Squirtle", "Eevee"]
    non_randomized_catch_em_all_slots = []
    if self.options.catch_em_all and not self.options.randomize_pokemon_locations:
        non_randomized_catch_em_all_slots = self.random.sample(
            [mon for mon in non_randomized_catch_em_all_candidate_slots
             if mon in [slot.name for slot in static_slots]], 4)

    for slot in static_slots:
        location = self.multiworld.get_location(slot.name, self.player)
        randomize_type = self.options.randomize_pokemon_locations.value
        prepend = ""
        if slot.type in ("Legendary Pokemon", "Static Pokemon"):
            prepend = "Static "
        elif slot.type == "Missable Pokemon":
            prepend = "Missable "
        if not randomize_type:
            if slot.name in non_randomized_catch_em_all_slots:
                location.place_locked_item(self.create_item(prepend + non_randomized_catch_em_all_mons.pop()))
            else:
                location.place_locked_item(self.create_item(prepend + slot.original_item))
        else:
            mon = self.create_item(prepend +
                                   randomize_pokemon(self, slot.original_item, mons_list, randomize_type,
                                                     self.random))
            location.place_locked_item(mon)
            if slot.type in ("Legendary Pokemon", "Static Pokemon"):
                static_placed_mons[mon.name.replace("Static ", "")] += 1
            elif slot.type == "Repeatable Static Pokemon":
                placed_mons[mon.name] += 1
    assert not (non_randomized_catch_em_all_mons and non_randomized_catch_em_all_slots)

    chosen_starter_mons = set()
    for slot in starter_slots:
        location = self.multiworld.get_location(slot.name, self.player)
        randomize_type = self.options.randomize_pokemon_locations.value
        slot_type = "Missable"
        if not randomize_type:
            location.place_locked_item(self.create_item(slot_type + " " + slot.original_item))
        else:
            mon = self.create_item(slot_type + " " + randomize_pokemon(self, slot.original_item, mons_list,
                                                                       randomize_type, self.random))
            while mon.name in chosen_starter_mons:
                mon = self.create_item(slot_type + " " + randomize_pokemon(self, slot.original_item, mons_list,
                                                                           randomize_type, self.random))
            chosen_starter_mons.add(mon.name)
            location.place_locked_item(mon)

    encounter_slots_master = get_encounter_slots(self, ["Wild Encounter"])
    encounter_slots = encounter_slots_master.copy()

    if self.options.randomize_pokemon_locations:
        evolutions_needed = []
        for mon in static_placed_mons:
            if static_placed_mons[mon]:
                if mon in poke_data.evolves_to:
                    evolutions_needed.append(poke_data.evolves_to[mon])
                else:
                    placed_mons[mon] += 1
        static_exclusives = [mon for mon in static_placed_mons if static_placed_mons[mon]]
        static_exclusives = self.random.sample(static_exclusives, int(len(static_exclusives) * 0.75))
        zone_mapping = {}
        zone_placed_mons = {}
        mons_list = [pokemon for pokemon in poke_data.pokemon_data.keys() if pokemon not in poke_data.legendary_pokemon
                     or self.options.randomize_legendary_pokemon.value == 3 and pokemon not in static_exclusives]
        self.random.shuffle(encounter_slots)
        locations = []
        for slot in encounter_slots:
            location = self.multiworld.get_location(slot.name, self.player)
            zone = " - ".join(location.name.split(" - ")[:-1])
            if zone not in zone_mapping:
                zone_mapping[zone] = {}
            if zone not in zone_placed_mons:
                zone_placed_mons[zone] = []
            original_mon = slot.original_item
            if self.options.area_1_to_1_mapping and original_mon in zone_mapping[zone]:
                mon = zone_mapping[zone][original_mon]
            else:
                mon = randomize_pokemon(self, original_mon, [m for m in mons_list if m not in zone_placed_mons[zone]],
                                        self.options.randomize_pokemon_locations.value, self.random)
            #
            while ("Pokemon Tower 6F" in slot.name and
                   self.multiworld.get_location("Pokemon Tower 6F - Restless Soul", self.player).item.name
                   == f"Missable {mon}"):
                # If you're fighting the Pokémon defined as the Restless Soul, and you're on the 6th floor of the tower,
                # the battle is treates as the Restless Soul battle and you cannot catch it. So, prevent any wild mons
                # from being the same species as the Restless Soul.
                # to account for the possibility that only one ground type Pokemon exists, match only stats for this fix
                mon = randomize_pokemon(self, original_mon, mons_list, 2, self.random)
            placed_mons[mon] += 1
            location.item = self.create_item(mon)
            location.locked = True
            location.item.location = location
            locations.append(location)
            zone_mapping[zone][original_mon] = mon
            zone_placed_mons[zone].append(mon)

        mons_to_add = []
        remaining_pokemon = [pokemon for pokemon in poke_data.pokemon_data.keys() if placed_mons[pokemon] == 0 and
                             (pokemon not in poke_data.legendary_pokemon or self.options.randomize_legendary_pokemon.value == 3)]
        if self.options.catch_em_all == "first_stage":
            mons_to_add = [pokemon for pokemon in poke_data.first_stage_pokemon if placed_mons[pokemon] == 0 and
                           (pokemon not in poke_data.legendary_pokemon or self.options.randomize_legendary_pokemon.value == 3)]
            mons_to_add += [pokemon for pokemon in evolutions_needed if placed_mons[pokemon] == 0]
        elif self.options.catch_em_all == "all_pokemon":
            mons_to_add = remaining_pokemon.copy()
        logic_needed_mons = max(self.options.oaks_aide_rt_2.value,
                                self.options.oaks_aide_rt_11.value,
                                self.options.oaks_aide_rt_15.value,
                                self.options.elite_four_pokedex_condition.total)
        if self.options.accessibility == "minimal":
            logic_needed_mons = self.options.elite_four_pokedex_condition.total

        self.random.shuffle(remaining_pokemon)
        while (len([pokemon for pokemon in placed_mons if placed_mons[pokemon] > 0])
               + len(mons_to_add) < logic_needed_mons):
            mons_to_add.append(remaining_pokemon.pop())
        for mon in mons_to_add:
            stat_base = get_base_stat_total(mon)
            candidate_locations = encounter_slots_master.copy()
            if self.options.randomize_pokemon_locations.current_key in ["match_base_stats", "match_types_and_base_stats"]:
                candidate_locations.sort(key=lambda slot: abs(get_base_stat_total(slot.original_item) - stat_base))
            if self.options.randomize_pokemon_locations.current_key in ["match_types", "match_types_and_base_stats"]:
                candidate_locations.sort(key=lambda slot: not any([poke_data.pokemon_data[slot.original_item]["type1"] in
                     [self.local_poke_data[mon]["type1"], self.local_poke_data[mon]["type2"]],
                     poke_data.pokemon_data[slot.original_item]["type2"] in
                     [self.local_poke_data[mon]["type1"], self.local_poke_data[mon]["type2"]]]))
            candidate_locations = [self.multiworld.get_location(location.name, self.player) for location in candidate_locations]
            for location in candidate_locations:
                zone = " - ".join(location.name.split(" - ")[:-1])
                if self.options.catch_em_all == "all_pokemon" and self.options.area_1_to_1_mapping:
                    if not [self.multiworld.get_location(l.name, self.player) for l in encounter_slots_master
                            if (not l.name.startswith(zone)) and
                               self.multiworld.get_location(l.name, self.player).item.name == location.item.name]:
                        continue
                if self.options.catch_em_all == "first_stage" and self.options.area_1_to_1_mapping:
                    if not [self.multiworld.get_location(l.name, self.player) for l in encounter_slots_master
                            if (not l.name.startswith(zone)) and
                               self.multiworld.get_location(l.name, self.player).item.name == location.item.name and l.name
                            not in poke_data.evolves_from]:
                        continue

                if placed_mons[location.item.name] < 2 and (location.item.name in poke_data.first_stage_pokemon
                                                            or self.options.catch_em_all):
                    continue

                if self.options.area_1_to_1_mapping:
                    place_locations = [place_location for place_location in candidate_locations if
                        place_location.name.startswith(zone) and
                        place_location.item.name == location.item.name]
                else:
                    place_locations = [location]
                for place_location in place_locations:
                    placed_mons[place_location.item.name] -= 1
                    place_location.item = self.create_item(mon)
                    place_location.item.location = place_location
                    placed_mons[mon] += 1
                break
            else:
                raise Exception

    else:
        for slot in encounter_slots:
            location = self.multiworld.get_location(slot.name, self.player)
            location.item = self.create_item(slot.original_item)
            location.locked = True
            location.item.location = location
            placed_mons[location.item.name] += 1
