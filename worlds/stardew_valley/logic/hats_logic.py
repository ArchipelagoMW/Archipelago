from functools import cached_property

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.hats_data import Hats
from ..options import FestivalLocations
from ..stardew_rule import StardewRule
from ..strings.fish_names import Fish
from ..strings.forageable_names import Mushroom
from ..strings.monster_names import Monster
from ..strings.region_names import LogicRegion, Region


class HatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hat = HatLogic(*args, **kwargs)


class HatLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.hat_rules.update({
            Hats.laurel_wreath_crown.name: self.can_get_unlikely_hat_at_outfit_services,
            Hats.joja_cap.name: self.can_get_unlikely_hat_at_outfit_services,
            Hats.dark_ballcap.name: self.can_get_unlikely_hat_at_outfit_services,
            Hats.dark_cowboy_hat.name: self.logic.region.can_reach(Region.skull_cavern_100),
            Hats.garbage_hat.name: self.logic.region.can_reach(Region.town) & self.logic.time.has_lived_months(12),
            Hats.mystery_hat.name: self.logic.region.can_reach(Region.blacksmith) & self.logic.grind.can_grind_mystery_boxes(100),
            Hats.tiger_hat.name: self.logic.monster.can_kill_max(Monster.tiger_slime),
            Hats.living_hat.name: self.logic.grind.can_grind_weeds(100000),
            Hats.deluxe_pirate_hat.name: self.logic.region.can_reach_all(Region.volcano, Region.volcano_floor_5, Region.volcano_floor_10),
            Hats.spotted_headscarf.name: self.logic.tailoring.can_tailor(Mushroom.red),
            Hats.fishing_hat.name: self.logic.tailoring.can_tailor(Fish.stonefish, Fish.ice_pip, Fish.scorpion_carp, Fish.spook_fish, Fish.midnight_squid,
                                                             Fish.void_salmon, Fish.slimejack),
            Hats.bucket_hat.name: self.has_bucket_hat,
        })

    @cached_property
    def can_get_unlikely_hat_at_outfit_services(self) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.desert_festival) & self.logic.time.has_lived_months(12)

    @cached_property
    def has_bucket_hat(self) -> StardewRule:
        trout_derby_rule = self.logic.region.can_reach(LogicRegion.trout_derby) & self.logic.fishing.can_catch_fish(self.content.fishes[Fish.rainbow_trout])
        if self.options.festival_locations == FestivalLocations.option_disabled:
            return trout_derby_rule
        return trout_derby_rule & self.logic.received(Hats.bucket_hat.name)
