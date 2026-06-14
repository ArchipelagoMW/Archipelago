from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ...data.artisan import MachineSource
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.game_item import ItemTag, Tag
from ...data.harvest import ArtifactSpotSource
from ...data.recipe_source import SkillSource
from ...data.requirement import SkillRequirement
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.animal_product_names import AnimalProduct
from ...strings.ap_names.mods.mod_items import ModBooks
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import ModMachine, ModConsumable, ModCraftable, ModFloor, Ring
from ...strings.fish_names import ModTrash, WaterItem
from ...strings.food_names import ArchaeologyMeal
from ...strings.forageable_names import Forageable
from ...strings.ingredient_names import Ingredient
from ...strings.material_names import Material
from ...strings.metal_names import all_artifacts, all_fossils, Fossil, Artifact, MetalBar, Mineral
from ...strings.seed_names import Seed
from ...strings.skill_names import ModSkill


def source_display_items(item: str, content: StardewContent):
    wood_display = f"Wooden Display: {item}"
    hardwood_display = f"Hardwood Display: {item}"
    if item == Fossil.trilobite:
        wood_display = f"Wooden Display: Trilobite Fossil"
        hardwood_display = f"Hardwood Display: Trilobite Fossil"
    content.source_item(wood_display, MachineSource(item=str(item), machine=ModMachine.preservation_chamber))
    content.source_item(hardwood_display, MachineSource(item=str(item), machine=ModMachine.hardwood_preservation_chamber))


class ArchaeologyContentPack(ContentPack):
    def artisan_good_hook(self, content: StardewContent):
        # Done as honestly there are too many display items to put into the initial registration traditionally.
        display_items = all_artifacts + all_fossils
        for item in display_items:
            source_display_items(item, content)
        content.source_item(ModTrash.rusty_scrap, *(MachineSource(item=artifact, machine=ModMachine.grinder) for artifact in all_artifacts))


register_mod_content_pack(ArchaeologyContentPack(
    ModNames.archaeology,
    skills=(Skill(name=ModSkill.archaeology, has_mastery=False),),
    harvest_sources={
        ModBooks.digging_like_worms: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ArtifactSpotSource(amount=22,  # I'm just copying Jack Be Nimble's chances for now -reptar
                               other_requirements=(SkillRequirement(ModSkill.archaeology, 2),)),
        )
    },
    cooking_recipes=(
        CookingRecipe(name=ArchaeologyMeal.diggers_delight, ingredients=((Forageable.cave_carrot, 2), (Ingredient.sugar, 1), (AnimalProduct.milk, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=3),),),
        CookingRecipe(name=ArchaeologyMeal.rocky_root, ingredients=((Forageable.cave_carrot, 3), (Seed.coffee, 1), (Material.stone, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=7),),),
        CookingRecipe(name=ArchaeologyMeal.ancient_jello, ingredients=((WaterItem.cave_jelly, 6), (Ingredient.sugar, 5), (AnimalProduct.egg, 1), (AnimalProduct.milk, 1), (Artifact.chipped_amphora, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=9),),),
    ),
    crafting_recipes=(
        CraftingRecipe(name=ModMachine.preservation_chamber, ingredients=((MetalBar.copper, 1), (Material.wood, 15), (ArtisanGood.oak_resin, 10),), sources=(SkillSource(skill=ModSkill.archaeology, level=1),),),
        CraftingRecipe(name=ModMachine.restoration_table, ingredients=((Material.wood, 25), (MetalBar.quartz, 1), (MetalBar.iron, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=1),),),
        CraftingRecipe(name=ModMachine.hardwood_preservation_chamber, ingredients=((MetalBar.copper, 1), (Material.hardwood, 15), (ArtisanGood.oak_resin, 10),), sources=(SkillSource(skill=ModSkill.archaeology, level=6),),),
        CraftingRecipe(name=ModMachine.grinder, ingredients=((Artifact.rusty_cog, 4), (MetalBar.iron, 5), (ArtisanGood.battery_pack, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=2),),),
        CraftingRecipe(name=ModMachine.ancient_battery, ingredients=((Material.stone, 40), (Material.clay, 10), (MetalBar.iron, 5),), sources=(SkillSource(skill=ModSkill.archaeology, level=7),),),
        CraftingRecipe(name=ModCraftable.glass_brazier, ingredients=((Artifact.glass_shards, 10), (Material.coal, 1), (Material.fiber, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=4),),),
        CraftingRecipe(name=ModFloor.glass_path, ingredients=((Artifact.glass_shards, 2),), sources=(SkillSource(skill=ModSkill.archaeology, level=3),),),
        CraftingRecipe(name=ModCraftable.glass_fence, ingredients=((Artifact.glass_shards, 2),), sources=(SkillSource(skill=ModSkill.archaeology, level=7),),),
        CraftingRecipe(name=ModFloor.bone_path, ingredients=((Fossil.bone_fragment, 2),), sources=(SkillSource(skill=ModSkill.archaeology, level=4),),),
        CraftingRecipe(name=ModFloor.rusty_path, ingredients=((ModTrash.rusty_scrap, 2),), sources=(SkillSource(skill=ModSkill.archaeology, level=2),),),
        CraftingRecipe(name=ModCraftable.rusty_brazier, ingredients=((ModTrash.rusty_scrap, 10), (Material.coal, 1), (Material.fiber, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=3),),),
        CraftingRecipe(name=ModCraftable.bone_fence, ingredients=((Fossil.bone_fragment, 2),), sources=(SkillSource(skill=ModSkill.archaeology, level=8),),),
        CraftingRecipe(name=ModCraftable.water_shifter, ingredients=((MetalBar.copper, 4), (Material.fiber, 8),), sources=(SkillSource(skill=ModSkill.archaeology, level=8),),),
        CraftingRecipe(name=ModCraftable.wooden_display, ingredients=((Material.wood, 25),), sources=(SkillSource(skill=ModSkill.archaeology, level=1),),),
        CraftingRecipe(name=ModCraftable.hardwood_display, ingredients=((Material.hardwood, 10),), sources=(SkillSource(skill=ModSkill.archaeology, level=6),),),
        CraftingRecipe(name=Ring.lucky_ring, ingredients=((Artifact.elvish_jewelry, 1), (AnimalProduct.rabbit_foot, 5), (Mineral.tigerseye, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=8),),),
        CraftingRecipe(name=ModConsumable.volcano_totem, ingredients=((Material.cinder_shard, 5), (Artifact.rare_disc, 1), (Artifact.dwarf_gadget, 1),), sources=(SkillSource(skill=ModSkill.archaeology, level=9),),),
    ),
))
