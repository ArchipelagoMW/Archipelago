from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...strings.ap_names.mods.mod_items import SVELocation, SVERunes, SVEQuestItem
from ...strings.quest_names import Quest, ModQuest
from ...strings.region_names import Region, SVERegion
from ...strings.tool_names import Tool
from ...strings.wallet_item_names import Wallet


class SVELogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sve = SVELogic(*args, **kwargs)


class SVELogic(BaseLogic):
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
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.iridium_bomb)
        return self.logic.quest.can_complete_quest(ModQuest.RailroadBoulder)

    def has_marlon_boat(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.marlon_boat_paddle)
        return self.logic.quest.can_complete_quest(ModQuest.MarlonsBoat)

    def has_grandpa_shed_repaired(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.grandpa_shed)
        return self.logic.quest.can_complete_quest(ModQuest.GrandpasShed)

    def has_bear_knowledge(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(Wallet.bears_knowledge)
        return self.logic.quest.can_complete_quest(Quest.strange_note)

    def can_buy_bear_recipe(self):
        access_rule = (self.logic.quest.can_complete_quest(Quest.strange_note) & self.logic.tool.has_tool(Tool.axe) &
                       self.logic.tool.has_tool(Tool.pickaxe))
        forage_rule = self.logic.region.can_reach_any(Region.forest, Region.backwoods, Region.mountain)
        knowledge_rule = self.has_bear_knowledge()
        return access_rule & forage_rule & knowledge_rule
