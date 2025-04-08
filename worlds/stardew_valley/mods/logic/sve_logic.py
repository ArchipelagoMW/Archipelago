from typing import Union

from ..mod_regions import SVERegion
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...logic.quest_logic import QuestLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...strings.ap_names.mods.mod_items import SVELocation, SVERunes, SVEQuestItem
from ...strings.quest_names import ModQuest
from ...strings.quest_names import Quest
from ...strings.region_names import Region
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.wallet_item_names import Wallet


class SVELogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sve = SVELogic(*args, **kwargs)


class SVELogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, QuestLogicMixin, RegionLogicMixin, RelationshipLogicMixin, TimeLogicMixin, ToolLogicMixin,
                               CookingLogicMixin, MoneyLogicMixin, CombatLogicMixin, SeasonLogicMixin]]):
    def initialize_rules(self):
        self.registry.sve_location_rules.update({
            SVELocation.tempered_galaxy_sword: self.logic.money.can_spend_at(SVERegion.alesia_shop, 350000),
            SVELocation.tempered_galaxy_dagger: self.logic.money.can_spend_at(SVERegion.isaac_shop, 600000),
            SVELocation.tempered_galaxy_hammer: self.logic.money.can_spend_at(SVERegion.isaac_shop, 400000),
        })

    def has_any_rune(self):
        rune_list = SVERunes.nexus_items
        return self.logic.or_(*(self.logic.received(rune) for rune in rune_list))

    def has_iridium_bomb(self):
        if self.options.quest_locations < 0:
            return self.logic.quest.can_complete_quest(ModQuest.RailroadBoulder)
        return self.logic.received(SVEQuestItem.iridium_bomb)

    def has_marlon_boat(self):
        if self.options.quest_locations < 0:
            return self.logic.quest.can_complete_quest(ModQuest.MarlonsBoat)
        return self.logic.received(SVEQuestItem.marlon_boat_paddle)

    def has_grandpa_shed_repaired(self):
        if self.options.quest_locations < 0:
            return self.logic.quest.can_complete_quest(ModQuest.GrandpasShed)
        return self.logic.received(SVEQuestItem.grandpa_shed)

    def has_bear_knowledge(self):
        if self.options.quest_locations < 0:
            return self.logic.quest.can_complete_quest(Quest.strange_note)
        return self.logic.received(Wallet.bears_knowledge)

    def can_buy_bear_recipe(self):
        access_rule = (self.logic.quest.can_complete_quest(Quest.strange_note) & self.logic.tool.has_tool(Tool.axe, ToolMaterial.basic) &
                       self.logic.tool.has_tool(Tool.pickaxe, ToolMaterial.basic))
        forage_rule = self.logic.region.can_reach_any((Region.forest, Region.backwoods, Region.mountain))
        knowledge_rule = self.has_bear_knowledge()
        return access_rule & forage_rule & knowledge_rule
