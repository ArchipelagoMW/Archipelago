from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data, villagers_data
from ...data.harvest import ForagingSource, HarvestCropSource
from ...data.shop import ShopSource
from ...strings.crop_names import Fruit, Vegetable
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.region_names import Region
from ...strings.season_names import Season
from ...strings.seed_names import Seed

the_desert = ContentPack(
    "The Desert (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.cactus_fruit: (
            ForagingSource(regions=(Region.desert,)),
            HarvestCropSource(seed=Seed.cactus, seasons=())
        ),
        Forageable.coconut: (
            ForagingSource(regions=(Region.desert,)),
        ),
        Mushroom.purple: (
            ForagingSource(regions=(Region.skull_cavern_25,)),
        ),

        Fruit.rhubarb: (HarvestCropSource(seed=Seed.rhubarb, seasons=(Season.spring,)),),
        Fruit.starfruit: (HarvestCropSource(seed=Seed.starfruit, seasons=(Season.summer,)),),
        Vegetable.beet: (HarvestCropSource(seed=Seed.beet, seasons=(Season.fall,)),),
    },
    shop_sources={
        Seed.cactus: (ShopSource(money_price=150, shop_region=Region.oasis),),
        Seed.rhubarb: (ShopSource(money_price=100, shop_region=Region.oasis, seasons=(Season.spring,)),),
        Seed.starfruit: (ShopSource(money_price=400, shop_region=Region.oasis, seasons=(Season.summer,)),),
        Seed.beet: (ShopSource(money_price=20, shop_region=Region.oasis, seasons=(Season.fall,)),),
    },
    fishes=(
        fish_data.sandfish,
        fish_data.scorpion_carp,
    ),
    villagers=(
        villagers_data.sandy,
    ),
)
