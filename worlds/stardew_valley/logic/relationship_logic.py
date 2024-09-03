import math
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .building_logic import BuildingLogicMixin
from .gift_logic import GiftLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .time_logic import TimeLogicMixin
from ..content.feature import friendsanity
from ..data.villagers_data import Villager
from ..stardew_rule import StardewRule, True_, false_, true_
from ..strings.ap_names.mods.mod_items import SVEQuestItem
from ..strings.crop_names import Fruit
from ..strings.generic_names import Generic
from ..strings.gift_names import Gift
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.villager_names import NPC, ModNPC

possible_kids = ("Cute Baby", "Ugly Baby")


def heart_item_name(npc: Union[str, Villager]) -> str:
    if isinstance(npc, Villager):
        npc = npc.name

    return f"{npc} <3"


class RelationshipLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relationship = RelationshipLogic(*args, **kwargs)


class RelationshipLogic(BaseLogic[Union[RelationshipLogicMixin, BuildingLogicMixin, SeasonLogicMixin, TimeLogicMixin, GiftLogicMixin, RegionLogicMixin,
ReceivedLogicMixin, HasLogicMixin]]):

    def can_date(self, npc: str) -> StardewRule:
        return self.logic.relationship.has_hearts(npc, 8) & self.logic.has(Gift.bouquet)

    def can_marry(self, npc: str) -> StardewRule:
        return self.logic.relationship.has_hearts(npc, 10) & self.logic.has(Gift.mermaid_pendant)

    def can_get_married(self) -> StardewRule:
        return self.logic.relationship.has_hearts_with_any_bachelor(10) & self.logic.has(Gift.mermaid_pendant)

    def has_children(self, number_children: int) -> StardewRule:
        assert number_children >= 0, "Can't have a negative amount of children."
        if number_children == 0:
            return True_()

        if not self.content.features.friendsanity.is_enabled:
            return self.logic.relationship.can_reproduce(number_children)

        return self.logic.received_n(*possible_kids, count=number_children) & self.logic.building.has_house(2)

    def can_reproduce(self, number_children: int = 1) -> StardewRule:
        assert number_children >= 0, "Can't have a negative amount of children."
        if number_children == 0:
            return True_()

        baby_rules = [self.logic.relationship.can_get_married(),
                      self.logic.building.has_house(2),
                      self.logic.relationship.has_hearts_with_any_bachelor(12),
                      self.logic.relationship.has_children(number_children - 1)]

        return self.logic.and_(*baby_rules)

    @cache_self1
    def has_hearts_with_any_bachelor(self, hearts: int = 1) -> StardewRule:
        assert hearts >= 0, f"Can't have a negative hearts with any bachelor."
        if hearts == 0:
            return True_()

        return self.logic.or_(*(self.logic.relationship.has_hearts(name, hearts)
                                for name, villager in self.content.villagers.items()
                                if villager.bachelor))

    @cache_self1
    def has_hearts_with_any(self, hearts: int = 1) -> StardewRule:
        assert hearts >= 0, f"Can't have a negative hearts with any npc."
        if hearts == 0:
            return True_()

        return self.logic.or_(*(self.logic.relationship.has_hearts(name, hearts)
                                for name, villager in self.content.villagers.items()))

    def has_hearts_with_n(self, amount: int, hearts: int = 1) -> StardewRule:
        assert hearts >= 0, f"Can't have a negative hearts with any npc."
        assert amount >= 0, f"Can't have a negative amount of npc."
        if hearts == 0 or amount == 0:
            return True_()

        return self.logic.count(amount, *(self.logic.relationship.has_hearts(name, hearts)
                                          for name, villager in self.content.villagers.items()))

    # Should be cached
    def has_hearts(self, npc: str, hearts: int = 1) -> StardewRule:
        assert hearts >= 0, f"Can't have a negative hearts with {npc}."

        villager = self.content.villagers.get(npc)
        if villager is None:
            return false_

        if hearts == 0:
            return true_

        heart_steps = self.content.features.friendsanity.get_randomized_hearts(villager)
        if not heart_steps or hearts > heart_steps[-1]:  # Hearts are sorted, bigger is the last one.
            return self.logic.relationship.can_earn_relationship(npc, hearts)

        return self.logic.relationship.received_hearts(villager, hearts)

    # Should be cached
    def received_hearts(self, villager: Villager, hearts: int) -> StardewRule:
        heart_item = friendsanity.to_item_name(villager.name)

        number_required = math.ceil(hearts / self.content.features.friendsanity.heart_size)
        return self.logic.received(heart_item, number_required) & self.can_meet(villager.name)

    @cache_self1
    def can_meet(self, npc: str) -> StardewRule:
        villager = self.content.villagers.get(npc)
        if villager is None:
            return false_

        rules = [self.logic.region.can_reach_any(villager.locations)]

        if npc == NPC.kent:
            rules.append(self.logic.time.has_year_two)

        elif npc == NPC.leo:
            rules.append(self.logic.received("Island North Turtle"))

        elif npc == ModNPC.lance:
            rules.append(self.logic.region.can_reach(Region.volcano_floor_10))

        elif npc == ModNPC.apples:
            rules.append(self.logic.has(Fruit.starfruit))

        elif npc == ModNPC.scarlett:
            scarlett_job = self.logic.received(SVEQuestItem.scarlett_job_offer)
            scarlett_spring = self.logic.season.has(Season.spring) & self.can_meet(ModNPC.andy)
            scarlett_summer = self.logic.season.has(Season.summer) & self.can_meet(ModNPC.susan)
            scarlett_fall = self.logic.season.has(Season.fall) & self.can_meet(ModNPC.sophia)
            rules.append(scarlett_job & (scarlett_spring | scarlett_summer | scarlett_fall))

        elif npc == ModNPC.morgan:
            rules.append(self.logic.received(SVEQuestItem.morgan_schooling))

        elif npc == ModNPC.goblin:
            rules.append(self.logic.region.can_reach_all((Region.witch_hut, Region.wizard_tower)))

        return self.logic.and_(*rules)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        rules = []

        for npc in self.content.villagers:
            meet_rule = self.logic.relationship.can_meet(npc)
            rules.append(meet_rule)

        rules.append(self.logic.gifts.has_any_universal_love)

        return self.logic.and_(*rules)

    # Should be cached
    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        assert hearts >= 0, f"Can't have a negative hearts with {npc}."

        villager = self.content.villagers.get(npc)
        if villager is None:
            return false_

        if hearts == 0:
            return True_()

        rules = [self.logic.relationship.can_meet(npc)]

        heart_size = self.content.features.friendsanity.heart_size
        max_randomized_hearts = self.content.features.friendsanity.get_randomized_hearts(villager)
        if max_randomized_hearts:
            if hearts > max_randomized_hearts[-1]:
                rules.append(self.logic.relationship.has_hearts(npc, hearts - 1))
            else:
                previous_heart = max(hearts - heart_size, 0)
                rules.append(self.logic.relationship.has_hearts(npc, previous_heart))

        if hearts > 2 or hearts > heart_size:
            rules.append(self.logic.season.has(villager.birthday))

        if villager.birthday == Generic.any:
            rules.append(self.logic.season.has_all() | self.logic.time.has_year_three)  # push logic back for any birthday-less villager

        if villager.bachelor:
            if hearts > 10:
                rules.append(self.logic.relationship.can_marry(npc))
            elif hearts > 8:
                rules.append(self.logic.relationship.can_date(npc))

        return self.logic.and_(*rules)
