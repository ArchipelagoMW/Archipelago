from typing import NamedTuple, Callable, Literal, TYPE_CHECKING, TypeVar, Any, Union

from BaseClasses import ItemClassification, LocationProgressType, CollectionState

if not TYPE_CHECKING:
    AccessRule: type = Any
    ExtendedRule: type = Any
    ClassificationMethod: type = Any
    ProgressTypeMethod: type = Any
    InclusionRule: type = Any
    RulesDict: type = Any
else:
    from .. import PokemonBWWorld
    AccessRule: type = Callable[[CollectionState], bool]
    ExtendedRule: type = Callable[[CollectionState, PokemonBWWorld], bool]
    ClassificationMethod: type = Callable[[PokemonBWWorld], ItemClassification]
    ProgressTypeMethod: type = Callable[[PokemonBWWorld], LocationProgressType]
    InclusionRule: type = Callable[[PokemonBWWorld], bool]
    RulesDict: type = dict[ExtendedRule | tuple[ExtendedRule, ...], AccessRule]

T = TypeVar("T")
U = TypeVar("U")


class ItemData(NamedTuple):
    item_id: int
    classification: ClassificationMethod


class BadgeItemData(NamedTuple):
    item_id: int
    bit: int
    classification: ClassificationMethod


class SeasonItemData(NamedTuple):
    item_id: int
    flag_id: int
    var_value: int
    classification: ClassificationMethod


class FlagLocationData(NamedTuple):
    # flags begin at 0x23bf28 (B) or 0x23bf48 (W)
    flag_id: int
    progress_type: ProgressTypeMethod
    region: str
    inclusion_rule: InclusionRule | None
    rule: ExtendedRule | None


class TMLocationData(NamedTuple):
    flag_id: int
    progress_type: ProgressTypeMethod
    region: str
    inclusion_rule: InclusionRule | None
    hm_rule: Callable[[str], bool] | None
    rule: ExtendedRule | None


class DexLocationData(NamedTuple):
    # caught flags are stored at 0x23D1B4 (B) or 0x23D1D4 (W)
    dex_number: int
    # Use special rule if there are more than one species for a dex entry (e.g. Wormadam, Deoxys, Castform, ...)
    special_rule: ExtendedRule | None = None
    ut_alias: str | None = None


class EncounterData(NamedTuple):
    species_black: tuple[int, int]
    species_white: tuple[int, int]
    encounter_region: str
    file_index: tuple[int, int, int]


class StaticEncounterData(NamedTuple):
    # (dex number, form)
    species_black: tuple[int, int]
    species_white: tuple[int, int]
    encounter_region: str
    inclusion_rule: InclusionRule | None
    access_rule: ExtendedRule | None


class TradeEncounterData(NamedTuple):
    # (dex number, form)
    species_black: tuple[int, int]
    species_white: tuple[int, int]
    # only dex number
    wanted_black: int
    wanted_white: int
    encounter_region: str


class TrainerData(NamedTuple):
    id: int
    trainer_class: int
    pokemon_count: int
    items: tuple[str | None, str | None, str | None, str | None] | None  # Will be filled in the future
    held_items: bool
    unique_moves: bool
    pokemon_entry_length: int
    # region: str
    # gym: str | None  # City name without the "City"


class TrainerPokemonData(NamedTuple):
    trainer_id: int
    team_number: int
    ivs: int
    gender: int
    ability: int
    level: int
    nature: int
    species: str
    # held_item: str | None
    # moves: tuple[str, str, str, str] | None


class RegionConnectionData(NamedTuple):
    exiting_region: str
    entering_region: str
    rule: ExtendedRule | None


class EncounterRegionConnectionData(NamedTuple):
    exiting_region: str
    entering_region: str
    rules: tuple[ExtendedRule, ...] | ExtendedRule | None
    inclusion_rule: InclusionRule | None  # None means always included
    # The following will become important when wild encounter randomization happens
    # file_number: int


class SpeciesData(NamedTuple):
    dex_name: str
    dex_number: int
    form: int
    type_1: str
    type_2: str
    base_hp: int
    base_attack: int
    base_defense: int
    base_sp_attack: int
    base_sp_defense: int
    base_speed: int
    catch_rate: int
    gender_ratio: int
    # starts with 0 for base evolutions
    evolution_stage: int
    # (primary, secondary, hidden)
    abilities: tuple[str, str, str]
    # tuple(method, parameter, evolve into)
    evolutions: list[tuple[str, int, str]]


class MovesetData(NamedTuple):
    # tuple(level, move name)
    level_up_moves: list[tuple[int, str]]
    # TM number (internal order is TM1-95 HM1-6)
    tm_hm_moves: set[str]


class MoveData(NamedTuple):
    type: str
    category: Literal["Physical", "Special", "Status"]
    power: int
    # (Number of positive effects) - (Number of negative effects)
    effects_difference: int
    pp: int


class TMHMData(NamedTuple):
    move: str
    is_HM: bool


class EvolutionMethodData(NamedTuple):
    id: int
    # Takes value from evolution data and returns the access rule for that evolution
    rule: Callable[[int], ExtendedRule] | None


class TypeData(NamedTuple):
    id: int


class WildAdjustmentData(NamedTuple):
    calculation: Callable[[int], int]
    file: int
    season: int
    method: Literal[
        "grass", "dark grass", "rustling grass", "surfing", "surfing rippling", "fishing", "fishing rippling"
    ]


class TrainerAdjustmentData(NamedTuple):
    calculation: Callable[[int], int]
    trainer_id: int


AnyItemData: type = Union[ItemData, BadgeItemData, SeasonItemData]
AnyLocationData: type = Union[FlagLocationData, DexLocationData, TMLocationData]
AnyEncounterData: type = Union[EncounterData, TradeEncounterData, StaticEncounterData]
