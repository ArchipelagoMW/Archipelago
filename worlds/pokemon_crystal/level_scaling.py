import logging
from collections import defaultdict
from dataclasses import replace

from BaseClasses import CollectionState, MultiWorld
from .data import EncounterKey
from .data import data
from .locations import PokemonCrystalLocation
from .options import LevelScaling
from .utils import bound


def perform_level_scaling(multiworld: MultiWorld):
    # Milestones that define sphere boundaries for the level curve.
    # Commented out events are for future-proofing (e.g. ER).
    battle_events = frozenset({
        # "EVENT_RIVAL_CHERRYGROVE_CITY",
        # "EVENT_BEAT_SAGE_LI", # Sprout Tower Boss
        "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
        "EVENT_CLEARED_SLOWPOKE_WELL",
        # "EVENT_HIVE_BADGE_FROM_BUGSY",
        "EVENT_RIVAL_AZALEA_TOWN",
        "EVENT_PLAIN_BADGE_FROM_WHITNEY",
        # "EVENT_RIVAL_BURNED_TOWER",
        # "EVENT_BEAT_KIMONO_GIRL_MIKI", # final girl
        "EVENT_FOG_BADGE_FROM_MORTY",
        "EVENT_BEAT_POKEFANM_DEREK",  # Route 39
        "EVENT_STORM_BADGE_FROM_CHUCK",
        # "EVENT_FOUGHT_EUSINE", # in Cianwood, for legendary hunt maybe? could be fun.
        "EVENT_MINERAL_BADGE_FROM_JASMINE",
        "EVENT_CLEARED_ROCKET_HIDEOUT",
        "EVENT_GLACIER_BADGE_FROM_PRYCE",
        "EVENT_BEAT_ROCKET_EXECUTIVEM_3",  # False Director
        "EVENT_RIVAL_GOLDENROD_UNDERGROUND",
        # "EVENT_BEAT_ROCKET_GRUNTF_3", # Puzzle Room
        # "EVENT_BEAT_ROCKET_GRUNTM_24", # Warehouse
        "EVENT_CLEARED_RADIO_TOWER",
        "EVENT_RISING_BADGE_FROM_CLAIR",
        "EVENT_BEAT_COOLTRAINERM_DARIN",  # Dragon's Den Entrance
        "EVENT_RIVAL_VICTORY_ROAD",
        # "EVENT_BEAT_ELITE_4_WILL",
        # "EVENT_BEAT_ELITE_4_KOGA",
        # "EVENT_BEAT_ELITE_4_BRUNO",
        # "EVENT_BEAT_ELITE_4_KAREN",
        "EVENT_BEAT_ELITE_FOUR",
        "EVENT_FAST_SHIP_LAZY_SAILOR",  # boat quest
        "EVENT_THUNDER_BADGE_FROM_LTSURGE",
        "EVENT_MARSH_BADGE_FROM_SABRINA",
        "EVENT_RAINBOW_BADGE_FROM_ERIKA",
        # "EVENT_BEAT_BIRD_KEEPER_BOB", # Route 18
        "EVENT_SOUL_BADGE_FROM_JANINE",
        # "EVENT_BEAT_POKEFANM_JOSHUA", # Fred
        # "EVENT_BEAT_COOLTRAINERM_KEVIN", # Fabulous Prize
        "EVENT_CASCADE_BADGE_FROM_MISTY",
        "EVENT_BOULDER_BADGE_FROM_BROCK",
        "EVENT_VOLCANO_BADGE_FROM_BLAINE",
        "EVENT_EARTH_BADGE_FROM_BLUE",
        "EVENT_BEAT_RIVAL_IN_MT_MOON",
        # "EVENT_RIVAL_INDIGO_PLATEAU_POKECENTER", # this is the league rematch, wed and fri only; requires mt. moon rival
        "EVENT_KOJI_ALLOWS_YOU_PASSAGE_TO_TIN_TOWER",  # 3rd of Wise Trio.
        "EVENT_BEAT_RED",  # Either Red is the final boss, or he's not lol.  Either way, might as well have a roof.
    })

    level_scaling_required = False
    state = CollectionState(multiworld)
    progression_locations = {loc for loc in multiworld.get_filled_locations() if loc.item.advancement}
    crystal_locations: set[PokemonCrystalLocation] = {loc for loc in multiworld.get_filled_locations() if
                                                      loc.game == data.manifest.game}
    scaling_locations = {loc for loc in crystal_locations if
                         ("trainer scaling" in loc.tags) or ("static scaling" in loc.tags) or (
                                 "wilds scaling" in loc.tags)}
    locations = progression_locations | scaling_locations
    collected_locations = set()
    spheres = list[set[PokemonCrystalLocation]]()

    for world in multiworld.get_game_worlds(data.manifest.game):
        if world.options.level_scaling != LevelScaling.option_off:
            level_scaling_required = True
        else:
            world.finished_level_scaling.set()

    if not level_scaling_required:
        return

    needs_distance = any(
        w.options.level_scaling == LevelScaling.option_spheres_and_distance
        for w in multiworld.get_game_worlds(data.manifest.game)
    )

    locations_by_region = defaultdict(set)
    for loc in locations:
        locations_by_region[loc.parent_region].add(loc)

    def calculate_distances():
        for world in multiworld.get_game_worlds(data.manifest.game):
            if world.options.level_scaling != LevelScaling.option_spheres_and_distance:
                continue
            start = multiworld.get_region("Menu", world.player)
            visited = {start}
            start.distance = 0
            frontier = [start]
            dist = 0
            while frontier:
                next_frontier = []
                dist += 1
                for region in frontier:
                    for exit in region.exits:
                        target = exit.connected_region
                        if target and target not in visited and exit.access_rule(state):
                            visited.add(target)
                            target.distance = dist
                            next_frontier.append(target)
                frontier = next_frontier

    while locations:
        if needs_distance:
            calculate_distances()

        sphere_locations = set()

        # Collect event locations first because they might unlock more locations in the same sphere
        while True:
            newly_reachable = set()
            empty_regions = []
            for region, region_locs in locations_by_region.items():
                # Skip all locations in unreachable regions
                if not region.can_reach(state):
                    continue
                reachable_in_region = {loc for loc in region_locs if loc.access_rule(state)}
                newly_reachable |= reachable_in_region
                region_locs -= reachable_in_region
                if not region_locs:
                    empty_regions.append(region)
            for region in empty_regions:
                del locations_by_region[region]

            if not newly_reachable:
                break

            locations -= newly_reachable
            sphere_locations |= newly_reachable

            for loc in newly_reachable:
                if loc.is_event and loc.item and loc.name not in battle_events:
                    collected_locations.add(loc)
                    state.collect(loc.item, True, loc)

        # If there's no currently accessible location then we're done. Dump the rest of the locations into the last sphere just in case
        if not sphere_locations:
            if locations:
                spheres.append(locations)
            break

        # Build the actual spheres, splitting them by distance if necessary
        if needs_distance:
            by_distance = {}
            for loc in sphere_locations:
                dist = getattr(loc.parent_region, "distance", 0) if loc.game == data.manifest.game else 0
                if dist not in by_distance:
                    by_distance[dist] = set()
                by_distance[dist].add(loc)
            for dist in sorted(by_distance.keys()):
                spheres.append(by_distance[dist])
        else:
            spheres.append(sphere_locations)

        # Collect the rest of the locations in the current sphere so we can continue on
        for loc in sphere_locations:
            if loc.item and loc not in collected_locations:
                collected_locations.add(loc)
                state.collect(loc.item, True, loc)

    for world in multiworld.get_game_worlds(data.manifest.game):
        if world.options.level_scaling == LevelScaling.option_off:
            continue

        # red_goal_adjustment = 73 / 40  # adjusts for when red is goal, 1.8 times higher level
        # e4_base_level = 40

        for sphere in spheres:
            wild_locations = [loc for loc in sphere if loc.player == world.player and "wilds scaling" in loc.tags]
            trainer_locations = [loc for loc in sphere if loc.player == world.player and "trainer scaling" in loc.tags]
            static_locations = [loc for loc in sphere if loc.player == world.player and "static scaling" in loc.tags]

            wild_locations.sort(key=lambda loc: world.encounter_region_name_list.index(loc.name))
            trainer_locations.sort(key=lambda loc: world.trainer_name_list.index(loc.name))
            static_locations.sort(key=lambda loc: world.static_name_list.index(loc.name))

            for wild_location in wild_locations:
                encounter_key = wild_location.encounter_key
                world.generated_wild[encounter_key] = [
                    replace(encounter, level=world.encounter_region_levels_list.pop(0)) for encounter in
                    world.generated_wild[encounter_key]]

            for trainer_location in trainer_locations:
                new_base_level = world.trainer_level_list.pop(0)
                old_base_level = world.trainer_name_level_dict[trainer_location.name]

                # if trainer_location.name in ["WILL_1", "KOGA_1", "BRUNO_1", "KAREN_1", "CHAMPION_1"]:
                #     e4_base_level = new_base_level
                # elif trainer_location.name == "RED_1":
                #     new_base_level = max(new_base_level, round(e4_base_level * red_goal_adjustment))

                trainer_data = world.generated_trainers[trainer_location.name]
                new_pokemon = []
                for pokemon in trainer_data.pokemon:
                    new_level = round(min((new_base_level * pokemon.level / old_base_level),
                                          (new_base_level + pokemon.level - old_base_level)))
                    new_level = bound(new_level, 1, 100)
                    new_pokemon.append(replace(pokemon, level=new_level))
                    logging.debug(
                        f"Setting level {new_level} {pokemon.pokemon} for {trainer_location.name} for {world.player_name}")
                world.generated_trainers[trainer_location.name] = replace(trainer_data, pokemon=new_pokemon)

            for static_location in static_locations:
                new_base_level = world.static_level_list.pop(0)

                encounter_key = EncounterKey.static(static_location.name)
                pokemon_data = world.generated_static[encounter_key]
                new_pokemon = replace(pokemon_data, level=new_base_level)
                world.generated_static[encounter_key] = new_pokemon
                logging.debug(
                    f"Setting level {new_base_level} for static {pokemon_data.pokemon} for {world.player_name}")

        world.finished_level_scaling.set()
