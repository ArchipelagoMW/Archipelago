from .mine_logic import MineLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .skill_logic import SkillLogic
from .tool_logic import ToolLogic
from ..mods.logic.magic_logic import MagicLogic
from ..mods.logic.skills_logic import ModSkillLogic
from ..options import NumberOfMovementBuffs, NumberOfLuckBuffs
from ..stardew_rule import StardewRule
from ..strings.ap_names.buff_names import Buff
from ..strings.region_names import Region
from ..strings.skill_names import Skill, ModSkill
from ..strings.tool_names import ToolMaterial, Tool


class AbilityLogic:
    player: int
    movement_buff_option: NumberOfMovementBuffs
    luck_buff_option: NumberOfLuckBuffs
    received: ReceivedLogic
    region: RegionLogic
    tool: ToolLogic
    skill: SkillLogic
    mine: MineLogic
    magic: MagicLogic
    mod_skill: ModSkillLogic

    def __init__(self, player: int, movement_buff_option: NumberOfMovementBuffs, luck_buff_option: NumberOfLuckBuffs, received: ReceivedLogic,
                 region: RegionLogic, tool: ToolLogic, skill: SkillLogic, mine: MineLogic):
        self.player = player
        self.movement_buff_option = movement_buff_option
        self.luck_buff_option = luck_buff_option
        self.received = received
        self.region = region
        self.tool = tool
        self.skill = skill
        self.mine = mine

    def set_magic(self, magic: MagicLogic, mod_skill: ModSkillLogic):
        self.magic = magic
        self.mod_skill = mod_skill

    def can_mine_perfectly(self) -> StardewRule:
        return self.mine.can_progress_in_the_mines_from_floor(160)

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_mine_perfectly() &
                self.region.can_reach(Region.skull_cavern))

    def can_farm_perfectly(self) -> StardewRule:
        tool_rule = self.tool.has_tool(Tool.hoe, ToolMaterial.iridium) & self.tool.can_water(4)
        return tool_rule & self.skill.has_farming_level(10)

    def can_fish_perfectly(self) -> StardewRule:
        skill_rule = self.skill.has_level(Skill.fishing, 10)
        return skill_rule & self.tool.has_fishing_rod(4)

    def can_chop_trees(self) -> StardewRule:
        return self.tool.has_tool(Tool.axe) & self.region.can_reach(Region.forest)

    def can_chop_perfectly(self) -> StardewRule:
        magic_rule = (self.magic.can_use_clear_debris_instead_of_tool_level(3)) & self.mod_skill.has_mod_level(ModSkill.magic, 10)
        tool_rule = self.tool.has_tool(Tool.axe, ToolMaterial.iridium)
        foraging_rule = self.skill.has_level(Skill.foraging, 10)
        region_rule = self.region.can_reach(Region.forest)
        return region_rule & ((tool_rule & foraging_rule) | magic_rule)

    def has_max_buffs(self) -> StardewRule:
        return self.received(Buff.movement, self.movement_buff_option.value) & self.received(Buff.luck, self.luck_buff_option.value)
