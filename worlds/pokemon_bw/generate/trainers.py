from typing import TYPE_CHECKING, Callable
from . import TrainerPokemonEntry

if TYPE_CHECKING:
    from .. import PokemonBWWorld
    from ..data import SpeciesData


def generate_trainer_teams(world: "PokemonBWWorld") -> list[TrainerPokemonEntry]:
    from ..data.trainers.pokemon import table
    from ..data.pokemon.species import by_name

    if "Randomize" not in world.options.randomize_trainer_pokemon:
        return [
            TrainerPokemonEntry(data.trainer_id, data.team_number, data.species)
            for data in table
        ]

    ret: list[TrainerPokemonEntry] = []
    all_species: list[str] = [name for name in by_name]
    world.random.shuffle(all_species)
    stats_total: Callable[["SpeciesData"], int] = lambda data: (
        data.base_hp + data.base_attack + data.base_defense +
        data.base_sp_attack + data.base_sp_defense + data.base_speed
    )

    if "Similar base stats" in world.options.randomize_trainer_pokemon:
        for next_data in table:
            vanilla_total = stats_total(by_name[next_data.species])
            stat_tolerance = world.options.pokemon_randomization_adjustments["Stats leniency"]
            while True:
                species = world.random.choice(all_species)
                random_total = stats_total(by_name[species])
                if random_total not in range(vanilla_total - stat_tolerance, vanilla_total + stat_tolerance + 1):
                    stat_tolerance += 2
                    continue
                ret.append(TrainerPokemonEntry(next_data.trainer_id, next_data.team_number, species))
                break
    else:
        for next_data in table:
            ret.append(TrainerPokemonEntry(
                next_data.trainer_id, next_data.team_number, world.random.choice(all_species)
            ))

    return ret
