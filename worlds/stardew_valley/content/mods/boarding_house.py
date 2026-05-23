from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data
from ...data.cooking_recipe import CookingRecipe
from ...data.recipe_source import FriendshipSource
from ...mods.mod_data import ModNames
from ...strings.animal_product_names import AnimalProduct
from ...strings.crop_names import Vegetable
from ...strings.food_names import BoardingHouseMeal
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
))
