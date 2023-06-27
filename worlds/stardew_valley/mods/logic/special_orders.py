from ...strings.craftable_names import Craftable
from ...strings.food_names import Meal
from ...strings.material_names import Material
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region
from ...strings.special_order_names import SpecialOrder, ModSpecialOrder
from ...strings.villager_names import ModNPC
from ..mod_data import ModNames
from ...options import StardewOptions
from ... import options


def modded_special_orders(self, world_options: StardewOptions):
    special_orders = {}
    if ModNames.juna in world_options[options.Mods]:
        special_orders.update({
            ModSpecialOrder.junas_monster_mash: self.has_relationship(ModNPC.juna, 4) &
                                   self.can_complete_special_order(SpecialOrder.a_curious_substance) &
                                   self.has_rusty_key() &
                                   self.can_reach_region(Region.forest) & self.has(Craftable.monster_musk) &
                                   self.has("Energy Tonic") & self.has(Material.sap) & self.has(Loot.bug_meat) &
                                   self.has(Craftable.oil_of_garlic) & self.has(Meal.strange_bun)
        })

    return special_orders
