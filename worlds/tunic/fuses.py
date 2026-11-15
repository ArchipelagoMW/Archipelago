from typing import NamedTuple, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from .constants import *
from .logic_helpers import has_ability, has_sword, fuse_activation_reqs

if TYPE_CHECKING:
    from . import TunicWorld


class TunicLocationData(NamedTuple):
    loc_group: str
    er_region: str


fuse_location_table: dict[str, TunicLocationData] = {
    "Overworld - [Southeast] Activate Fuse": TunicLocationData("Overworld", "Overworld"),
    "Swamp - [Central] Activate Fuse": TunicLocationData("Swamp", "Swamp Mid"),
    "Swamp - [Outside Cathedral] Activate Fuse": TunicLocationData("Swamp", "Swamp Mid"),
    "Cathedral - Activate Fuse": TunicLocationData("Cathedral", "Cathedral Main"),
    "West Furnace - Activate Fuse": TunicLocationData("West Furnace", "Furnace Fuse"),
    "West Garden - [South Highlands] Activate Fuse": TunicLocationData("West Garden", "West Garden South Checkpoint"),
    "Ruined Atoll - [Northwest] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Ruined Atoll - [Northeast] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Ruined Atoll - [Southeast] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll Ladder Tops"),
    "Ruined Atoll - [Southwest] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Library Lab - Activate Fuse": TunicLocationData("Library Lab", "Library Lab"),
    "Fortress Courtyard - [From Overworld] Activate Fuse": TunicLocationData("Fortress Courtyard", "Fortress Exterior from Overworld"),
    "Fortress Courtyard - [Near Cave] Activate Fuse": TunicLocationData("Fortress Courtyard", "Fortress Exterior from Overworld"),
    "Fortress Courtyard - [Upper] Activate Fuse": TunicLocationData("Fortress Courtyard", "Fortress Courtyard Upper"),
    "Fortress Courtyard - [Central] Activate Fuse": TunicLocationData("Fortress Courtyard", "Fortress Courtyard"),
    "Beneath the Fortress - Activate Fuse": TunicLocationData("Beneath the Fortress", "Beneath the Vault Back"),
    "Eastern Vault Fortress - [Candle Room] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Eastern Vault Fortress - [Left of Door] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Eastern Vault Fortress - [Right of Door] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Quarry Entryway - Activate Fuse": TunicLocationData("Quarry Connector", "Quarry Connector"),
    "Quarry - Activate Fuse": TunicLocationData("Quarry", "Quarry Entry"),
    "Rooted Ziggurat Lower - [Miniboss] Activate Fuse": TunicLocationData("Rooted Ziggurat Lower", "Rooted Ziggurat Lower Miniboss Platform"),
    "Rooted Ziggurat Lower - [Before Boss] Activate Fuse": TunicLocationData("Rooted Ziggurat Lower", "Rooted Ziggurat Lower Back"),
}

fuse_location_base_id = base_id + 10000
fuse_location_name_to_id: dict[str, int] = {name: fuse_location_base_id + index
                                            for index, name in enumerate(fuse_location_table)}

fuse_location_groups: dict[str, set[str]] = {}
for location_name, location_data in fuse_location_table.items():
    fuse_location_groups.setdefault(location_data.loc_group, set()).add(location_name)
    fuse_location_groups.setdefault("Fuses", set()).add(location_name)


# to be deduplicated in the big refactor
def has_ladder(ladder: str, state: CollectionState, world: "TunicWorld") -> bool:
    return not world.options.shuffle_ladders or state.has(ladder, world.player)


def set_fuse_location_rules(world: "TunicWorld") -> None:
    player = world.player

    set_rule(world.get_location("Overworld - [Southeast] Activate Fuse"),
             lambda state: state.has(laurels, player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Swamp - [Central] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[swamp_fuse_2], player)
             and has_ability(prayer, state, world)
             and has_sword(state, player))
    set_rule(world.get_location("Swamp - [Outside Cathedral] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[swamp_fuse_3], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Cathedral - Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("West Furnace - Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("West Garden - [South Highlands] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Ruined Atoll - [Northwest] Activate Fuse"),
             lambda state: state.has_any([grapple, laurels], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Ruined Atoll - [Northeast] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Ruined Atoll - [Southeast] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Ruined Atoll - [Southwest] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Library Lab - Activate Fuse"),
             lambda state: has_ability(prayer, state, world)
             and has_ladder("Ladders in Library", state, world))
    set_rule(world.get_location("Fortress Courtyard - [From Overworld] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Fortress Courtyard - [Near Cave] Activate Fuse"),
             lambda state: state.has(fortress_exterior_fuse_1, player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Fortress Courtyard - [Upper] Activate Fuse"),
             lambda state: state.has(fortress_exterior_fuse_1, player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Fortress Courtyard - [Central] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[fortress_courtyard_lower_fuse], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Beneath the Fortress - Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[beneath_the_vault_fuse], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Eastern Vault Fortress - [Candle Room] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[fortress_candles_fuse], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Eastern Vault Fortress - [Left of Door] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[fortress_door_left_fuse], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Eastern Vault Fortress - [Right of Door] Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[fortress_door_right_fuse], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Quarry Entryway - Activate Fuse"),
             lambda state: state.has(grapple, player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Quarry - Activate Fuse"),
             lambda state: state.has_all(fuse_activation_reqs[quarry_fuse_2], player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Rooted Ziggurat Lower - [Miniboss] Activate Fuse"),
             lambda state: has_sword(state, player)
             and has_ability(prayer, state, world))
    set_rule(world.get_location("Rooted Ziggurat Lower - [Before Boss] Activate Fuse"),
             lambda state: has_ability(prayer, state, world))
