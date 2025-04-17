from worlds.generic.Rules import set_rule, forbid_items_for_player, add_rule
from BaseClasses import CollectionState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import CrystalProjectWorld

def get_job_count(player: int, state: CollectionState) -> int:
    count = 0
    if state.has("Job - Fencer", player):
        count += 1
    if state.has("Job - Shaman", player):
        count += 1
    if state.has("Job - Scholar", player):
        count += 1
    if state.has("Job - Aegis", player):
        count += 1
    if state.has("Job - Hunter", player):
        count += 1
    if state.has("Job - Chemist", player):
        count += 1
    if state.has("Job - Reaper", player):
        count += 1
    if state.has("Job - Ninja", player):
        count += 1
    if state.has("Job - Nomad", player):
        count += 1
    if state.has("Job - Dervish", player):
        count += 1
    if state.has("Job - Beatsmith", player):
        count += 1
    if state.has("Job - Samurai", player):
        count += 1
    if state.has("Job - Assassin", player):
        count += 1
    if state.has("Job - Valkyrie", player):
        count += 1
    if state.has("Job - Summoner", player):
        count += 1
    if state.has("Job - Beastmaster", player):
        count += 1
    if state.has("Job - Weaver", player):
        count += 1
    if state.has("Job - Mimic", player):
        count += 1

    return count