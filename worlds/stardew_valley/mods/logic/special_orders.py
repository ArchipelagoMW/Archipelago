from typing import Union
from ...strings.craftable_names import Craftable
from ...strings.food_names import Meal
from ...strings.material_names import Material
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region
from ...strings.special_order_names import SpecialOrder, ModSpecialOrder
from ...strings.villager_names import ModNPC
from ..mod_data import ModNames


def get_modded_special_orders_rules(vanilla_logic, active_mods):
    special_orders = {}
    if ModNames.juna in active_mods:
        special_orders.update({
            ModSpecialOrder.junas_monster_mash: vanilla_logic.has_relationship(ModNPC.juna, 4) &
                                                vanilla_logic.can_complete_special_order(SpecialOrder.a_curious_substance) &
                                                vanilla_logic.has_rusty_key() &
                                                vanilla_logic.can_reach_region(Region.forest) & vanilla_logic.has(Craftable.monster_musk) &
                                                vanilla_logic.has("Energy Tonic") & vanilla_logic.has(Material.sap) & vanilla_logic.has(Loot.bug_meat) &
                                                vanilla_logic.has(Craftable.oil_of_garlic) & vanilla_logic.has(Meal.strange_bun)
        })

    return special_orders
