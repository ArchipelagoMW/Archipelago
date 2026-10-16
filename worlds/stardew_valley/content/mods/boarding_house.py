from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.recipe_source import FriendshipSource
from ...data.shop import ShopSource
from ...mods.mod_data import ModNames
from ...strings.animal_product_names import AnimalProduct
from ...strings.craftable_names import ModCraftable
from ...strings.crop_names import Vegetable
from ...strings.food_names import BoardingHouseMeal
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar, ModFossil
from ...strings.region_names import LogicRegion
from ...strings.villager_names import ModNPC

register_mod_content_pack(ContentPack(
    ModNames.boarding_house,
    villagers=(
        villagers_data.gregory,
        villagers_data.sheila,
        villagers_data.joel,
    ),
    cooking_recipes=(
        CookingRecipe(name=BoardingHouseMeal.special_pumpkin_soup, ingredients=((Vegetable.pumpkin, 2), (AnimalProduct.large_goat_milk, 1), (Vegetable.garlic, 1),), sources=(FriendshipSource(friend=ModNPC.joel, hearts=6),),),
    ),
    crafting_recipes=(
        CraftingRecipe(name=ModCraftable.neanderthal_skeleton, ingredients=((ModFossil.neanderthal_skull, 1), (ModFossil.neanderthal_ribs, 1), (ModFossil.neanderthal_pelvis, 1), (ModFossil.neanderthal_limb_bones, 1), (MetalBar.iron, 5), (Material.hardwood, 10),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.pterodactyl_skeleton_l, ingredients=((ModFossil.pterodactyl_phalange, 1), (ModFossil.pterodactyl_skull, 1), (ModFossil.pterodactyl_l_wing_bone, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.pterodactyl_skeleton_m, ingredients=((ModFossil.pterodactyl_phalange, 1), (ModFossil.pterodactyl_vertebra, 1), (ModFossil.pterodactyl_ribs, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.pterodactyl_skeleton_r, ingredients=((ModFossil.pterodactyl_phalange, 1), (ModFossil.pterodactyl_claw, 1), (ModFossil.pterodactyl_r_wing_bone, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.trex_skeleton_l, ingredients=((ModFossil.dinosaur_vertebra, 1), (ModFossil.dinosaur_tooth, 1), (ModFossil.dinosaur_skull, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.trex_skeleton_m, ingredients=((ModFossil.dinosaur_vertebra, 1), (ModFossil.dinosaur_ribs, 1), (ModFossil.dinosaur_claw, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
        CraftingRecipe(name=ModCraftable.trex_skeleton_r, ingredients=((ModFossil.dinosaur_vertebra, 1), (ModFossil.dinosaur_femur, 1), (ModFossil.dinosaur_pelvis, 1), (MetalBar.iron, 10), (Material.hardwood, 15),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000),),),
    ),
))
