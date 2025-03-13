from typing import NamedTuple, Dict, TYPE_CHECKING, List

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from .rules import has_ability, has_sword

if TYPE_CHECKING:
    from . import TunicWorld


class TunicLocationData(NamedTuple):
    loc_group: str
    er_region: str


laurels = "Hero's Laurels"
grapple = "Magic Orb"
ice_dagger = "Magic Dagger"
fire_wand = "Magic Wand"
gun = "Gun"
lantern = "Lantern"
fairies = "Fairy"
coins = "Golden Coin"
prayer = "Pages 24-25 (Prayer)"
holy_cross = "Pages 42-43 (Holy Cross)"
icebolt = "Pages 52-53 (Icebolt)"
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"

swamp_fuse_1 = "Swamp Fuse 1"
swamp_fuse_2 = "Swamp Fuse 2"
swamp_fuse_3 = "Swamp Fuse 3"
cathedral_elevator_fuse = "Cathedral Elevator Fuse"
quarry_fuse_1 = "Quarry Fuse 1"
quarry_fuse_2 = "Quarry Fuse 2"
ziggurat_miniboss_fuse = "Ziggurat Miniboss Fuse"
ziggurat_teleporter_fuse = "Ziggurat Teleporter Fuse"
fortress_exterior_fuse_1 = "Fortress Exterior Fuse 1"
fortress_exterior_fuse_2 = "Fortress Exterior Fuse 2"
fortress_courtyard_upper_fuse = "Fortress Courtyard Upper Fuse"
fortress_courtyard_lower_fuse = "Fortress Courtyard Fuse"
beneath_the_vault_fuse = "Beneath the Vault Fuse" # event needs to be renamed probably
fortress_candles_fuse = "Fortress Candles Fuse"
fortress_door_left_fuse = "Fortress Door Left Fuse"
fortress_door_right_fuse = "Fortress Door Right Fuse"
west_furnace_fuse = "West Furnace Fuse"
west_garden_fuse = "West Garden Fuse"
atoll_northeast_fuse = "Atoll Northeast Fuse"
atoll_northwest_fuse = "Atoll Northwest Fuse"
atoll_southeast_fuse = "Atoll Southeast Fuse"
atoll_southwest_fuse = "Atoll Southwest Fuse"
library_lab_fuse = "Library Lab Fuse"

fuse_location_base_id = 509342400 + 10000

fuse_location_table: Dict[str, TunicLocationData] = {
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

# for fuse locations and reusing event names to simplify er_rules
fuse_activation_reqs: Dict[str, List[str]] = {
    swamp_fuse_2: [swamp_fuse_1],
    swamp_fuse_3: [swamp_fuse_1, swamp_fuse_2],
    fortress_exterior_fuse_2: [fortress_exterior_fuse_1],
    beneath_the_vault_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2],
    fortress_candles_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse],
    fortress_door_left_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse,
                              fortress_candles_fuse],
    fortress_courtyard_upper_fuse: [fortress_exterior_fuse_1],
    fortress_courtyard_lower_fuse: [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse],
    fortress_door_right_fuse: [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse, fortress_courtyard_lower_fuse],
    quarry_fuse_2: [quarry_fuse_1],
    "Activate Furnace Fuse": [west_furnace_fuse],
    "Activate South and West Fortress Exterior Fuses": [fortress_exterior_fuse_1, fortress_exterior_fuse_2],
    "Activate Upper and Central Fortress Exterior Fuses": [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse,
                                                           fortress_courtyard_lower_fuse],
    "Activate Beneath the Vault Fuse": [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse],
    "Activate Eastern Vault West Fuses": [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse,
                                          fortress_candles_fuse, fortress_door_left_fuse],
    "Activate Eastern Vault East Fuse": [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse,
                                         fortress_courtyard_lower_fuse, fortress_door_right_fuse],
    "Activate Quarry Connector Fuse": [quarry_fuse_1],
    "Activate Quarry Fuse": [quarry_fuse_1, quarry_fuse_2],
    "Activate Ziggurat Fuse": [ziggurat_teleporter_fuse],
    "Activate West Garden Fuse": [west_garden_fuse],
    "Activate Library Fuse": [library_lab_fuse],
}

fuse_location_name_to_id: dict[str, int] = {name: fuse_location_base_id + index
                                            for index, name in enumerate(fuse_location_table)}

fuse_location_groups: dict[str, set[str]] = {}
for location_name, location_data in fuse_location_table.items():
    fuse_location_groups.setdefault(location_data.loc_group, set()).add(location_name)
    fuse_location_groups.setdefault("Fuses", set()).add(location_name)


def has_fuses(fuse_event: str, state: CollectionState, world: "TunicWorld") -> bool:
    player = world.player
    if world.options.shuffle_fuses:
        return state.has_all(fuse_activation_reqs[fuse_event], player)

    return state.has(fuse_event, player)


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
