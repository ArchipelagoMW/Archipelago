import typing
from . import Names
from worlds.generic.Rules import set_rule, add_rule

if typing.TYPE_CHECKING:
    from . import MM2World


def set_rules(world: "MM2World") -> None:
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings

    # Always require Crash Bomber for Boobeam Trap
    add_rule(world.multiworld.get_location(Names.wily_4, world.player),
             lambda state: state.has(Names.crash_bomber, world.player))

    if not world.multiworld.yoku_jumps[world.player]:
        add_rule(world.multiworld.get_entrance("To Heat Man Stage", world.player),
                 lambda state: state.has(Names.item_2, world.player))

    if not world.multiworld.enable_lasers[world.player]:
        add_rule(world.multiworld.get_entrance("To Quick Man Stage", world.player),
                 lambda state: state.has(Names.time_stopper, world.player))

    if world.multiworld.consumables[world.player]:
        add_rule(world.multiworld.get_location(Names.flash_man_c2, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.flash_man_c3, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.flash_man_c4, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.quick_man_c1, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.metal_man_c2, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2], world.player))
        add_rule(world.multiworld.get_location(Names.metal_man_c3, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2], world.player))
        add_rule(world.multiworld.get_location(Names.crash_man_c3, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.wily_2_c5, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_2_c6, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_3_c1, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_3_c2, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
