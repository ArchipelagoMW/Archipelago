"""
Functions related to AP regions for Pokémon FireRed and LeafGreen (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple, Callable
from BaseClasses import Entrance, Region, CollectionState, ItemClassification
from entrance_rando import ERPlacementState
from .data import (data, LocationCategory, fly_plando_maps, kanto_fly_destinations, sevii_fly_destinations,
                   starting_town_blacklist_map)
from .items import PokemonFRLGItem
from .locations import PokemonFRLGLocation
from .options import LevelScaling

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

INDIRECT_CONDITIONS: Dict[str, List[str]] = {
    "Seafoam Islands 1F": ["Seafoam Islands B3F Southwest Surfing Spot", "Seafoam Islands B3F Southwest Landing",
                           "Seafoam Islands B3F East Landing (South)", "Seafoam Islands B3F East Surfing Spot (South)",
                           "Seafoam Islands B3F South Water (Water Battle)"],
    "Seafoam Islands B3F Southwest": ["Seafoam Islands B4F Surfing Spot (West)",
                                      "Seafoam Islands B4F Near Articuno Landing"],
    "Victory Road 3F Southwest": ["Victory Road 2F Center Rock Barrier"],
    "Vermilion City": ["Navel Rock Arrival", "Birth Island Arrival"]
}

STATIC_POKEMON_SPOILER_NAMES = {
    "TRADE_POKEMON_MR_MIME": "Route 2 Trade House",
    "GIFT_POKEMON_MAGIKARP": "Route 4 Pokemon Center 1F",
    "TRADE_POKEMON_JYNX": "Cerulean Trade House",
    "TRADE_POKEMON_NIDORAN": "Underground Path North Entrance",
    "TRADE_POKEMON_FARFETCHD": "Vermilion Trade House",
    "TRADE_POKEMON_NIDORINOA": "Route 11 Gate 2F",
    "STATIC_POKEMON_ELECTRODE_1": "Power Plant (Static)",
    "STATIC_POKEMON_ELECTRODE_2": "Power Plant (Static)",
    "LEGENDARY_POKEMON_ZAPDOS": "Power Plant (Static)",
    "CELADON_PRIZE_POKEMON_1": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_2": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_3": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_4": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_5": "Celadon Game Corner Prize Room",
    "GIFT_POKEMON_EEVEE": "Celadon Condominiums Roof Room",
    "STATIC_POKEMON_ROUTE12_SNORLAX": "Route 12 (Static)",
    "STATIC_POKEMON_ROUTE16_SNORLAX": "Route 16 (Static)",
    "TRADE_POKEMON_LICKITUNG": "Route 18 Gate 2F",
    "GIFT_POKEMON_HITMONCHAN": "Saffron Dojo",
    "GIFT_POKEMON_HITMONLEE": "Saffron Dojo",
    "GIFT_POKEMON_LAPRAS": "Silph Co. 7F",
    "LEGENDARY_POKEMON_ARTICUNO": "Seafoam Islands B4F (Static)",
    "TRADE_POKEMON_ELECTRODE": "Pokemon Lab Lounge",
    "TRADE_POKEMON_TANGELA": "Pokemon Lab Lounge",
    "GIFT_POKEMON_OMANYTE": "Pokemon Lab Experiment Room (Helix)",
    "GIFT_POKEMON_KABUTO": "Pokemon Lab Experiment Room (Dome)",
    "GIFT_POKEMON_AERODACTYL": "Pokemon Lab Experiment Room (Amber)",
    "TRADE_POKEMON_SEEL": "Pokemon Lab Experiment Room (Trade)",
    "LEGENDARY_POKEMON_MOLTRES": "Mt. Ember Summit",
    "STATIC_POKEMON_HYPNO": "Berry Forest (Static)",
    "EGG_POKEMON_TOGEPI": "Water Labyrinth (Egg)",
    "LEGENDARY_POKEMON_MEWTWO": "Cerulean Cave B1F (Static)",
    "LEGENDARY_POKEMON_HO_OH": "Navel Rock Summit",
    "LEGENDARY_POKEMON_LUGIA": "Navel Rock Base",
    "LEGENDARY_POKEMON_DEOXYS": "Birth Island Exterior"
}

starting_town_map = {
    "SPAWN_PALLET_TOWN": "Pallet Town",
    "SPAWN_VIRIDIAN_CITY": "Viridian City South",
    "SPAWN_PEWTER_CITY": "Pewter City",
    "SPAWN_CERULEAN_CITY": "Cerulean City",
    "SPAWN_LAVENDER_TOWN": "Lavender Town",
    "SPAWN_VERMILION_CITY": "Vermilion City",
    "SPAWN_CELADON_CITY": "Celadon City",
    "SPAWN_FUCHSIA_CITY": "Fuchsia City",
    "SPAWN_CINNABAR_ISLAND": "Cinnabar Island",
    "SPAWN_INDIGO_PLATEAU": "Indigo Plateau",
    "SPAWN_SAFFRON_CITY": "Saffron City",
    "SPAWN_ROUTE4": "Route 4 West",
    "SPAWN_ROUTE10": "Route 10 North",
    "SPAWN_ONE_ISLAND": "One Island Town",
    "SPAWN_TWO_ISLAND": "Two Island Town",
    "SPAWN_THREE_ISLAND": "Three Island Town South",
    "SPAWN_FOUR_ISLAND": "Four Island Town",
    "SPAWN_FIVE_ISLAND": "Five Island Town",
    "SPAWN_SEVEN_ISLAND": "Seven Island Town",
    "SPAWN_SIX_ISLAND": "Six Island Town"
}

fly_destination_entrance_map = {
      "Pallet Town Fly Destination": "SPAWN_PALLET_TOWN",
      "Viridian City Fly Destination": "SPAWN_VIRIDIAN_CITY",
      "Pewter City Fly Destination": "SPAWN_PEWTER_CITY",
      "Route 4 Fly Destination": "SPAWN_ROUTE4",
      "Cerulean City Fly Destination": "SPAWN_CERULEAN_CITY",
      "Vermilion City Fly Destination": "SPAWN_VERMILION_CITY",
      "Route 10 Fly Destination": "SPAWN_ROUTE10",
      "Lavender Town Fly Destination": "SPAWN_LAVENDER_TOWN",
      "Celadon City Fly Destination": "SPAWN_CELADON_CITY",
      "Fuchsia City Fly Destination": "SPAWN_FUCHSIA_CITY",
      "Saffron City Fly Destination": "SPAWN_SAFFRON_CITY",
      "Cinnabar Island Fly Destination": "SPAWN_CINNABAR_ISLAND",
      "Indigo Plateau Fly Destination": 'SPAWN_INDIGO_PLATEAU',
      "One Island Fly Destination": "SPAWN_ONE_ISLAND",
      "Two Island Fly Destination": "SPAWN_TWO_ISLAND",
      "Three Island Fly Destination": "SPAWN_THREE_ISLAND",
      "Four Island Fly Destination": "SPAWN_FOUR_ISLAND",
      "Five Island Fly Destination": "SPAWN_FIVE_ISLAND",
      "Six Island Fly Destination": "SPAWN_SIX_ISLAND",
      "Seven Island Fly Destination": "SPAWN_SEVEN_ISLAND"
}


class PokemonFRLGEntrance(Entrance):
    connected_entrance_name: str | None = None

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        return (self.randomization_type == other.randomization_type
                and (not er_state.coupled or self.name != other.name)
                and (self.connected_entrance_name is None or self.connected_entrance_name == other.name))


class PokemonFRLGRegion(Region):
    distance: int | None
    entrance_type = PokemonFRLGEntrance

    def __init__(self, name, player, multiworld):
        super().__init__(name, player, multiworld)
        self.distance = None


def create_regions(world: "PokemonFRLGWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """

    # Used in connect_to_map_encounters. Splits encounter categories into "subcategories" and gives them names
    # and rules so the rods can only access their specific slots.
    encounter_categories: Dict[str, List[Tuple[str | None, range, Callable[[CollectionState], bool] | None]]] = {
        "Land": [(None, range(0, 12), None)],
        "Water": [(None, range(0, 5), None)],
        "Fishing": [
            ("Old Rod", range(0, 2), lambda state: state.has("Old Rod", world.player)),
            ("Good Rod", range(2, 5), lambda state: state.has("Good Rod", world.player)),
            ("Super Rod", range(5, 10), lambda state: state.has("Super Rod", world.player)),
        ],
    }

    game_version = world.options.game_version.current_key

    def connect_to_map_encounters(regions: Dict[str, Region], region: Region, map_name: str, encounter_region_name: str,
                                  include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild Pokémon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc.).

        These regions are created lazily and dynamically so as not to bother with unused maps.
        """

        if True in include_slots and encounter_region_name is None:
            raise AssertionError(f"{region.name} has encounters but does not have an encounter region name")

        for i, encounter_category in enumerate(encounter_categories.items()):
            if include_slots[i]:
                region_name = f"{encounter_region_name} {encounter_category[0]} Encounters"

                # If the region hasn't been created yet, create it now
                try:
                    encounter_region = regions[region_name]
                except KeyError:
                    encounter_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)
                    encounter_slots = getattr(world.modified_maps[map_name],
                                              f"{encounter_category[0].lower()}_encounters").slots[game_version]

                    # Subcategory is for splitting fishing rods; land and water only have one subcategory
                    for subcategory in encounter_category[1]:
                        # Want to create locations per species, not per slot
                        # encounter_categories includes info on which slots belong to which subcategory
                        unique_species = []
                        for j, species_data in enumerate(encounter_slots):
                            species_id = species_data.species_id
                            if j in subcategory[1] and species_id not in unique_species:
                                unique_species.append(species_id)

                        # Create a location for the species
                        for j, species_id in enumerate(unique_species):
                            subcategory_name = subcategory[0] if subcategory[0] is not None else encounter_category[0]

                            encounter_location = PokemonFRLGLocation(
                                world.player,
                                f"{encounter_region_name} - {subcategory_name} Encounter {j + 1}",
                                None,
                                LocationCategory.EVENT_WILD_POKEMON,
                                encounter_region,
                                None,
                                None,
                                spoiler_name=f"{encounter_region_name} ({subcategory_name})",
                            )
                            encounter_location.show_in_spoiler = False

                            # Add access rules
                            if subcategory[2] is not None:
                                encounter_location.access_rule = subcategory[2]

                            # Fill the location with an event for catching that species
                            encounter_location.place_locked_item(PokemonFRLGItem(
                                data.species[species_id].name,
                                ItemClassification.progression_skip_balancing,
                                None,
                                world.player
                            ))
                            if data.species[species_id].name not in world.logic.wild_pokemon:
                                world.logic.wild_pokemon.append(data.species[species_id].name)
                            encounter_region.locations.append(encounter_location)

                    # Add the new encounter region to the multiworld
                    regions[region_name] = encounter_region

                # Encounter region exists, just connect to it
                region.connect(encounter_region, f"{region.name} ({encounter_category[0]} Battle)")

    def exclude_region(region_id: str):
        elite_four_ids = [
            "REGION_POKEMON_LEAGUE_LORELEIS_ROOM/MAIN", "REGION_POKEMON_LEAGUE_BRUNOS_ROOM/MAIN",
            "REGION_POKEMON_LEAGUE_AGATHAS_ROOM/MAIN", "REGION_POKEMON_LEAGUE_LANCES_ROOM/MAIN"
        ]

        if world.options.kanto_only and not data.regions[region_id].kanto:
            return True
        if world.options.skip_elite_four and region_id in elite_four_ids:
            return True
        return False

    def exclude_event(event_id: str):
        if world.options.kanto_only and event_id == "EVENT_DEFEAT_CHAMPION_REMATCH":
            return True
        if data.events[event_id].category == LocationCategory.EVENT_SHOP and world.options.shopsanity:
            return True
        if data.events[event_id].category == LocationCategory.EVENT_EVOLUTION_POKEMON:
            # Exclude the event if the evolution method is not required for logic.
            event_data = data.events[event_id]
            pokemon = event_data.name.split(" - ")[1].strip()
            evo_data = data.evolutions[pokemon]
            return evo_data.method not in world.logic.evo_methods_required
        return False

    def exclude_exit(region_id: str, exit_region_id: str):
        if world.options.kanto_only and not data.regions[exit_region_id].kanto:
            return True
        if (not world.options.kanto_only and
                region_id == "REGION_CINNABAR_ISLAND_POKEMON_CENTER_1F/MAIN" and
                exit_region_id == "REGION_VERMILION_CITY/MAIN"):
            return True
        return False

    def exclude_warp(warp: str):
        source_warp = data.warps[warp]
        dest_warp = data.warps[data.warp_map[warp]]
        if source_warp.name == "":
            return True
        if dest_warp.parent_region_id is None:
            return True
        if world.options.kanto_only and not data.regions[dest_warp.parent_region_id].kanto:
            return True
        return False

    def exclude_scaling(scaling_id: str):
        elite_four_ids = [
            "TRAINER_SCALING_POKEMON_LEAGUE_ELITE_FOUR/MAIN",
            "TRAINER_SCALING_POKEMON_LEAGUE_ELITE_FOUR_REMATCH/MAIN"
        ]
        champion_ids = [
            "TRAINER_SCALING_POKEMON_LEAGUE_CHAMPIONS_ROOM/MAIN",
            "TRAINER_SCALING_POKEMON_LEAGUE_CHAMPIONS_ROOM_REMATCH/MAIN"
        ]

        if world.options.kanto_only and not data.scaling[scaling_id].kanto:
            return True
        if world.options.skip_elite_four and scaling_id in elite_four_ids:
            return True
        if not world.options.skip_elite_four and scaling_id in champion_ids:
            return True
        return False

    def modify_entrance_name(world: "PokemonFRLGWorld", name: str) -> str:
        route_2_modification = {
            "Route 2 Northwest Cuttable Tree": "Route 2 Northwest Smashable Rock",
            "Route 2 Northeast Cuttable Tree (North)": "Route 2 Northeast Smashable Rock",
            "Route 2 Northeast Cuttable Tree (South)": "Route 2 Northeast Cuttable Tree"
        }
        block_tunnels = {
            "Route 5 Unobstructed Path": "Route 5 Smashable Rocks",
            "Route 5 Near Tunnel Unobstructed Path": "Route 5 Near Tunnel Smashable Rocks",
            "Route 6 Unobstructed Path": "Route 6 Smashable Rocks",
            "Route 6 Near Tunnel Unobstructed Path": "Route 6 Near Tunnel Smashable Rocks",
            "Route 7 Unobstructed Path": "Route 7 Smashable Rocks",
            "Route 7 Near Tunnel Unobstructed Path": "Route 7 Near Tunnel Smashable Rocks",
            "Route 8 Unobstructed Path": "Route 8 Smashable Rocks",
            "Route 8 Near Tunnel Unobstructed Path": "Route 8 Near Tunnel Smashable Rocks"
        }
        block_pokemon_tower = {
            "Pokemon Tower 1F Unobstructed Path": "Pokemon Tower 1F Reveal Ghost",
            "Pokemon Tower 1F Near Stairs Unobstructed Path": "Pokemon Tower 1F Near Stairs Pass Ghost"
        }
        rotue_23_trees = {
            "Route 23 Near Water Unobstructed Path": "Route 23 Near Water Cuttable Trees",
            "Route 23 Center Unobstructed Path": "Route 23 Center Cuttable Trees"
        }
        route_23_modification = {
            "Route 23 South Water Unobstructed Path": "Route 23 Waterfall Ascend",
            "Route 23 North Water Unobstructed Path": "Route 23 Waterfall Drop"
        }

        if "Modify Route 2" in world.options.modify_world_state.value and name in route_2_modification.keys():
            return route_2_modification[name]
        if "Block Tunnels" in world.options.modify_world_state.value and name in block_tunnels.keys():
            return block_tunnels[name]
        if "Block Tower" in world.options.modify_world_state.value and name in block_pokemon_tower.keys():
            return block_pokemon_tower[name]
        if "Route 23 Trees" in world.options.modify_world_state.value and name in rotue_23_trees.keys():
            return rotue_23_trees[name]
        if "Modify Route 23" in world.options.modify_world_state.value and name in route_23_modification.keys():
            return route_23_modification[name]
        return name

    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    for region_id, region_data in data.regions.items():
        if exclude_region(region_id):
            continue

        region_name = region_data.name

        new_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)

        for event_id in region_data.events:
            event_data = world.modified_events[event_id]

            if exclude_event(event_id):
                continue

            event = PokemonFRLGLocation(world.player,
                                        event_data.name,
                                        None,
                                        event_data.category,
                                        new_region,
                                        None,
                                        None,
                                        spoiler_name=STATIC_POKEMON_SPOILER_NAMES[event_id]
                                        if event_id in STATIC_POKEMON_SPOILER_NAMES else None)
            event.place_locked_item(PokemonFRLGItem(event_data.item,
                                                    ItemClassification.progression,
                                                    None,
                                                    world.player))
            event.show_in_spoiler = False
            new_region.locations.append(event)

        for exit_region_id, exit_name in region_data.exits.items():
            if exclude_exit(region_id, exit_region_id):
                continue
            exit_region_name = data.regions[exit_region_id].name
            connections.append((exit_name, region_name, exit_region_name))

        for warp in region_data.warps:
            if exclude_warp(warp):
                continue
            source_warp = data.warps[warp]
            dest_warp = data.warps[data.warp_map[warp]]
            dest_region_name = data.regions[dest_warp.parent_region_id].name
            if world.options.skip_elite_four:
                if source_warp.name == "Pokemon League":
                    dest_region_name = "Pokemon League Champion's Room"
                elif source_warp.name == "Pokemon League Champion's Room Exit (South)":
                    dest_region_name = "Indigo Plateau Pokemon Center 1F"
            connections.append((source_warp.name, region_name, dest_region_name))

        regions[region_name] = new_region

        parent_map_name = region_data.parent_map.name if region_data.parent_map is not None else None
        connect_to_map_encounters(regions, new_region, parent_map_name, region_data.encounter_region,
                                  (region_data.has_land, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        name = modify_entrance_name(world, name)
        regions[source].connect(regions[dest], name)

    if world.options.level_scaling != LevelScaling.option_off:
        trainer_name_level_list: List[Tuple[str, int]] = []
        encounter_name_level_list: List[Tuple[str, int]] = []

        for scaling_id, scaling_data in data.scaling.items():
            if exclude_scaling(scaling_id):
                continue
            if scaling_data.region not in regions:
                region = PokemonFRLGRegion(scaling_data.region, world.player, world.multiworld)
                regions[scaling_data.region] = region

                for connection in scaling_data.connections:
                    if connection not in regions:
                        continue
                    name = f"{regions[connection].name} -> {region.name}"
                    regions[connection].connect(region, name)
            else:
                region = regions[scaling_data.region]

            for location_name, data_ids in scaling_data.locations.items():
                if scaling_data.category == LocationCategory.EVENT_TRAINER_SCALING:
                    scaling_event = PokemonFRLGLocation(
                        world.player,
                        location_name,
                        None,
                        scaling_data.category,
                        region,
                        None,
                        None,
                        data_ids
                    )
                    scaling_event.place_locked_item(PokemonFRLGItem("Trainer Party",
                                                                    ItemClassification.filler,
                                                                    None,
                                                                    world.player))
                    scaling_event.show_in_spoiler = False
                    region.locations.append(scaling_event)
                elif scaling_data.category == LocationCategory.EVENT_STATIC_POKEMON_SCALING:
                    scaling_event = PokemonFRLGLocation(
                        world.player,
                        location_name,
                        None,
                        scaling_data.category,
                        region,
                        None,
                        None,
                        data_ids
                    )
                    scaling_event.place_locked_item(PokemonFRLGItem("Static Encounter",
                                                                    ItemClassification.filler,
                                                                    None,
                                                                    world.player))
                    scaling_event.show_in_spoiler = False
                    region.locations.append(scaling_event)
                elif scaling_data.category == LocationCategory.EVENT_WILD_POKEMON_SCALING:
                    index = 1
                    events: Dict[str, Tuple[str, List[str], Callable[[CollectionState], bool] | None]] = {}
                    encounter_category_data = encounter_categories[scaling_data.type]
                    for data_id in data_ids:
                        map_data = data.maps[data_id]
                        if world.options.kanto_only and not map_data.kanto:
                            continue
                        encounters = (map_data.land_encounters if scaling_data.type == "Land" else
                                      map_data.water_encounters if scaling_data.type == "Water" else
                                      map_data.fishing_encounters)
                        for subcategory in encounter_category_data:
                            for i in subcategory[1]:
                                subcategory_name = subcategory[0] if subcategory[0] is not None else scaling_data.type
                                species_name = f"{subcategory_name} {encounters.slots[game_version][i].species_id}"
                                if species_name not in events:
                                    encounter_data = (f"{location_name} {index}", [f"{data_id} {i}"], subcategory[2])
                                    events[species_name] = encounter_data
                                    index = index + 1
                                else:
                                    events[species_name][1].append(f"{data_id} {i}")

                    for event in events.values():
                        scaling_event = PokemonFRLGLocation(
                            world.player,
                            event[0],
                            None,
                            scaling_data.category,
                            region,
                            None,
                            None,
                            event[1]
                        )

                        scaling_event.place_locked_item(PokemonFRLGItem("Wild Encounter",
                                                                        ItemClassification.filler,
                                                                        None,
                                                                        world.player))
                        scaling_event.show_in_spoiler = False
                        if event[2] is not None:
                            scaling_event.access_rule = event[2]
                        region.locations.append(scaling_event)

        for region in regions.values():
            for location in region.locations:
                if location.category == LocationCategory.EVENT_TRAINER_SCALING:
                    min_level = 100

                    for data_id in location.data_ids:
                        trainer_data = data.trainers[data_id]
                        for pokemon in trainer_data.party.pokemon:
                            min_level = min(min_level, pokemon.level)

                    trainer_name_level_list.append((location.name, min_level))
                    world.trainer_name_level_dict[location.name] = min_level
                elif location.category == LocationCategory.EVENT_STATIC_POKEMON_SCALING:
                    for data_id in location.data_ids:
                        pokemon_data = None

                        if data_id in data.misc_pokemon:
                            pokemon_data = data.misc_pokemon[data_id]
                        elif data_id in data.legendary_pokemon:
                            pokemon_data = data.legendary_pokemon[data_id]

                        encounter_name_level_list.append((location.name, pokemon_data.level[game_version]))
                        world.encounter_name_level_dict[location.name] = pokemon_data.level[game_version]
                elif location.category == LocationCategory.EVENT_WILD_POKEMON_SCALING:
                    max_level = 1

                    for data_id in location.data_ids:
                        data_ids = data_id.split()
                        map_data = data.maps[data_ids[0]]
                        encounters = (map_data.land_encounters if "Land" in location.name else
                                      map_data.water_encounters if "Water" in location.name else
                                      map_data.fishing_encounters)

                        encounter_max_level = encounters.slots[game_version][int(data_ids[1])].max_level
                        max_level = max(max_level, encounter_max_level)

                    encounter_name_level_list.append((location.name, max_level))
                    world.encounter_name_level_dict[location.name] = max_level

        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        world.trainer_level_list = [i[1] for i in trainer_name_level_list]
        encounter_name_level_list.sort(key=lambda i: i[1])
        world.encounter_name_list = [i[0] for i in encounter_name_level_list]
        world.encounter_level_list = [i[1] for i in encounter_name_level_list]

    if world.options.random_starting_town:
        forbidden_starting_towns = ["SPAWN_INDIGO_PLATEAU"]
        if not world.options.shuffle_badges:
            forbidden_starting_towns.append("SPAWN_ROUTE10")
        if world.options.kanto_only:
            forbidden_starting_towns.extend(["SPAWN_ONE_ISLAND", "SPAWN_TWO_ISLAND", "SPAWN_THREE_ISLAND",
                                             "SPAWN_FOUR_ISLAND", "SPAWN_FIVE_ISLAND", "SPAWN_SIX_ISLAND",
                                             "SPAWN_SEVEN_ISLAND"])
        blacklisted_starting_towns = [v for k, v in starting_town_blacklist_map.items()
                                      if k in world.options.starting_town_blacklist.value]
        allowed_starting_towns = [town for town in starting_town_map.keys()
                                  if town not in forbidden_starting_towns and town not in blacklisted_starting_towns]
        if len(allowed_starting_towns) == 0:
            allowed_starting_towns = [town for town in starting_town_map.keys() if town not in forbidden_starting_towns]
        world.starting_town = world.random.choice(allowed_starting_towns)

    if world.options.randomize_fly_destinations:
        fly_destinations = kanto_fly_destinations.copy()
        if not world.options.kanto_only:
            fly_destinations.update(sevii_fly_destinations)
        maps_already_chosen = set()
        exit_already_randomized = set()
        for exit_name, warp_name in world.options.fly_destination_plando.value.items():
            fly_plando = fly_plando_maps[warp_name]
            if fly_plando[0] in maps_already_chosen or fly_plando[0] not in fly_destinations.keys():
                continue
            exit = world.multiworld.get_entrance(exit_name, world.player)
            regions[exit.connected_region.name].entrances.remove(exit)
            exit.connected_region = None
            maps_already_chosen.add(fly_plando[0])
            exit_already_randomized.add(exit_name)
            exit.connected_region = regions[fly_plando[1]]
            regions[fly_plando[1]].entrances.append(exit)
            world.fly_destination_data[fly_destination_entrance_map[exit.name]] = fly_plando[2]
        for exit in regions["Sky"].exits:
            if exit.name in exit_already_randomized:
                continue
            regions[exit.connected_region.name].entrances.remove(exit)
            exit.connected_region = None
            allowed_maps = [k for k in fly_destinations.keys() if k not in maps_already_chosen]
            map = world.random.choice(allowed_maps)
            allowed_regions = list(fly_destinations[map].keys())
            map_region = world.random.choice(allowed_regions)
            allowed_warps = fly_destinations[map][map_region]
            map_warp = world.random.choice(allowed_warps)
            maps_already_chosen.add(map)
            exit.connected_region = regions[map_region]
            regions[map_region].entrances.append(exit)
            world.fly_destination_data[fly_destination_entrance_map[exit.name]] = map_warp

    regions["Title Screen"].connect(regions[starting_town_map[world.starting_town]], "Start Game")
    regions["Title Screen"].connect(regions["Player's PC"], "Use PC")
    regions["Title Screen"].connect(regions["Pokedex"], "Pokedex")
    regions["Title Screen"].connect(regions["Evolutions"], "Evolve")
    regions["Title Screen"].connect(regions["Sky"], "Flying")

    return regions


def create_indirect_conditions(world: "PokemonFRLGWorld"):
    for region, entrances in INDIRECT_CONDITIONS.items():
        for entrance in entrances:
            world.multiworld.register_indirect_condition(world.get_region(region), world.get_entrance(entrance))
