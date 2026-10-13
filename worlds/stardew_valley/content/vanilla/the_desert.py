from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data, villagers_data
from ...data.game_item import CustomRuleSource, ItemTag, Tag
from ...data.harvest import ForagingSource, HarvestCropSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.requirement import RegionRequirement, MeetRequirement, MonsterKillRequirement
from ...data.shop import ShopSource
from ...logic.tailoring_logic import TailoringSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.crop_names import Fruit, Vegetable
from ...strings.currency_names import Currency
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.geode_names import Geode
from ...strings.metal_names import Artifact
from ...strings.monster_names import Monster
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed
from ...strings.villager_names import NPC

the_desert = ContentPack(
    "The Desert (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.cactus_fruit: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.desert,)),
            HarvestCropSource(seed=Seed.cactus, seasons=())
        ),
        Forageable.coconut: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.desert,)),
        ),
        Mushroom.purple: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.skull_cavern_25,)),
        ),

        Fruit.rhubarb: (HarvestCropSource(seed=Seed.rhubarb, seasons=(Season.spring,)),),
        Fruit.starfruit: (HarvestCropSource(seed=Seed.starfruit, seasons=(Season.summer,)),),
        Vegetable.beet: (HarvestCropSource(seed=Seed.beet, seasons=(Season.fall,)),),
    },
    shop_sources={
        Seed.cactus: (ShopSource(price=150, shop_region=Region.oasis),),
        Seed.rhubarb: (ShopSource(price=100, shop_region=Region.oasis, seasons=(Season.spring,)),),
        Seed.starfruit: (ShopSource(price=400, shop_region=Region.oasis, seasons=(Season.summer,)),),
        Seed.beet: (ShopSource(price=20, shop_region=Region.oasis, seasons=(Season.fall,)),),
    },
    fishes=(
        fish_data.sandfish,
        fish_data.scorpion_carp,
    ),
    villagers=(
        villagers_data.sandy,
    ),
    hat_sources={
        Hats.top_hat: (Tag(ItemTag.HAT), ShopSource(price=8000, shop_region=Region.casino, currency=Currency.qi_coin),),
        Hats.gils_hat: (Tag(ItemTag.HAT), ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                                          other_requirements=(
                                                              RegionRequirement(Region.skull_cavern_100), RegionRequirement(LogicRegion.desert_festival),)),),
        Hats.abigails_bow: (Tag(ItemTag.HAT), ShopSource(price=60, currency=Currency.calico_egg, shop_region=LogicRegion.desert_festival,
                                                              other_requirements=(MeetRequirement(NPC.abigail),)),),
        Hats.tricorn: (Tag(ItemTag.HAT), ShopSource(price=100, currency=Currency.calico_egg, shop_region=LogicRegion.desert_festival,
                                                              other_requirements=(MeetRequirement(NPC.elliott),)),),
        Hats.blue_bow: (Tag(ItemTag.HAT), ShopSource(price=60, currency=Currency.calico_egg, shop_region=LogicRegion.desert_festival),),
        Hats.dark_velvet_bow: (Tag(ItemTag.HAT), ShopSource(price=75, currency=Currency.calico_egg, shop_region=LogicRegion.desert_festival),),
        Hats.mummy_mask: (Tag(ItemTag.HAT), ShopSource(price=120, currency=Currency.calico_egg, shop_region=LogicRegion.desert_festival),),
        Hats.arcane_hat: (Tag(ItemTag.HAT), ShopSource(price=20000, shop_region=Region.adventurer_guild,
                                                            other_requirements=(MonsterKillRequirement((Monster.mummy,), 100),)),),
        Hats.green_turban: (Tag(ItemTag.HAT), ShopSource(price=50, currency=Geode.omni, shop_region=Region.desert,),),
        Hats.magic_cowboy_hat: (Tag(ItemTag.HAT), ShopSource(price=333, currency=Geode.omni, shop_region=Region.desert,),),
        Hats.magic_turban: (Tag(ItemTag.HAT), ShopSource(price=333, currency=Geode.omni, shop_region=Region.desert,),),

        Hats.laurel_wreath_crown: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.hat.can_get_unlikely_hat_at_outfit_services),),
        Hats.joja_cap: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.hat.can_get_unlikely_hat_at_outfit_services),),
        Hats.dark_ballcap: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.hat.can_get_unlikely_hat_at_outfit_services),),
        Hats.dark_cowboy_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.skull_cavern_100,)),),
        Hats.blue_cowboy_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.skull_cavern_100,))),
        Hats.red_cowboy_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.skull_cavern_100,))),
        Hats.golden_mask: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Artifact.golden_mask,)),),
        Hats.white_turban: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.skull_cavern_100,))),
        Hats.knights_helmet: (Tag(ItemTag.HAT), MonsterSource(monsters=(Monster.pepper_rex,), amount_tier=MAX_MONTHS,
                                                                   other_requirements=(RegionRequirement(region=Region.adventurer_guild),)),),
    }
)
