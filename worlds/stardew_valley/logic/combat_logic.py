from typing import Iterable

from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..data.monster_data import StardewMonster
from ..mods.logic.magic_logic import MagicLogic
from ..stardew_rule import StardewRule, Or, And
from ..strings.performance_names import Performance
from ..items import all_items, Group


class CombatLogic:
    player: int
    received: ReceivedLogic
    region: RegionLogic
    magic: MagicLogic

    def __init__(self, player: int, received: ReceivedLogic, region: RegionLogic):
        self.player = player
        self.region = region
        self.received = received

    def set_magic(self, magic: MagicLogic):
        self.magic = magic

    def can_fight_at_level(self, level: str) -> StardewRule:
        if level == Performance.basic:
            return self.has_any_weapon() | self.magic.has_any_spell()
        if level == Performance.decent:
            return self.has_decent_weapon() | self.magic.has_decent_spells()
        if level == Performance.good:
            return self.has_good_weapon() | self.magic.has_good_spells()
        if level == Performance.great:
            return self.has_great_weapon() | self.magic.has_great_spells()
        if level == Performance.galaxy:
            return self.has_galaxy_weapon() | self.magic.has_amazing_spells()
        if level == Performance.maximum:
            return self.has_galaxy_weapon() | self.magic.has_amazing_spells() # Someday we will have the ascended weapons in AP

    def has_any_weapon(self) -> StardewRule:
        higher_weapon_rule = self.has_decent_weapon()
        this_weapon_rule = self.received(item.name for item in all_items if Group.WEAPON in item.groups)
        return higher_weapon_rule | this_weapon_rule

    def has_decent_weapon(self) -> StardewRule:
        higher_weapon_rule = self.has_good_weapon()
        this_weapon_rule = self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and (Group.MINES_FLOOR_50 in item.groups or Group.MINES_FLOOR_60 in item.groups))
        return (higher_weapon_rule | this_weapon_rule) & self.received("Adventurer's Guild")

    def has_good_weapon(self) -> StardewRule:
        higher_weapon_rule = self.has_great_weapon()
        this_weapon_rule = self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and (Group.MINES_FLOOR_80 in item.groups or Group.MINES_FLOOR_90 in item.groups))
        return (higher_weapon_rule | this_weapon_rule) & self.received("Adventurer's Guild")

    def has_great_weapon(self) -> StardewRule:
        higher_weapon_rule = self.has_galaxy_weapon()
        this_weapon_rule = self.received(item.name for item in all_items if Group.WEAPON in item.groups and Group.MINES_FLOOR_110 in item.groups)
        return (higher_weapon_rule | this_weapon_rule) & self.received("Adventurer's Guild")

    def has_galaxy_weapon(self) -> StardewRule:
        this_weapon_rule = self.received(item.name for item in all_items if Group.WEAPON in item.groups and Group.GALAXY_WEAPONS in item.groups)
        return this_weapon_rule & self.received("Adventurer's Guild")

    def can_kill_monster(self, monster: StardewMonster) -> StardewRule:
        region_rule = self.region.can_reach_any(monster.locations)
        combat_rule = self.can_fight_at_level(monster.difficulty)
        return region_rule & combat_rule

    def can_kill_any_monster(self, monsters: Iterable[StardewMonster]) -> StardewRule:
        rules = [self.can_kill_monster(monster) for monster in monsters]
        return Or(rules)

    def can_kill_all_monsters(self, monsters: Iterable[StardewMonster]) -> StardewRule:
        rules = [self.can_kill_monster(monster) for monster in monsters]
        return And(rules)

