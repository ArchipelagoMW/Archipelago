"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
import re
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, cast, Iterable
from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule, add_rule
from .data import data, NAME_TO_SPECIES_ID, EvolutionMethodEnum, LocationCategory
from .locations import PokemonFRLGLocation
from .options import (CeruleanCaveRequirement, EliteFourRequirement, FlashRequired, Goal, IslandPasses,
                      ItemfinderRequired, PewterCityRoadblock, Route22GateRequirement, Route23GuardRequirement,
                      ViridianCityRoadblock, ViridianGymRequirement)
from .pokemon import add_hm_compatability
from .util import HM_TO_COMPATIBILITY_ID, int_to_bool_array


if TYPE_CHECKING:
    from . import PokemonFRLGWorld

BADGE_REQUIREMENTS: Dict[str, str] = {
    "Cut": "Cascade Badge",
    "Fly": "Thunder Badge",
    "Surf": "Soul Badge",
    "Strength": "Rainbow Badge",
    "Flash": "Boulder Badge",
    "Rock Smash": "Marsh Badge",
    "Waterfall": "Volcano Badge"
}

EVO_METHODS_LEVEL = {
    EvolutionMethodEnum.LEVEL,
    EvolutionMethodEnum.LEVEL_NINJASK,
    EvolutionMethodEnum.LEVEL_SHEDINJA
}

EVO_METHODS_TYROGUE_LEVEL = {
    EvolutionMethodEnum.LEVEL_ATK_LT_DEF,
    EvolutionMethodEnum.LEVEL_ATK_EQ_DEF,
    EvolutionMethodEnum.LEVEL_ATK_GT_DEF
}

EVO_METHODS_WURMPLE_LEVEL = {
    EvolutionMethodEnum.LEVEL_SILCOON,
    EvolutionMethodEnum.LEVEL_CASCOON
}

EVO_METHODS_LEVEL_ANY = {*EVO_METHODS_LEVEL, *EVO_METHODS_TYROGUE_LEVEL, *EVO_METHODS_WURMPLE_LEVEL}

EVO_METHODS_ITEM = {
    EvolutionMethodEnum.ITEM
}

EVO_METHODS_HELD_ITEM = {
    EvolutionMethodEnum.ITEM_HELD
}

EVO_METHODS_FRIENDSHIP = {
    EvolutionMethodEnum.FRIENDSHIP
}


ISLAND_PASSES = ("Tri Pass", "Rainbow Pass")
SPLIT_ISLAND_PASSES = ("One Pass", "Two Pass", "Three Pass", "Four Pass", "Five Pass", "Six Pass", "Seven Pass")
CARD_KEYS_PER_FLOOR = {floor: ("Card Key", f"Card Key {floor}F") for floor in range(1, 12)}
BADGES = ("Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge",
          "Volcano Badge", "Earth Badge")
GYMS = ("Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika", "Defeat Koga", "Defeat Sabrina",
        "Defeat Blaine", "Defeat Giovanni")


class PokemonFRLGLogic:
    player: int
    compatible_hm_pokemon: Dict[str, List[str]]
    evo_methods_required: Set[EvolutionMethodEnum]
    required_trade_pokemon: Dict[str, str]
    resort_gorgeous_pokemon: int
    wild_pokemon: List[str]
    world_item_id_map: Dict[int, str]
    badge_required: Dict[str, bool]
    dexsanity_requires_evos: bool
    hms_require_evos: bool
    oaks_aides_require_evos: bool
    randomizing_entrances: bool
    dexsanity_state_item_names_lookup: Dict[str, Tuple[str, ...]]
    oaks_aides_species_item_names: List[Tuple[str, ...]]
    pokemon_hm_use: Dict[str, List[str]]
    evolution_state_item_names_lookup: Dict[str, List[str]]

    def __init__(self, player: int, item_id_to_name: Dict[int, str]) -> None:
        self.player = player
        self.compatible_hm_pokemon = defaultdict(list)
        self.evo_methods_required = set()
        self.required_trade_pokemon = {}
        self.resort_gorgeous_pokemon = data.constants["SPECIES_PIKACHU"]
        self.wild_pokemon = []
        self.world_item_id_map = item_id_to_name
        self.badge_required = {}
        self.dexsanity_requires_evos = False
        self.hms_require_evos = False
        self.oaks_aides_require_evos = False
        self.randomizing_entrances = False
        self.dexsanity_state_item_names_lookup = {}
        self.oaks_aides_species_item_names = []
        self.evolution_state_item_names_lookup = {}

    def update_hm_compatible_pokemon(self):
        pokemon_hm_use = defaultdict(list)
        for hm, species_list in self.compatible_hm_pokemon.items():
            hm_logic_name = f"Teach {hm}"
            for species in species_list:
                pokemon_hm_use[species].append(hm_logic_name)
                if self.hms_require_evos:
                    pokemon_hm_use[f"Evolved {species}"].append(hm_logic_name)
        self.pokemon_hm_use = pokemon_hm_use

    def add_hm_compatible_pokemon(self, hm: str, species: str):
        self.compatible_hm_pokemon[hm].append(species)
        hm_logic_name = f"Teach {hm}"
        self.pokemon_hm_use.setdefault(species, []).append(hm_logic_name)
        if self.hms_require_evos:
            self.pokemon_hm_use.setdefault(f"Evolved {species}", []).append(hm_logic_name)

    def has_badge_requirement(self, state: CollectionState, hm: str) -> bool:
        return not self.badge_required[hm] or state.has(BADGE_REQUIREMENTS[hm], self.player)

    def can_cut(self, state: CollectionState) -> bool:
        return (state.has_all(("HM01 Cut", "TM Case", "Teach Cut"), self.player) and
                self.has_badge_requirement(state, "Cut"))

    def can_fly(self, state: CollectionState) -> bool:
        return (state.has_all(("HM02 Fly", "TM Case", "Teach Fly"), self.player) and
                self.has_badge_requirement(state, "Fly"))

    def can_surf(self, state: CollectionState) -> bool:
        return (state.has_all(("HM03 Surf", "TM Case", "Teach Surf"), self.player) and
                self.has_badge_requirement(state, "Surf"))

    def can_strength(self, state: CollectionState) -> bool:
        return (state.has_all(("HM04 Strength", "TM Case", "Teach Strength"), self.player) and
                self.has_badge_requirement(state, "Strength"))

    def can_flash(self, state: CollectionState) -> bool:
        return (state.has_all(("HM05 Flash", "TM Case", "Teach Flash"), self.player) and
                self.has_badge_requirement(state, "Flash"))

    def can_rock_smash(self, state: CollectionState) -> bool:
        return (state.has_all(("HM06 Rock Smash", "TM Case", "Teach Rock Smash"), self.player) and
                self.has_badge_requirement(state, "Rock Smash"))

    def can_waterfall(self, state: CollectionState) -> bool:
        return (state.has_all(("HM07 Waterfall", "TM Case", "Teach Waterfall"), self.player) and
                self.has_badge_requirement(state, "Waterfall"))

    def has_n_badges(self, state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique(BADGES, self.player, n)

    def has_n_gyms(self, state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique(GYMS, self.player, n)

    def has_pokemon(self, state: CollectionState, pokemon: str) -> bool:
        return state.has_any(self.dexsanity_state_item_names_lookup[pokemon], self.player)

    def has_pokemon_for_evolution(self, state: CollectionState, pokemon: str) -> bool:
        return state.has_any(self.evolution_state_item_names_lookup[pokemon], self.player)

    def has_n_pokemon(self, state: CollectionState, n: int) -> bool:
        if n <= 0:
            return True
        player = self.player
        for species_item_names in self.oaks_aides_species_item_names:
            # There are multiple item names for a species that can provide Pokédex progress for that species.
            if state.has_any(species_item_names, player):
                # Subtraction is used to make use of a common programming performance 'trick' where, comparing two
                # variables, e.g. `if count == n`, can be replaced with comparing a variable and a constant, e.g.
                # `if n == 0`.
                n -= 1
                # Further minor optimisation of `if n == 0` -> `if not n`
                if not n:
                    return True
        return False

    def has_trade_pokemon(self, state: CollectionState, location_name: str) -> bool:
        return state.has(self.required_trade_pokemon[location_name], self.player)

    def can_show_selphy_pokemon(self, state: CollectionState) -> bool:
        return state.has_all(("Rescue Selphy", data.species[self.resort_gorgeous_pokemon].name), self.player)

    def has_island_pass(self, state: CollectionState, group: int) -> bool:
        return state.has(ISLAND_PASSES[group - 1], self.player) or state.has("Progressive Pass", self.player, group)

    def has_split_island_pass(self, state: CollectionState, island: int) -> bool:
        return (state.has(SPLIT_ISLAND_PASSES[island - 1], self.player)
                or state.has("Progressive Pass", self.player, island))

    def has_card_key(self, state: CollectionState, floor: int) -> bool:
        return (state.has_any(CARD_KEYS_PER_FLOOR[floor], self.player) or
                state.has("Progressive Card Key", self.player, floor - 1))

    def can_stop_seafoam_b3f_current(self, state) -> bool:
        return self.can_strength(state) and state.can_reach_region("Seafoam Islands 1F", self.player)

    def can_stop_seafoam_b4f_current(self, state: CollectionState) -> bool:
        return self.can_strength(state) and state.can_reach_region("Seafoam Islands B3F Southwest", self.player)

    def can_turn_in_meteorite(self, state: CollectionState) -> bool:
        return state.has_all(("Rescue Lostelle", "Meteorite"), self.player)

    def can_turn_in_ruby(self, state: CollectionState) -> bool:
        return state.has_all(("Deliver Meteorite", "Ruby"), self.player)

    def can_turn_in_sapphire(self, state: CollectionState) -> bool:
        return state.has_all(("Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"), self.player)

    def has_lorelei_returned(self, state: CollectionState) -> bool:
        return state.has_all(("Defeat Champion", "Restore Pokemon Network Machine"), self.player)

    def two_island_stall_expansion(self, state: CollectionState, expansion_level: int) -> bool:
        if expansion_level == 1:
            return state.has("Rescue Lostelle", self.player)
        elif expansion_level == 2:
            return state.has_all(("Rescue Lostelle", "Defeat Champion"), self.player)
        elif expansion_level == 3:
            return state.has_all(("Rescue Lostelle", "Defeat Champion", "Restore Pokemon Network Machine"), self.player)
        return False

    def update_species(self, world: "PokemonFRLGWorld"):
        """
        Update available species items used in logic for oak's aide, dexsanity and pokemon request locations, for the
        wild/static/legendary/evolution pokemon events that exist in the world.
        """
        pokemon_event_categories = {
            LocationCategory.EVENT_WILD_POKEMON,
            LocationCategory.EVENT_STATIC_POKEMON,
            LocationCategory.EVENT_LEGENDARY_POKEMON,
            LocationCategory.EVENT_EVOLUTION_POKEMON,
        }

        pokemon_events_that_exist = [location for location
                                     in cast(Iterable[PokemonFRLGLocation], world.get_locations())
                                     if location.category in pokemon_event_categories and location.advancement]
        assert pokemon_events_that_exist

        if not self.oaks_aides_require_evos:
            # Filter out evolutions.
            evolution_category = LocationCategory.EVENT_EVOLUTION_POKEMON
            oaks_aide_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist
                                                      if location.category is not evolution_category}
        else:
            oaks_aide_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        if not self.dexsanity_requires_evos:
            # Filter out evolutions.
            evolution_category = LocationCategory.EVENT_EVOLUTION_POKEMON
            dexsanity_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist
                                                      if location.category is not evolution_category}
        else:
            dexsanity_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        evolution_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        oaks_aides_species_item_names = []
        dexsanity_state_item_names = {}
        evolution_state_item_names = {}
        for species in data.species.values():
            species_name = species.name
            static_species_name = f"Static {species_name}"
            evolved_species_name = f"Evolved {species_name}"

            oaks_aide_item_names = []
            dexsanity_item_names = []
            for name in (species_name, static_species_name, evolved_species_name):
                if name in oaks_aide_relevant_pokemon_event_names:
                    oaks_aide_item_names.append(name)
                if name in dexsanity_relevant_pokemon_event_names:
                    dexsanity_item_names.append(name)

            if oaks_aide_item_names:
                oaks_aides_species_item_names.append(tuple(oaks_aide_item_names))

            dexsanity_state_item_names[species_name] = tuple(dexsanity_item_names)

            evolution_item_names = []
            for name in (species_name, evolved_species_name):
                if name in evolution_relevant_pokemon_event_names:
                    evolution_item_names.append(name)

            evolution_state_item_names[species_name] = tuple(evolution_item_names)

        self.oaks_aides_species_item_names[:] = oaks_aides_species_item_names
        self.dexsanity_state_item_names_lookup.update(dexsanity_state_item_names)
        self.evolution_state_item_names_lookup.update(evolution_state_item_names)


