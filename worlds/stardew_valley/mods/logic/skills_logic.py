from typing import Iterable
from .magic_logic import MagicLogic
from ... import options
from ...logic.action_logic import ActionLogic
from ...logic.building_logic import BuildingLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.tool_logic import ToolLogic
from ...strings.building_names import Building
from ...strings.geode_names import Geode
from ...strings.region_names import Region
from ...strings.skill_names import ModSkill
from ...strings.spells import MagicSpell
from ...strings.machine_names import Machine
from ...strings.tool_names import Tool, ToolMaterial
from ...mods.mod_data import ModNames
from ...data.villagers_data import all_villagers
from ...stardew_rule import Count, StardewRule, False_, True_


class ModSkillLogic:
    player: int
    skill_option: int
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    action: ActionLogic
    relationship: RelationshipLogic
    building: BuildingLogic
    tool: ToolLogic
    fishing: FishingLogic
    cooking: CookingLogic
    magic: MagicLogic
    mods_option: Iterable[str]

    def __init__(self, player: int, skill_option: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic, action: ActionLogic,
                 relationship: RelationshipLogic, building: BuildingLogic, tool: ToolLogic, fishing: FishingLogic, cooking: CookingLogic,
                 magic: MagicLogic, mods_option: Iterable[str]):
        self.player = player
        self.skill_option = skill_option
        self.received = received
        self.has = has
        self.region = region
        self.action = action
        self.relationship = relationship
        self.building = building
        self.tool = tool
        self.fishing = fishing
        self.cooking = cooking
        self.magic = magic
        self.mods_option = mods_option

    def has_mod_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        if self.skill_option == options.SkillProgression.option_progressive:
            return self.received(f"{skill} Level", level)

        return self.can_earn_mod_skill_level(skill, level)

    def can_earn_mod_skill_level(self, skill: str, level: int) -> StardewRule:
        if ModNames.luck_skill in self.mods_option and skill == ModSkill.luck:
            return self.can_earn_luck_skill_level(level)
        if ModNames.magic in self.mods_option and skill == ModSkill.magic:
            return self.can_earn_magic_skill_level(level)
        if ModNames.socializing_skill in self.mods_option and skill == ModSkill.socializing:
            return self.can_earn_socializing_skill_level(level)
        if ModNames.archaeology in self.mods_option and skill == ModSkill.archaeology:
            return self.can_earn_archaeology_skill_level(level)
        if ModNames.cooking_skill in self.mods_option and skill == ModSkill.cooking:
            return self.can_earn_cooking_skill_level(level)
        if ModNames.binning_skill in self.mods_option and skill == ModSkill.binning:
            return self.can_earn_binning_skill_level(level)
        return False_()

    def can_earn_luck_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.fishing.can_fish_chests() | self.action.can_open_geode(Geode.magma)
        else:
            return self.fishing.can_fish_chests() | self.action.can_open_geode(Geode.geode)

    def can_earn_magic_skill_level(self, level: int) -> StardewRule:
        spell_count = [self.received(MagicSpell.clear_debris), self.received(MagicSpell.water),
                       self.received(MagicSpell.blink), self.received(MagicSpell.fireball),
                       self.received(MagicSpell.frostbite),
                       self.received(MagicSpell.descend), self.received(MagicSpell.tendrils),
                       self.received(MagicSpell.shockwave),
                       self.received(MagicSpell.meteor),
                       self.received(MagicSpell.spirit)]
        return self.magic.can_use_altar() & Count(level, spell_count)

    def can_earn_socializing_skill_level(self, level: int) -> StardewRule:
        villager_count = []
        for villager in all_villagers:
            if villager.mod_name in self.mods_option or villager.mod_name is None:
                villager_count.append(self.relationship.can_earn_relationship(villager.name, level))
        return Count(level * 2, villager_count)

    def can_earn_archaeology_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.action.can_pan() | self.tool.has_tool(Tool.hoe, ToolMaterial.gold)
        else:
            return self.action.can_pan() | self.tool.has_tool(Tool.hoe, ToolMaterial.basic)

    def can_earn_cooking_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.cooking.can_cook() & self.region.can_reach(Region.saloon) & \
                self.building.has_building(Building.coop) & self.building.has_building(Building.barn)
        else:
            return self.cooking.can_cook()

    def can_earn_binning_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.region.can_reach(Region.town) & self.has(Machine.recycling_machine)
        else:
            return self.region.can_reach(Region.town) | self.has(Machine.recycling_machine)
