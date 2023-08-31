from .combat_logic import CombatLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .skill_logic import SkillLogic
from .tool_logic import ToolLogic
from .. import options
from ..mods.logic.elevator_logic import ModElevatorLogic
from ..stardew_rule import StardewRule, And, True_
from ..strings.performance_names import Performance
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial


class MineLogic:
    player: int
    tool_option = int
    skill_option = int
    elevator_option = int
    received: ReceivedLogic
    region: RegionLogic
    combat: CombatLogic
    tool: ToolLogic
    skill: SkillLogic
    mod_elevator: ModElevatorLogic

    def __init__(self, player: int, tool_option: int, skill_option: int, elevator_option: int, received: ReceivedLogic, region: RegionLogic,
                 combat: CombatLogic, tool: ToolLogic, skill: SkillLogic):
        self.player = player
        self.tool_option = tool_option
        self.skill_option = skill_option
        self.elevator_option = elevator_option
        self.received = received
        self.region = region
        self.combat = combat
        self.tool = tool
        self.skill = skill

    def set_modded_elevator(self, mod_elevator: ModElevatorLogic):
        self.mod_elevator = mod_elevator

    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.region.can_reach(Region.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.region.can_reach(Region.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.region.can_reach(Region.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(120) &
                self.region.can_reach(Region.skull_cavern))

    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.combat.can_fight_at_level(Performance.galaxy)
        if tier >= 3:
            return self.combat.can_fight_at_level(Performance.great)
        if tier >= 2:
            return self.combat.can_fight_at_level(Performance.good)
        if tier >= 1:
            return self.combat.can_fight_at_level(Performance.decent)
        return self.combat.can_fight_at_level(Performance.basic)

    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40)
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.tool_option & options.ToolProgression.option_progressive:
            rules.append(self.tool.has_tool(Tool.pickaxe, ToolMaterial.tiers[tier]))
        if self.skill_option == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.skill.has_level(Skill.combat, combat_tier))
        return And(rules)

    def can_progress_easily_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40) + 1
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.tool_option & options.ToolProgression.option_progressive:
            rules.append(self.tool.has_tool(Tool.pickaxe, ToolMaterial.tiers[tier]))
        if self.skill_option == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.skill.has_level(Skill.combat, combat_tier))
        return And(rules)

    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        if self.elevator_option != options.ElevatorProgression.option_vanilla:
            return self.received("Progressive Mine Elevator", int(floor / 5))
        return True_()

    def can_mine_to_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 5, 0)
        previous_previous_elevator = max(floor - 10, 0)
        return ((self.has_mine_elevator_to_floor(previous_elevator) &
                 self.can_progress_in_the_mines_from_floor(previous_elevator)) |
                (self.has_mine_elevator_to_floor(previous_previous_elevator) &
                 self.can_progress_easily_in_the_mines_from_floor(previous_previous_elevator)))

    def can_progress_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        tier = floor // 50
        rules = []
        weapon_rule = self.combat.has_great_weapon()
        rules.append(weapon_rule)
        if self.tool_option & options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", min(4, max(0, tier + 2))))
        if self.skill_option == options.SkillProgression.option_progressive:
            skill_tier = min(10, max(0, tier * 2 + 6))
            rules.extend({self.skill.has_level(Skill.combat, skill_tier),
                          self.skill.has_level(Skill.mining, skill_tier)})
        return And(rules)

    def can_progress_easily_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        return self.can_progress_in_the_skull_cavern_from_floor(floor + 50)

    def can_mine_to_skull_cavern_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 25, 0)
        previous_previous_elevator = max(floor - 50, 0)
        has_mine_elevator = self.has_mine_elevator_to_floor(5) # Skull Cavern Elevator menu needs a normal elevator...
        return ((self.mod_elevator.has_skull_cavern_elevator_to_floor(previous_elevator) &
                 self.can_progress_in_the_skull_cavern_from_floor(previous_elevator)) |
                (self.mod_elevator.has_skull_cavern_elevator_to_floor(previous_previous_elevator) &
                 self.can_progress_easily_in_the_skull_cavern_from_floor(previous_previous_elevator))) & has_mine_elevator

