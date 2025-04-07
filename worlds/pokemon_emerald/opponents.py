from typing import TYPE_CHECKING, Dict, List, Set

from .data import NUM_REAL_SPECIES, UNEVOLVED_POKEMON, data
from .options import RandomizeTrainerParties
from .pokemon import filter_species_by_nearby_bst
from .util import int_to_bool_array

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


def randomize_opponent_parties(world: "PokemonEmeraldWorld") -> None:
    if world.options.trainer_parties == RandomizeTrainerParties.option_vanilla:
        return

    from collections import defaultdict

    should_match_bst = world.options.trainer_parties in {
        RandomizeTrainerParties.option_match_base_stats,
        RandomizeTrainerParties.option_match_base_stats_and_type,
    }
    should_match_type = world.options.trainer_parties in {
        RandomizeTrainerParties.option_match_type,
        RandomizeTrainerParties.option_match_base_stats_and_type,
    }

    per_species_tmhm_moves: Dict[int, List[int]] = {}

    for trainer in world.modified_trainers:
        new_party = []
        for pokemon in trainer.party.pokemon:
            original_species = data.species[pokemon.species_id]

            # Construct progressive tiers of blacklists that can be peeled back if they
            # collectively cover too much of the pokedex. A lower index in `blacklists`
            # indicates a more important set of species to avoid. Entries at `0` will
            # always be blacklisted.
            blacklists: Dict[int, List[Set[int]]] = defaultdict(list)

            # Blacklist unevolved species
            if pokemon.level >= world.options.force_fully_evolved:
                blacklists[0].append(UNEVOLVED_POKEMON)

            # Blacklist from player options
            blacklists[2].append(world.blacklisted_opponent_pokemon)

            # Type matching blacklist
            if should_match_type:
                blacklists[3].append({
                    species.species_id
                    for species in world.modified_species.values()
                    if not bool(set(species.types) & set(original_species.types))
                })

            merged_blacklist: Set[int] = set()
            for max_priority in reversed(sorted(blacklists.keys())):
                merged_blacklist = set()
                for priority in blacklists.keys():
                    if priority <= max_priority:
                        for blacklist in blacklists[priority]:
                            merged_blacklist |= blacklist

                if len(merged_blacklist) < NUM_REAL_SPECIES:
                    break
            else:
                raise RuntimeError("This should never happen")

            candidates = [
                species
                for species in world.modified_species.values()
                if species.species_id not in merged_blacklist
            ]

            if should_match_bst:
                candidates = filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

            new_species = world.random.choice(candidates)

            if new_species.species_id not in per_species_tmhm_moves:
                per_species_tmhm_moves[new_species.species_id] = sorted({
                    world.modified_tmhm_moves[i]
                    for i, is_compatible in enumerate(int_to_bool_array(new_species.tm_hm_compatibility))
                    if is_compatible and world.modified_tmhm_moves[i] not in world.blacklisted_moves
                })

            # TMs and HMs compatible with the species
            tm_hm_movepool = per_species_tmhm_moves[new_species.species_id]

            # Moves the pokemon could have learned by now
            level_up_movepool = sorted({
                move.move_id
                for move in new_species.learnset
                if move.move_id != 0 and move.level <= pokemon.level
            })

            if len(level_up_movepool) < 4:
                level_up_moves = [level_up_movepool[i] if i < len(level_up_movepool) else 0 for i in range(4)]
            else:
                level_up_moves = world.random.sample(level_up_movepool, 4)

            if len(tm_hm_movepool) < 4:
                hm_moves = list(reversed(list(tm_hm_movepool[i] if i < len(tm_hm_movepool) else 0 for i in range(4))))
            else:
                hm_moves = world.random.sample(tm_hm_movepool, 4)

            # 25% chance to pick a move from TMs or HMs
            new_moves = (
                hm_moves[0] if world.random.random() < 0.25 else level_up_moves[0],
                hm_moves[1] if world.random.random() < 0.25 else level_up_moves[1],
                hm_moves[2] if world.random.random() < 0.25 else level_up_moves[2],
                hm_moves[3] if world.random.random() < 0.25 else level_up_moves[3]
            )

            new_party.append(pokemon._replace(species_id=new_species.species_id, moves=new_moves))

        trainer.party = trainer.party._replace(pokemon=new_party)