def set_logic_options(world: "PokemonFRLGWorld") -> None:
    logic = world.logic

    for hm, badge in BADGE_REQUIREMENTS.items():
        logic.badge_required[hm] = hm not in world.options.remove_badge_requirement.value

    logic.dexsanity_requires_evos = "Dexsanity" in world.options.evolutions_required.value
    logic.hms_require_evos = "HM Requirement" in world.options.evolutions_required.value
    logic.oaks_aides_require_evos = "Oak's Aides" in world.options.evolutions_required.value

    # Until locations have been created, assume all pokemon species are present in the world.
    dexsanity_state_item_names = {}
    oaks_aides_species_item_names = []
    evolution_state_item_names = {}
    for species in data.species.values():
        species_name = species.name

        if logic.dexsanity_requires_evos and species.pre_evolution is not None:
            state_item_names = (species_name, f"Static {species_name}", f"Evolved {species_name}")
        else:
            state_item_names = (species_name, f"Static {species_name}")
        dexsanity_state_item_names[species_name] = state_item_names

        if logic.oaks_aides_require_evos and species.pre_evolution is not None:
            oaks_aide_item_names = (species_name, f"Static {species_name}", f"Evolved {species_name}")
        else:
            oaks_aide_item_names = (species_name, f"Static {species_name}")
        oaks_aides_species_item_names.append(oaks_aide_item_names)

        evolution_item_names = (species_name, f"Evolved {species_name}")
        evolution_state_item_names[species_name] = evolution_item_names

    logic.dexsanity_state_item_names_lookup.update(dexsanity_state_item_names)
    logic.oaks_aides_species_item_names[:] = oaks_aides_species_item_names
    logic.evolution_state_item_names_lookup.update(evolution_state_item_names)

    if "Level" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_LEVEL)
    if "Level Tyrogue" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_TYROGUE_LEVEL)
    if "Level Wurmple" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_WURMPLE_LEVEL)
    if "Evo Item" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_ITEM)
    if "Evo & Held Item" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_HELD_ITEM)
    if "Friendship" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_FRIENDSHIP)


