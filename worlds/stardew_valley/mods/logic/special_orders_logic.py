from typing import Union

from ..mod_data import ModNames
from ...logic.action_logic import ActionLogicMixin
from ...logic.artisan_logic import ArtisanLogicMixin
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.crafting_logic import CraftingLogicMixin
from ...logic.crop_logic import CropLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.wallet_logic import WalletLogicMixin
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import Consumable, Edible, Bomb
from ...strings.crop_names import Fruit
from ...strings.fertilizer_names import Fertilizer
from ...strings.food_names import Meal
from ...strings.geode_names import Geode
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region, SVERegion
from ...strings.special_order_names import SpecialOrder, ModSpecialOrder
from ...strings.villager_names import ModNPC


class ModSpecialOrderLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special_order = ModSpecialOrderLogic(*args, **kwargs)


class ModSpecialOrderLogic(BaseLogic[Union[ActionLogicMixin, ArtisanLogicMixin, CraftingLogicMixin, CropLogicMixin, HasLogicMixin, RegionLogicMixin,
RelationshipLogicMixin, SeasonLogicMixin, WalletLogicMixin]]):
    def get_modded_special_orders_rules(self):
        special_orders = {}
        if ModNames.juna in self.options.mods:
            special_orders.update({
                ModSpecialOrder.junas_monster_mash: self.logic.relationship.has_hearts(ModNPC.juna, 4) &
                                                    self.registry.special_order_rules[SpecialOrder.a_curious_substance] &
                                                    self.logic.wallet.has_rusty_key() &
                                                    self.logic.region.can_reach(Region.forest) & self.logic.has(Consumable.monster_musk) &
                                                    self.logic.has("Energy Tonic") & self.logic.has(Material.sap) & self.logic.has(Loot.bug_meat) &
                                                    self.logic.has(Edible.oil_of_garlic) & self.logic.has(Meal.strange_bun)
            })
        if ModNames.sve in self.options.mods:
            special_orders.update({
                ModSpecialOrder.andys_cellar: self.logic.has(Material.stone) & self.logic.has(Material.wood) & self.logic.has(Material.hardwood) &
                                              self.logic.has(MetalBar.iron) &
                                              self.logic.region.can_reach(SVERegion.fairhaven_farm),
                ModSpecialOrder.a_mysterious_venture: self.logic.has(Bomb.cherry_bomb) & self.logic.has(Bomb.bomb) & self.logic.has(Bomb.mega_bomb) &
                                                      self.logic.region.can_reach(Region.adventurer_guild),
                ModSpecialOrder.an_elegant_reception: self.logic.artisan.can_keg(Fruit.starfruit) & self.logic.has(ArtisanGood.cheese) &
                                                      self.logic.has(ArtisanGood.goat_cheese) & self.logic.season.has_any_not_winter() &
                                                      self.logic.region.can_reach(SVERegion.jenkins_cellar),
                ModSpecialOrder.fairy_garden: self.logic.has(Consumable.fairy_dust) &
                                              self.logic.region.can_reach(Region.island_south) & (
                                                      self.logic.action.can_open_geode(Geode.frozen) | self.logic.action.can_open_geode(Geode.omni)) &
                                              self.logic.region.can_reach(SVERegion.blue_moon_vineyard),
                ModSpecialOrder.homemade_fertilizer: self.logic.has(Fertilizer.quality) & self.logic.region.can_reach(SVERegion.susans_house)
            })

        return special_orders
