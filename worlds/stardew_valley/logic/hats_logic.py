from functools import cached_property

from .base_logic import BaseLogicMixin, BaseLogic
from ..options import FestivalLocations
from ..stardew_rule import StardewRule
from ..strings.fish_names import Fish
from ..strings.forageable_names import Mushroom
from ..strings.geode_names import Geode
from ..strings.hat_names import Hat
from ..strings.monster_names import Monster
from ..strings.region_names import LogicRegion, Region


class HatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hat = HatLogic(*args, **kwargs)


class HatLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.hat_rules.update({
            Hat.laurel_wreath_crown: self.can_get_unlikely_hat_at_outfit_services,
            Hat.joja_cap: self.can_get_unlikely_hat_at_outfit_services,
            Hat.dark_ballcap: self.can_get_unlikely_hat_at_outfit_services,
            Hat.dark_cowboy_hat: self.logic.region.can_reach(Region.skull_cavern_100),
            Hat.garbage_hat: self.logic.region.can_reach(Region.town) & self.logic.time.has_lived_months(12),
            Hat.mystery_hat: self.logic.region.can_reach(Region.blacksmith) & self.logic.grind.can_grind_mystery_boxes(100),
            Hat.golden_helmet: self.logic.region.can_reach(Region.blacksmith) & self.logic.has(Geode.golden_coconut),
            Hat.tiger_hat: self.logic.monster.can_kill_max(Monster.tiger_slime),
            Hat.living_hat: self.logic.grind.can_grind_weeds(100000),
            Hat.deluxe_pirate_hat: self.logic.region.can_reach_all(Region.volcano, Region.volcano_floor_5, Region.volcano_floor_10),
            Hat.spotted_headscarf: self.logic.tailoring.can_tailor(Mushroom.red),
            Hat.fishing_hat: self.logic.tailoring.can_tailor(Fish.stonefish, Fish.ice_pip, Fish.scorpion_carp, Fish.spook_fish, Fish.midnight_squid,
                                                             Fish.void_salmon, Fish.slimejack),
            Hat.bucket_hat: self.has_bucket_hat,
        })

    @cached_property
    def can_get_unlikely_hat_at_outfit_services(self) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.desert_festival) & self.logic.time.has_lived_months(12)

    @cached_property
    def has_bucket_hat(self) -> StardewRule:
        trout_derby_rule = self.logic.region.can_reach(LogicRegion.trout_derby) & self.logic.fishing.can_catch_fish(self.content.fishes[Fish.rainbow_trout])
        if self.options.festival_locations == FestivalLocations.option_disabled:
            return trout_derby_rule
        return trout_derby_rule & self.logic.received(Hat.bucket_hat)
