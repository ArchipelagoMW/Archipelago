from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data, fish_data
from ...data.cooking_recipe import CookingRecipe
from ...data.game_item import ItemTag, Tag
from ...data.harvest import ForagingSource, HarvestCropSource
from ...data.recipe_source import FriendshipSource
from ...data.requirement import QuestRequirement
from ...mods.mod_data import ModNames
from ...strings.crop_names import DistantLandsCrop
from ...strings.fish_names import Fish, DistantLandsFish, WaterItem
from ...strings.food_names import DistantLandsMeal
from ...strings.forageable_names import DistantLandsForageable, Forageable, Mushroom
from ...strings.material_names import Material
from ...strings.monster_drop_names import Loot
from ...strings.quest_names import ModQuest
from ...strings.region_names import Region
from ...strings.season_names import Season
from ...strings.seed_names import DistantLandsSeed
from ...strings.villager_names import ModNPC


class DistantLandsContentPack(ContentPack):

    def harvest_source_hook(self, content: StardewContent):
        content.untag_item(DistantLandsSeed.void_mint, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(DistantLandsSeed.vile_ancient_fruit, tag=ItemTag.CROPSANITY_SEED)


register_mod_content_pack(DistantLandsContentPack(
    ModNames.distant_lands,
    fishes=(
        fish_data.void_minnow,
        fish_data.purple_algae,
        fish_data.swamp_leech,
        fish_data.giant_horsehoe_crab,
    ),
    villagers=(
        villagers_data.zic,
    ),
    harvest_sources={
        DistantLandsForageable.swamp_herb: (ForagingSource(regions=(Region.witch_swamp,)),),
        DistantLandsForageable.brown_amanita: (ForagingSource(regions=(Region.witch_swamp,)),),
        DistantLandsSeed.void_mint: (ForagingSource(regions=(Region.witch_swamp,), other_requirements=(QuestRequirement(ModQuest.CorruptedCropsTask),)),),
        DistantLandsCrop.void_mint: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=DistantLandsSeed.void_mint, seasons=(Season.spring, Season.summer, Season.fall)),),
        DistantLandsSeed.vile_ancient_fruit: (ForagingSource(regions=(Region.witch_swamp,), other_requirements=(QuestRequirement(ModQuest.CorruptedCropsTask),)),),
        DistantLandsCrop.vile_ancient_fruit: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=DistantLandsSeed.vile_ancient_fruit, seasons=(Season.spring, Season.summer, Season.fall)),)
    },
    cooking_recipes=(
        CookingRecipe(name=DistantLandsMeal.mushroom_kebab, ingredients=((Mushroom.chanterelle, 1), (Mushroom.common, 1), (Mushroom.red, 1), (Material.wood, 1),), sources=(FriendshipSource(friend=ModNPC.goblin, hearts=2),),),
        CookingRecipe(name=DistantLandsMeal.void_mint_tea, ingredients=((DistantLandsCrop.void_mint, 1),), sources=(FriendshipSource(friend=ModNPC.goblin, hearts=4),),),
        CookingRecipe(name=DistantLandsMeal.crayfish_soup, ingredients=((Forageable.cave_carrot, 1), (Fish.crayfish, 1), (DistantLandsFish.purple_algae, 1), (WaterItem.white_algae, 1),), sources=(FriendshipSource(friend=ModNPC.goblin, hearts=6),),),
        CookingRecipe(name=DistantLandsMeal.pemmican, ingredients=((Loot.bug_meat, 1), (Fish.any, 1), (Forageable.salmonberry, 3), (Material.stone, 2),), sources=(FriendshipSource(friend=ModNPC.goblin, hearts=8),),),
    ),
))