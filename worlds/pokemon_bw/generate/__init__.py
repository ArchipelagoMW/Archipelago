from typing import NamedTuple

from ..data import InclusionRule, ExtendedRule


class SpeciesEntry(NamedTuple):
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
    # tuple(level, move name)
    level_up_moves: list[tuple[int, str]]
    # TM number (internal order is TM1-95 HM1-6)
    tm_hm_moves: set[str]


class EncounterEntry(NamedTuple):
    species_id: tuple[int, int]
    encounter_region: str
    file_index: tuple[int, int, int]
    write: bool


class StaticEncounterEntry(NamedTuple):
    species_id: tuple[int, int]
    encounter_region: str
    inclusion_rule: InclusionRule | None
    access_rule: ExtendedRule | None


class TradeEncounterEntry(NamedTuple):
    species_id: tuple[int, int]
    wanted_dex_number: int
    encounter_region: str


class TrainerPokemonEntry(NamedTuple):
    trainer_id: int
    team_number: int
    species: str
    # ability: int
    # nature: int
    # held_item: str | None
    # moves: tuple[str, str, str, str] | None
