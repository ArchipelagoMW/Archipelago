from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data, fish_data
from ...data.game_item import ItemTag, Tag
from ...data.harvest import ForagingSource, HarvestCropSource
from ...mods.mod_data import ModNames
from ...strings.crop_names import DistantLandsCrop
from ...strings.forageable_names import DistantLandsForageable
from ...strings.region_names import Region
from ...strings.season_names import Season
from ...strings.seed_names import DistantLandsSeed

register_mod_content_pack(ContentPack(
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
        DistantLandsForageable.swamp_herb: (ForagingSource(regions=Region.witch_swamp),),
        DistantLandsForageable.brown_amanita: (ForagingSource(regions=Region.witch_swamp),),
        DistantLandsSeed.void_mint: (ForagingSource(regions=Region.witch_swamp),),
        DistantLandsCrop.void_mint: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=DistantLandsSeed.void_mint, seasons=(Season.spring, Season.summer, Season.fall)),),
        DistantLandsSeed.vile_ancient_fruit: (ForagingSource(regions=Region.witch_swamp),),
        DistantLandsCrop.vile_ancient_fruit: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=DistantLandsSeed.vile_ancient_fruit, seasons=(Season.spring, Season.summer, Season.fall)),)
    }
))
