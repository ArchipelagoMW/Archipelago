from .base_logic import BaseLogic, BaseLogicMixin
from ..data.fish_pond_data import fish_pond_quests
from ..stardew_rule import StardewRule
from ..strings.building_names import Building
from ..strings.fish_names import Fish


class FishPondLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fish_pond = FishPondLogic(*args, **kwargs)


class FishPondLogic(BaseLogic):

    def can_get_fish_pond_reward(self, fish: str, population: int, desired_item: str) -> StardewRule:
        building_rule = self.logic.building.has_building(Building.fish_pond)
        if fish == Fish.any:
            return self.logic.fishing.can_fish_anywhere() & building_rule

        fish_rule = self.logic.has(fish)

        if population <= 1:
            return building_rule & fish_rule

        assert fish in fish_pond_quests, f"Cannot raise the population of {fish} to {population} in a fish pond to get {desired_item} without knowing the required quest items"
        # if fish not in fish_pond_quests:
        #     return building_rule & fish_rule

        item_rules = []
        fish_quests = fish_pond_quests[fish]
        for i in range(0, population):
            if i not in fish_quests:
                continue
            quests_for_that_level = fish_quests[i]
            num_quests = len(quests_for_that_level)
            if num_quests <= 0:
                continue

            level_rules = []
            for quest_item in quests_for_that_level:
                if quest_item == desired_item:
                    continue
                level_rules.append(self.logic.has(quest_item))
            if num_quests <= 2:
                item_rules.append(self.logic.count(num_quests, *level_rules))
            else:
                item_rules.append(self.logic.count(num_quests - 1, *level_rules))

        return building_rule & fish_rule & self.logic.and_(*item_rules)