def set_entrance_rules(world: "PokemonFRLGWorld") -> None:
    def add_rule_safe(entrance_name: str, rule: CollectionRule) -> None:
        try:
            entrance = world.get_entrance(entrance_name)
        except KeyError:
            return
        add_rule(entrance, rule)

    logic = world.logic
    player = world.player
    options = world.options

    # Sky
    add_rule_safe("Flying",
                  lambda state: logic.can_fly(state))
    add_rule_safe("Pallet Town Fly Destination",
                  lambda state: state.has("Fly Unlock (Pallet Town)", player))
    add_rule_safe("Viridian City Fly Destination",
                  lambda state: state.has("Fly Unlock (Viridian City)", player))
    add_rule_safe("Pewter City Fly Destination",
                  lambda state: state.has("Fly Unlock (Pewter City)", player))
    add_rule_safe("Route 4 Fly Destination",
                  lambda state: state.has("Fly Unlock (Route 4)", player))
    add_rule_safe("Cerulean City Fly Destination",
                  lambda state: state.has("Fly Unlock (Cerulean City)", player))
    add_rule_safe("Vermilion City Fly Destination",
                  lambda state: state.has("Fly Unlock (Vermilion City)", player))
    add_rule_safe("Route 10 Fly Destination",
                  lambda state: state.has("Fly Unlock (Route 10)", player))
    add_rule_safe("Lavender Town Fly Destination",
                  lambda state: state.has("Fly Unlock (Lavender Town)", player))
    add_rule_safe("Celadon City Fly Destination",
                  lambda state: state.has("Fly Unlock (Celadon City)", player))
    add_rule_safe("Fuchsia City Fly Destination",
                  lambda state: state.has("Fly Unlock (Fuchsia City)", player))
    add_rule_safe("Saffron City Fly Destination",
                  lambda state: state.has("Fly Unlock (Saffron City)", player))
    add_rule_safe("Cinnabar Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Cinnabar Island)", player))
    add_rule_safe("Indigo Plateau Fly Destination",
                  lambda state: state.has("Fly Unlock (Indigo Plateau)", player))
    add_rule_safe("One Island Fly Destination",
                  lambda state: state.has("Fly Unlock (One Island)", player))
    add_rule_safe("Two Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Two Island)", player))
    add_rule_safe("Three Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Three Island)", player))
    add_rule_safe("Four Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Four Island)", player))
    add_rule_safe("Five Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Five Island)", player))
    add_rule_safe("Six Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Six Island)", player))
    add_rule_safe("Seven Island Fly Destination",
                  lambda state: state.has("Fly Unlock (Seven Island)", player))

    # Seagallop
    if "Block Vermilion Sailing" in options.modify_world_state.value:
        add_rule_safe("Vermilion City Arrival",
                      lambda state: state.has("S.S. Ticket", player))
    if options.island_passes.value in {IslandPasses.option_vanilla, IslandPasses.option_progressive}:
        add_rule_safe("One Island Arrival",
                      lambda state: logic.has_island_pass(state, 1))
        add_rule_safe("Two Island Arrival",
                      lambda state: logic.has_island_pass(state, 1))
        add_rule_safe("Three Island Arrival",
                      lambda state: logic.has_island_pass(state, 1))
        add_rule_safe("Four Island Arrival",
                      lambda state: logic.has_island_pass(state, 2))
        add_rule_safe("Five Island Arrival",
                      lambda state: logic.has_island_pass(state, 2))
        add_rule_safe("Six Island Arrival",
                      lambda state: logic.has_island_pass(state, 2))
        add_rule_safe("Seven Island Arrival",
                      lambda state: logic.has_island_pass(state, 2))
    elif options.island_passes.value in {IslandPasses.option_split, IslandPasses.option_progressive_split}:
        add_rule_safe("One Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 1))
        add_rule_safe("Two Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 2))
        add_rule_safe("Three Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 3))
        add_rule_safe("Four Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 4))
        add_rule_safe("Five Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 5))
        add_rule_safe("Six Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 6))
        add_rule_safe("Seven Island Arrival",
                      lambda state: logic.has_split_island_pass(state, 7))
    add_rule_safe("Navel Rock Arrival",
                  lambda state: state.has("Mystic Ticket", player) and
                                state.can_reach_region("Vermilion City", player))
    add_rule_safe("Birth Island Arrival",
                  lambda state: state.has("Aurora Ticket", player) and
                                state.can_reach_region("Vermilion City", player))

    # Pallet Town
    add_rule_safe("Pallet Town Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Viridian City
    if options.viridian_city_roadblock != ViridianCityRoadblock.option_open:
        add_rule_safe("Viridian City South Roadblock",
                      lambda state: state.has("Deliver Oak's Parcel", player) or
                                    logic.can_cut(state))
    add_rule_safe("Viridian City South Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.viridian_gym_requirement.value == ViridianGymRequirement.option_badges:
        add_rule_safe("Viridian Gym",
                      lambda state: logic.has_n_badges(state, options.viridian_gym_count.value))
    elif options.viridian_gym_requirement.value == ViridianGymRequirement.option_gyms:
        add_rule_safe("Viridian Gym",
                      lambda state: logic.has_n_gyms(state, options.viridian_gym_count.value))
    if options.gym_keys:
        add_rule_safe("Viridian Gym",
                      lambda state: state.has("Viridian Key", player))

    # Route 22
    add_rule_safe("Route 22 Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.route22_gate_requirement.value == Route22GateRequirement.option_badges:
        add_rule_safe("Route 22 Gate Exit (North)",
                      lambda state: logic.has_n_badges(state, options.route22_gate_count.value))
    elif options.route22_gate_requirement.value == Route22GateRequirement.option_gyms:
        add_rule_safe("Route 22 Gate Exit (North)",
                      lambda state: logic.has_n_gyms(state, options.route22_gate_count.value))

    # Route 2
    add_rule_safe("Route 2 Southwest Cuttable Trees",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 2 Southeast Cuttable Trees",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 2 East Cuttable Tree",
                  lambda state: logic.can_cut(state))
    if "Modify Route 2" in options.modify_world_state.value:
        add_rule_safe("Route 2 Northwest Smashable Rock",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 2 Northeast Smashable Rock",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 2 Northeast Cuttable Tree",
                      lambda state: logic.can_cut(state))
    else:
        add_rule_safe("Route 2 Northwest Cuttable Tree",
                      lambda state: logic.can_cut(state))
        add_rule_safe("Route 2 Northeast Cuttable Tree (North)",
                      lambda state: logic.can_cut(state))
        add_rule_safe("Route 2 Northeast Cuttable Tree (South)",
                      lambda state: logic.can_cut(state))

    # Pewter City
    add_rule_safe("Pewter City Cuttable Tree",
                  lambda state: logic.can_cut(state))
    if options.pewter_city_roadblock.value == PewterCityRoadblock.option_brock:
        add_rule_safe("Pewter City Exit (East)",
                      lambda state: state.has("Defeat Brock", player))
    elif options.pewter_city_roadblock.value == PewterCityRoadblock.option_any_gym:
        add_rule_safe("Pewter City Exit (East)",
                      lambda state: logic.has_n_gyms(state, 1))
    elif options.pewter_city_roadblock.value == PewterCityRoadblock.option_boulder_badge:
        add_rule_safe("Pewter City Exit (East)",
                      lambda state: state.has("Boulder Badge", player))
    elif options.pewter_city_roadblock.value == PewterCityRoadblock.option_any_badge:
        add_rule_safe("Pewter City Exit (East)",
                      lambda state: logic.has_n_badges(state, 1))
    if options.gym_keys:
        add_rule_safe("Pewter Gym",
                      lambda state: state.has("Pewter Key", player))

    # Cerulean City
    add_rule_safe("Cerulean City Cuttable Tree",
                  lambda state: logic.can_cut(state))
    if "Remove Cerulean Roadblocks" not in options.modify_world_state.value:
        add_rule_safe("Cerulean City Cuttable Tree",
                      lambda state: state.has("Help Bill", player))
        add_rule_safe("Robbed House (Front)",
                      lambda state: state.has("Help Bill", player))
    if options.gym_keys:
        add_rule_safe("Cerulean Gym",
                      lambda state: state.has("Cerulean Key", player))
    if "Modify Route 9" in options.modify_world_state.value:
        add_rule_safe("Cerulean City Outskirts Exit (East)",
                      lambda state: logic.can_rock_smash(state))
    else:
        add_rule_safe("Cerulean City Outskirts Exit (East)",
                      lambda state: logic.can_cut(state))
    add_rule_safe("Cerulean City Near Cave Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_vanilla:
        add_rule_safe("Cerulean Cave",
                      lambda state: logic.has_lorelei_returned(state))
    elif options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_champion:
        add_rule_safe("Cerulean Cave",
                      lambda state: state.has("Defeat Champion", player))
    elif options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_restore_network:
        add_rule_safe("Cerulean Cave",
                      lambda state: state.has("Restore Pokemon Network Machine", player))
    elif options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_badges:
        add_rule_safe("Cerulean Cave",
                      lambda state: logic.has_n_badges(state, options.cerulean_cave_count.value))
    elif options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_gyms:
        add_rule_safe("Cerulean Cave",
                      lambda state: logic.has_n_gyms(state, options.cerulean_cave_count.value))

    # Route 24
    add_rule_safe("Route 24 Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Route 25
    add_rule_safe("Route 25 Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Route 5
    add_rule_safe("Route 5 Gate North Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Blue Tea"), player))
    add_rule_safe("Route 5 Gate South Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Blue Tea"), player))
    if "Block Tunnels" in options.modify_world_state.value:
        add_rule_safe("Route 5 Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 5 Near Tunnel Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))

    # Route 6
    add_rule_safe("Route 6 Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 6 Gate South Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Red Tea"), player))
    add_rule_safe("Route 6 Gate North Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Red Tea"), player))
    if "Block Tunnels" in options.modify_world_state.value:
        add_rule_safe("Route 6 Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 6 Near Tunnel Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))

    # Vermilion City
    add_rule_safe("Vermilion City Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Vermilion City Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Vermilion City Checkpoint",
                  lambda state: state.has("S.S. Ticket", player))
    add_rule_safe("Vermilion City Near Gym Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Vermilion City Near Gym Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.gym_keys:
        add_rule_safe("Vermilion Gym",
                      lambda state: state.has("Vermilion Key", player))

    # S.S. Anne
    add_rule_safe("S.S. Anne Exterior Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Route 11
    add_rule_safe("Route 11 West Surfing Spot",
                  lambda state: logic.can_surf(state))
    if "Route 12 Boulders" in options.modify_world_state.value:
        add_rule_safe("Route 11 East Exit",
                      lambda state: logic.can_strength(state))

    # Route 9
    if "Modify Route 9" in options.modify_world_state.value:
        add_rule_safe("Route 9 Exit (West)",
                      lambda state: logic.can_rock_smash(state))
    else:
        add_rule_safe("Route 9 Exit (West)",
                      lambda state: logic.can_cut(state))

    # Route 10
    add_rule_safe("Route 10 North Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 10 Near Power Plant Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.extra_key_items:
        add_rule_safe("Power Plant (Front)",
                      lambda state: state.has("Machine Part", player))
    add_rule_safe("Route 10 Waterfall Drop",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Route 10 Waterfall Ascend",
                  lambda state: logic.can_waterfall(state))
    if "Modify Route 10" in options.modify_world_state.value:
        add_rule_safe("Route 10 South Surfing Spot",
                      lambda state: logic.can_surf(state))
    else:
        add_rule_safe("Route 10 South Surfing Spot",
                      lambda state: False)
        add_rule_safe("Route 10 South Landing",
                      lambda state: False)
        add_rule_safe("Route 10 South (Fishing Battle)",
                      lambda state: False)

    # Lavender Town
    if "Route 12 Boulders" in options.modify_world_state.value:
        add_rule_safe("Lavender Town Exit (South)",
                      lambda state: logic.can_strength(state))

    # Route 8
    add_rule_safe("Route 8 Cuttable Trees",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 8 Gate East Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Purple Tea"), player))
    add_rule_safe("Route 8 Gate West Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Purple Tea"), player))
    if "Block Tunnels" in options.modify_world_state.value:
        add_rule_safe("Route 8 Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 8 Near Tunnel Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))

    # Route 7
    add_rule_safe("Route 7 Gate West Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Green Tea"), player))
    add_rule_safe("Route 7 Gate East Guard Checkpoint",
                  lambda state: state.has_any(("Tea", "Green Tea"), player))
    if "Block Tunnels" in options.modify_world_state.value:
        add_rule_safe("Route 7 Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 7 Near Tunnel Smashable Rocks",
                      lambda state: logic.can_rock_smash(state))

    # Celadon City
    add_rule_safe("Celadon City Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Celadon City Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Celadon City Near Gym Cuttable Tree",
                  lambda state: logic.can_cut(state))
    if options.gym_keys:
        add_rule_safe("Celadon Gym",
                      lambda state: state.has("Celadon Key", player))
    if options.extra_key_items:
        add_rule_safe("Rocket Hideout",
                      lambda state: state.has("Hideout Key", player))
    add_rule_safe("Celadon Gym Cuttable Trees",
                  lambda state: logic.can_cut(state))

    # Rocket Hideout
    add_rule_safe("Rocket Hideout Elevator B1F Stop",
                  lambda state: state.has("Lift Key", player))
    add_rule_safe("Rocket Hideout Elevator B2F Stop",
                  lambda state: state.has("Lift Key", player))
    add_rule_safe("Rocket Hideout Elevator B4F Stop",
                  lambda state: state.has("Lift Key", player))

    # Pokemon Tower
    if "Block Tower" in options.modify_world_state.value:
        add_rule_safe("Pokemon Tower 1F Reveal Ghost",
                      lambda state: state.has("Silph Scope", player))
        add_rule_safe("Pokemon Tower 1F (Ghost Battle)",
                      lambda state: state.has("Silph Scope", player))
    else:
        add_rule_safe("Pokemon Tower 1F (Ghost Battle)",
                      lambda state: False)
    add_rule_safe("Pokemon Tower 6F Reveal Ghost",
                  lambda state: state.has("Silph Scope", player))
    add_rule_safe("Pokemon Tower 6F (Ghost Battle)",
                  lambda state: state.has("Silph Scope", player))
    add_rule_safe("Follow Mr. Fuji",
                  lambda state: state.has("Rescue Mr. Fuji", player))

    # Route 12
    if "Route 12 Boulders" in options.modify_world_state.value:
        add_rule_safe("Route 12 West Exit",
                      lambda state: logic.can_strength(state))
        add_rule_safe("Route 12 North Exit",
                      lambda state: logic.can_strength(state))
        add_rule_safe("Route 12 South Exit",
                      lambda state: logic.can_strength(state))
    add_rule_safe("Route 12 West Play Poke Flute",
                  lambda state: state.has("Poke Flute", player))
    add_rule_safe("Route 12 North Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 12 Center Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 12 Center Play Poke Flute",
                  lambda state: state.has("Poke Flute", player))
    add_rule_safe("Route 12 South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 12 South Cuttable Tree (North)",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 12 South Cuttable Tree (South)",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 12 South Play Poke Flute",
                  lambda state: state.has("Poke Flute", player))
    if "Modify Route 12" in options.modify_world_state.value:
        add_rule_safe("Route 12 Center Water Unobstructed Path",
                      lambda state: False)
        add_rule_safe("Route 12 South Water Unobstructed Path",
                      lambda state: False)

    # Route 13
    if "Route 12 Boulders" in options.modify_world_state.value:
        add_rule_safe("Route 13 Exit (East)",
                      lambda state: logic.can_strength(state))
    add_rule_safe("Route 13 Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 13 Cuttable Tree",
                  lambda state: logic.can_cut(state))

    # Route 14
    add_rule_safe("Route 14 Cuttable Tree (North)",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 14 Cuttable Tree (South)",
                  lambda state: logic.can_cut(state))

    # Route 16
    add_rule_safe("Route 16 Southeast Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 16 Southeast Play Poke Flute",
                  lambda state: state.has("Poke Flute", player))
    add_rule_safe("Route 16 Northeast Cuttable Tree",
                  lambda state: logic.can_cut(state))
    if "Modify Route 16" in options.modify_world_state.value:
        add_rule_safe("Route 16 Northeast Smashable Rock",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Route 16 Center Smashable Rock",
                      lambda state: logic.can_rock_smash(state))
    else:
        add_rule_safe("Route 16 Northeast Smashable Rock",
                      lambda state: False)
        add_rule_safe("Route 16 Center Smashable Rock",
                      lambda state: False)
    add_rule_safe("Route 16 Center Play Poke Flute",
                  lambda state: state.has("Poke Flute", player)),
    add_rule_safe("Route 16 Gate 1F Southeast Bike Checkpoint",
                  lambda state: state.has("Bicycle", player))

    # Route 18
    add_rule_safe("Route 18 Gate 1F East Bike Checkpoint",
                  lambda state: state.has("Bicycle", player))

    # Fuchsia City
    if options.gym_keys:
        add_rule_safe("Fuchsia Gym",
                      lambda state: state.has("Fuchsia Key", player))
    add_rule_safe("Fuchsia City Backyard Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.extra_key_items:
        add_rule_safe("Safari Zone",
                      lambda state: state.has("Safari Pass", player))

    # Safari Zone
    add_rule_safe("Safari Zone Center Area South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone Center Area Northwest Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone Center Area Northeast Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone East Area Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone North Area Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone West Area North Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Safari Zone West Area South Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Saffron City
    if "Remove Saffron Rockets" not in options.modify_world_state.value:
        if "Open Silph" not in options.modify_world_state.value:
            add_rule_safe("Silph Co.",
                          lambda state: state.has_any(("Rescue Mr. Fuji", "Liberate Silph Co."), player))
        add_rule_safe("Copycat's House",
                      lambda state: state.has("Liberate Silph Co.", player))
        add_rule_safe("Saffron Gym",
                      lambda state: state.has("Liberate Silph Co.", player))
        add_rule_safe("Saffron Pidgey House",
                      lambda state: state.has("Liberate Silph Co.", player))
    if options.gym_keys:
        add_rule_safe("Saffron Gym",
                      lambda state: state.has("Saffron Key", player))

    # Silph Co.
    add_rule_safe("Silph Co. 2F Barrier (Northwest)",
                  lambda state: logic.has_card_key(state, 2))
    add_rule_safe("Silph Co. 2F Barrier (Southwest)",
                  lambda state: logic.has_card_key(state, 2))
    add_rule_safe("Silph Co. 2F Northwest Room Barrier",
                  lambda state: logic.has_card_key(state, 2))
    add_rule_safe("Silph Co. 2F Southwest Room Barrier",
                  lambda state: logic.has_card_key(state, 2))
    add_rule_safe("Silph Co. 3F Barrier",
                  lambda state: logic.has_card_key(state, 3))
    add_rule_safe("Silph Co. 3F Center Room Barrier (East)",
                  lambda state: logic.has_card_key(state, 3))
    add_rule_safe("Silph Co. 3F Center Room Barrier (West)",
                  lambda state: logic.has_card_key(state, 3))
    add_rule_safe("Silph Co. 3F West Room Barrier",
                  lambda state: logic.has_card_key(state, 3))
    add_rule_safe("Silph Co. 4F Barrier (West)",
                  lambda state: logic.has_card_key(state, 4))
    add_rule_safe("Silph Co. 4F Barrier (Center)",
                  lambda state: logic.has_card_key(state, 4))
    add_rule_safe("Silph Co. 4F North Room Barrier",
                  lambda state: logic.has_card_key(state, 4))
    add_rule_safe("Silph Co. 5F Barrier (Northwest)",
                  lambda state: logic.has_card_key(state, 5))
    add_rule_safe("Silph Co. 5F Barrier (Center)",
                  lambda state: logic.has_card_key(state, 5))
    add_rule_safe("Silph Co. 5F Barrier (Southwest)",
                  lambda state: logic.has_card_key(state, 5))
    add_rule_safe("Silph Co. 5F Southwest Room Barrier",
                  lambda state: logic.has_card_key(state, 5))
    add_rule_safe("Silph Co. 6F Barrier",
                  lambda state: logic.has_card_key(state, 6))
    add_rule_safe("Silph Co. 7F Barrier (Center)",
                  lambda state: logic.has_card_key(state, 7))
    add_rule_safe("Silph Co. 7F Barrier (East)",
                  lambda state: logic.has_card_key(state, 7))
    add_rule_safe("Silph Co. 7F East Room Barrier (North)",
                  lambda state: logic.has_card_key(state, 7))
    add_rule_safe("Silph Co. 7F East Room Barrier (South)",
                  lambda state: logic.has_card_key(state, 7))
    add_rule_safe("Silph Co. 7F Southeast Room Barrier",
                  lambda state: logic.has_card_key(state, 7))
    add_rule_safe("Silph Co. 8F Barrier",
                  lambda state: logic.has_card_key(state, 8))
    add_rule_safe("Silph Co. 8F West Room Barrier",
                  lambda state: logic.has_card_key(state, 8))
    add_rule_safe("Silph Co. 9F Barrier",
                  lambda state: logic.has_card_key(state, 9))
    add_rule_safe("Silph Co. 9F Northwest Room Barrier",
                  lambda state: logic.has_card_key(state, 9))
    add_rule_safe("Silph Co. 9F Southwest Room Barrier (East)",
                  lambda state: logic.has_card_key(state, 9))
    add_rule_safe("Silph Co. 9F Southwest Room Barrier (West)",
                  lambda state: logic.has_card_key(state, 9))
    add_rule_safe("Silph Co. 10F Barrier",
                  lambda state: logic.has_card_key(state, 10))
    add_rule_safe("Silph Co. 10F Southeast Room Barrier",
                  lambda state: logic.has_card_key(state, 10))
    add_rule_safe("Silph Co. 11F West Barrier",
                  lambda state: logic.has_card_key(state, 11))

    # Route 19
    add_rule_safe("Route 19 Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Route 20
    add_rule_safe("Route 20 Near North Cave Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 20 Near South Cave Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Seafoam Islands
    add_rule_safe("Seafoam Islands B3F Southwest Surfing Spot",
                  lambda state: logic.can_surf(state) and
                                logic.can_stop_seafoam_b3f_current(state))
    add_rule_safe("Seafoam Islands B3F Southwest Landing",
                  lambda state: logic.can_stop_seafoam_b3f_current(state))
    add_rule_safe("Seafoam Islands B3F South Water (Water Battle)",
                  lambda state: logic.can_stop_seafoam_b3f_current(state))
    add_rule_safe("Seafoam Islands B3F East Landing (South)",
                  lambda state: logic.can_stop_seafoam_b3f_current(state))
    add_rule_safe("Seafoam Islands B3F East Surfing Spot (South)",
                  lambda state: logic.can_surf(state) and
                                logic.can_stop_seafoam_b3f_current(state))
    add_rule_safe("Seafoam Islands B3F East Surfing Spot (North)",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Seafoam Islands B3F Waterfall Ascend (Northeast)",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Seafoam Islands B3F Waterfall Drop (Northeast)",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Seafoam Islands B3F Waterfall Drop (Northwest)",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Seafoam Islands B3F Waterfall Ascend (Northwest)",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Seafoam Islands B3F Northwest Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Seafoam Islands B4F Surfing Spot (West)",
                  lambda state: logic.can_surf(state) and
                                logic.can_stop_seafoam_b4f_current(state))
    add_rule_safe("Seafoam Islands B4F Near Articuno Landing",
                  lambda state: logic.can_stop_seafoam_b4f_current(state))

    # Cinnabar Island
    add_rule_safe("Cinnabar Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    if options.gym_keys:
        add_rule_safe("Cinnabar Gym",
                      lambda state: state.has("Cinnabar Key", player))
    else:
        add_rule_safe("Cinnabar Gym",
                      lambda state: state.has("Secret Key", player))
    if options.extra_key_items:
        add_rule_safe("Pokemon Mansion",
                      lambda state: state.has("Letter", player))
    add_rule_safe("Follow Bill",
                  lambda state: state.has("Defeat Blaine", player))
    add_rule_safe("Pokemon Mansion 1F Southeast Exit",
                  lambda state: not logic.randomizing_entrances)

    # Route 23
    add_rule_safe("Route 23 South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Route 23 Near Water Surfing Spot",
                  lambda state: logic.can_surf(state))
    if "Route 23 Trees" in options.modify_world_state.value:
        add_rule_safe("Route 23 Near Water Cuttable Trees",
                      lambda state: logic.can_cut(state))
        add_rule_safe("Route 23 Center Cuttable Trees",
                      lambda state: logic.can_cut(state))
    if "Modify Route 23" in options.modify_world_state.value:
        add_rule_safe("Route 23 Waterfall Ascend",
                      lambda state: logic.can_waterfall(state))
        add_rule_safe("Route 23 Waterfall Drop",
                      lambda state: logic.can_waterfall(state))
    if options.route23_guard_requirement.value == Route23GuardRequirement.option_badges:
        add_rule_safe("Route 23 Center Guard Checkpoint",
                      lambda state: logic.has_n_badges(state, options.route23_guard_count.value))
    elif options.route23_guard_requirement.value == Route23GuardRequirement.option_gyms:
        add_rule_safe("Route 23 Center Guard Checkpoint",
                      lambda state: logic.has_n_gyms(state, options.route23_guard_count.value))

    # Victory Road
    add_rule_safe("Victory Road 1F South Rock Barrier",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 1F North Strength Boulder",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 2F Southwest Rock Barrier",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 2F Center Rock Barrier",
                  lambda state: logic.can_strength(state) and
                                state.can_reach_region("Victory Road 3F Southwest", player))
    add_rule_safe("Victory Road 2F Northwest Strength Boulder",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 3F North Rock Barrier",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 3F Southwest Strength Boulder",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 3F Southeast Strength Boulder",
                  lambda state: logic.can_strength(state))
    if "Victory Road Rocks" in options.modify_world_state.value:
        add_rule_safe("Victory Road 1F South Rock Barrier",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Victory Road 2F Southwest Rock Barrier",
                      lambda state: logic.can_rock_smash(state))
        add_rule_safe("Victory Road 3F North Rock Barrier",
                      lambda state: logic.can_rock_smash(state))

    # Indigo Plateau
    if options.elite_four_requirement.value == EliteFourRequirement.option_badges:
        add_rule_safe("Pokemon League",
                      lambda state: logic.has_n_badges(state, options.elite_four_count.value))
    elif options.elite_four_requirement.value == EliteFourRequirement.option_gyms:
        add_rule_safe("Pokemon League",
                      lambda state: logic.has_n_gyms(state, options.elite_four_count.value))

    # One Island Town
    add_rule_safe("One Island Town Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Kindle Road
    add_rule_safe("Kindle Road South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Kindle Road Center Surfing Spot (South)",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Kindle Road Center Surfing Spot (North)",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Kindle Road North Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Mt. Ember
    add_rule_safe("Mt. Ember Exterior South Strength Boulders",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Mt. Ember Ruby Path B2F West Strength Boulders",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B2F East Strength Boulders",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southwest)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southeast)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Northwest)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Southeast)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Northwest)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Southwest)",
                  lambda state: logic.can_strength(state))

    # Cape Brink
    add_rule_safe("Cape Brink Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Bond Bridge
    add_rule_safe("Bond Bridge Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Berry Forest
    add_rule_safe("Berry Forest Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Follow Lostelle",
                  lambda state: state.has("Rescue Lostelle", player))

    # Four Island Town
    add_rule_safe("Four Island Town Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Four Island Town Near Cave Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Icefall Cave
    add_rule_safe("Icefall Cave Front South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Icefall Cave Front Waterfall Ascend",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Icefall Cave Front Waterfall Drop",
                  lambda state: logic.can_waterfall(state))
    add_rule_safe("Icefall Cave Front Center Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Icefall Cave Front North Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Icefall Cave Back Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Five Island Town
    add_rule_safe("Five Island Town Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Five Isle Meadow
    add_rule_safe("Five Isle Meadow Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Rocket Warehouse",
                  lambda state: state.has_all(("Learn Goldeen Need Log", "Learn Yes Nah Chansey"), player))

    # Resort Gorgeous
    add_rule_safe("Resort Gorgeous Near Resort Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Resort Gorgeous Near Cave Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Lost Cave
    add_rule_safe("Follow Selphy",
                  lambda state: state.has("Rescue Selphy", player))

    # Water Path
    add_rule_safe("Water Path South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Water Path North Surfing Spot (South)",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Water Path North Surfing Spot (North)",
                  lambda state: logic.can_surf(state))

    # Ruin Valley
    add_rule_safe("Ruin Valley Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Dotted Hole",
                  lambda state: state.has("Help Lorelei", player) and
                                logic.can_cut(state))

    # Green Path
    add_rule_safe("Green Path West Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Outcast Island
    add_rule_safe("Outcast Island Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Tanoby Ruins
    add_rule_safe("Tanoby Ruins Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Monean Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Liptoo Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Weepth Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Dilford Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Scufib Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Rixy Island Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Tanoby Ruins Viapois Island Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Monean Chamber
    add_rule_safe("Monean Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Liptoo Chamber
    add_rule_safe("Liptoo Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Weepth Chamber
    add_rule_safe("Weepth Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Dilford Chamber
    add_rule_safe("Dilford Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Scufib Chamber
    add_rule_safe("Scufib Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Rixy Chamber
    add_rule_safe("Rixy Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Viapois Chamber
    add_rule_safe("Viapois Chamber (Land Battle)",
                  lambda state: state.has("Unlock Ruins", player))

    # Trainer Tower
    add_rule_safe("Trainer Tower Exterior South Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Trainer Tower Exterior North Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Cerulean Cave
    add_rule_safe("Cerulean Cave 1F Southeast Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Cerulean Cave 1F Northeast Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Cerulean Cave 1F Surfing Spot",
                  lambda state: logic.can_surf(state))
    add_rule_safe("Cerulean Cave B1F Surfing Spot",
                  lambda state: logic.can_surf(state))

    # Navel Rock
    if "Block Vermilion Sailing" in options.modify_world_state.value:
        add_rule_safe("Navel Rock Seagallop",
                      lambda state: state.has("S.S. Ticket", player))

    # Birth Island
    if "Block Vermilion Sailing" in options.modify_world_state.value:
        add_rule_safe("Birth Island Seagallop",
                      lambda state: state.has("S.S. Ticket", player))


def set_location_rules(world: "PokemonFRLGWorld") -> None:
    def add_rule_safe(location_name: str, rule: CollectionRule) -> None:
        try:
            location = world.get_location(location_name)
        except KeyError:
            return
        add_rule(location, rule)

    logic = world.logic
    player = world.player
    options = world.options

    # Pallet Town
    add_rule_safe("Rival's House - Daisy Gift",
                  lambda state: state.has("Deliver Oak's Parcel", player))
    add_rule_safe("Professor Oak's Lab - Oak's Delivery",
                  lambda state: state.has("Oak's Parcel", player))
    add_rule_safe("Professor Oak's Lab - Oak Gift (Deliver Parcel)",
                  lambda state: state.has("Oak's Parcel", player))
    add_rule_safe("Professor Oak's Lab - Oak Info",
                  lambda state: state.has("Oak's Parcel", player))
    add_rule_safe("Professor Oak's Lab - Oak Gift (Post Route 22 Rival)",
                  lambda state: state.has("Defeat Route 22 Rival", player))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Professor Oak's Lab - Oak's Aide M Info (Right)",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Professor Oak's Lab - Oak's Aide M Info (Left)",
                      lambda state: state.has("Defeat Champion", player))

    # Viridian City
    if options.viridian_city_roadblock != ViridianCityRoadblock.option_open:
        add_rule_safe("Viridian City - Tutorial Man Gift",
                      lambda state: state.has("Deliver Oak's Parcel", player))
    if options.viridian_gym_requirement.value == ViridianGymRequirement.option_badges:
        add_rule_safe("Viridian City - Old Man Gift",
                      lambda state: logic.has_n_badges(state, options.viridian_gym_count.value))
    elif options.viridian_gym_requirement.value == ViridianGymRequirement.option_gyms:
        add_rule_safe("Viridian City - Old Man Gift",
                      lambda state: logic.has_n_gyms(state, options.viridian_gym_count.value))
    add_rule_safe("Viridian Gym - Hidden Item Under Giovanni",
                  lambda state: state.has("Itemfinder", player))
    add_rule_safe("Viridian Gym - Gym Guy Info",
                  lambda state: state.has("Defeat Giovanni", player))

    # Route 22
    add_rule_safe("Route 22 - Early Rival Battle",
                  lambda state: state.has("Deliver Oak's Parcel", player))
    add_rule_safe("Route 22 - Early Rival Reward",
                  lambda state: state.has("Deliver Oak's Parcel", player))
    add_rule_safe("Route 22 Early Rival Scaling",
                  lambda state: state.has("Deliver Oak's Parcel", player))
    add_rule_safe("Route 22 - Late Rival Reward",
                  lambda state: state.has_all(("Defeat Route 22 Rival", "Defeat Giovanni"), player))
    add_rule_safe("Route 22 Late Rival Scaling",
                  lambda state: state.has_all(("Defeat Route 22 Rival", "Defeat Giovanni"), player))

    # Route 2
    add_rule_safe("Route 2 Gate - Oak's Aide Gift (Pokedex Progress)",
                  lambda state: logic.has_n_pokemon(state, options.oaks_aide_route_2.value))
    add_rule_safe("Route 2 Trade House - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Route 2 Trade House - Trade Pokemon"))

    # Pewter City
    add_rule_safe("Pewter City - Gift from Mom",
                  lambda state: state.has("Defeat Brock", player) and
                                state.can_reach_region("Route 3", player))

    # Cerulean City
    add_rule_safe("Cerulean Trade House - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Cerulean Trade House - Trade Pokemon"))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Cerulean Pokemon Center 1F - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Cerulean Gym - Hidden Item in Water",
                  lambda state: logic.can_surf(state) and state.has("Itemfinder", player))
    add_rule_safe("Bike Shop - Bicycle Purchase",
                  lambda state: state.has("Bike Voucher", player))
    add_rule_safe("Berry Powder Man's House - Berry Powder Man Gift",
                  lambda state: state.has("Berry Pouch", player))

    # Route 25
    add_rule_safe("Route 25 - Item Near Bush",
                  lambda state: logic.can_cut(state))

    # Underground Path North-South Tunnel
    add_rule_safe("Underground Path North Entrance - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Underground Path North Entrance - Trade Pokemon"))

    # Vermilion City
    add_rule_safe("Vermilion Pokemon Center 1F - Bookshelf Info",
                  lambda state: state.has("Defeat Lt. Surge", player))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Pokemon Fan Club - Worker Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Vermilion Trade House - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Vermilion Trade House - Trade Pokemon"))

    # Route 11
    add_rule_safe("Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)",
                  lambda state: logic.has_n_pokemon(state, options.oaks_aide_route_11.value))
    add_rule_safe("Route 11 Gate 2F - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Route 11 Gate 2F - Trade Pokemon"))

    # Route 10
    add_rule_safe("Route 10 - Hidden Item Behind Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)",
                  lambda state: logic.has_n_pokemon(state, options.oaks_aide_route_10.value))

    # Lavender Town
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Lavender Pokemon Center 1F - Balding Man Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Volunteer Pokemon House - Mr. Fuji Gift",
                  lambda state: state.has("Rescue Mr. Fuji", player))

    # Route 8
    add_rule_safe("Route 8 - Twins Eli & Anne Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Celadon City
    add_rule_safe("Celadon Game Corner - Fisherman Gift",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Scientist Gift",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Gentleman Gift",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner Prize Room - Prize Pokemon 1",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner Prize Room - Prize Pokemon 2",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner Prize Room - Prize Pokemon 3",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner Prize Room - Prize Pokemon 4",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner Prize Room - Prize Pokemon 5",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Prize Pokemon 1 Scaling",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Prize Pokemon 2 Scaling",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Prize Pokemon 3 Scaling",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Prize Pokemon 4 Scaling",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Prize Pokemon 5 Scaling",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Northwest Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - North Hidden Item (Left)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - North Hidden Item (Right)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Northeast Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - West Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Center Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - East Hidden Item (Left)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - East Hidden Item (Right)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Southwest Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - South Hidden Item (Left)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - South Hidden Item (Right)",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Game Corner - Southeast Hidden Item",
                  lambda state: state.has("Coin Case", player))
    add_rule_safe("Celadon Condominiums 1F - Brock Gift",
                  lambda state: state.has("Defeat Brock", player))
    add_rule_safe("Celadon Condominiums 1F - Misty Gift",
                  lambda state: state.has("Defeat Misty", player))
    add_rule_safe("Celadon Condominiums 1F - Erika Gift",
                  lambda state: state.has("Defeat Erika", player))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Celadon Condominiums 1F - Tea Woman Info",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Celadon Department Store 2F - Woman Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Celadon Condominiums 2F - Bookshelf Info",
                  lambda state: state.has("Defeat Erika", player))

    # Pokemon Tower
    for i in range(3, 8):
        for j in range(1, 4):
            add_rule_safe(f"Pokemon Tower {i}F - Land Encounter {j}",
                          lambda state: state.has("Silph Scope", player))
    add_rule_safe("Pokemon Tower - Ghost Pokemon",
                  lambda state: state.has("Silph Scope", player))
    add_rule_safe("Static Marowak Scaling",
                  lambda state: state.has("Silph Scope", player))
    add_rule_safe("Pokemon Tower 7F - Hidden Item Under Mr. Fuji",
                  lambda state: state.has("Itemfinder", player))

    # Route 12
    add_rule_safe("Route 12 - Young Couple Gia & Jes Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))
    add_rule_safe("Route 12 - Hidden Item Under Snorlax",
                  lambda state: state.has("Itemfinder", player))
    add_rule_safe("Route 12 Fishing House - Fishing Guru Gift (Show Magikarp)",
                  lambda state: state.has("Magikarp", player))

    # Route 14
    add_rule_safe("Route 14 - Twins Kiri & Jan Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Route 15
    add_rule_safe("Route 15 - Crush Kin Ron & Mya Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))
    add_rule_safe("Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)",
                  lambda state: logic.has_n_pokemon(state, options.oaks_aide_route_15.value))

    # Route 16
    add_rule_safe("Route 16 - Young Couple Lea & Jed Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))
    add_rule_safe("Route 16 - Hidden Item Under Snorlax",
                  lambda state: state.has("Itemfinder", player))
    add_rule_safe("Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)",
                  lambda state: logic.has_n_pokemon(state, options.oaks_aide_route_16.value))

    # Route 18
    add_rule_safe("Route 18 Gate 2F - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Route 18 Gate 2F - Trade Pokemon"))

    # Fuchsia City
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Fuchsia City - Koga's Daughter Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Safari Zone Warden's House - Warden Gift (Return Teeth)",
                  lambda state: state.has("Gold Teeth", player))
    add_rule_safe("Safari Zone Warden's House - Item",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Safari Zone Warden's House - Bookshelf Info",
                  lambda state: state.has("Defeat Koga", player))

    # Saffron City
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Saffron City - Battle Girl Info",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Pokemon Trainer Fan Club - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))
    add_rule_safe("Saffron Pokemon Center 1F - Bookshelf Info",
                  lambda state: state.has("Defeat Sabrina", player))

    # Route 19
    add_rule_safe("Route 19 - Sis and Bro Lia & Luc Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Cinnabar Island
    add_rule_safe("Pokemon Lab Lounge - Trade Pokemon 1",
                  lambda state: logic.has_trade_pokemon(state, "Pokemon Lab Lounge - Trade Pokemon 1"))
    add_rule_safe("Pokemon Lab Lounge - Trade Pokemon 2",
                  lambda state: logic.has_trade_pokemon(state, "Pokemon Lab Lounge - Trade Pokemon 2"))
    add_rule_safe("Pokemon Lab Experiment Room - Trade Pokemon",
                  lambda state: logic.has_trade_pokemon(state, "Pokemon Lab Experiment Room - Trade Pokemon"))
    add_rule_safe("Pokemon Lab Experiment Room - Revive Helix Fossil",
                  lambda state: state.has("Helix Fossil", player))
    add_rule_safe("Gift Omanyte Scaling",
                  lambda state: state.has("Helix Fossil", player))
    add_rule_safe("Pokemon Lab Experiment Room - Revive Dome Fossil",
                  lambda state: state.has("Dome Fossil", player))
    add_rule_safe("Gift Kabuto Scaling",
                  lambda state: state.has("Dome Fossil", player))
    add_rule_safe("Pokemon Lab Experiment Room - Revive Old Amber",
                  lambda state: state.has("Old Amber", player))
    add_rule_safe("Gift Aerodactyl Scaling",
                  lambda state: state.has("Old Amber", player))
    add_rule_safe("Cinnabar Pokemon Center 1F - Bill Gift",
                  lambda state: state.has("Defeat Blaine", player))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Cinnabar Pokemon Center 1F - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))

    # Route 21
    add_rule_safe("Route 21 - Sis and Bro Lil & Ian Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Victory Road
    add_rule_safe("Victory Road 1F - North Item (Left)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 1F - North Item (Right)",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Victory Road 3F - Cool Couple Ray & Tyra Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Indigo Plateau
    if options.elite_four_requirement.value == EliteFourRequirement.option_badges:
        add_rule_safe("Lorelei's Room - Elite Four Lorelei Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Bruno's Room - Elite Four Bruno Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Agatha's Room - Elite Four Agatha Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Lance's Room - Elite Four Lance Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Battle",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Elite Four Rematch Scaling",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion Rematch Scaling",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_badges(state, options.elite_four_rematch_count.value))
    elif options.elite_four_requirement.value == EliteFourRequirement.option_gyms:
        add_rule_safe("Lorelei's Room - Elite Four Lorelei Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Bruno's Room - Elite Four Bruno Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Agatha's Room - Elite Four Agatha Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Lance's Room - Elite Four Lance Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Battle",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion's Room - Champion Rematch Reward",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Elite Four Rematch Scaling",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
        add_rule_safe("Champion Rematch Scaling",
                      lambda state: logic.has_lorelei_returned(state) and
                                    logic.has_n_gyms(state, options.elite_four_rematch_count.value))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Indigo Plateau Pokemon Center 1F - Black Belt Info 1",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Indigo Plateau Pokemon Center 1F - Black Belt Info 2",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Indigo Plateau Pokemon Center 1F - Cooltrainer Info",
                      lambda state: state.has("Defeat Champion", player))
        add_rule_safe("Indigo Plateau Pokemon Center 1F - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))

    # One Island Town
    add_rule_safe("One Island Pokemon Center 1F - Celio Gift (Deliver Ruby)",
                  lambda state: logic.can_turn_in_ruby(state))
    add_rule_safe("One Island Pokemon Center 1F - Help Celio",
                  lambda state: logic.can_turn_in_sapphire(state))
    add_rule_safe("One Island Pokemon Center 1F - Celio Gift (Deliver Sapphire)",
                  lambda state: logic.can_turn_in_sapphire(state))
    add_rule_safe("One Island Pokemon Center 1F - Celio Info 1",
                  lambda state: state.has("Restore Pokemon Network Machine", player))
    add_rule_safe("One Island Pokemon Center 1F - Celio Info 2",
                  lambda state: state.has("Restore Pokemon Network Machine", player))
    add_rule_safe("One Island Pokemon Center 1F - Celio Info 3",
                  lambda state: state.has("Restore Pokemon Network Machine", player))

    # Kindle Road
    add_rule_safe("Kindle Road - Plateau Item",
                  lambda state: logic.can_rock_smash(state))
    add_rule_safe("Kindle Road - Item Behind Smashable Rock",
                  lambda state: logic.can_rock_smash(state))
    add_rule_safe("Kindle Road - Crush Kin Mik & Kia Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Ember Spa
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Ember Spa - Black Belt Info",
                      lambda state: state.has("Defeat Champion", player))

    # Mt. Ember
    add_rule_safe("Mt. Ember Exterior - Eavesdrop on Team Rocket Grunts",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Mt. Ember Exterior - Team Rocket Grunt Reward (Left)",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Mt. Ember Exterior - Team Rocket Grunt Reward (Right)",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Team Rocket Grunt 43 Scaling",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Team Rocket Grunt 44 Scaling",
                  lambda state: state.has("Deliver Meteorite", player))
    add_rule_safe("Mt. Ember Exterior - Item Near Summit",
                  lambda state: logic.can_strength(state) and
                                logic.can_rock_smash(state))
    add_rule_safe("Mt. Ember Summit - Legendary Pokemon",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Legendary Moltres Scaling",
                  lambda state: logic.can_strength(state))

    # Two Island Town
    add_rule_safe("Two Island Town - Item Behind Cuttable Tree",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Two Island Town - Market Stall Item 2",
                  lambda state: logic.two_island_stall_expansion(state, 1))
    add_rule_safe("Two Island Town - Market Stall Item 3",
                  lambda state: logic.two_island_stall_expansion(state, 3))
    add_rule_safe("Two Island Town - Market Stall Item 4",
                  lambda state: logic.two_island_stall_expansion(state, 3))
    add_rule_safe("Two Island Town - Market Stall Item 5",
                  lambda state: logic.two_island_stall_expansion(state, 2))
    add_rule_safe("Two Island Town - Market Stall Item 6",
                  lambda state: logic.two_island_stall_expansion(state, 1))
    add_rule_safe("Two Island Town - Market Stall Item 8",
                  lambda state: logic.two_island_stall_expansion(state, 2))
    add_rule_safe("Two Island Town - Market Stall Item 9",
                  lambda state: logic.two_island_stall_expansion(state, 3))
    add_rule_safe("Two Island Town - Beauty Info",
                  lambda state: logic.two_island_stall_expansion(state, 2))
    add_rule_safe("Two Island Game Corner - Lostelle's Dad Gift (Deliver Meteorite)",
                  lambda state: logic.can_turn_in_meteorite(state))
    add_rule_safe("Two Island Game Corner - Lostelle's Dad's Delivery",
                  lambda state: logic.can_turn_in_meteorite(state))

    # Cape Brink
    add_rule_safe("Cape Brink - Hidden Item Across Pond",
                  lambda state: state.has("Itemfinder", player))

    # Three Island Town
    add_rule_safe("Three Island Town - Item Behind East Fence",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Three Island Town - Hidden Item Behind West Fence",
                  lambda state: logic.can_cut(state))
    add_rule_safe("Lostelle's House - Lostelle Gift",
                  lambda state: state.has("Deliver Meteorite", player))

    # Bond Bridge
    add_rule_safe("Bond Bridge - Twins Joy & Meg Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Berry Forest
    add_rule_safe("Berry Forest - Item Past Southwest Pond",
                  lambda state: logic.can_cut(state))

    # Four Island Town
    add_rule_safe("Four Island Town - Beach Item",
                  lambda state: logic.can_rock_smash(state))
    add_rule_safe("Four Island Town - Old Woman Info",
                  lambda state: state.has("Restore Pokemon Network Machine", player))

    # Five Island Town
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Five Island Pokemon Center 1F - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))

    # Five Isle Meadow
    add_rule_safe("Five Isle Meadow - Item Behind Cuttable Tree",
                  lambda state: logic.can_cut(state))

    # Rocket Warehouse
    add_rule_safe("Rocket Warehouse - Scientist Gideon Info",
                  lambda state: state.has("Restore Pokemon Network Machine", player))

    # Memorial Pillar
    add_rule_safe("Memorial Pillar - Memorial Man Gift",
                  lambda state: state.has("Lemonade", player))

    # Water Labyrinth
    add_rule_safe("Water Labyrinth - Gentleman Info",
                  lambda state: state.has_any(("Togepi", "Togetic"), player))

    # Resort Gorgeous
    add_rule_safe("Selphy's House - Selphy Gift (Show Pokemon)",
                  lambda state: logic.can_show_selphy_pokemon(state))

    # Water Path
    add_rule_safe("Water Path - Twins Miu & Mia Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))
    add_rule_safe("Water Path Heracross Woman's House - Woman Gift (Show Heracross)",
                  lambda state: state.has("Heracross", player))

    # Ruin Valley
    add_rule_safe("Ruin Valley - Plateau Item",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Ruin Valley - Southwest Item",
                  lambda state: logic.can_strength(state))
    add_rule_safe("Ruin Valley - Southeast Item",
                  lambda state: logic.can_strength(state))

    # Dotted Hole
    add_rule_safe("Dotted Hole 1F - Dropped Item",
                  lambda state: state.has("Learn Yes Nah Chansey", player))

    # Outcast Island
    add_rule_safe("Outcast Island - Sis and Bro Ava & Geb Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Seven Island Town
    add_rule_safe("Seven Island Town - Scientist Gift 1 (Trade Scanner)",
                  lambda state: state.has("Scanner", player))
    add_rule_safe("Seven Island Town - Scientist Gift 2 (Trade Scanner)",
                  lambda state: state.has("Scanner", player))
    if "Early Gossipers" not in options.modify_world_state.value:
        add_rule_safe("Seven Island Pokemon Center 1F - Bookshelf Info",
                      lambda state: state.has("Defeat Champion", player))

    # Canyon Entrance
    add_rule_safe("Canyon Entrance - Young Couple Eve & Jon Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Sevault Canyon
    add_rule_safe("Sevault Canyon - Item Behind Smashable Rocks",
                  lambda state: logic.can_strength(state) and logic.can_rock_smash(state))
    add_rule_safe("Sevault Canyon - Cool Couple Lex & Nya Reward",
                  lambda state: state.has_any(logic.wild_pokemon, player))

    # Tanoby Key
    add_rule_safe("Tanoby Key - Solve Puzzle",
                  lambda state: logic.can_strength(state))

    # Tanoby Ruins
    add_rule_safe("Tanoby Ruins - Island Item",
                  lambda state: state.has("Unlock Ruins", player))

    # Cerulean Cave
    add_rule_safe("Cerulean Cave 2F - East Item",
                  lambda state: logic.can_rock_smash(state))
    add_rule_safe("Cerulean Cave 2F - West Item",
                  lambda state: logic.can_rock_smash(state))
    add_rule_safe("Cerulean Cave 2F - Center Item",
                  lambda state: logic.can_rock_smash(state))

    # Navel Rock
    add_rule_safe("Navel Rock - Hidden Item Near Ho-Oh",
                  lambda state: state.has("Itemfinder", player))


def _add_evolution_rule(world: "PokemonFRLGWorld", location: PokemonFRLGLocation):
    pokemon = location.name.split(" - ")[1].strip()
    pokemon_species_name = re.sub(r' \d+', '', pokemon)
    evo_data = data.evolutions[pokemon]
    evo_method = evo_data.method
    player = world.player
    logic = world.logic
    if evo_method in EVO_METHODS_ITEM:
        use_item = logic.world_item_id_map[evo_data.param]
        add_rule(location, lambda state: (logic.has_pokemon_for_evolution(state, pokemon_species_name)
                                          and state.has(use_item, player)))
    elif evo_method in EVO_METHODS_HELD_ITEM:
        items = (logic.world_item_id_map[evo_data.param], logic.world_item_id_map[evo_data.param2])
        add_rule(location, lambda state: (logic.has_pokemon_for_evolution(state, pokemon_species_name)
                                          and state.has_all(items, player)))
    elif evo_method in EVO_METHODS_LEVEL_ANY:
        gyms_requirement = evo_data.param // 7
        add_rule(location, lambda state: (logic.has_pokemon_for_evolution(state, pokemon_species_name)
                                          and logic.has_n_gyms(state, gyms_requirement)))
    elif evo_method in EVO_METHODS_FRIENDSHIP:
        add_rule(location, lambda state: logic.has_pokemon_for_evolution(state, pokemon_species_name))
    else:
        raise RuntimeError(f"Unexpected evo method: {evo_method}")


def set_rules(world: "PokemonFRLGWorld") -> None:
    logic = world.logic
    player = world.player
    options = world.options
    multiworld = world.multiworld

    if options.goal == Goal.option_champion:
        multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion", player)
    elif options.goal == Goal.option_champion_rematch:
        multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion (Rematch)", player)

    if options.pokemon_request_locations and not options.kanto_only:
        logic.resort_gorgeous_pokemon = NAME_TO_SPECIES_ID[world.random.choice(logic.wild_pokemon)]

    set_entrance_rules(world)
    set_location_rules(world)

    # Add rules that are the same for specific location categories
    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if (options.itemfinder_required != ItemfinderRequired.option_off and
                location.category in {LocationCategory.HIDDEN_ITEM, LocationCategory.HIDDEN_ITEM_RECURRING}):
            add_rule(location, lambda state: state.has("Itemfinder", player))
        if options.fame_checker_required and location.category == LocationCategory.FAMESANITY:
            add_rule(location, lambda state: state.has("Fame Checker", player))
        if location.category == LocationCategory.DEXSANITY:
            name = location.name.split(" - ")[1].strip()
            add_rule(location, lambda state, pokemon=name: logic.has_pokemon(state, pokemon))
        if location.category == LocationCategory.EVENT_EVOLUTION_POKEMON:
            _add_evolution_rule(world, location)

    # Add dark cave logic
    if options.flash_required != FlashRequired.option_off:
        dark_cave_regions = []
        dark_cave_regions.extend(["Rock Tunnel 1F Northeast", "Rock Tunnel 1F Northwest", "Rock Tunnel 1F South",
                                  "Rock Tunnel B1F Southeast", "Rock Tunnel B1F Northwest",
                                  "Rock Tunnel 1F Land Encounters",
                                  "Rock Tunnel B1F Land Encounters"])
        if "Mt. Moon" in options.additional_dark_caves.value:
            dark_cave_regions.extend(["Mt. Moon 1F", "Mt. Moon B1F First Tunnel", "Mt. Moon B1F Second Tunnel",
                                      "Mt. Moon B1F Third Tunnel", "Mt. Moon B1F Fourth Tunnel",
                                      "Mt. Moon B2F South", "Mt. Moon B2F Northeast", "Mt. Moon B2F",
                                      "Mt. Moon 1F Land Encounters", "Mt. Moon B1F Land Encounters",
                                      "Mt. Moon B2F Land Encounters"])
        if "Diglett's Cave" in options.additional_dark_caves.value:
            dark_cave_regions.extend(["Diglett's Cave B1F", "Diglett's Cave B1F Land Encounters"])
        if "Victory Road" in options.additional_dark_caves.value:
            dark_cave_regions.extend(["Victory Road 1F South", "Victory Road 1F North", "Victory Road 2F Southwest",
                                      "Victory Road 2F Center", "Victory Road 2F Northwest",
                                      "Victory Road 2F Southeast", "Victory Road 2F East", "Victory Road 3F North",
                                      "Victory Road 3F Southwest", "Victory Road 3F Southeast",
                                      "Victory Road 1F Land Encounters", "Victory Road 2F Land Encounters",
                                      "Victory Road 3F Land Encounters"])

        for region in dark_cave_regions:
            for exit in world.get_region(region).exits:
                add_rule(exit, lambda state: logic.can_flash(state))
            for location in world.get_region(region).locations:
                add_rule(location, lambda state: logic.can_flash(state))


def set_hm_compatible_pokemon(world: "PokemonFRLGWorld") -> None:
    logic = world.logic
    hms = frozenset({"Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"})
    for hm in hms:
        for species in world.modified_species.values():
            combatibility_array = int_to_bool_array(species.tm_hm_compatibility)
            if combatibility_array[HM_TO_COMPATIBILITY_ID[hm]] == 1:
                logic.compatible_hm_pokemon[hm].append(species.name)
    logic.update_hm_compatible_pokemon()


def verify_hm_accessibility(world: "PokemonFRLGWorld") -> None:
    logic = world.logic

    def can_use_hm(state: CollectionState, hm: str) -> bool:
        if hm == "Cut":
            return logic.can_cut(state)
        elif hm == "Fly":
            return logic.can_fly(state)
        elif hm == "Surf":
            return logic.can_surf(state)
        elif hm == "Strength":
            return logic.can_strength(state)
        elif hm == "Flash":
            return logic.can_flash(state)
        elif hm == "Rock Smash":
            return logic.can_rock_smash(state)
        elif hm == "Waterfall":
            return logic.can_waterfall(state)
        return False

    hms: List[str] = ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]
    world.random.shuffle(hms)
    last_hm_verified = None
    while len(hms) > 0:
        hm_to_verify = hms[0]
        state = world.get_world_collection_state()
        if not can_use_hm(state, hm_to_verify) and logic.has_badge_requirement(state, hm_to_verify):
            if hm_to_verify == last_hm_verified:
                raise Exception(f"Failed to ensure access to {hm_to_verify} for player {world.player}")
            last_hm_verified = hm_to_verify
            valid_pokemon = [mon for mon in logic.wild_pokemon if state.has(mon, world.player)
                             and mon not in logic.compatible_hm_pokemon[hm_to_verify]]
            pokemon = world.random.choice(valid_pokemon)
            add_hm_compatability(world, pokemon, hm_to_verify)
            logic.add_hm_compatible_pokemon(hm_to_verify, pokemon)
        else:
            hms.pop(0)
    logic.update_hm_compatible_pokemon()
