from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.recipe_source import SkillSource
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.animal_product_names import AnimalProduct
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import ModMachine
from ...strings.crop_names import Vegetable
from ...strings.fish_names import Fish, Trash
from ...strings.flower_names import Flower
from ...strings.food_names import TrashyMeal, Meal
from ...strings.forageable_names import Forageable
from ...strings.gift_names import Gift
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar
from ...strings.monster_drop_names import Loot
from ...strings.skill_names import ModSkill

register_mod_content_pack(ContentPack(
    ModNames.luck_skill,
    skills=(Skill(name=ModSkill.luck, has_mastery=False),),
    crafting_recipes=(
        CraftingRecipe(name=ModMachine.copper_slot_machine, ingredients=((MetalBar.copper, 15), (Material.stone, 1), (Material.wood, 1), (Material.fiber, 1), (Material.sap, 1), (Loot.slime, 1), (Forageable.salmonberry, 1), (Material.clay, 1), (Trash.joja_cola, 1),), sources=(SkillSource(skill=ModSkill.luck, level=2),),),
        CraftingRecipe(name=ModMachine.gold_slot_machine, ingredients=((MetalBar.gold, 15), (ModMachine.copper_slot_machine, 1),), sources=(SkillSource(skill=ModSkill.luck, level=4),),),
        CraftingRecipe(name=ModMachine.iridium_slot_machine, ingredients=((MetalBar.iridium, 15), (ModMachine.gold_slot_machine, 1),), sources=(SkillSource(skill=ModSkill.luck, level=6),),),
        CraftingRecipe(name=ModMachine.radioactive_slot_machine, ingredients=((MetalBar.radioactive, 15), (ModMachine.iridium_slot_machine, 1),), sources=(SkillSource(skill=ModSkill.luck, level=8),),),
    ),
))

register_mod_content_pack(ContentPack(
    ModNames.socializing_skill,
    skills=(Skill(name=ModSkill.socializing, has_mastery=False),),
    crafting_recipes=(
        CraftingRecipe(name=Gift.bouquet, ingredients=((Flower.tulip, 3),), sources=(SkillSource(skill=ModSkill.socializing, level=3),),),
    ),
))

register_mod_content_pack(ContentPack(
    ModNames.cooking_skill,
    skills=(Skill(name=ModSkill.cooking, has_mastery=False),),
))

register_mod_content_pack(ContentPack(
    ModNames.binning_skill,
    skills=(Skill(name=ModSkill.binning, has_mastery=False),),
    cooking_recipes=(
        CookingRecipe(name=TrashyMeal.grilled_cheese, ingredients=((Meal.bread, 1), (ArtisanGood.cheese, 1),), sources=(SkillSource(skill=ModSkill.binning, level=1),),),
        CookingRecipe(name=TrashyMeal.fish_casserole, ingredients=((Fish.any, 1), (AnimalProduct.milk, 1), (Vegetable.carrot, 1),), sources=(SkillSource(skill=ModSkill.binning, level=8),),),
    ),
    crafting_recipes=(
        CraftingRecipe(name=ModMachine.trash_bin, ingredients=((Material.stone, 30), (MetalBar.iron, 2),), sources=(SkillSource(skill=ModSkill.binning, level=2),),),
        CraftingRecipe(name=ModMachine.composter, ingredients=((Material.wood, 70), (Material.sap, 20), (Material.fiber, 30),), sources=(SkillSource(skill=ModSkill.binning, level=4),),),
        CraftingRecipe(name=ModMachine.recycling_bin, ingredients=((MetalBar.iron, 3), (Material.fiber, 10), (MetalBar.gold, 2),), sources=(SkillSource(skill=ModSkill.binning, level=7),),),
        CraftingRecipe(name=ModMachine.advanced_recycling_machine, ingredients=((MetalBar.iridium, 5), (ArtisanGood.battery_pack, 2), (MetalBar.quartz, 10),), sources=(SkillSource(skill=ModSkill.binning, level=9),),),
    ),
))
