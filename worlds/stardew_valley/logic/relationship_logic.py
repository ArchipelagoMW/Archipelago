import math
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic
from .building_logic import BuildingLogicMixin
from .gift_logic import GiftLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .time_logic import TimeLogicMixin
from ..data.villagers_data import all_villagers_by_name, Villager
from ..options import Friendsanity
from ..stardew_rule import StardewRule, True_, And, Or, Count
from ..strings.generic_names import Generic
from ..strings.gift_names import Gift
from ..strings.region_names import Region
from ..strings.villager_names import NPC, ModNPC

possible_kids = ("Cute Baby", "Ugly Baby")


class RelationshipLogicMixin(BaseLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relationship = RelationshipLogic(*args, **kwargs)


class RelationshipLogic(BuildingLogicMixin, SeasonLogicMixin, TimeLogicMixin, GiftLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin):

    def can_date(self, npc: str) -> StardewRule:
        return self.has_hearts(npc, 8) & self.has(Gift.bouquet)

    def can_marry(self, npc: str) -> StardewRule:
        return self.has_hearts(npc, 10) & self.has(Gift.mermaid_pendant)

    def can_get_married(self) -> StardewRule:
        return self.has_hearts(Generic.bachelor, 10) & self.has(Gift.mermaid_pendant)

    def has_children(self, number_children: int) -> StardewRule:
        if number_children <= 0:
            return True_()
        if self.options.friendsanity == Friendsanity.option_none:
            return self.can_reproduce(number_children)
        return self.received(possible_kids, number_children) & self.buildings.has_house(2)

    def can_reproduce(self, number_children: int = 1) -> StardewRule:
        if number_children <= 0:
            return True_()
        baby_rules = [self.can_get_married(), self.buildings.has_house(2), self.has_hearts(Generic.bachelor, 12),
                      self.has_children(number_children - 1)]
        return And(*baby_rules)

    # Should be cached
    def has_hearts(self, npc: str, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()
        if self.options.friendsanity == Friendsanity.option_none:
            return self.can_earn_relationship(npc, hearts)
        if npc not in all_villagers_by_name:
            if npc == Generic.any or npc == Generic.bachelor:
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    if npc == Generic.any or all_villagers_by_name[name].bachelor:
                        possible_friends.append(self.has_hearts(name, hearts))
                return Or(*possible_friends)
            if npc == Generic.all:
                mandatory_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    mandatory_friends.append(self.has_hearts(name, hearts))
                return And(*mandatory_friends)
            if npc.isnumeric():
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    possible_friends.append(self.has_hearts(name, hearts))
                return Count(int(npc), possible_friends)
            return self.can_earn_relationship(npc, hearts)

        if not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        if self.options.friendsanity == Friendsanity.option_bachelors and not villager.bachelor:
            return self.can_earn_relationship(npc, hearts)
        if self.options.friendsanity == Friendsanity.option_starting_npcs and not villager.available:
            return self.can_earn_relationship(npc, hearts)
        is_capped_at_8 = villager.bachelor and self.options.friendsanity != Friendsanity.option_all_with_marriage
        if is_capped_at_8 and hearts > 8:
            return self.received_hearts(villager.name, 8) & self.can_earn_relationship(npc, hearts)
        return self.received_hearts(villager.name, hearts)

    # Should be cached
    def received_hearts(self, npc: str, hearts: int) -> StardewRule:
        return self.received(self.heart(npc), math.ceil(hearts / self.options.friendsanity_heart_size))

    @cache_self1
    def can_meet(self, npc: str) -> StardewRule:
        if npc not in all_villagers_by_name or not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        rules = [self.region.can_reach_any(villager.locations)]
        if npc == NPC.kent:
            rules.append(self.time.has_year_two)
        elif npc == NPC.leo:
            rules.append(self.received("Island West Turtle"))
        elif npc == ModNPC.lance:
            rules.append(self.region.can_reach(Region.volcano_floor_10))

        return And(*rules)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        rules = []
        for npc in all_villagers_by_name:
            if not self.npc_is_in_current_slot(npc):
                continue
            meet_rule = self.can_meet(npc)
            rules.append(meet_rule)
        rules.append(self.gifts.has_any_universal_love)
        return And(*rules)

    # Should be cached
    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        if hearts <= 0:
            return True_()

        previous_heart = hearts - self.options.friendsanity_heart_size
        previous_heart_rule = self.has_hearts(npc, previous_heart)

        if npc not in all_villagers_by_name or not self.npc_is_in_current_slot(npc):
            return previous_heart_rule

        rules = [previous_heart_rule, self.can_meet(npc)]
        villager = all_villagers_by_name[npc]
        if hearts > 2 or hearts > self.options.friendsanity_heart_size:
            rules.append(self.season.has(villager.birthday))
        if villager.bachelor:
            if hearts > 8:
                rules.append(self.can_date(npc))
            if hearts > 10:
                rules.append(self.can_marry(npc))

        return And(*rules)

    @cache_self1
    def npc_is_in_current_slot(self, name: str) -> bool:
        npc = all_villagers_by_name[name]
        mod = npc.mod_name
        return mod is None or mod in self.options.mods

    def heart(self, npc: Union[str, Villager]) -> str:
        if isinstance(npc, str):
            return f"{npc} <3"
        return self.heart(npc.name)
