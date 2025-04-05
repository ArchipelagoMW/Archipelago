from typing import Dict, Union

from .ability_logic import AbilityLogicMixin
from .arcade_logic import ArcadeLogicMixin
from .artisan_logic import ArtisanLogicMixin
from .base_logic import BaseLogicMixin, BaseLogic
from .cooking_logic import CookingLogicMixin
from .has_logic import HasLogicMixin
from .mine_logic import MineLogicMixin
from .money_logic import MoneyLogicMixin
from .monster_logic import MonsterLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .season_logic import SeasonLogicMixin
from .shipping_logic import ShippingLogicMixin
from .skill_logic import SkillLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..content.vanilla.qi_board import qi_board_content_pack
from ..stardew_rule import StardewRule, Has, false_
from ..strings.animal_product_names import AnimalProduct
from ..strings.ap_names.transport_names import Transportation
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Vegetable, Fruit
from ..strings.fertilizer_names import Fertilizer
from ..strings.fish_names import Fish
from ..strings.forageable_names import Forageable
from ..strings.machine_names import Machine
from ..strings.material_names import Material
from ..strings.metal_names import Mineral
from ..strings.monster_drop_names import Loot
from ..strings.monster_names import Monster
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.special_order_names import SpecialOrder
from ..strings.villager_names import NPC


class SpecialOrderLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special_order = SpecialOrderLogic(*args, **kwargs)


class SpecialOrderLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, TimeLogicMixin, MoneyLogicMixin,
ShippingLogicMixin, ArcadeLogicMixin, ArtisanLogicMixin, RelationshipLogicMixin, ToolLogicMixin, SkillLogicMixin,
MineLogicMixin, CookingLogicMixin,
AbilityLogicMixin, SpecialOrderLogicMixin, MonsterLogicMixin]]):

    def initialize_rules(self):
        self.update_rules({
            SpecialOrder.cave_patrol: self.logic.relationship.can_meet(NPC.clint),
            SpecialOrder.aquatic_overpopulation: self.logic.relationship.can_meet(NPC.demetrius) & self.logic.ability.can_fish_perfectly(),
            SpecialOrder.biome_balance: self.logic.relationship.can_meet(NPC.demetrius) & self.logic.ability.can_fish_perfectly(),
            SpecialOrder.rock_rejuivenation: (self.logic.relationship.has_hearts(NPC.emily, 4) &
                                              self.logic.has_all(Mineral.ruby, Mineral.topaz, Mineral.emerald, Mineral.jade, Mineral.amethyst,
                                                                 ArtisanGood.cloth)),
            SpecialOrder.gifts_for_george: self.logic.season.has(Season.spring) & self.logic.has(Forageable.leek),
            SpecialOrder.fragments_of_the_past: self.logic.monster.can_kill(Monster.skeleton),
            SpecialOrder.gus_famous_omelet: self.logic.has(AnimalProduct.any_egg),
            SpecialOrder.crop_order: self.logic.ability.can_farm_perfectly() & self.logic.shipping.can_use_shipping_bin,
            SpecialOrder.community_cleanup: self.logic.skill.can_crab_pot,
            SpecialOrder.the_strong_stuff: self.logic.has(ArtisanGood.specific_juice(Vegetable.potato)),
            SpecialOrder.pierres_prime_produce: self.logic.ability.can_farm_perfectly(),
            SpecialOrder.robins_project: self.logic.relationship.can_meet(NPC.robin) & self.logic.ability.can_chop_perfectly() &
                                         self.logic.has(Material.hardwood),
            SpecialOrder.robins_resource_rush: self.logic.relationship.can_meet(NPC.robin) & self.logic.ability.can_chop_perfectly() &
                                               self.logic.has(Fertilizer.tree) & self.logic.ability.can_mine_perfectly(),
            SpecialOrder.juicy_bugs_wanted: self.logic.has(Loot.bug_meat),
            SpecialOrder.a_curious_substance: self.logic.region.can_reach(Region.wizard_tower),
            SpecialOrder.prismatic_jelly: self.logic.region.can_reach(Region.wizard_tower),

        })

        if ginger_island_content_pack.name in self.content.registered_packs:
            self.update_rules({
                SpecialOrder.island_ingredients: self.logic.relationship.can_meet(NPC.caroline) & self.logic.special_order.has_island_transport() &
                                                 self.logic.ability.can_farm_perfectly() & self.logic.shipping.can_ship(Vegetable.taro_root) &
                                                 self.logic.shipping.can_ship(Fruit.pineapple) & self.logic.shipping.can_ship(Forageable.ginger),
                SpecialOrder.tropical_fish: self.logic.relationship.can_meet(NPC.willy) & self.logic.received("Island Resort") &
                                            self.logic.special_order.has_island_transport() &
                                            self.logic.has(Fish.stingray) & self.logic.has(Fish.blue_discus) & self.logic.has(Fish.lionfish),
            })
        else:
            self.update_rules({
                SpecialOrder.island_ingredients: false_,
                SpecialOrder.tropical_fish: false_,
            })

        if qi_board_content_pack.name in self.content.registered_packs:
            self.update_rules({
                SpecialOrder.qis_crop: self.logic.ability.can_farm_perfectly() & self.logic.region.can_reach(Region.greenhouse) &
                                       self.logic.region.can_reach(Region.island_west) & self.logic.skill.has_total_level(50) &
                                       self.logic.has(Machine.seed_maker) & self.logic.shipping.can_use_shipping_bin,
                SpecialOrder.lets_play_a_game: self.logic.arcade.has_junimo_kart_max_level(),
                SpecialOrder.four_precious_stones: self.logic.time.has_lived_max_months & self.logic.has("Prismatic Shard") &
                                                   self.logic.ability.can_mine_perfectly_in_the_skull_cavern(),
                SpecialOrder.qis_hungry_challenge: self.logic.ability.can_mine_perfectly_in_the_skull_cavern(),
                SpecialOrder.qis_cuisine: self.logic.cooking.can_cook() & self.logic.shipping.can_use_shipping_bin &
                                          (self.logic.money.can_spend_at(Region.saloon, 205000) | self.logic.money.can_spend_at(Region.pierre_store, 170000)),
                SpecialOrder.qis_kindness: self.logic.relationship.can_give_loved_gifts_to_everyone(),
                SpecialOrder.extended_family: self.logic.ability.can_fish_perfectly() & self.logic.has(Fish.angler) & self.logic.has(Fish.glacierfish) &
                                              self.logic.has(Fish.crimsonfish) & self.logic.has(Fish.mutant_carp) & self.logic.has(Fish.legend),
                SpecialOrder.danger_in_the_deep: self.logic.ability.can_mine_perfectly() & self.logic.mine.has_mine_elevator_to_floor(120),
                SpecialOrder.skull_cavern_invasion: self.logic.ability.can_mine_perfectly_in_the_skull_cavern(),
                SpecialOrder.qis_prismatic_grange: self.logic.has(Loot.bug_meat) &  # 100 Bug Meat
                                                   self.logic.money.can_spend_at(Region.saloon, 24000) &  # 100 Spaghetti
                                                   self.logic.money.can_spend_at(Region.blacksmith, 15000) &  # 100 Copper Ore
                                                   self.logic.money.can_spend_at(Region.ranch, 5000) &  # 100 Hay
                                                   self.logic.money.can_spend_at(Region.saloon, 22000) &  # 100 Salads
                                                   self.logic.money.can_spend_at(Region.saloon, 7500) &  # 100 Joja Cola
                                                   self.logic.money.can_spend(80000),  # I need this extra rule because money rules aren't additive...)
            })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.registry.special_order_rules.update(new_rules)

    def can_complete_special_order(self, special_order: str) -> StardewRule:
        return Has(special_order, self.registry.special_order_rules, "special order")

    def has_island_transport(self) -> StardewRule:
        return self.logic.received(Transportation.island_obelisk) | self.logic.received(Transportation.boat_repair)
