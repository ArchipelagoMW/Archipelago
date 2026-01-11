from typing import List, Set

from BaseClasses import CollectionState, MultiWorld

from .data import data, EncounterType, LocationCategory, TRAINER_REMATCH_MAP
from .locations import PokemonFRLGLocation
from .options import LevelScaling
from .regions import PokemonFRLGRegion
from .util import bound


def level_scaling(multiworld: MultiWorld):
    battle_events = ["Route 22 - Early Rival Battle", "Pewter Gym - Gym Leader Battle",
                     "Cerulean Gym - Gym Leader Battle", "Vermilion Gym - Gym Leader Battle",
                     "Celadon Gym - Gym Leader Battle", "Fuchsia Gym - Gym Leader Battle",
                     "Saffron Gym - Gym Leader Battle", "Cinnabar Gym - Gym Leader Battle",
                     "Viridian Gym - Gym Leader Battle", "Champion's Room - Champion Battle",
                     "Champion's Room - Champion Rematch Battle", "Pokemon Tower 7F - Hostage",
                     "Silph Co. 11F - Giovanni Battle", "Berry Forest - Hypno Battle",
                     "Icefall Cave Back - Team Rocket Grunt Battle"]

    scaling_categories = [LocationCategory.EVENT_TRAINER_SCALING,
                          LocationCategory.EVENT_WILD_POKEMON_SCALING,
                          LocationCategory.EVENT_STATIC_POKEMON_SCALING]

    level_scaling_required = False
    state = CollectionState(multiworld)
    progression_locations = {loc for loc in multiworld.get_filled_locations() if loc.item.advancement}
    frlg_locations: Set[PokemonFRLGLocation] = {loc for loc in multiworld.get_filled_locations()
                                                if loc.game == "Pokemon FireRed and LeafGreen"}
    scaling_locations = {loc for loc in frlg_locations if loc.category in scaling_categories}
    locations = progression_locations | scaling_locations
    collected_locations = set()
    spheres = []

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        if world.options.level_scaling != LevelScaling.option_off:
            level_scaling_required = True
        else:
            world.finished_level_scaling.set()

    if not level_scaling_required:
        return

    while len(locations) > 0:
        new_spheres: List[Set] = []
        new_battle_events = set()
        battle_events_found = True

        while battle_events_found:
            battle_events_found = False
            events_found = True
            sphere = set()
            old_sphere = set()
            distances = {}

            while events_found:
                events_found = False

                for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
                    if world.options.level_scaling != LevelScaling.option_spheres_and_distance:
                        continue
                    regions = {multiworld.get_region("Title Screen", world.player)}
                    checked_regions = set()
                    distance = 0
                    while regions:
                        update_regions = True
                        while update_regions:
                            update_regions = False
                            same_distance_regions = set()
                            for region in regions:
                                keys = ["Encounter", "Encounters", "Trainers"]
                                encounter_regions = {e.connected_region for e in region.exits
                                                     if e.access_rule(state)
                                                     and any(key in e.connected_region.name for key in keys)}
                                same_distance_regions.update(encounter_regions)
                            regions_len = len(regions)
                            regions.update(same_distance_regions)
                            if len(regions) > regions_len:
                                update_regions = True
                        next_regions = set()
                        for region in regions:
                            if not getattr(region, "distance") or distance < region.distance:
                                region.distance = distance
                            next_regions.update({e.connected_region for e in region.exits if e.connected_region not in
                                                 checked_regions and e.access_rule(state)})
                        checked_regions.update(regions)
                        regions = next_regions
                        distance += 1

                for location in locations:
                    if location.can_reach(state):
                        sphere.add(location)

                        if location.game == "Pokemon FireRed and LeafGreen":
                            parent_region: PokemonFRLGRegion = location.parent_region
                            if getattr(parent_region, "distance", None) is None:
                                distance = 0
                            else:
                                distance = parent_region.distance
                        else:
                            distance = 0

                        if distance not in distances:
                            distances[distance] = {location}
                        else:
                            distances[distance].add(location)

                locations -= sphere
                old_sphere ^= sphere

                for location in old_sphere:
                    if location.is_event and location.item and location not in collected_locations:
                        if location.name not in battle_events:
                            collected_locations.add(location)
                            state.collect(location.item, True, location)
                            events_found = True
                        else:
                            new_battle_events.add(location)
                            battle_events_found = True

                old_sphere |= sphere

            if sphere:
                for distance in sorted(distances.keys()):
                    new_spheres.append(distances[distance])

            for event in new_battle_events:
                if event.item and event not in collected_locations:
                    collected_locations.add(event)
                    state.collect(event.item, True, event)

        if len(new_spheres) > 0:
            for sphere in new_spheres:
                spheres.append(sphere)

                for location in sphere:
                    if location.item and location not in collected_locations:
                        collected_locations.add(location)
                        state.collect(location.item, True, location)
        else:
            spheres.append(locations)
            break

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        if world.options.level_scaling == LevelScaling.option_off:
            continue

        game_version = world.options.game_version.current_key

        if world.options.skip_elite_four:
            e4_base_level = data.trainers["TRAINER_CHAMPION_FIRST_BULBASAUR"].party.base_level
            e4_rematch_base_level = data.trainers["TRAINER_CHAMPION_REMATCH_BULBASAUR"].party.base_level
            e4_rematch_adjustment = e4_rematch_base_level / e4_base_level
        else:
            e4_base_level = data.trainers["TRAINER_ELITE_FOUR_LORELEI"].party.base_level
            e4_rematch_base_level = data.trainers["TRAINER_ELITE_FOUR_LORELEI_2"].party.base_level
            e4_rematch_adjustment = e4_rematch_base_level / e4_base_level

        for sphere in spheres:
            scaling_locations = [loc for loc in sphere if loc.player == world.player
                                 and loc.category in scaling_categories]
            trainer_locations = [loc for loc in scaling_locations
                                 if loc.category == LocationCategory.EVENT_TRAINER_SCALING]
            encounter_locations = [loc for loc in scaling_locations
                                   if loc.category in [LocationCategory.EVENT_WILD_POKEMON_SCALING,
                                                       LocationCategory.EVENT_STATIC_POKEMON_SCALING]]

            trainer_locations.sort(key=lambda loc: world.trainer_name_list.index(loc.name))
            encounter_locations.sort(key=lambda loc: world.encounter_name_list.index(loc.name))

            for trainer_location in trainer_locations:
                new_base_level = world.trainer_level_list.pop(0)
                old_base_level = world.trainer_name_level_dict[trainer_location.name]

                if trainer_location.name in ["Elite Four Scaling", "Champion Scaling"]:
                    e4_base_level = new_base_level
                elif trainer_location.name in ["Elite Four Rematch Scaling", "Champion Rematch Scaling"]:
                    new_base_level = max(new_base_level, round(e4_base_level * e4_rematch_adjustment))

                for scaling_id in trainer_location.scaling_ids:
                    trainer_data = world.modified_trainers[scaling_id]
                    for pokemon in trainer_data.party.pokemon:
                        new_level = round(min((new_base_level * pokemon.level / old_base_level),
                                              (new_base_level + pokemon.level - old_base_level)))
                        new_level = bound(new_level, 1, 100)
                        pokemon.level = new_level
                    if f"{scaling_id}_REWARD" in TRAINER_REMATCH_MAP:
                        trainer_base_level = data.trainers[scaling_id].party.base_level
                        for rematch_id in TRAINER_REMATCH_MAP[f"{scaling_id}_REWARD"]:
                            rematch_trainer_data = world.modified_trainers[rematch_id[:-7]]
                            rematch_base_level = data.trainers[rematch_id[:-7]].party.base_level
                            new_rematch_base_level = min(new_base_level * (rematch_base_level / trainer_base_level),
                                                         new_base_level + (rematch_base_level - trainer_base_level))
                            for pokemon in rematch_trainer_data.party.pokemon:
                                new_level = round(min((new_rematch_base_level * pokemon.level / rematch_base_level),
                                                      (new_rematch_base_level + pokemon.level - rematch_base_level)))
                                new_level = bound(new_level, 1, 100)
                                pokemon.level = new_level

            for encounter_location in encounter_locations:
                new_base_level = world.encounter_level_list.pop(0)
                old_base_level = world.encounter_name_level_dict[encounter_location.name]

                for scaling_id in encounter_location.scaling_ids:
                    if encounter_location.category == LocationCategory.EVENT_STATIC_POKEMON_SCALING:
                        pokemon_data = None

                        if scaling_id in world.modified_misc_pokemon:
                            pokemon_data = world.modified_misc_pokemon[scaling_id]
                        elif scaling_id in world.modified_legendary_pokemon:
                            pokemon_data = world.modified_legendary_pokemon[scaling_id]

                        pokemon_data.level[game_version] = new_base_level
                    elif encounter_location.category == LocationCategory.EVENT_WILD_POKEMON_SCALING:
                        scaling_ids = scaling_id.split()
                        map_data = world.modified_maps[scaling_ids[0]]
                        encounters = (map_data.encounters[EncounterType.LAND]
                                      if "Land" in encounter_location.name else
                                      map_data.encounters[EncounterType.WATER]
                                      if "Water" in encounter_location.name else
                                      map_data.encounters[EncounterType.FISHING])
                        encounter_data = encounters.slots[game_version][int(scaling_ids[1])]
                        new_max_level = round(max((new_base_level * encounter_data.max_level / old_base_level),
                                                  (new_base_level + encounter_data.max_level - old_base_level)))
                        new_min_level = round(max((new_base_level * encounter_data.min_level / old_base_level),
                                                  (new_base_level + encounter_data.min_level - old_base_level)))
                        new_max_level = bound(new_max_level, 1, 100)
                        new_min_level = bound(new_min_level, 1, 100)
                        encounter_data.max_level = new_max_level
                        encounter_data.min_level = new_min_level

        world.finished_level_scaling.set()
