from typing import Iterable

from ...logic.has_logic import HasLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.wallet_logic import WalletLogic
from ...strings.craftable_names import Consumable, Edible
from ...strings.food_names import Meal
from ...strings.material_names import Material
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region
from ...strings.special_order_names import SpecialOrder, ModSpecialOrder
from ...strings.villager_names import ModNPC
from ..mod_data import ModNames


class ModSpecialOrderLogic:
    player: int
    has: HasLogic
    region: RegionLogic
    relationship: RelationshipLogic
    wallet: WalletLogic
    mods_option: Iterable[str]

    def __init__(self, player: int, has: HasLogic, region: RegionLogic, relationship: RelationshipLogic, wallet: WalletLogic, mods_option: Iterable[str]):
        self.player = player
        self.has = has
        self.region = region
        self.relationship = relationship
        self.wallet = wallet
        self.mods_option = mods_option

    def get_modded_special_orders_rules(self, vanilla_rules):
        special_orders = {}
        if ModNames.juna in self.mods_option:
            special_orders.update({
                ModSpecialOrder.junas_monster_mash: self.relationship.has_hearts(ModNPC.juna, 4) &
                                                    vanilla_rules[SpecialOrder.a_curious_substance] &
                                                    self.wallet.has_rusty_key() &
                                                    self.region.can_reach(Region.forest) & self.has(Consumable.monster_musk) &
                                                    self.has("Energy Tonic") & self.has(Material.sap) & self.has(Loot.bug_meat) &
                                                    self.has(Edible.oil_of_garlic) & self.has(Meal.strange_bun)
            })

        return special_orders
