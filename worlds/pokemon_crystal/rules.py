from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule, CollectionRule
from .data import data, EvolutionType, EvolutionData, FishingRodType, EncounterKey, LogicalAccess, EncounterType
from .evolution import evolution_location_name
from .items import PokemonCrystalGlitchedToken
from .options import Goal, JohtoOnly, Route32Condition, UndergroundsRequirePower, Route2Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, KantoAccessRequirement, Route3Access, BreedingMethodsRequired, \
    MtSilverRequirement, FreeFlyLocation, HMBadgeRequirements, EliteFourRequirement, RedRequirement, \
    Route44AccessRequirement, RandomizeBadges, RadioTowerRequirement, PokemonCrystalOptions, Shopsanity, FlyCheese, \
    RequireFlash, RequireItemfinder, Route42Access, RedGyaradosAccess, RandomizePhoneCalls
from .pokemon import add_hm_compatibility, get_chamber_event_for_unown
from .pokemon_data import ALL_UNOWN
from .utils import get_fly_regions, get_mart_slot_location_name

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


class PokemonCrystalLogic:
    available_pokemon: set[str]
    all_pokemon: set[str]
    evolution: dict[str, list[tuple[EvolutionData, LogicalAccess]]]
    breeding: dict[str, list[tuple[str, LogicalAccess]]]
    wild_regions: dict[EncounterKey, LogicalAccess]
    guaranteed_hm_access: bool

    pokemon_hm_use: dict[str, list[str]]
    compatible_hm_pokemon: dict[str, list[str]]

    badge_items: dict[str, str]
    hm_badge_requirements_johto: dict[str, tuple]
    hm_badge_requirements_kanto: dict[str, tuple]
    pokemon_hm_use: dict[str, list[str]]
    gym_events: dict[str, str]

    map_card_fly_unlocks: tuple
    expn_components: tuple

    fishing_rod_rules: dict[FishingRodType, CollectionRule]

    player: int
    options: PokemonCrystalOptions

    def __init__(self, world: "PokemonCrystalWorld"):
        self.available_pokemon = set()
        self.all_pokemon = set(world.generated_pokemon.keys())
        self.evolution = defaultdict(list)
        self.breeding = defaultdict(list)
        self.wild_regions = defaultdict(lambda: LogicalAccess.Inaccessible)
        self.compatible_hm_pokemon = defaultdict(list)
        self.guaranteed_hm_access = False

        self.hm_badge_requirements_johto = {}
        self.hm_badge_requirements_kanto = {}
        self.pokemon_hm_use = {}

        self.player = world.player
        self.options = world.options
        self.is_universal_tracker = world.is_universal_tracker

        if self.options.randomize_badges == RandomizeBadges.option_vanilla:
            self.badge_items = {
                "zephyr": "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
                "hive": "EVENT_HIVE_BADGE_FROM_BUGSY",
                "plain": "EVENT_PLAIN_BADGE_FROM_WHITNEY",
                "fog": "EVENT_FOG_BADGE_FROM_MORTY",
                "mineral": "EVENT_STORM_BADGE_FROM_CHUCK",
                "storm": "EVENT_MINERAL_BADGE_FROM_JASMINE",
                "glacier": "EVENT_GLACIER_BADGE_FROM_PRYCE",
                "rising": "EVENT_RISING_BADGE_FROM_CLAIR" if world.options.vanilla_clair else "EVENT_RISING_BADGE_FROM_CLAIR_GYM",

                "boulder": "EVENT_BOULDER_BADGE_FROM_BROCK",
                "cascade": "EVENT_CASCADE_BADGE_FROM_MISTY",
                "thunder": "EVENT_THUNDER_BADGE_FROM_LTSURGE",
                "rainbow": "EVENT_RAINBOW_BADGE_FROM_ERIKA",
                "soul": "EVENT_SOUL_BADGE_FROM_JANINE",
                "marsh": "EVENT_MARSH_BADGE_FROM_SABRINA",
                "volcano": "EVENT_VOLCANO_BADGE_FROM_BLAINE",
                "earth": "EVENT_EARTH_BADGE_FROM_BLUE"
            }
        else:
            self.badge_items = {
                "zephyr": "Zephyr Badge",
                "hive": "Hive Badge",
                "plain": "Plain Badge",
                "fog": "Fog Badge",
                "mineral": "Mineral Badge",
                "storm": "Storm Badge",
                "glacier": "Glacier Badge",
                "rising": "Rising Badge",

                "boulder": "Boulder Badge",
                "cascade": "Cascade Badge",
                "thunder": "Thunder Badge",
                "rainbow": "Rainbow Badge",
                "soul": "Soul Badge",
                "marsh": "Marsh Badge",
                "volcano": "Volcano Badge",
                "earth": "Earth Badge"
            }

        self.gym_events = {
            "falkner": "EVENT_BEAT_FALKNER",
            "bugsy": "EVENT_BEAT_BUGSY",
            "whitney": "EVENT_BEAT_WHITNEY",
            "morty": "EVENT_BEAT_MORTY",
            "jasmine": "EVENT_BEAT_JASMINE",
            "chuck": "EVENT_BEAT_CHUCK",
            "pryce": "EVENT_BEAT_PRYCE",
            "clair": "EVENT_BEAT_CLAIR",

            "brock": "EVENT_BEAT_BROCK",
            "misty": "EVENT_BEAT_MISTY",
            "ltsurge": "EVENT_BEAT_LTSURGE",
            "erika": "EVENT_BEAT_ERIKA",
            "janine": "EVENT_BEAT_JANINE",
            "sabrina": "EVENT_BEAT_SABRINA",
            "blaine": "EVENT_BEAT_BLAINE",
            "blue": "EVENT_BEAT_BLUE"
        }

        if world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges:
            if "Cut" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["CUT"] = ("hive",)
                    self.hm_badge_requirements_kanto["CUT"] = ("hive",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["CUT"] = ("hive", "cascade")
                    self.hm_badge_requirements_kanto["CUT"] = ("hive", "cascade")
                else:
                    self.hm_badge_requirements_johto["CUT"] = ("hive",)
                    self.hm_badge_requirements_kanto["CUT"] = ("cascade",)

            if "Fly" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["FLY"] = ("storm",)
                    self.hm_badge_requirements_kanto["FLY"] = ("storm",)
                else:
                    self.hm_badge_requirements_johto["FLY"] = ("storm", "thunder")
                    self.hm_badge_requirements_kanto["FLY"] = ("storm", "thunder")

            if "Surf" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["SURF"] = ("fog",)
                    self.hm_badge_requirements_kanto["SURF"] = ("fog",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["SURF"] = ("fog", "soul")
                    self.hm_badge_requirements_kanto["SURF"] = ("fog", "soul")
                else:
                    self.hm_badge_requirements_johto["SURF"] = ("fog",)
                    self.hm_badge_requirements_kanto["SURF"] = ("soul",)

            if "Strength" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["STRENGTH"] = ("plain",)
                    self.hm_badge_requirements_kanto["STRENGTH"] = ("plain",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["STRENGTH"] = ("plain", "rainbow")
                    self.hm_badge_requirements_kanto["STRENGTH"] = ("plain", "rainbow")
                else:
                    self.hm_badge_requirements_johto["STRENGTH"] = ("plain",)
                    self.hm_badge_requirements_kanto["STRENGTH"] = ("rainbow",)

            if "Flash" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["FLASH"] = ("zephyr",)
                    self.hm_badge_requirements_kanto["FLASH"] = ("zephyr",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["FLASH"] = ("zephyr", "boulder")
                    self.hm_badge_requirements_kanto["FLASH"] = ("zephyr", "boulder")
                else:
                    self.hm_badge_requirements_johto["FLASH"] = ("zephyr",)
                    self.hm_badge_requirements_kanto["FLASH"] = ("boulder",)

            if "Whirlpool" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["WHIRLPOOL"] = ("glacier",)
                    self.hm_badge_requirements_kanto["WHIRLPOOL"] = ("glacier",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["WHIRLPOOL"] = ("glacier", "volcano")
                    self.hm_badge_requirements_kanto["WHIRLPOOL"] = ("glacier", "volcano")
                else:
                    self.hm_badge_requirements_johto["WHIRLPOOL"] = ("glacier",)
                    self.hm_badge_requirements_kanto["WHIRLPOOL"] = ("volcano",)

            if "Waterfall" not in world.options.remove_badge_requirement:
                if world.options.hm_badge_requirements == HMBadgeRequirements.option_vanilla:
                    self.hm_badge_requirements_johto["WATERFALL"] = ("rising",)
                    self.hm_badge_requirements_kanto["WATERFALL"] = ("rising",)
                elif world.options.hm_badge_requirements == HMBadgeRequirements.option_add_kanto:
                    self.hm_badge_requirements_johto["WATERFALL"] = ("rising", "earth")
                    self.hm_badge_requirements_kanto["WATERFALL"] = ("rising", "earth")
                else:
                    self.hm_badge_requirements_johto["WATERFALL"] = ("rising",)
                    self.hm_badge_requirements_kanto["WATERFALL"] = ("earth",)

        if world.options.randomize_pokegear:
            self.map_card_fly_unlocks = ("Map Card", "Pokegear")
            self.expn_components = ("Pokegear", "Radio Card", "EXPN Card")
            if world.options.randomize_phone_call_items == RandomizePhoneCalls.option_on_simple:
                self.phone_call_components = ("Pokegear", "Phone Card")
            else:
                self.phone_call_components = ("Pokegear", "Phone Card", "EVENT_CHANGE_DST")
        else:
            self.map_card_fly_unlocks = ("EVENT_GOT_MAP_CARD", "EVENT_GOT_POKEGEAR")
            self.expn_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_RADIO_CARD", "EVENT_GOT_EXPN_CARD")
            if world.options.randomize_phone_call_items == RandomizePhoneCalls.option_on_simple:
                self.phone_call_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_PHONE_CARD")
            else:
                self.phone_call_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_PHONE_CARD", "EVENT_CHANGE_DST")

        if world.options.progressive_rods:
            self.fishing_rod_rules = {
                FishingRodType.Old: lambda state: state.has("Progressive Rod", self.player),
                FishingRodType.Good: lambda state: state.has("Progressive Rod", self.player, 2),
                FishingRodType.Super: lambda state: state.has("Progressive Rod", self.player, 3),
            }
        else:
            self.fishing_rod_rules = {
                FishingRodType.Old: lambda state: state.has("Old Rod", self.player),
                FishingRodType.Good: lambda state: state.has("Good Rod", self.player),
                FishingRodType.Super: lambda state: state.has("Super Rod", self.player),
            }

    def has_badge(self, state: CollectionState, badge: str):
        return state.has(self.badge_items[badge], self.player)

    def has_n_badges(self, state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique(self.badge_items.values(), self.player, n)

    def has_beaten_gym(self, state: CollectionState, leader: str):
        return state.has(self.gym_events[leader], self.player)

    def has_beaten_n_gyms(self, state: CollectionState, n: int):
        return state.has_from_list_unique(self.gym_events.values(), self.player, n)

    def has_n_pokemon(self, state: CollectionState, n: int):
        return state.has_from_list_unique(self.all_pokemon, self.player, n)

    def has_hm_badge_requirement(self, hm: str, kanto: bool) -> CollectionRule:
        if kanto:
            return lambda state: state.has_any(
                (self.badge_items[badge] for badge in self.hm_badge_requirements_kanto[hm]),
                self.player) if hm in self.hm_badge_requirements_kanto else True
        else:
            return lambda state: state.has_any(
                (self.badge_items[badge] for badge in self.hm_badge_requirements_johto[hm]),
                self.player) if hm in self.hm_badge_requirements_johto else True

    def can_cut(self, kanto: bool = False) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("CUT", kanto=kanto)
        required_items = {"HM01 Cut"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach CUT")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_fly(self) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("FLY", kanto=False)
        required_items = {"HM02 Fly"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach FLY")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_surf(self, kanto: bool = False) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("SURF", kanto=kanto)
        required_items = {"HM03 Surf"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach SURF")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_strength(self, kanto: bool = False) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("STRENGTH", kanto=kanto)
        required_items = {"HM04 Strength"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach STRENGTH")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_flash(self, kanto: bool = False, allow_ool: bool = True) -> CollectionRule:
        if self.options.require_flash == RequireFlash.option_not_required and allow_ool:
            return lambda _: True
        badge_requirement = self.has_hm_badge_requirement("FLASH", kanto=kanto)
        required_items = {"HM05 Flash"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach FLASH")
        if self.is_universal_tracker and allow_ool and self.options.require_flash == RequireFlash.option_logically_required:
            return lambda state: (state.has_all(required_items, self.player) and badge_requirement(
                state)) or state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, self.player)
        else:
            return lambda state: (state.has_all(required_items, self.player) and badge_requirement(state))

    def can_whirlpool(self, kanto: bool = False) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("WHIRLPOOL", kanto=kanto)
        required_items = {"HM06 Whirlpool"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach WHIRLPOOL")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_waterfall(self, kanto: bool = False) -> CollectionRule:
        badge_requirement = self.has_hm_badge_requirement("WATERFALL", kanto=kanto)
        required_items = {"HM07 Waterfall"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach WATERFALL")
        return lambda state: state.has_all(required_items, self.player) and badge_requirement(state)

    def can_headbutt(self) -> CollectionRule:
        required_items = {"TM02"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach HEADBUTT")
        return lambda state: state.has_all(required_items, self.player)

    def can_rock_smash(self) -> CollectionRule:
        required_items = {"TM08"}
        if not self.options.field_moves_always_usable:
            required_items.add("Teach ROCK_SMASH")
        return lambda state: state.has_all(required_items, self.player)

    def has_tea(self) -> CollectionRule:
        return lambda state: state.has("Tea", self.player)

    def can_map_card_fly(self) -> CollectionRule:
        return lambda state: state.has_all(self.map_card_fly_unlocks, self.player)

    def has_expn(self) -> CollectionRule:
        return lambda state: state.has_all(self.expn_components, self.player)

    def has_rockets_requirement(self) -> CollectionRule:
        if self.options.radio_tower_requirement == RadioTowerRequirement.option_badges:
            return lambda state: self.has_n_badges(state, self.options.radio_tower_count.value)
        else:
            return lambda state: self.has_beaten_n_gyms(state, self.options.radio_tower_count.value)

    def has_route_44_access(self) -> CollectionRule:
        if self.options.route_44_access_requirement == Route44AccessRequirement.option_badges:
            return lambda state: self.has_n_badges(state, self.options.route_44_access_count.value)
        else:
            return lambda state: self.has_beaten_n_gyms(state, self.options.route_44_access_count.value)

    def has_elite_four_requirement(self) -> CollectionRule:
        if self.options.elite_four_requirement == EliteFourRequirement.option_gyms:
            return lambda state: self.has_beaten_n_gyms(state, self.options.elite_four_count.value)
        elif self.options.elite_four_requirement == EliteFourRequirement.option_badges:
            return lambda state: self.has_n_badges(state, self.options.elite_four_count.value)
        else:
            johto_badges = list(self.badge_items.values())[:8]
            return lambda state: state.has_from_list_unique(johto_badges, self.player,
                                                            self.options.elite_four_count.value)

    def has_red_requirement(self) -> CollectionRule:
        if self.options.red_requirement == RedRequirement.option_gyms:
            return lambda state: self.has_beaten_n_gyms(state, self.options.red_count.value)
        else:
            return lambda state: self.has_n_badges(state, self.options.red_count.value)

    def has_mt_silver_requirement(self) -> CollectionRule:
        if self.options.mt_silver_requirement == MtSilverRequirement.option_gyms:
            return lambda state: self.has_beaten_n_gyms(state, self.options.mt_silver_count.value)
        else:
            return lambda state: self.has_n_badges(state, self.options.mt_silver_count.value)

    def has_kanto_access_requirement(self) -> CollectionRule:
        if self.options.kanto_access_requirement == KantoAccessRequirement.option_wake_snorlax:
            return lambda state: state.has("EVENT_FOUGHT_SNORLAX", self.player)
        elif self.options.kanto_access_requirement == KantoAccessRequirement.option_badges:
            return lambda state: self.has_n_badges(state, self.options.kanto_access_count.value)
        elif self.options.kanto_access_requirement == KantoAccessRequirement.option_gyms:
            return lambda state: self.has_beaten_n_gyms(state, self.options.kanto_access_count.value)
        else:
            return lambda state: state.has("EVENT_BEAT_ELITE_FOUR", self.player)

    def has_route_32_condition(self) -> CollectionRule | None:
        if self.options.route_32_condition == Route32Condition.option_egg_from_aide:
            return lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", self.player)
        elif self.options.route_32_condition == Route32Condition.option_any_badge:
            return lambda state: self.has_n_badges(state, 1)
        elif self.options.route_32_condition == Route32Condition.option_any_gym:
            return lambda state: self.has_beaten_n_gyms(state, 1)
        elif self.options.route_32_condition == Route32Condition.option_zephyr_badge:
            return lambda state: self.has_badge(state, "zephyr")
        else:
            return None

    def set_hm_compatible_pokemon(self, world: "PokemonCrystalWorld"):
        hms = ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH")
        for hm in hms:
            for pokemon_id, pokemon_data in world.generated_pokemon.items():
                if hm in pokemon_data.tm_hm:
                    self.compatible_hm_pokemon[hm].append(pokemon_id)

        pokemon_hm_use = defaultdict(list)
        for hm, species_list in self.compatible_hm_pokemon.items():
            for species in species_list:
                pokemon_hm_use[species].append(f"Teach {hm}")
        self.pokemon_hm_use = pokemon_hm_use

    def add_hm_compatible_pokemon(self, hm: str, pokemon_id: str):
        self.compatible_hm_pokemon[hm].append(pokemon_id)
        self.pokemon_hm_use.setdefault(pokemon_id, []).append(f"Teach {hm}")


def set_rules(world: "PokemonCrystalWorld") -> None:
    unown_unlocks = ("ENGINE_UNLOCKED_UNOWNS_A_TO_K",
                     "ENGINE_UNLOCKED_UNOWNS_L_TO_R",
                     "ENGINE_UNLOCKED_UNOWNS_S_TO_W",
                     "ENGINE_UNLOCKED_UNOWNS_X_TO_Z")
    evolution_item_unlocks = ("EVENT_GOLDENROD_EVOLUTION_ITEMS", "EVENT_CELADON_EVOLUTION_ITEMS")
    happiness_unlocks = ("EVENT_DAISY_GROOMING", "EVENT_HAIRCUT_BROTHERS")

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.multiworld.get_location(location, world.player)

    def safe_set_location_rule(spot: str, rule: CollectionRule) -> None:
        try:
            location = world.get_location(spot)
        except KeyError:
            return
        set_rule(location, rule)

    def hidden():
        return world.options.randomize_hidden_items

    def johto_only():
        return world.options.johto_only.value

    def rematchsanity():
        return world.options.rematchsanity or world.options.randomize_phone_call_items

    can_cut = world.logic.can_cut()
    can_cut_kanto = world.logic.can_cut(kanto=True)

    can_fly = world.logic.can_fly()

    can_surf = world.logic.can_surf()
    can_surf_kanto = world.logic.can_surf(kanto=True)

    can_strength = world.logic.can_strength()

    can_flash = world.logic.can_flash()
    can_flash_kanto = world.logic.can_flash(kanto=True)

    can_whirlpool = world.logic.can_whirlpool()

    can_waterfall = world.logic.can_waterfall()

    can_headbutt = world.logic.can_headbutt()
    can_rock_smash = world.logic.can_rock_smash()

    can_surf_and_whirlpool = lambda state: can_surf(state) and can_whirlpool(state)
    can_surf_and_waterfall = lambda state: can_surf(state) and can_waterfall(state)

    kanto_gyms_access = lambda state: state.has_any(
        ("EVENT_SILVER_CAVE_ACCESS", "EVENT_FOUGHT_SNORLAX", "EVENT_FOUGHT_LUGIA", "EVENT_FOUGHT_HO_OH",
         "EVENT_FOUGHT_SUICUNE", "EVENT_VICTORY_ROAD_ACCESS"), world.player
    )

    can_phone_call = lambda state: state.has_all(world.logic.phone_call_components, world.player)

    # Goal
    if world.options.goal == Goal.option_red:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("EVENT_BEAT_RED", world.player)
    elif world.options.goal == Goal.option_diploma:
        world.multiworld.completion_condition[world.player] = lambda state: state.has(
            "EVENT_OBTAINED_DIPLOMA", world.player)
    elif world.options.goal == Goal.option_rival:
        rival_events = [
            "EVENT_BEAT_CHERRYGROVE_RIVAL",
            "EVENT_BEAT_AZALEA_RIVAL",
            "EVENT_RIVAL_BURNED_TOWER",
            "EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL",
            "EVENT_BEAT_VICTORY_ROAD_RIVAL",
        ]
        if world.options.johto_only == JohtoOnly.option_off:
            rival_events.extend([
                "EVENT_BEAT_RIVAL_IN_MT_MOON",
                "EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU"
            ])
        world.multiworld.completion_condition[world.player] = lambda state: state.has_all(rival_events, world.player)
    elif world.options.goal == Goal.option_defeat_team_rocket:
        rocket_events = [
            "EVENT_CLEARED_SLOWPOKE_WELL",
            "EVENT_CLEARED_ROCKET_HIDEOUT",
            "EVENT_BEAT_ROCKET_EXECUTIVEM_3",
            "EVENT_CLEARED_RADIO_TOWER",
        ]
        if world.options.johto_only == JohtoOnly.option_off:
            rocket_events.extend([
                "EVENT_ROUTE_24_ROCKET"
            ])
        world.multiworld.completion_condition[world.player] = lambda state: state.has_all(rocket_events, world.player)
    elif world.options.goal == Goal.option_unown_hunt:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("EVENT_GOT_ALL_UNOWN",
                                                                                      world.player)
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has(
            "EVENT_BEAT_ELITE_FOUR", world.player)

    # Free Fly
    set_rule(get_entrance("Fly"), can_fly)
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_card_fly_entrance = f"Free Fly {world.map_card_fly_location.exit_region}"
        add_rule(get_entrance(map_card_fly_entrance), world.logic.can_map_card_fly())

    # Fly Unlocks

    if world.options.randomize_fly_unlocks:
        for fly_region in get_fly_regions(world):
            set_rule(get_entrance(f"REGION_FLY -> {fly_region.exit_region}"),
                     lambda state, fly_unlock=f"Fly {fly_region.name}": state.has(fly_unlock, world.player))

    # New Bark Town
    # set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_29"),
    #          lambda state: state.has("EVENT_GOT_A_POKEMON_FROM_ELM", world.player))

    set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27:WEST"), can_surf)

    # set_rule(get_location("Elm's Lab - Everstone from Elm"),
    #          lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))

    set_rule(get_location("Elm's Lab - Gift from Aide after returning Mystery Egg"),
             lambda state: state.has_all(("Mystery Egg", "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON"), world.player))

    set_rule(get_location("Elm's Lab - Master Ball from Elm"), lambda state: world.logic.has_badge(state, "rising"))

    set_rule(get_location("Elm's Lab - S.S. Ticket from Elm"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    # Route 29
    set_rule(get_location("Route 29 - Pink Bow from Tuscany"), lambda state: world.logic.has_badge(state, "zephyr"))

    # Route 30

    route_30_rule = lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player) or can_cut(
        state)

    if world.options.route_30_battle:
        set_rule(get_entrance("REGION_ROUTE_30:NORTHWEST -> REGION_ROUTE_30"), route_30_rule)

    set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_30:NORTHWEST"), route_30_rule)
    set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_30:POST_MYSTERY_EGG"),
             lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player))

    set_rule(get_location("Route 30 - Exp Share from Mr Pokemon"), lambda state: state.has("Red Scale", world.player))

    if rematchsanity():
        safe_set_location_rule("YOUNGSTER_JOEY_GOLDENROD",
                               lambda state: state.has("ENGINE_FLYPOINT_GOLDENROD", world.player))
        safe_set_location_rule("YOUNGSTER_JOEY_OLIVINE",
                               lambda state: state.has("ENGINE_FLYPOINT_OLIVINE", world.player))
        safe_set_location_rule("YOUNGSTER_JOEY_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("YOUNGSTER_JOEY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 30 - HP Up from Joey"),
                 lambda state: can_phone_call(state) and state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    # Cherrygrove
    set_rule(get_location("Cherrygrove City - Mystic Water from Island Man"), can_surf)

    safe_set_location_rule("Cherrygrove City - Rival",
                           lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player))
    set_rule(get_location("EVENT_BEAT_CHERRYGROVE_RIVAL"),
             lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player))

    # Route 31
    if "Dark Cave" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_31 -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST"), can_flash)

    set_rule(get_location("EVENT_GAVE_KENYA"), lambda state: state.has("EVENT_GOT_KENYA", world.player))
    set_rule(get_location("Route 31 - TM50 for delivering Kenya"),
             lambda state: state.has("EVENT_GOT_KENYA", world.player))

    if rematchsanity():
        safe_set_location_rule("BUG_CATCHER_WADE_GOLDENROD",
                               lambda state: state.has("ENGINE_FLYPOINT_GOLDENROD", world.player))
        safe_set_location_rule("BUG_CATCHER_WADE_MAHOGANY",
                               lambda state: state.has("ENGINE_FLYPOINT_MAHOGANY", world.player))
        safe_set_location_rule("BUG_CATCHER_WADE_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        # Dark Cave Violet
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("BUG_CATCHER_WADE_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 31 - Berry from Wade"), can_phone_call)

    set_rule(get_location("Dark Cave Violet Entrance - Southeast Item (Left)"), can_rock_smash)
    set_rule(get_location("Dark Cave Violet Entrance - Southeast Item (Right)"), can_rock_smash)
    set_rule(get_location("Dark Cave Violet Entrance - Northeast Item"), can_rock_smash)
    if hidden():
        set_rule(get_location("Dark Cave Violet Entrance - Hidden Item"), can_rock_smash)

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:EAST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST"),
             can_rock_smash)
    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:EAST"),
             can_rock_smash)

    if "Dark Cave" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_46:NORTH -> REGION_DARK_CAVE_VIOLET_ENTRANCE:EAST"),
                 can_flash)
        set_rule(get_entrance("REGION_ROUTE_45 -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST"),
                 can_flash)

    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTH_EAST"), can_surf)
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTH_EAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST"), can_surf)
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_WEST"), can_surf)
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_WEST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST"), can_surf)

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WATER -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST"), can_surf)

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WATER"),
                 can_surf_and_waterfall)
    else:
        set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WATER"),
                 can_surf)

    # Violet City
    if hidden():
        set_rule(get_location("Violet City - Hidden Item behind Cut Tree"), can_cut)
    set_rule(get_location("Violet City - Northwest Item across Water"), can_surf)
    set_rule(get_location("Violet City - Northeast Item across Water"), can_surf)

    set_rule(get_location("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"),
             lambda state: world.logic.has_beaten_gym(state, "falkner"))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:NORTH -> REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH"),
             can_surf)
    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH -> REGION_RUINS_OF_ALPH_OUTSIDE:NORTH"),
             can_surf)

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_KABUTO_CHAMBER -> REGION_RUINS_OF_ALPH_KABUTO_ITEM_ROOM"),
             lambda state: state.has("EVENT_MART_ESCAPE_ROPE", world.player))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OMANYTE_CHAMBER -> REGION_RUINS_OF_ALPH_OMANYTE_ITEM_ROOM"),
             lambda state: state.has_any(("EVENT_GOLDENROD_EVOLUTION_ITEMS", "EVENT_CELADON_EVOLUTION_ITEMS"),
                                         world.player))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_AERODACTYL_CHAMBER -> REGION_RUINS_OF_ALPH_AERODACTYL_ITEM_ROOM"),
             world.logic.can_flash(allow_ool=False))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_HO_OH_CHAMBER -> REGION_RUINS_OF_ALPH_HO_OH_ITEM_ROOM"),
             lambda state: state.has("Rainbow Wing", world.player))

    if world.options.goal == Goal.option_unown_hunt:
        set_rule(get_location("EVENT_GOT_ALL_UNOWN"), lambda state: state.has_all(ALL_UNOWN, world.player))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_A_TO_K"),
                 lambda state: state.has("Kabuto Tile", world.player, 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_L_TO_R"),
                 lambda state: state.has("Omanyte Tile", world.player, 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_S_TO_W"),
                 lambda state: state.has("Aerodactyl Tile", world.player, 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_X_TO_Z"),
                 lambda state: state.has("Ho-Oh Tile", world.player, 16))

        set_rule(get_entrance("REGION_RUINS_OF_ALPH_KABUTO_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 lambda state: state.has("Kabuto Tile", world.player, 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_AERODACTYL_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 lambda state: state.has("Aerodactyl Tile", world.player, 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_OMANYTE_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 lambda state: state.has("Omanyte Tile", world.player, 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_HO_OH_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 lambda state: state.has("Ho-Oh Tile", world.player, 16))

    # Route 32
    route_32_access_rule = world.logic.has_route_32_condition()
    if route_32_access_rule:
        set_rule(get_entrance("REGION_ROUTE_32:NORTH -> REGION_ROUTE_32:SOUTH"), route_32_access_rule)
        set_rule(get_entrance("REGION_ROUTE_32:SOUTH -> REGION_ROUTE_32:NORTH"), route_32_access_rule)

    set_rule(get_location("Route 32 - Miracle Seed from Man in North"),
             lambda state: world.logic.has_badge(state, "zephyr"))
    set_rule(get_location("Route 32 - TM05 from Roar Guy"), can_cut)

    if rematchsanity():
        safe_set_location_rule("FISHER_RALPH_ECRUTEAK",
                               lambda state: state.has("ENGINE_FLYPOINT_ECRUTEAK", world.player))
        safe_set_location_rule("FISHER_RALPH_LAKE",
                               lambda state: state.has("ENGINE_FLYPOINT_LAKE_OF_RAGE", world.player))
        safe_set_location_rule("PICNICKER_LIZ_ECRUTEAK",
                               lambda state: state.has("ENGINE_FLYPOINT_ECRUTEAK", world.player))
        safe_set_location_rule("PICNICKER_LIZ_ROCKETHQ",
                               lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))
        safe_set_location_rule("PICNICKER_LIZ_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("FISHER_RALPH_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("PICNICKER_LIZ_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("FISHER_RALPH_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Union Cave
    set_rule(get_entrance("REGION_UNION_CAVE_1F -> REGION_UNION_CAVE_B1F:SOUTH"), can_surf)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F -> REGION_UNION_CAVE_B1F:NORTH"), can_surf)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:NORTH -> REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH:UNION_LEDGE"),
             can_strength)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:SOUTH -> REGION_UNION_CAVE_B2F"), can_surf)

    if "Union Cave" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_32:SOUTH -> REGION_UNION_CAVE_1F"), can_flash)
        set_rule(get_entrance("REGION_ROUTE_33 -> REGION_UNION_CAVE_1F"), can_flash)
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:TRAINER -> REGION_UNION_CAVE_B1F:NORTH"), can_flash)

    # Route 33
    if rematchsanity():
        safe_set_location_rule("HIKER_ANTHONY_OLIVINE",
                               lambda state: state.has("ENGINE_FLYPOINT_OLIVINE", world.player))
        safe_set_location_rule("HIKER_ANTHONY_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("HIKER_ANTHONY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("HIKER_ANTHONY_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Azalea Town
    if "Slowpoke Well" in world.options.dark_areas:
        set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_SLOWPOKE_WELL_B1F"), can_flash)

    slowpoke_well_rule = lambda state: can_strength(state) and can_surf(state) and state.has(
        "EVENT_CLEARED_SLOWPOKE_WELL", world.player)

    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F -> REGION_SLOWPOKE_WELL_B1F:WEST"),
             slowpoke_well_rule)

    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F:WEST -> REGION_SLOWPOKE_WELL_B1F"), slowpoke_well_rule)

    set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    safe_set_location_rule("Azalea Town - Rival",
                           lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
    set_rule(get_location("EVENT_BEAT_AZALEA_RIVAL"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    set_rule(get_location("Azalea Town - Lure Ball from Kurt"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    if Shopsanity.apricorns in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_KURTS_HOUSE -> REGION_MART_KURTS_BALLS"),
                 lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Red Apricorn"),
                 lambda state: state.has("Red Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Grn Apricorn"),
                 lambda state: state.has("Grn Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Blu Apricorn"),
                 lambda state: state.has("Blu Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Ylw Apricorn"),
                 lambda state: state.has("Ylw Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Blk Apricorn"),
                 lambda state: state.has("Blk Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Wht Apricorn"),
                 lambda state: state.has("Wht Apricorn", world.player))
        set_rule(get_location("Azalea Town - Kurt's Ball Shop - Pnk Apricorn"),
                 lambda state: state.has("Pnk Apricorn", world.player))

    set_rule(get_location("Charcoal Kiln - Charcoal"), lambda state: state.has("EVENT_HERDED_FARFETCHD", world.player))

    if world.options.level_scaling:
        set_rule(get_location("RIVAL_BAYLEEF_AZALEA"),
                 lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
        set_rule(get_location("RIVAL_CROCONAW_AZALEA"),
                 lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
        set_rule(get_location("RIVAL_QUILAVA_AZALEA"),
                 lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    # Ilex Forest

    if "Ilex Forest" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ILEX_FOREST_AZALEA_GATE -> REGION_ILEX_FOREST:SOUTH"), can_flash)
        set_rule(get_entrance("REGION_ROUTE_34_ILEX_FOREST_GATE -> REGION_ILEX_FOREST:NORTH"), can_flash)

    if not world.options.remove_ilex_cut_tree:
        set_rule(get_entrance("REGION_ILEX_FOREST:NORTH -> REGION_ILEX_FOREST:SOUTH"), can_cut)
        set_rule(get_entrance("REGION_ILEX_FOREST:SOUTH -> REGION_ILEX_FOREST:NORTH"), can_cut)

    celebi_rule = lambda state: state.has("GS Ball", world.player) and state.has("EVENT_CLEARED_SLOWPOKE_WELL",
                                                                                 world.player)
    if world.options.level_scaling:
        set_rule(get_location("Celebi"), celebi_rule)
    if world.options.static_pokemon_required:
        set_rule(get_location("Static_Celebi_1"), celebi_rule)

    set_rule(get_location("EVENT_HERDED_FARFETCHD"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    set_rule(get_location("Ilex Forest - HM01 from Farfetch'd Guy"),
             lambda state: state.has("EVENT_HERDED_FARFETCHD", world.player))

    # Route 34
    set_rule(get_entrance("REGION_ROUTE_34 -> REGION_ROUTE_34:WATER"), can_surf)

    if rematchsanity():
        safe_set_location_rule("PICNICKER_GINA_MAHOGANY",
                               lambda state: state.has("ENGINE_FLYPOINT_MAHOGANY", world.player))
        safe_set_location_rule("PICNICKER_GINA_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))
        safe_set_location_rule("CAMPER_TODD_CIANWOOD",
                               lambda state: state.has("ENGINE_FLYPOINT_CIANWOOD", world.player))
        safe_set_location_rule("CAMPER_TODD_BLACKTHORN",
                               lambda state: state.has("ENGINE_FLYPOINT_BLACKTHORN", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("CAMPER_TODD_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("PICNICKER_GINA_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("CAMPER_TODD_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("PICNICKER_GINA_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 34 - Leaf Stone from Gina"),
                 lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player) and can_phone_call(state))

    # Goldenrod City
    set_rule(get_location("Goldenrod City - Squirtbottle from Flower Shop"),
             lambda state: world.logic.has_badge(state, "plain"))
    set_rule(get_location("Goldenrod City - Post-E4 GS Ball from Trade Corner Receptionist"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
    if world.options.level_scaling:
        set_rule(get_location("Eevee"), lambda state: state.has("EVENT_MET_BILL", world.player))
    if world.options.static_pokemon_required:
        set_rule(get_location("Static_Eevee_1"), lambda state: state.has("EVENT_MET_BILL", world.player))

    if Shopsanity.johto_marts in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_ROOF -> REGION_MART_ROOFTOP_SALE"),
                 lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    if not johto_only():
        if world.options.magnet_train_access:
            rule = lambda state: state.has("Pass", world.player) and state.has("EVENT_RESTORED_POWER_TO_KANTO",
                                                                               world.player)
        else:
            rule = lambda state: state.has("Pass", world.player)
        set_rule(get_entrance("REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
                 rule)

    set_rule(get_location("Goldenrod City - Exchange Eon Mail in Pokecenter"),
             lambda state: state.has("EVENT_GOT_EON_MAIL_FROM_EUSINE", world.player))

    # Underground

    if "Goldenrod Underground" in world.options.dark_areas:
        set_rule(get_entrance("REGION_GOLDENROD_CITY -> REGION_GOLDENROD_UNDERGROUND"), can_flash)
        set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES -> REGION_GOLDENROD_UNDERGROUND"),
                 can_flash)

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES"),
             lambda state: state.has("Basement Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F -> REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE -> REGION_GOLDENROD_DEPT_STORE_B1F"),
             lambda state: state.has("Card Key", world.player))

    has_rockets_requirement = world.logic.has_rockets_requirement()

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND_WAREHOUSE -> REGION_GOLDENROD_UNDERGROUND_WAREHOUSE:TAKEOVER"),
             has_rockets_requirement)

    set_rule(get_entrance(
        "REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES:TAKEOVER"),
        has_rockets_requirement)

    if Shopsanity.game_corners in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_GOLDENROD_GAME_CORNER -> REGION_MART_GOLDENROD_GAME_CORNER"),
                 lambda state: state.has("Coin Case", world.player))

    if world.options.static_pokemon_required:
        set_rule(get_location("Static_GoldenrodGameCorner1_1"), lambda state: state.has("Coin Case", world.player))
        set_rule(get_location("Static_GoldenrodGameCorner2_1"), lambda state: state.has("Coin Case", world.player))
        set_rule(get_location("Static_GoldenrodGameCorner3_1"), lambda state: state.has("Coin Case", world.player))

    if world.options.level_scaling:
        set_rule(get_location("GoldenrodGameCorner1"), lambda state: state.has("Coin Case", world.player))
        set_rule(get_location("GoldenrodGameCorner2"), lambda state: state.has("Coin Case", world.player))
        set_rule(get_location("GoldenrodGameCorner2"), lambda state: state.has("Coin Case", world.player))

    # Radio Tower
    set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_2F:TAKEOVER"), has_rockets_requirement)

    if Shopsanity.blue_card in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_MART_BLUE_CARD"),
                 lambda state: state.has("Blue Card", world.player))

        blue_card_points = (2, 2, 3, 3, 5, 5, 5, 5, 5)

        for i, points in enumerate(blue_card_points):
            slot_name = get_mart_slot_location_name("MART_BLUE_CARD", i)
            set_rule(get_location(f"Radio Tower 2F - Blue Card Shop - {slot_name}"),
                     lambda state, num_points=points: state.has("Blue Card Point", world.player, count=num_points))

    set_rule(get_entrance("REGION_RADIO_TOWER_3F:NOCARDKEY -> REGION_RADIO_TOWER_3F:CARDKEY"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_location("Radio Tower 3F - TM11 from Woman"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_location("Radio Tower 4F - Pink Bow from Mary"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    if world.options.level_scaling:
        set_rule(get_location("GRUNTM_3"), has_rockets_requirement)

    safe_set_location_rule("Radio Tower 1F - Grunt", has_rockets_requirement)

    # Route 35
    set_rule(get_location("Route 35 - HP Up after delivering Kenya"),
             lambda state: state.has("EVENT_GAVE_KENYA", world.player))

    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_35:FRUITTREE"), can_surf)

    if rematchsanity():
        safe_set_location_rule("BUG_CATCHER_ARNIE_LAKE",
                               lambda state: state.has("ENGINE_FLYPOINT_LAKE_OF_RAGE", world.player))
        safe_set_location_rule("BUG_CATCHER_ARNIE_BLACKTHORN",
                               lambda state: state.has("ENGINE_FLYPOINT_BLACKTHORN", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("BUG_CATCHER_ARNIE_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("BUG_CATCHER_ARNIE_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # National Park
    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        set_rule(get_entrance("REGION_ROUTE_35_NATIONAL_PARK_GATE -> REGION_ROUTE_35_NATIONAL_PARK_GATE:BIKE"),
                 lambda state: state.has("Bicycle", world.player))
        set_rule(get_entrance("REGION_ROUTE_36_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK"),
                 lambda state: state.has("Bicycle", world.player))
        set_rule(get_entrance("REGION_ROUTE_36_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK:CONTEST"),
                 lambda state: state.has("Bicycle", world.player))

    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        request_pokemon = world.generated_request_pokemon[5]
        set_rule(get_location("National Park - Nugget from Beverly"),
                 lambda state, request=request_pokemon: can_phone_call(state) and state.has(request, world.player))

    if "Bug Catching Contest" not in world.options.wild_encounter_methods_required and world.is_universal_tracker:
        for i in range(len(world.generated_contest)):
            set_rule(get_location(f"Bug Catching Contest Slot {i + 1}"),
                     lambda state: state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player))

    if rematchsanity():
        safe_set_location_rule("SCHOOLBOY_JACK_OLIVINE",
                               lambda state: state.has("ENGINE_FLYPOINT_OLIVINE", world.player))
        safe_set_location_rule("SCHOOLBOY_JACK_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("SCHOOLBOY_JACK_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("SCHOOLBOY_JACK_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Sudowoodo
    has_squirtbottle = lambda state: state.has("Squirtbottle", world.player)
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_37"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_36:WEST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_36:EAST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_37"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:EAST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:WEST"), has_squirtbottle)

    if world.options.level_scaling:
        set_rule(get_location("Sudowoodo"), has_squirtbottle)
    if world.options.static_pokemon_required:
        set_rule(get_location("Static_Sudowoodo_1"), has_squirtbottle)

    # Route 36
    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_36:WEST"), can_cut)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_35"), can_cut)

    set_rule(get_location("EVENT_SAW_SUICUNE_ON_ROUTE_36"),
             lambda state: state.has("EVENT_RELEASED_THE_BEASTS", world.player))

    if rematchsanity():
        safe_set_location_rule("SCHOOLBOY_ALAN_OLIVINE",
                               lambda state: state.has("ENGINE_FLYPOINT_OLIVINE", world.player))
        safe_set_location_rule("SCHOOLBOY_ALAN_BLACKTHORN",
                               lambda state: state.has("ENGINE_FLYPOINT_BLACKTHORN", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("SCHOOLBOY_ALAN_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("SCHOOLBOY_ALAN_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 36 - Fire Stone from Alan"), can_phone_call)

    set_rule(get_location("Route 36 - TM08 from Rock Smash Guy"), has_squirtbottle)

    # Ecruteak City
    set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM"),
             lambda state: state.has("EVENT_BURNED_TOWER_MORTY", world.player))

    if "Burned Tower" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_BURNED_TOWER_1F"), can_flash)

    set_rule(get_location("Burned Tower 1F - Item"), can_rock_smash)
    set_rule(get_location("Burned Tower B1F - Item"), can_strength)

    set_rule(get_entrance("REGION_ECRUTEAK_TIN_TOWER_ENTRANCE -> REGION_WISE_TRIOS_ROOM"),
             lambda state: state.has("Clear Bell", world.player))
    set_rule(get_entrance("REGION_TIN_TOWER_1F -> REGION_TIN_TOWER_2F"),
             lambda state: state.has("Rainbow Wing", world.player))

    set_rule(get_location("EVENT_FOUGHT_HO_OH"), lambda state: state.has("Rainbow Wing", world.player))
    if world.options.level_scaling:
        set_rule(get_location("Ho_Oh"), lambda state: state.has("Rainbow Wing", world.player))
    if world.options.static_pokemon_required:
        set_rule(get_location("Static_Ho_Oh_1"), lambda state: state.has("Rainbow Wing", world.player))

    set_rule(get_location("Tin Tower 1F - Rainbow Wing"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    set_rule(get_location("EVENT_GOT_EON_MAIL_FROM_EUSINE"), lambda state: state.has_all(
        ("EVENT_SAW_SUICUNE_ON_ROUTE_36", "EVENT_SAW_SUICUNE_ON_ROUTE_42", "EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY"),
        world.player))

    # Route 38
    if rematchsanity():
        safe_set_location_rule("SCHOOLBOY_CHAD_MAHOGANY",
                               lambda state: state.has("ENGINE_FLYPOINT_MAHOGANY", world.player))
        safe_set_location_rule("SCHOOLBOY_CHAD_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))
        safe_set_location_rule("LASS_DANA_CIANWOOD",
                               lambda state: state.has("ENGINE_FLYPOINT_CIANWOOD", world.player))
        safe_set_location_rule("LASS_DANA_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("SCHOOLBOY_CHAD_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("LASS_DANA_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("SCHOOLBOY_CHAD_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("LASS_DANA_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 38 - Thunderstone from Dana"), can_phone_call)

    # Route 39
    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        request_pokemon = world.generated_request_pokemon[6]
        set_rule(get_location("Route 39 - Nugget from Derek"),
                 lambda state, request=request_pokemon: can_phone_call(state) and state.has(request, world.player))

    # Olivine City
    set_rule(get_location("EVENT_JASMINE_RETURNED_TO_GYM"), lambda state: state.has("Secretpotion", world.player))

    if "Olivine Lighthouse" in world.options.dark_areas:
        set_rule(get_entrance("REGION_OLIVINE_CITY -> REGION_OLIVINE_LIGHTHOUSE_1F"), can_flash)

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_OLIVINE_LIGHTHOUSE_2F -> REGION_OLIVINE_LIGHTHOUSE_2F:POWER"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and can_phone_call(state))

    if not johto_only():

        if world.options.ss_aqua_access:
            ship_rule = lambda state: state.has("S.S. Ticket", world.player) and state.has(
                "EVENT_JASMINE_RETURNED_TO_GYM", world.player)
        else:
            ship_rule = lambda state: state.has("S.S. Ticket", world.player)

        set_rule(get_entrance("REGION_OLIVINE_PORT -> REGION_FAST_SHIP_1F"), ship_rule)

        set_rule(get_entrance("REGION_FAST_SHIP_1F -> REGION_OLIVINE_PORT"),
                 lambda state: state.has("EVENT_FAST_SHIP_LAZY_SAILOR", world.player))

        if hidden():
            set_rule(get_location("Olivine Port - Hidden Item in Buoy"),
                     lambda state: ship_rule(state) and can_surf(state))

    set_rule(get_entrance("REGION_OLIVINE_GYM -> REGION_OLIVINE_GYM:JASMINE"),
             lambda state: state.has("EVENT_JASMINE_RETURNED_TO_GYM", world.player))

    if rematchsanity():
        safe_set_location_rule("SAILOR_HUEY_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("SAILOR_HUEY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("SAILOR_HUEY_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Route 40
    set_rule(get_entrance("REGION_ROUTE_40 -> REGION_ROUTE_40:WATER"), can_surf)

    if hidden():
        set_rule(get_location("Route 40 - Hidden Item in Rock"), can_rock_smash)

    # Route 41
    if hidden():
        set_rule(get_location("Route 41 - Hidden Item on Southwest Island"), can_surf_and_whirlpool)
    if "Whirl Islands" in world.options.dark_areas:
        whirl_access = lambda state: can_surf_and_whirlpool(state) and can_flash(state)
    else:
        whirl_access = lambda state: can_surf_and_whirlpool(state)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NW"), whirl_access)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NE"), whirl_access)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SW"), whirl_access)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SE"), whirl_access)

    set_rule(get_location("EVENT_FOUGHT_LUGIA"), lambda state: state.has("Silver Wing", world.player))
    if world.options.level_scaling:
        set_rule(get_location("Lugia"), lambda state: state.has("Silver Wing", world.player))
    if world.options.static_pokemon_required:
        set_rule(get_location("Static_Lugia_1"), lambda state: state.has("Silver Wing", world.player))

    # Cianwood
    set_rule(get_entrance("REGION_CIANWOOD_CITY -> REGION_ROUTE_41"), can_surf)
    if hidden():
        set_rule(get_location("Cianwood City - Hidden Item in West Rock"), can_rock_smash)
        set_rule(get_location("Cianwood City - Hidden Item in North Rock"), can_rock_smash)

    set_rule(get_location("Cianwood City - HM02 from Chuck's Wife"),
             lambda state: world.logic.has_beaten_gym(state, "chuck"))

    set_rule(get_entrance("REGION_CIANWOOD_GYM -> REGION_CIANWOOD_GYM:STRENGTH"), can_strength)

    safe_set_location_rule("Cianwood City - Mysticalman Eusine",
                           lambda state: state.has("EVENT_RELEASED_THE_BEASTS", world.player))

    if world.options.level_scaling:
        set_rule(get_location("MYSTICALMAN_EUSINE"),
                 lambda state: state.has("EVENT_RELEASED_THE_BEASTS", world.player))

    set_rule(get_location("EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY"),
             lambda state: state.has("EVENT_RELEASED_THE_BEASTS", world.player))

    # Route 42
    if world.options.route_42_access.value == Route42Access.option_vanilla:
        set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), can_surf)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), can_surf)

        set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), can_surf)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), can_surf)
    elif world.options.route_42_access.value in \
            (Route42Access.option_whirlpool, Route42Access.option_whirlpool_open_mortar):
        set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), can_surf_and_whirlpool)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), can_surf_and_whirlpool)

        set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), can_surf_and_whirlpool)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), can_surf_and_whirlpool)
    # else: blocked -> connection doesn't even exist

    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:CENTERFRUIT"), can_cut)

    set_rule(get_location("EVENT_SAW_SUICUNE_ON_ROUTE_42"),
             lambda state: state.has("EVENT_RELEASED_THE_BEASTS", world.player))

    if hidden():
        set_rule(get_location("Route 42 - Hidden Item in Pond Rock"), can_surf)

    if rematchsanity():
        safe_set_location_rule("FISHER_TULLY_ROCKETHQ",
                               lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("FISHER_TULLY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("FISHER_TULLY_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 42 - Water Stone from Tully"), can_phone_call)

    # Mt Mortar
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_2F_OUTSIDE"),
             can_surf_and_waterfall)

    if world.options.mount_mortar_access:
        set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:WEST:ENTRANCE -> REGION_MOUNT_MORTAR_1F_OUTSIDE:WEST"),
                 can_rock_smash)
        set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:WEST -> REGION_MOUNT_MORTAR_1F_OUTSIDE:WEST:ENTRANCE"),
                 can_rock_smash)
        set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:EAST:ENTRANCE -> REGION_MOUNT_MORTAR_1F_OUTSIDE:EAST"),
                 can_rock_smash)
        set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:EAST -> REGION_MOUNT_MORTAR_1F_OUTSIDE:EAST:ENTRANCE"),
                 can_rock_smash)

    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_1F_OUTSIDE:BELOW_WATERFALL"),
             can_surf)
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:BELOW_WATERFALL -> REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER"),
             can_surf)

    # 1F Inside Front
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_INSIDE:FRONT -> REGION_MOUNT_MORTAR_1F_INSIDE:STRENGTH"),
             can_strength)
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_INSIDE:STRENGTH -> REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"),
             can_strength)

    # 1F C -> B1F Everything needs surf so im being lazy
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_B1F"), can_surf)

    # Behind boulder, need to come down from 2F for this
    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F:BACK -> REGION_MOUNT_MORTAR_B1F"),
             lambda state: can_strength(state) and can_surf_and_waterfall(state))

    if "Mount Mortar" in world.options.dark_areas:
        add_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:WEST -> REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"), can_flash)
        add_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:EAST -> REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"), can_flash)
        add_rule(get_entrance("REGION_MOUNT_MORTAR_2F_OUTSIDE -> REGION_MOUNT_MORTAR_2F_INSIDE"), can_flash)
        add_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_B1F"), can_flash)

        if world.options.route_42_access.value in (Route42Access.option_blocked,
                                                   Route42Access.option_whirlpool_open_mortar):
            set_rule(
                get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:BELOW_WATERFALL -> REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"),
                can_flash)

    # Mahogany Town
    if Shopsanity.johto_marts in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_MAHOGANY_MART_1F -> REGION_MART_MAHOGANY_2"),
                 lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_GYM"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_MART_1F -> REGION_TEAM_ROCKET_BASE_B1F"),
             lambda state: state.has("EVENT_DECIDED_TO_HELP_LANCE", world.player))

    has_route_44_access = world.logic.has_route_44_access()

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_ROUTE_44"), has_route_44_access)
    if not world.options.randomize_fly_unlocks and world.options.fly_cheese == FlyCheese.option_in_logic:
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_MAHOGANY_TOWN"),
                 lambda state: has_route_44_access(state) or can_fly(state))
    elif (not world.options.randomize_fly_unlocks
          and world.options.fly_cheese == FlyCheese.option_out_of_logic and world.is_universal_tracker):
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_MAHOGANY_TOWN"),
                 lambda state: has_route_44_access(state) or (
                         state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player) and can_fly(state)))
    else:
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_MAHOGANY_TOWN"), has_route_44_access)

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_ROUTE_44:POWER"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and can_phone_call(state))

    # Route 43
    set_rule(get_entrance("REGION_ROUTE_43 -> REGION_ROUTE_43:FRUITTREE"),
             lambda state: can_cut(state) and can_surf(state))

    set_rule(get_location("Route 43 - TM36 from Guard in Gate"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    if rematchsanity():
        safe_set_location_rule("POKEMANIAC_BRENT_ROCKETHQ",
                               lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))
        safe_set_location_rule("PICNICKER_TIFFANY_RADIO",
                               lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

        if world.options.goal == Goal.option_red:
            safe_set_location_rule("POKEMANIAC_BRENT_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("PICNICKER_TIFFANY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("POKEMANIAC_BRENT_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("PICNICKER_TIFFANY_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        request_pokemon = world.generated_request_pokemon[7]
        set_rule(get_location("Route 43 - Pink Bow from Tiffany"),
                 lambda state, request=request_pokemon: can_phone_call(state) and state.has(request, world.player))

    # Lake of Rage
    if world.options.red_gyarados_access == RedGyaradosAccess.option_whirlpool:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:WATER"), can_surf_and_whirlpool)
    elif world.options.red_gyarados_access == RedGyaradosAccess.option_vanilla:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:WATER"), can_surf)

    set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:CUT"), can_cut)

    if world.options.randomize_pokemon_requests:
        set_rule(get_location("Lake of Rage - Magikarp Prize"),
                 lambda state: state.has("MAGIKARP", world.player) and state.has("EVENT_CLEARED_ROCKET_HIDEOUT",
                                                                                 world.player))

    # Route 44
    set_rule(get_entrance("REGION_ROUTE_44 -> REGION_ROUTE_44:WATER"), can_surf)

    if rematchsanity():
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("BIRD_KEEPER_VANCE_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("FISHER_WILTON_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("BIRD_KEEPER_VANCE_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("FISHER_WILTON_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 44 - Poke Ball from Wilton"), can_phone_call)

    # Ice Path

    if "Ice Path" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_ICE_PATH_1F:WEST"), can_flash)
        set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_ICE_PATH_1F:EAST"), can_flash)
    set_rule(get_entrance("REGION_ICE_PATH_B2F_MAHOGANY_SIDE -> REGION_ICE_PATH_B2F_MAHOGANY_SIDE:MIDDLE"),
             can_strength)

    # Blackthorn
    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_GYM_1F"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_entrance("REGION_BLACKTHORN_GYM_2F -> REGION_BLACKTHORN_GYM_1F:STRENGTH"), can_strength)

    if "Dragons Den" in world.options.dark_areas:
        dragons_den_access = lambda state: world.logic.has_beaten_gym(state, "clair") and can_flash(state)
    else:
        dragons_den_access = lambda state: world.logic.has_beaten_gym(state, "clair")

    set_rule(get_entrance("REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE -> REGION_DRAGONS_DEN_1F"), dragons_den_access)
    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE"), can_surf)
    set_rule(get_entrance("REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE -> REGION_BLACKTHORN_CITY"), can_surf)

    # Dragons Den
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F -> REGION_DRAGONS_DEN_B1F:WATER"), can_surf)
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:WATER -> REGION_DRAGONS_DEN_B1F:WHIRLPOOL"), can_surf_and_whirlpool)

    # Route 45
    if hidden():
        set_rule(get_location("Route 45 - Hidden Item in Southeast Pond"), can_surf)

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 45 - PP Up from Kenji"), can_phone_call)

        if not world.options.johto_only:
            set_rule(get_entrance("REGION_ROUTE_45 -> REGION_ROUTE_45:POWER"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and can_phone_call(state))

    if rematchsanity():
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("HIKER_PARRY_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("HIKER_PARRY_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Route 46
    if world.options.randomize_phone_call_items and not world.options.johto_only:
        set_rule(get_location("Route 46 - Calcium from Erin"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and can_phone_call(state))

    if rematchsanity():
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("PICNICKER_ERIN_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("PICNICKER_ERIN_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_ROUTE_45 -> REGION_ROUTE_45:POWER"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and can_phone_call(state))

    # Route 26
    if rematchsanity():
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("COOLTRAINERM_GAVEN_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("COOLTRAINERF_BETH_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("COOLTRAINERM_GAVEN_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("COOLTRAINERF_BETH_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Route 27
    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_NEW_BARK_TOWN"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_ROUTE_27:WESTWATER"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:CENTER -> REGION_ROUTE_27:EAST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:CENTER"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:EASTWHIRLPOOL"), can_surf_and_whirlpool)

    set_rule(get_location("Route 27 - West Item across Water"), can_surf)

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 27 - Star Piece from Jose"), can_phone_call)

    if rematchsanity():
        if world.options.goal == Goal.option_red:
            safe_set_location_rule("BIRD_KEEPER_JOSE_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            safe_set_location_rule("COOLTRAINERF_REENA_CHAMPION",
                                   lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

            if not johto_only():
                safe_set_location_rule("BIRD_KEEPER_JOSE_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))
                safe_set_location_rule("COOLTRAINERF_REENA_POWER",
                                       lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    set_rule(get_location("Tohjo Falls - Item"), can_surf)

    if "Tohjo Falls" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_TOHJO_FALLS:WEST"), can_flash)
        set_rule(get_entrance("REGION_ROUTE_27:CENTER -> REGION_TOHJO_FALLS:EAST"), can_flash)
    set_rule(get_entrance("REGION_TOHJO_FALLS:WEST -> REGION_TOHJO_FALLS:EAST"), can_surf_and_waterfall)
    set_rule(get_entrance("REGION_TOHJO_FALLS:EAST -> REGION_TOHJO_FALLS:WEST"), can_surf_and_waterfall)

    # Victory Road
    has_e4_requirement = world.logic.has_elite_four_requirement()
    if "Victory Road" in world.options.dark_areas:
        vroad_access = lambda state: can_flash(state) and has_e4_requirement(state)
    else:
        vroad_access = has_e4_requirement

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD:ENTRANCE"), vroad_access)

    if world.options.victory_road_access:
        set_rule(get_entrance("REGION_VICTORY_ROAD:ENTRANCE -> REGION_VICTORY_ROAD"), can_strength)

    if "Victory Road" in world.options.dark_areas:
        set_rule(get_entrance("REGION_ROUTE_23 -> REGION_VICTORY_ROAD"), can_flash)

    if johto_only() != JohtoOnly.option_on:
        has_mt_silver_requirement = world.logic.has_mt_silver_requirement()
        set_rule(get_entrance("REGION_ROUTE_28 -> REGION_VICTORY_ROAD_GATE"), has_mt_silver_requirement)
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_28"), has_mt_silver_requirement)
        set_rule(get_location("EVENT_OPENED_MT_SILVER"), has_mt_silver_requirement)

        set_rule(get_location("EVENT_BEAT_RED"), world.logic.has_red_requirement())
        # set_rule(get_location("RED_1"), has_red_requirement)

        # Route 28
        set_rule(get_location("Route 28 - TM47 from Celebrity in House"), can_cut)
        if hidden():
            set_rule(get_location("Route 28 - Hidden Item behind Cut Tree"), can_cut)

        # Silver Cave
        if "Silver Cave" in world.options.dark_areas:
            set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_SILVER_CAVE_ROOM_1"), can_flash)

        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_SILVER_CAVE_OUTSIDE:SURF"), can_surf)
        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE:SURF -> REGION_SILVER_CAVE_OUTSIDE"), can_surf)

        set_rule(get_location("Silver Cave 2F - Northeast Item"), can_surf_and_waterfall)
        set_rule(get_location("Silver Cave 2F - West Item"), can_surf_and_waterfall)

        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2 -> REGION_SILVER_CAVE_ITEM_ROOMS"), can_surf_and_waterfall)

    if not johto_only():

        has_kanto_access_requirement = world.logic.has_kanto_access_requirement()
        set_rule(get_entrance("REGION_ROUTE_22 -> REGION_VICTORY_ROAD_GATE"), has_kanto_access_requirement)
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_22"), has_kanto_access_requirement)

        set_rule(get_entrance("REGION_INDIGO_PLATEAU_POKECENTER_1F -> REGION_INDIGO_PLATEAU_POKECENTER_1F:RIVAL"),
                 lambda state: state.has("EVENT_BEAT_RIVAL_IN_MT_MOON", world.player))

        # Viridian
        set_rule(get_location("Viridian City - TM42 from Sleepy Guy"),
                 lambda state: can_surf_kanto(state) or can_cut_kanto(state))

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_VIRIDIAN_CITY -> REGION_VIRIDIAN_GYM"), kanto_gyms_access)

        set_rule(get_entrance("REGION_VIRIDIAN_GYM -> REGION_VIRIDIAN_GYM:BLUE"),
                 lambda state: state.has("EVENT_VIRIDIAN_GYM_BLUE", world.player))

        # Route 2
        if world.options.route_2_access.value != Route2Access.option_open:
            set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:NORTHEAST"), can_cut_kanto)
        if world.options.route_2_access.value == Route2Access.option_vanilla:
            set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:WEST"), can_cut_kanto)

        if "Digletts Cave" in world.options.dark_areas:
            set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_DIGLETTS_CAVE"), can_flash_kanto)

        set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:SOUTHEAST"), can_cut_kanto)

        set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:WEST"), can_cut_kanto)

        set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:NORTHEAST"), can_cut_kanto)

        set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:SOUTHEAST"), can_cut_kanto)

        # Pewter City
        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_PEWTER_CITY -> REGION_PEWTER_GYM"), kanto_gyms_access)

        # Route 3
        if world.options.route_3_access.value == Route3Access.option_boulder_badge:
            set_rule(get_entrance("REGION_PEWTER_CITY -> REGION_ROUTE_3"),
                     lambda state: world.logic.has_badge(state, "boulder"))
            set_rule(get_entrance("REGION_ROUTE_3 -> REGION_PEWTER_CITY"),
                     lambda state: world.logic.has_badge(state, "boulder"))

        if hidden():
            set_rule(get_location("Mount Moon Square - Hidden Item under Rock"), can_rock_smash)

        if "Mount Moon" in world.options.dark_areas:
            set_rule(get_entrance("REGION_ROUTE_3 -> REGION_MOUNT_MOON"), can_flash_kanto)
            set_rule(get_entrance("REGION_ROUTE_4:WEST -> REGION_MOUNT_MOON"), can_flash_kanto)
            set_rule(get_entrance("REGION_MOUNT_MOON_SQUARE -> REGION_MOUNT_MOON"), can_flash_kanto)

        if world.options.lock_kanto_gyms:
            add_rule(get_entrance("REGION_ROUTE_3 -> REGION_MOUNT_MOON"), kanto_gyms_access)
            add_rule(get_entrance("REGION_ROUTE_4:WEST -> REGION_MOUNT_MOON"), kanto_gyms_access)
            add_rule(get_entrance("REGION_MOUNT_MOON_SQUARE -> REGION_MOUNT_MOON"), kanto_gyms_access)

        # Cerulean
        set_rule(get_entrance("REGION_ROUTE_24 -> REGION_CERULEAN_CITY:SURF"), can_surf_kanto)
        safe_set_location_rule("Route 24 - Grunt",
                               lambda state: state.has("EVENT_CERULEAN_GYM_ROCKET", world.player))

        set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_ROUTE_9"), can_cut_kanto)

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_CERULEAN_GYM"), kanto_gyms_access)

        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_CERULEAN_CITY"), can_cut_kanto)
        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_ROUTE_10_NORTH:SURF"), can_surf_kanto)
        set_rule(get_entrance("REGION_ROUTE_10_NORTH:SURF -> REGION_ROUTE_9"), can_surf_kanto)

        # Route 25
        set_rule(get_location("Route 25 - Item behind Cut Tree"), can_cut_kanto)

        # Power Plant
        set_rule(get_location("EVENT_RESTORED_POWER_TO_KANTO"), lambda state: state.has("Machine Part", world.player))

        set_rule(get_location("Power Plant - TM07 from Manager"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Rock Tunnel
        if "Rock Tunnel" in world.options.dark_areas:
            set_rule(get_entrance("REGION_ROUTE_9 -> REGION_ROCK_TUNNEL_1F"), can_flash_kanto)
            set_rule(get_entrance("REGION_ROUTE_10_SOUTH -> REGION_ROCK_TUNNEL_1F"), can_flash_kanto)

        # Lavender
        if world.options.randomize_pokegear:
            set_rule(get_location("Lavender Radio Tower - EXPN Card"), lambda state: state.has(
                "EVENT_RESTORED_POWER_TO_KANTO", world.player))
        else:
            set_rule(get_location("EVENT_GOT_EXPN_CARD"), lambda state: state.has(
                "EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Route 12
        if world.options.route_12_access:
            set_rule(get_entrance("REGION_ROUTE_12:NORTH -> REGION_ROUTE_12:SOUTH"),
                     lambda state: state.has("Squirtbottle", world.player) or can_surf_kanto(state))
            set_rule(get_entrance("REGION_ROUTE_12:SOUTH -> REGION_ROUTE_12:NORTH"),
                     lambda state: state.has("Squirtbottle", world.player) or can_surf_kanto(state))

        set_rule(get_location("Route 12 - Item behind North Cut Tree"), can_cut_kanto)

        set_rule(get_location("Route 12 - Item behind South Cut Tree across Water"),
                 lambda state: can_cut_kanto(state) and can_surf_kanto(state))

        if hidden():
            set_rule(get_location("Route 12 - Hidden Item on Island"), can_surf_kanto)

        # Route 13
        set_rule(get_entrance("REGION_ROUTE_13 -> REGION_ROUTE_13:CUT"), can_cut_kanto)

        # Route 14
        set_rule(get_entrance("REGION_ROUTE_14 -> REGION_ROUTE_14:CUT"), can_cut_kanto)

        # Vermilion
        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_GYM"),
                     lambda state: (can_cut_kanto(state) or can_surf_kanto(state)) and kanto_gyms_access(state))
        else:
            set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_GYM"),
                     lambda state: can_cut_kanto(state) or can_surf_kanto(state))

        kanto_badges = list(world.logic.badge_items.values())[8:]
        set_rule(get_location("Vermilion City - HP Up from Man nowhere near PokeCenter"),
                 lambda state: state.has_all(kanto_badges, world.player))

        set_rule(get_location("Vermilion City - Lost Item from Guy in Fan Club"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        has_expn = world.logic.has_expn()
        set_rule(get_location("EVENT_FOUGHT_SNORLAX"), has_expn)
        if world.options.level_scaling:
            set_rule(get_location("Snorlax"), has_expn)
        if world.options.static_pokemon_required:
            set_rule(get_location("Static_Snorlax_1"), has_expn)

        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_ROUTE_11"), has_expn)
        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE"), has_expn)

        if "Digletts Cave" in world.options.dark_areas:
            set_rule(get_entrance("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_DIGLETTS_CAVE"),
                     can_flash_kanto)

        if not world.options.randomize_fly_unlocks and world.options.fly_cheese == FlyCheese.option_in_logic:
            digletts_cave_rule = lambda state: has_expn(state) or can_fly(state)
        elif (not world.options.randomize_fly_unlocks
              and world.options.fly_cheese == FlyCheese.option_out_of_logic and world.is_universal_tracker):
            digletts_cave_rule = lambda state: has_expn(state) or (
                    state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player) and can_fly(state))
        else:
            digletts_cave_rule = has_expn

        set_rule(get_entrance("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY"),
                 digletts_cave_rule)
        set_rule(get_entrance("REGION_ROUTE_11 -> REGION_VERMILION_CITY"), digletts_cave_rule)
        set_rule(get_entrance("REGION_VERMILION_PORT -> REGION_FAST_SHIP_1F"), ship_rule)

        if hidden():
            set_rule(get_location("Vermilion Port - Hidden Item in Buoy"),
                     lambda state: ship_rule(state) and can_surf_kanto(state))

        set_rule(get_entrance("REGION_FAST_SHIP_1F -> REGION_VERMILION_PORT"),
                 lambda state: state.has("EVENT_FAST_SHIP_LAZY_SAILOR", world.player))

        # Saffron
        set_rule(get_location("Copycat's House - Pass from Copycat"),
                 lambda state: state.has("Lost Item", world.player))

        if world.options.magnet_train_access:
            rule = lambda state: state.has("Pass", world.player) and state.has("EVENT_RESTORED_POWER_TO_KANTO",
                                                                               world.player)
        else:
            rule = lambda state: state.has("Pass", world.player)
        set_rule(get_entrance("REGION_SAFFRON_MAGNET_TRAIN_STATION -> REGION_GOLDENROD_MAGNET_TRAIN_STATION"), rule)

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_SAFFRON_GYM"), kanto_gyms_access)

        has_tea = world.logic.has_tea()

        if "North" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_5_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_5_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "East" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_8_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_8_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "South" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_6_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_6_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "West" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_7_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_7_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        # Underground Paths
        if world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_north_south,
                                                              UndergroundsRequirePower.option_both):
            set_rule(get_entrance("REGION_ROUTE_5 -> REGION_ROUTE_5_UNDERGROUND_PATH_ENTRANCE"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

            set_rule(get_entrance("REGION_ROUTE_6 -> REGION_ROUTE_6_UNDERGROUND_PATH_ENTRANCE"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        if (world.options.east_west_underground
                and world.options.undergrounds_require_power.value in (
                        UndergroundsRequirePower.option_east_west,
                        UndergroundsRequirePower.option_both)):
            set_rule(get_entrance("REGION_ROUTE_7 -> REGION_ROUTE_8"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

            set_rule(get_entrance("REGION_ROUTE_8 -> REGION_ROUTE_7"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Route 8
        set_rule(get_entrance("REGION_ROUTE_8 -> REGION_ROUTE_8:CUT"), can_cut_kanto)
        set_rule(get_entrance("REGION_ROUTE_8:CUT -> REGION_ROUTE_8"), can_cut_kanto)

        # Celadon
        set_rule(get_entrance("REGION_CELADON_CITY -> REGION_CELADON_CITY:GYM_ENTRANCE"), can_cut_kanto)
        set_rule(get_entrance("REGION_CELADON_CITY:GYM_ENTRANCE -> REGION_CELADON_CITY"), can_cut_kanto)

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_CELADON_CITY:GYM_ENTRANCE -> REGION_CELADON_GYM"), kanto_gyms_access)

        if Shopsanity.game_corners in world.options.shopsanity.value:
            set_rule(
                get_entrance("REGION_CELADON_GAME_CORNER_PRIZE_ROOM -> REGION_MART_CELADON_GAME_CORNER_PRIZE_ROOM"),
                lambda state: state.has("Coin Case", world.player))

        if world.options.static_pokemon_required:
            set_rule(get_location("Static_CeladonGameCornerPrizeRoom1_1"),
                     lambda state: state.has("Coin Case", world.player))
            set_rule(get_location("Static_CeladonGameCornerPrizeRoom2_1"),
                     lambda state: state.has("Coin Case", world.player))
            set_rule(get_location("Static_CeladonGameCornerPrizeRoom3_1"),
                     lambda state: state.has("Coin Case", world.player))

        if world.options.level_scaling:
            set_rule(get_location("CeladonGameCornerPrizeRoom1"), lambda state: state.has("Coin Case", world.player))
            set_rule(get_location("CeladonGameCornerPrizeRoom2"), lambda state: state.has("Coin Case", world.player))
            set_rule(get_location("CeladonGameCornerPrizeRoom3"), lambda state: state.has("Coin Case", world.player))

        diploma_count = len(world.logic.available_pokemon) if not world.is_universal_tracker else world.ut_slot_data[
            "logically_available_pokemon_count"]
        set_rule(get_location("EVENT_OBTAINED_DIPLOMA"),
                 lambda state: world.logic.has_n_pokemon(state, diploma_count))

        # Route 16
        set_rule(get_entrance("REGION_ROUTE_16 -> REGION_ROUTE_16:CUT"), can_cut_kanto)
        set_rule(get_entrance("REGION_ROUTE_16:CUT -> REGION_ROUTE_16"), can_cut_kanto)

        # Cycling Road
        set_rule(get_entrance("REGION_ROUTE_16 -> REGION_ROUTE_17"), lambda state: state.has("Bicycle", world.player))

        set_rule(get_entrance("REGION_ROUTE_17_ROUTE_18_GATE -> REGION_ROUTE_17"),
                 lambda state: state.has("Bicycle", world.player))

        # Route 15
        set_rule(get_location("Route 15 - Item"), can_cut_kanto)

        # Fuchsia City
        set_rule(get_entrance("REGION_FUCHSIA_CITY -> REGION_FUCHSIA_CITY:CUT"), can_cut_kanto)
        set_rule(get_entrance("REGION_FUCHSIA_CITY:CUT -> REGION_FUCHSIA_CITY"), can_cut_kanto)

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_FUCHSIA_CITY -> REGION_FUCHSIA_GYM"), kanto_gyms_access)

        set_rule(get_entrance("REGION_ROUTE_19:GATE_ENTRANCE -> REGION_ROUTE_19"),
                 lambda state: state.has("EVENT_CINNABAR_ROCKS_CLEARED", world.player) and can_surf_kanto(state))

        # Cinnabar
        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_20"), can_surf_kanto)

        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_21"), can_surf_kanto)

        set_rule(get_entrance("REGION_PALLET_TOWN -> REGION_ROUTE_21"), can_surf_kanto)

        if world.options.lock_kanto_gyms:
            set_rule(get_entrance("REGION_ROUTE_20 -> REGION_SEAFOAM_GYM"), kanto_gyms_access)

        if world.options.goal == Goal.option_unown_hunt:
            for location, unown in world.generated_unown_signs.items():
                chamber_event = get_chamber_event_for_unown(unown)
                set_rule(get_location(location),
                         lambda state, event=chamber_event: state.has(event, world.player))
                set_rule(get_location(f"{location}_Encounter"),
                         lambda state, event=chamber_event: state.has(event, world.player))

        if world.options.randomize_pokemon_requests:
            bills_grandpa_locations = (
                "Bill's House - Everstone from Bill's Grandpa",
                "Bill's House - Leaf Stone from Bill's Grandpa",
                "Bill's House - Water Stone from Bill's Grandpa",
                "Bill's House - Fire Stone from Bill's Grandpa",
                "Bill's House - Thunderstone from Bill's Grandpa"
            )

            for i, location in enumerate(bills_grandpa_locations):
                required_pokemon = world.generated_request_pokemon[:i + 1]
                set_rule(get_location(location),
                         lambda state, pokemon=required_pokemon: state.has_all(pokemon, world.player))

        for trade_id, trade in world.generated_trades.items():
            if world.options.trades_required and world.is_universal_tracker:
                rule = lambda state, request=trade.requested_pokemon: state.has(request, world.player) or state.has(
                    PokemonCrystalGlitchedToken.TOKEN_NAME, world.player)
            elif world.is_universal_tracker:
                rule = lambda state: state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player)
            else:
                rule = lambda state, request=trade.requested_pokemon: state.has(request, world.player)
            safe_set_location_rule(trade_id, rule)

    if world.options.require_itemfinder:
        if world.options.require_itemfinder == RequireItemfinder.option_logically_required and world.is_universal_tracker:
            rule = lambda state: state.has("Itemfinder", world.player) or state.has(
                PokemonCrystalGlitchedToken.TOKEN_NAME, world.player)
        else:
            rule = lambda state: state.has("Itemfinder", world.player)

        for location in world.multiworld.get_locations(world.player):
            if "Hidden" in location.tags:
                add_rule(location, rule)

    if world.options.grasssanity:
        for region in world.get_regions():
            if region.name in data.grass_tiles:
                region_data = data.regions[region.name]
                rule = can_cut if region_data.johto or region_data.silver_cave else can_cut_kanto
                add_rule(get_entrance(f"{region.name} -> {region.name}:GRASS"), rule)

    for pokemon_id in world.generated_dexsanity:
        pokemon_data = world.generated_pokemon[pokemon_id]
        set_rule(get_location(f"Pokedex - {pokemon_data.friendly_name}"),
                 lambda state, species_id=pokemon_id: state.has(species_id, world.player))

    logically_available_pokemon_count = len(world.logic.available_pokemon) if not world.is_universal_tracker else \
        world.ut_slot_data["logically_available_pokemon_count"]

    for dexcountsanity_count in world.generated_dexcountsanity[:-1]:
        logical_count = min(logically_available_pokemon_count,
                            dexcountsanity_count + world.options.dexcountsanity_leniency)
        set_rule(get_location(f"Pokedex - Catch {dexcountsanity_count} Pokemon"),
                 lambda state, count=logical_count: world.logic.has_n_pokemon(state, count))

    if world.generated_dexcountsanity:
        logical_count = min(logically_available_pokemon_count,
                            world.generated_dexcountsanity[-1] + world.options.dexcountsanity_leniency)
        set_rule(get_location("Pokedex - Final Catch"),
                 lambda state, count=logical_count: world.logic.has_n_pokemon(state, count))

    for encounter_key, encounter_access in world.logic.wild_regions.items():

        if encounter_access is LogicalAccess.Inaccessible: continue
        if encounter_access is LogicalAccess.OutOfLogic and not world.is_universal_tracker: continue

        rule = None

        if encounter_key.encounter_type is EncounterType.Water:
            region = world.get_region(encounter_key.region_name())
            parent_region = region.entrances[0].parent_region
            region_data = data.regions[parent_region.name]
            rule = can_surf if (region_data.johto or region_data.silver_cave) else can_surf_kanto
        elif encounter_key.encounter_type is EncounterType.Fish:
            rule = world.logic.fishing_rod_rules[encounter_key.fishing_rod]
        elif encounter_key.encounter_type is EncounterType.Tree:
            rule = can_headbutt
        elif encounter_key.encounter_type is EncounterType.RockSmash:
            rule = can_rock_smash
        elif encounter_key.encounter_type is EncounterType.Static:
            if not world.is_universal_tracker: continue

            location = get_location(f"{encounter_key.region_name()}_1")
            if encounter_access is LogicalAccess.OutOfLogic:
                add_rule(location, lambda state: state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player))
            continue

        region_name = encounter_key.region_name()
        for i, encounter in enumerate(world.generated_wild[encounter_key]):
            location = get_location(f"{region_name}_{i + 1}")

            if rule:
                set_rule(location, rule)

            if encounter.pokemon == "UNOWN":
                add_rule(location, lambda state: state.has_any(unown_unlocks, world.player))

            if encounter_access is LogicalAccess.OutOfLogic:
                add_rule(location, lambda state: state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player))

    def evolution_logic(state: CollectionState, evolved_from: str, evolutions: list[EvolutionData],
                        access: LogicalAccess) -> bool:
        if not state.has(evolved_from, world.player): return False
        logical_access_satisfied = access is LogicalAccess.InLogic or (
                access is LogicalAccess.OutOfLogic and state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player))
        for evo in evolutions:
            if evo.evo_type is EvolutionType.Level or (
                    evo.evo_type is EvolutionType.Stats and state.has_any(evolution_item_unlocks, world.player)):
                if state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player): return True
                if access is LogicalAccess.OutOfLogic: return False
                required_gyms = ((evo.level - 1) // world.options.evolution_gym_levels) + 1
                if world.logic.has_beaten_n_gyms(state, required_gyms): return True
            if evo.evo_type is EvolutionType.Item and state.has_any(evolution_item_unlocks,
                                                                    world.player) and logical_access_satisfied: return True
            if evo.evo_type is EvolutionType.Happiness and state.has_any(happiness_unlocks,
                                                                         world.player) and logical_access_satisfied: return True

        return False

    locations_to_evolutions = defaultdict[str, list[EvolutionData]](list)
    locations_to_pokemon = dict[str, str]()
    locations_to_logic = defaultdict[str, LogicalAccess](lambda: LogicalAccess.Inaccessible)

    for evolvee, evolutions in world.logic.evolution.items():
        for evo_access in evolutions:
            evolution, logical_access = evo_access
            if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic: continue
            location_name = evolution_location_name(world, evolvee, evolution.pokemon)
            locations_to_pokemon[location_name] = evolvee
            locations_to_evolutions[location_name].append(evolution)
            if locations_to_logic[location_name] is not LogicalAccess.InLogic:
                locations_to_logic[location_name] = logical_access

    seen_locations = set()

    for location_name, evo_data in locations_to_evolutions.items():
        evolves_from = locations_to_pokemon[location_name]
        logical_access = locations_to_logic[location_name]
        if location_name not in seen_locations:
            set_rule(
                get_location(location_name),
                lambda state, from_pokemon=evolves_from, evolutions=evo_data, access=logical_access:
                evolution_logic(state, from_pokemon, evolutions, access)
            )
            seen_locations.add(location_name)
        else:
            add_rule(
                get_location(location_name),
                lambda state, from_pokemon=evolves_from, evolutions=evo_data, access=logical_access:
                evolution_logic(state, from_pokemon, evolutions, access),
                combine="or"
            )

    def breeding_logic(state: CollectionState, breeders_access: set[tuple[str, LogicalAccess]]) -> bool:
        for breeder_access in breeders_access:
            breeder, access = breeder_access
            if state.has(breeder, world.player):
                if access is LogicalAccess.InLogic:
                    return True
                elif (access is LogicalAccess.OutOfLogic
                      and state.has(PokemonCrystalGlitchedToken.TOKEN_NAME, world.player)):
                    return True
        return False

    if world.options.breeding_methods_required or world.is_universal_tracker:
        set_rule(get_entrance("Menu -> Breeding"), lambda state: state.has("EVENT_UNLOCKED_DAY_CARE", world.player))

        if world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto:
            add_rule(get_entrance("Menu -> Breeding"),
                     lambda state: state.has("DITTO", world.player) or state.has(PokemonCrystalGlitchedToken.TOKEN_NAME,
                                                                                 world.player))

    for base_form_id, breeders in world.logic.breeding.items():
        logical_access = [access for _, access in breeders]
        if not world.is_universal_tracker and (LogicalAccess.InLogic not in logical_access): continue
        set_rule(
            get_location(f"Hatch {world.generated_pokemon[base_form_id].friendly_name}"),
            lambda state, b=breeders: breeding_logic(state, b)
        )


def verify_hm_accessibility(world: "PokemonCrystalWorld") -> None:
    logic = world.logic

    def can_use_hm(state: CollectionState, hm: str) -> bool:
        if hm == "CUT":
            return logic.can_cut()(state) or logic.can_cut(True)(state)
        elif hm == "FLY":
            return logic.can_fly()(state)
        elif hm == "SURF":
            return logic.can_surf()(state) or logic.can_surf(True)(state)
        elif hm == "STRENGTH":
            return logic.can_strength()(state) or logic.can_strength(True)(state)
        elif hm == "FLASH":
            return logic.can_flash(allow_ool=False)(state) or logic.can_flash(True, allow_ool=False)(state)
        elif hm == "WHIRLPOOL":
            return logic.can_whirlpool()(state) or logic.can_whirlpool(True)(state)
        elif hm == "WATERFALL":
            return logic.can_waterfall()(state) or logic.can_waterfall(True)(state)
        elif hm == "HEADBUTT":
            return logic.can_headbutt()(state)
        elif hm == "ROCK_SMASH":
            return logic.can_rock_smash()(state)
        return False

    def do_verify(hms: list[str]):
        hms_to_verify = hms.copy()
        unverified_hms = []
        last_hm = None

        while hms_to_verify:
            state = world.get_world_collection_state()
            hm_to_verify = hms_to_verify[0]
            if not can_use_hm(state, hm_to_verify):

                if last_hm == hm_to_verify:
                    if not can_use_hm(state, hm_to_verify):
                        unverified_hms.append(hms_to_verify.pop(0))
                    else:
                        hms_to_verify.pop(0)
                    continue

                last_hm = hm_to_verify
                logical_pokemon = sorted(logic.available_pokemon)
                world.random.shuffle(logical_pokemon)
                valid_pokemon = [mon for mon in logical_pokemon if state.has(mon, world.player)
                                 and mon not in logic.compatible_hm_pokemon[hm_to_verify]]
                if valid_pokemon:
                    pokemon = world.random.choice(valid_pokemon)
                    add_hm_compatibility(world, pokemon, hm_to_verify)
            else:
                hms_to_verify.pop(0)

        if unverified_hms and unverified_hms == hms:
            state = world.get_world_collection_state()
            if any((logic.has_hm_badge_requirement(hm, False)(state)
                    or logic.has_hm_badge_requirement(hm, True)(state)) for hm in unverified_hms):
                unverified_hms_list = ",".join(unverified_hms)
                raise Exception(f"Failed to ensure access to {unverified_hms_list} for player {world.player}")
        elif unverified_hms:
            unverified_hms.reverse()
            do_verify(unverified_hms)

    hms = ["CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH"]
    world.random.shuffle(hms)
    do_verify(hms)
