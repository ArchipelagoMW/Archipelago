from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, Or, Rule, True_

from worlds.generic.Rules import add_item_rule
from ..Locations import location_table
from ..Items import item_table
from ..Options import HomecomingMaterials
from . import (
    agrabah,
    atlantica,
    deep_jungle,
    destiny_islands,
    end_of_the_world,
    halloween_town,
    hollow_bastion,
    hundred_acre_wood,
    monstro,
    neverland,
    olympus_coliseum,
    traverse_town,
    wonderland,
)
from ._constants import KEYBLADES, WORLDS
from ._context import build_context
from ._custom_rules import HasCappedSum
from ._helpers import has_final_rest_door_rule, has_lucky_emblems_rule, has_x_worlds_rule
from ._option_filters import (
    EOTW_UNLOCK_LUCKY_EMBLEMS,
    EXACTLY_BEGINNER,
    KEYBLADES_UNLOCK_CHESTS_OFF,
    KEYBLADES_UNLOCK_CHESTS_ON,
    NOT_EXACTLY_BEGINNER,
)

__all__ = ["set_rules", "build_rule_dicts", "export_rules_to_dict", "HasCappedSum"]


def build_rule_dicts(kh1world) -> tuple[dict[str, Rule], dict[str, Rule]]:
    """Builds KH1's (unresolved) access rules. Doesn't touch the world - callers either
    resolve+apply them (set_rules) or export them (_export.py)."""
    player = kh1world.player
    options = kh1world.options

    ctx = build_context()

    location_rules: dict[str, Rule] = {}
    location_rules.update(traverse_town.build_rules(ctx, kh1world))
    location_rules.update(wonderland.build_rules(ctx))
    location_rules.update(deep_jungle.build_rules(ctx, bool(options.jungle_slider)))
    location_rules.update(agrabah.build_rules(ctx, bool(options.super_bosses)))
    location_rules.update(monstro.build_rules(ctx))
    location_rules.update(halloween_town.build_rules(ctx))
    location_rules.update(olympus_coliseum.build_rules(
        ctx, options.cups.current_key, bool(options.super_bosses), options.final_rest_door_key.current_key,
    ))
    location_rules.update(neverland.build_rules(ctx, bool(options.super_bosses)))
    location_rules.update(hollow_bastion.build_rules(
        ctx, bool(options.super_bosses), options.final_rest_door_key.current_key,
    ))
    location_rules.update(end_of_the_world.build_rules(ctx))
    location_rules.update(hundred_acre_wood.build_rules(ctx, bool(options.hundred_acre_wood)))
    location_rules.update(atlantica.build_rules(ctx, bool(options.atlantica)))
    location_rules.update(destiny_islands.build_rules(ctx, bool(options.destiny_islands)))

    for i in range(1, options.level_checks + 1):
        level_world_rule = has_x_worlds_rule(min(((i // 10) * 2), 8))
        location_rules[f"Level {i + 1:03} (Slot 1)"] = level_world_rule
        if i + 1 in kh1world.get_slot_2_levels():
            location_rules[f"Level {i + 1:03} (Slot 2)"] = level_world_rule

    eotw_access = Or(has_lucky_emblems_rule() & EOTW_UNLOCK_LUCKY_EMBLEMS, Has("End of the World"))
    location_rules["Final Ansem"] = (
        ctx.x_worlds_8
        & (
            (Has("Destiny Islands") & Has("Raft Materials", count=FromOption(HomecomingMaterials)))
            | (eotw_access & has_final_rest_door_rule())
        )
        & ctx.defensive_tools
    )

    for accessory in kh1world.get_accessory_locations():
        location_rules[accessory] = Has(accessory.replace("Accessory ", ""))

    for location_name, location_data in location_table.items():
        try:
            kh1world.get_location(location_name)
        except KeyError:
            continue
        if location_data.behind_boss:
            location_rules[location_name] = location_rules.get(location_name, True_()) & Or(
                ctx.basic_tools & EXACTLY_BEGINNER,
                True_() & NOT_EXACTLY_BEGINNER,
            )
        if options.remote_items.current_key == "off" and location_data.type == "Synth":
            add_item_rule(kh1world.get_location(location_name),
                          lambda i: (i.player != player or item_table[i.name].type == "Item"))
        if location_data.type == "Chest":
            location_world = location_data.category
            location_required_keyblade = KEYBLADES[WORLDS.index(location_world)]
            location_rules[location_name] = location_rules.get(location_name, True_()) & Or(
                Has(location_required_keyblade) & KEYBLADES_UNLOCK_CHESTS_ON,
                True_() & KEYBLADES_UNLOCK_CHESTS_OFF,
            )

    entrance_rules: dict[str, Rule] = {}
    if options.destiny_islands:
        entrance_rules["Destiny Islands"] = Has("Destiny Islands")
    entrance_rules["Wonderland"] = Has("Wonderland") & ctx.x_worlds_3
    entrance_rules["Olympus Coliseum"] = Has("Olympus Coliseum") & ctx.x_worlds_3
    entrance_rules["Deep Jungle"] = Has("Deep Jungle") & ctx.x_worlds_3
    entrance_rules["Agrabah"] = Has("Agrabah") & ctx.x_worlds_3
    entrance_rules["Monstro"] = Has("Monstro") & ctx.x_worlds_3
    if options.atlantica:
        entrance_rules["Atlantica"] = Has("Atlantica") & ctx.x_worlds_3
    entrance_rules["Halloween Town"] = Has("Halloween Town") & ctx.x_worlds_3
    entrance_rules["Neverland"] = Has("Neverland") & ctx.x_worlds_4
    entrance_rules["Hollow Bastion"] = Has("Hollow Bastion") & ctx.x_worlds_6
    entrance_rules["End of the World"] = ctx.x_worlds_8 & eotw_access
    entrance_rules["100 Acre Wood"] = Has("Progressive Fire")

    return location_rules, entrance_rules


def set_rules(kh1world) -> None:
    """Builds and applies KH1's access rules to kh1world. Called by KH1World.set_rules()."""
    location_rules, entrance_rules = build_rule_dicts(kh1world)

    for name, rule in entrance_rules.items():
        kh1world.set_rule(kh1world.get_entrance(name), rule)
    for name, rule in location_rules.items():
        kh1world.set_rule(kh1world.get_location(name), rule)

    kh1world.multiworld.completion_condition[kh1world.player] = lambda state: state.has("Victory", kh1world.player)


from ._export import export_rules_to_dict
