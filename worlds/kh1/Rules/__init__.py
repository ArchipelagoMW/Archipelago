from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, HasAll, Rule

from worlds.generic.Rules import add_item_rule
from ..Locations import get_locations_by_group
from ..Items import item_name_groups
from ..Options import Day2Materials
from . import agrabah, atlantica, deep_jungle, destiny_islands, end_of_the_world
from . import halloween_town, hollow_bastion, hundred_acre_wood, monstro
from . import neverland, olympus_coliseum, traverse_town, wonderland
from ..Data import CHEST_KEYBLADES
from ._helpers import BASIC_TOOLS, DEFENSIVE_TOOLS, EOTW_ACCESS, X_WORLDS_3, X_WORLDS_4, X_WORLDS_6
from ._helpers import X_WORLDS_8, by_difficulty, has_final_rest_door_rule, has_x_worlds_rule
from ._option_filters import KEYBLADES_UNLOCK_CHESTS_OFF, RAFT_FINISH_ON


def add_location_rule(location_rules: dict[str, Rule], location_name: str, rule: Rule) -> None:
    if location_name in location_rules:
        rule = location_rules[location_name] & rule
    location_rules[location_name] = rule


def build_area_rules(kh1world) -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    location_rules.update(traverse_town.build_rules(kh1world))
    location_rules.update(wonderland.build_rules())
    location_rules.update(deep_jungle.build_rules())
    location_rules.update(agrabah.build_rules())
    location_rules.update(monstro.build_rules())
    location_rules.update(halloween_town.build_rules())
    location_rules.update(olympus_coliseum.build_rules())
    location_rules.update(neverland.build_rules())
    location_rules.update(hollow_bastion.build_rules())
    location_rules.update(end_of_the_world.build_rules())
    location_rules.update(hundred_acre_wood.build_rules())
    location_rules.update(atlantica.build_rules())
    location_rules.update(destiny_islands.build_rules())
    return location_rules


def build_level_rules(kh1world) -> dict[str, Rule]:
    level_locations = kh1world.get_level_locations()
    location_rules: dict[str, Rule] = {}
    for level in range(2, 101):
        worlds_required = min((level - 1) // 10 * 2, 8)
        rule = has_x_worlds_rule(worlds_required)
        for slot in ("Slot 1", "Slot 2"):
            location_name = f"Level {level:03} ({slot})"
            if location_name in level_locations:
                location_rules[location_name] = rule
    return location_rules


def build_accessory_rules(kh1world) -> dict[str, Rule]:
    return {accessory: Has(accessory.replace("Accessory ", "")) for accessory in kh1world.get_accessory_locations()}


def build_final_ansem_rule() -> Rule:
    raft_route = Has("Destiny Islands") & Has("Raft Materials", count=FromOption(Day2Materials)) & RAFT_FINISH_ON
    final_rest_route = EOTW_ACCESS & has_final_rest_door_rule()
    return X_WORLDS_8 & (raft_route | final_rest_route) & DEFENSIVE_TOOLS


def add_boss_rules(location_rules: dict[str, Rule]) -> None:
    for location_name in get_locations_by_group("Boss"):
        add_location_rule(location_rules, location_name, by_difficulty(beginner=BASIC_TOOLS, normal=True))


def add_chest_rules(location_rules: dict[str, Rule]) -> None:
    for location_name, location_data in get_locations_by_group("Chest").items():
        chest_keyblade = Has(CHEST_KEYBLADES[location_data.region]) | KEYBLADES_UNLOCK_CHESTS_OFF
        add_location_rule(location_rules, location_name, chest_keyblade)


def add_synth_item_rules(kh1world) -> None:
    if kh1world.options.remote_items.current_key != "off":
        return
    player = kh1world.player
    for location_name in get_locations_by_group("Synth"):
        add_item_rule(kh1world.get_location(location_name),
                      lambda item: item.player != player or item.name in item_name_groups["Items"])


def build_entrance_rules() -> dict[str, Rule]:
    return {
        "Destiny Islands": Has("Destiny Islands"),
        "Wonderland": Has("Wonderland") & X_WORLDS_3,
        "Olympus Coliseum": Has("Olympus Coliseum") & X_WORLDS_3,
        "Deep Jungle": Has("Deep Jungle") & X_WORLDS_3,
        "Agrabah": Has("Agrabah") & X_WORLDS_3,
        "Monstro": Has("Monstro") & X_WORLDS_3,
        "Atlantica": Has("Atlantica") & X_WORLDS_3,
        "Halloween Town": Has("Halloween Town") & X_WORLDS_3,
        "Neverland": Has("Neverland") & X_WORLDS_4,
        "Hollow Bastion": Has("Hollow Bastion") & X_WORLDS_6,
        "End of the World": X_WORLDS_8 & EOTW_ACCESS,
        "100 Acre Wood": HasAll("Progressive Fire", "Old Book"),
    }


def build_rule_dicts(kh1world) -> tuple[dict[str, Rule], dict[str, Rule]]:
    location_rules = build_area_rules(kh1world)
    location_rules.update(build_level_rules(kh1world))
    location_rules.update(build_accessory_rules(kh1world))
    location_rules["Final Ansem"] = build_final_ansem_rule()
    add_boss_rules(location_rules)
    add_chest_rules(location_rules)
    return location_rules, build_entrance_rules()


def set_rules(kh1world) -> None:
    location_rules, entrance_rules = build_rule_dicts(kh1world)

    for name, rule in entrance_rules.items():
        kh1world.set_rule(kh1world.get_entrance(name), rule)
    for name, rule in location_rules.items():
        kh1world.set_rule(kh1world.get_location(name), rule)
    add_synth_item_rules(kh1world)

    kh1world.multiworld.completion_condition[kh1world.player] = lambda state: state.has("Victory", kh1world.player)
