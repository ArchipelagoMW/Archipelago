from __future__ import annotations

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from dataclasses import dataclass

import regex  # type: ignore

rules = \
[
    "FlyingFullorRuinsSonicSH",
    "FlyingOneCharorTripleSpringSonicSH",
    "FlyingFullor(RuinsandSingleSpringandSmallStonePlatform)SonicSH",
    "DashRampSonicSH",
    "DashPanelorSpeedSonicSH",
    "SingleSpringSonicSH",
    "(BreakandSingleSpring)orFlyingAnySonicSH",
    "FlyingAnySonicSH",
    "FlyingAnyandSmallStonePlatformSonicSH",
    "(BreakandTripleSpring)orFlyingAnySonicSH",
    "FlyingAnyorTripleSpringSonicSH",
    "BreakorFlyingAnyorHomingSonicSH",
    "BreakorFlyingAnySonicSH",
    "(CannonAnyorFlyingFull)andRuinsSonicSH",
    "FlyingFullandRuinsSonicSH",
    "CannonFlyingSonicSH",
    "CannonPowerSonicSH",
    "DashRingorFlyingAnySonicSH",
    "DashRampandDashRingandFlyingAnySonicSH",
    "RuinsSonicSH",
    "FlyingAnyandRuinsSonicSH",
    "FlyingFullSonicSH",
    "DashPanelor(DashRingandFlyingAny)orSpeedSonicSH",
    "((BreakorHoming)andSingleSpring)orFlyingAnySonicSH",
    "TripleSpringSonicSH",
    "DashRingandFlyingAnyandSingleSpringSonicSH",
    "Breakand(DashRingorFlyingAny)andSingleSpringSonicSH",
    "DashRingandFlyingAnySonicSH",
    "CannonSpeedSonicSH",
    "GlideandRuinsandTripleSpringSonicSH",
]


@dataclass
class SonicHeroesRule:
    conditions: list[str]

    team: str
    level: str

    def parse_rule(self, world: SonicHeroesWorld):
        return

test_rule = "TestRule((BreakorHoming)andSingleSpring)orFlyingAnySonicSH"



and_condition_pattern = regex.compile(r"(and)", regex.IGNORECASE)
or_condition_pattern = regex.compile(r"(or)", regex.IGNORECASE)
outer_parentheses_pattern = regex.compile(r"\((?>[^()]|(?R))*\)", regex.IGNORECASE)

#match - only look at start of str (bad)
#search - only find first match
#findall - match all but only return str
#finditer - match all return list of match obj
#split - split
#sub


#match object has:
#start - start index (inclusive)
#end - end index (exclusive)
#group - string match (0 is entire, 1 is first grouping match ())

outer_match = outer_parentheses_pattern.finditer(test_rule)

for match in outer_match:
    print(match)

print(outer_parentheses_pattern.split(test_rule))

print(or_condition_pattern.split(outer_parentheses_pattern.split(test_rule)[1]))


result_str_list: list[str] = []
parens_mapping_list: list[tuple[int, int]] = []


def is_there_team_level_str(rule: str) -> bool:
    if 'SonicSH' in rule:
        return True
    return False

def is_there_parens(rule: str) -> bool:
    if '(' in rule and ')' in rule:
        return True
    return False

def is_there_and(rule: str) -> bool:
    if 'and' in rule.lower():
        return True
    return False

def is_there_or(rule: str) -> bool:
    if 'or' in rule.lower():
        return True
    return False


def handle_rule(rule: str):
    if rule == '':
        return

    if rule.lower() == 'or':
        result_str_list.append('OR')
        return

    if rule.lower() == 'and':
        result_str_list.append('AND')
        return

    if is_there_team_level_str(rule):
        handle_rule(rule.replace("SonicSH", ""))
        result_str_list.append("SonicSH")
        return
    if rule[0] == '(' and rule[-1] == ')':
        handle_rule(rule[1:-1])
        return

    if is_there_parens(rule):
        temp_var = outer_parentheses_pattern.split(rule)
        handle_rule(temp_var[0])

        temp_scanner = outer_parentheses_pattern.finditer(rule)
        for scan_match in temp_scanner:
            temp_index = len(result_str_list)
            result_str_list.append('(')
            temp_tuple = (temp_index, temp_index)
            handle_rule(scan_match.group())
            temp_index = len(result_str_list)
            result_str_list.append(')')
            temp_tuple = (temp_tuple[0], temp_index)
            parens_mapping_list.append(temp_tuple)

        handle_rule(temp_var[1])
        return

    if is_there_and(rule):
        temp_var = and_condition_pattern.split(rule)
        print(f"Temp AND Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split)
            #if index < len(temp_var) - 1:
                #result_str_list.append('AND')
        return

    if is_there_or(rule):
        temp_var = or_condition_pattern.split(rule)
        print(f"Temp OR Var here: {temp_var}")
        for index, split in enumerate(temp_var):
            handle_rule(split)
        return

    result_str_list.append(rule)


print("TESTING HERE")
handle_rule(test_rule)

print(result_str_list)
print(parens_mapping_list)


