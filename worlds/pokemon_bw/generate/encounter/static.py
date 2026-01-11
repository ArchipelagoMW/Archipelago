from typing import TYPE_CHECKING
from .. import StaticEncounterEntry, TradeEncounterEntry

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_static_encounters(world: "PokemonBWWorld",
                               species_checklist: tuple[list[str], set[str]]) -> dict[str, StaticEncounterEntry]:
    from ...data.locations.encounters.static import static, legendary, fossils, gift
    from .checklist import check_species
    from ...data.pokemon.species import by_id

    versioned_species = (
        (lambda d: d.species_white)
        if world.options.version == "white"
        else (lambda d: d.species_black)
    )

    encounters: dict[str, StaticEncounterEntry] = {}
    for table in (static, legendary, fossils, gift):
        for name, data in table.items():
            encounters[name] = StaticEncounterEntry(
                versioned_species(data), data.encounter_region, data.inclusion_rule, data.access_rule
            )
            check_species(world, species_checklist, by_id[versioned_species(data)])

    return encounters


def generate_trade_encounters(world: "PokemonBWWorld", species_checklist: tuple[list[str], set[str]]) -> dict[str, TradeEncounterEntry]:
    from ...data.locations.encounters.static import trade
    from .checklist import check_species, add_species_to_check
    from ...data.pokemon.species import by_id

    is_black = world.options.version == "black"
    versioned_species = (
        (lambda d: d.species_black)
        if is_black
        else (lambda d: d.species_white)
    )
    versioned_wanted = (
        (lambda d: d.wanted_black)
        if is_black
        else (lambda d: d.wanted_white)
    )

    encounters: dict[str, TradeEncounterEntry] = {}
    for name, data in trade.items():
        encounters[name] = TradeEncounterEntry(
            versioned_species(data),
            versioned_wanted(data),
            data.encounter_region
        )
        check_species(world, species_checklist, by_id[versioned_species(data)])
        add_species_to_check(species_checklist, by_id[(versioned_wanted(data), 0)])

    return encounters
