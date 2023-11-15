from typing import Iterable

from ...logic.action_logic import ActionLogic
from ...logic.artisan_logic import ArtisanLogic
from ...logic.crafting_logic import CraftingLogic
from ...logic.crop_logic import CropLogic
from ...logic.has_logic import HasLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.wallet_logic import WalletLogic
from ...options import Mods
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import Consumable, Edible, Bomb
from ...strings.fertilizer_names import Fertilizer
from ...strings.flower_names import Flower
from ...strings.food_names import Meal
from ...strings.crop_names import Fruit
from ...strings.geode_names import Geode
from ...strings.machine_names import Machine
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region, SVERegion
from ...strings.special_order_names import SpecialOrder, ModSpecialOrder
from ...strings.villager_names import ModNPC
from ..mod_data import ModNames


class ModSpecialOrderLogic:
    player: int
    action: ActionLogic
    artisan: ArtisanLogic
    crafting: CraftingLogic
    crop: CropLogic
    has: HasLogic
    region: RegionLogic
    relationship: RelationshipLogic
    season: SeasonLogic
    wallet: WalletLogic
    mods_option: Mods

    def __init__(self, player: int, action: ActionLogic, artisan: ArtisanLogic, crafting: CraftingLogic, crop: CropLogic, has: HasLogic, region: RegionLogic, relationship: RelationshipLogic,
                 season: SeasonLogic, wallet: WalletLogic, mods_option: Mods):
        self.player = player
        self.action = action
        self.artisan = artisan
        self.crafting = crafting
        self.crop = crop
        self.has = has
        self.region = region
        self.relationship = relationship
        self.season = season
        self.wallet = wallet
        self.mods_option = mods_option

    def get_modded_special_orders_rules(self, vanilla_rules):
        special_orders = {}
        if ModNames.juna in self.mods_option:
            special_orders.update({
                ModSpecialOrder.junas_monster_mash: self.relationship.has_hearts(ModNPC.juna, 4) &
                                                    vanilla_rules[SpecialOrder.a_curious_substance] &
                                                    self.wallet.has_rusty_key &
                                                    self.region.can_reach(Region.forest) & self.has(Consumable.monster_musk) &
                                                    self.has("Energy Tonic") & self.has(Material.sap) & self.has(Loot.bug_meat) &
                                                    self.has(Edible.oil_of_garlic) & self.has(Meal.strange_bun)
            })
        if ModNames.sve in self.mods_option:
            special_orders.update({
                ModSpecialOrder.andys_cellar: self.has(Material.stone) & self.has(Material.wood) & self.has(Material.hardwood) & self.has(MetalBar.iron) &
                                              self.region.can_reach(SVERegion.fairhaven_farm),
                ModSpecialOrder.a_mysterious_venture: self.has(Bomb.cherry_bomb) & self.has(Bomb.bomb) & self.has(Bomb.mega_bomb) &
                                                      self.region.can_reach(Region.adventurer_guild),
                ModSpecialOrder.an_elegant_reception: self.artisan.can_keg(Fruit.starfruit) & self.has(ArtisanGood.cheese) &
                                                      self.has(ArtisanGood.goat_cheese) & self.season.has_any_not_winter() & self.region.can_reach(SVERegion.jenkins_cellar),
                ModSpecialOrder.fairy_garden: self.has(Consumable.fairy_dust) &
                                              self.region.can_reach(Region.island_south) & (self.action.can_open_geode(Geode.frozen) | self.action.can_open_geode(Geode.omni)) &
                                              self.region.can_reach(SVERegion.blue_moon_vineyard),
                ModSpecialOrder.homemade_fertilizer: self.has(Fertilizer.quality) & self.region.can_reach(SVERegion.susans_house)
            })

        return special_orders
