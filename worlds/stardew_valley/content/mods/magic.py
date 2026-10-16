from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.shop import ShopSource
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.craftable_names import ModEdible, Edible, ModCraftable
from ...strings.forageable_names import Mushroom
from ...strings.monster_drop_names import Loot
from ...strings.region_names import Region
from ...strings.skill_names import ModSkill

register_mod_content_pack(ContentPack(
    ModNames.magic,
    skills=(Skill(name=ModSkill.magic, has_mastery=False),),
    cooking_recipes=(
        CookingRecipe(name=ModEdible.magic_elixir, ingredients=((Edible.life_elixir, 1), (Mushroom.purple, 1),), sources=(ShopSource(shop_region=Region.adventurer_guild, price=3000),), ),
    ),
    crafting_recipes=(
        CraftingRecipe(name=ModCraftable.travel_core, ingredients=((Loot.solar_essence, 1), (Loot.void_essence, 1),), sources=(ShopSource(shop_region=Region.adventurer_guild, price=250),),),
    ),
))
