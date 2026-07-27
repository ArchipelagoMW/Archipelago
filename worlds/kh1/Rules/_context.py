import dataclasses

from rule_builder.rules import Has, HasAll, HasAny, Rule

from ._constants import DODGE_AIRGUARD, HJ_GLIDE
from ._helpers import (
    can_dumbo_skip_rule,
    has_defensive_tools_rule,
    has_emblems_rule,
    has_basic_tools_rule,
    has_parasite_cage_rule,
    has_x_worlds_rule,
)


@dataclasses.dataclass(frozen=True)
class RuleContext:
    emblems: Rule
    x_worlds_3: Rule
    x_worlds_4: Rule
    x_worlds_6: Rule
    x_worlds_8: Rule
    parasite_cage: Rule
    basic_tools: Rule
    defensive_tools: Rule
    dumbo_skip: Rule
    dumbo_summon: Rule
    hj1: Rule
    hj2: Rule
    hj3: Rule
    glide: Rule
    hj_glide_all: Rule
    hj_glide_any: Rule
    dodge_airguard_all: Rule
    combo_master: Rule


def build_context() -> RuleContext:
    dumbo_skip = can_dumbo_skip_rule()
    return RuleContext(
        emblems=has_emblems_rule(),
        x_worlds_3=has_x_worlds_rule(3),
        x_worlds_4=has_x_worlds_rule(4),
        x_worlds_6=has_x_worlds_rule(6),
        x_worlds_8=has_x_worlds_rule(8),
        parasite_cage=has_parasite_cage_rule(),
        basic_tools=has_basic_tools_rule(),
        defensive_tools=has_defensive_tools_rule(),
        dumbo_skip=dumbo_skip,
        dumbo_summon=dumbo_skip & Has("Summon Anywhere"),
        hj1=Has("High Jump"),
        hj2=Has("High Jump", count=2),
        hj3=Has("High Jump", count=3),
        glide=Has("Progressive Glide"),
        hj_glide_all=HasAll(*HJ_GLIDE),
        hj_glide_any=HasAny(*HJ_GLIDE),
        dodge_airguard_all=HasAll(*DODGE_AIRGUARD),
        combo_master=Has("Combo Master"),
    )
