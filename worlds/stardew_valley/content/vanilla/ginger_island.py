from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack, StardewContent
from ...data import villagers_data, fish_data
from ...data.animal import Animal, AnimalName, OstrichIncubatorSource
from ...data.game_item import ItemTag, Tag, CustomRuleSource
from ...data.harvest import ForagingSource, HarvestFruitTreeSource, HarvestCropSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.requirement import WalnutRequirement, ForgeInfinityWeaponRequirement, CookedRecipesRequirement, \
    CraftedItemsRequirement, CaughtFishRequirement, FullShipmentRequirement, RegionRequirement, \
    AllAchievementsRequirement, PerfectionPercentRequirement, ReadAllBooksRequirement, HasItemRequirement
from ...data.shop import ShopSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.animal_product_names import AnimalProduct
from ...strings.book_names import Book
from ...strings.building_names import Building
from ...strings.crop_names import Fruit, Vegetable
from ...strings.fish_names import Fish
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.geode_names import Geode
from ...strings.metal_names import Fossil, Mineral
from ...strings.monster_names import Monster
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed


class GingerIslandContentPack(ContentPack):

    def harvest_source_hook(self, content: StardewContent):
        content.tag_item(Fruit.banana, ItemTag.FRUIT)
        content.tag_item(Fruit.pineapple, ItemTag.FRUIT)
        content.tag_item(Fruit.mango, ItemTag.FRUIT)
        content.tag_item(Vegetable.taro_root, ItemTag.VEGETABLE)
        content.tag_item(Mushroom.magma_cap, ItemTag.EDIBLE_MUSHROOM)


ginger_island_content_pack = GingerIslandContentPack(
    "Ginger Island (Vanilla)",
    weak_dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        # Foraging
        Forageable.dragon_tooth: (
            ForagingSource(regions=(Region.volcano_floor_10,)),
        ),
        Forageable.ginger: (
            ForagingSource(regions=(Region.island_west,)),
        ),
        Mushroom.magma_cap: (
            ForagingSource(regions=(Region.volcano_floor_5,)),
        ),

        # Fruit tree
        Fruit.banana: (HarvestFruitTreeSource(sapling=Sapling.banana, seasons=(Season.summer,)),),
        Fruit.mango: (HarvestFruitTreeSource(sapling=Sapling.mango, seasons=(Season.summer,)),),

        # Crop
        Vegetable.taro_root: (HarvestCropSource(seed=Seed.taro, seasons=(Season.summer,)),),
        Fruit.pineapple: (HarvestCropSource(seed=Seed.pineapple, seasons=(Season.summer,)),),

        # Temporary animal stuff, will be moved once animal products are properly content-packed
        AnimalProduct.ostrich_egg_starter: (CustomRuleSource(lambda logic: logic.tool.can_forage(Generic.any, Region.island_north, True)
                                                                           & logic.has(Forageable.journal_scrap)
                                                                           & logic.region.can_reach(Region.volcano_floor_5)),),
        AnimalProduct.ostrich_egg: (CustomRuleSource(lambda logic: logic.has(AnimalProduct.ostrich_egg_starter)
                                                                   | logic.animal.has_animal(AnimalName.ostrich)),),

    },
    shop_sources={
        Seed.taro: (ShopSource(items_price=((2, Fossil.bone_fragment),), shop_region=Region.island_trader),),
        Seed.pineapple: (ShopSource(items_price=((1, Mushroom.magma_cap),), shop_region=Region.island_trader),),
        Sapling.banana: (ShopSource(items_price=((5, Forageable.dragon_tooth),), shop_region=Region.island_trader),),
        Sapling.mango: (ShopSource(items_price=((75, Fish.mussel_node),), shop_region=Region.island_trader),),

        # This one is 10 diamonds, should maybe add time?
        Book.the_diamond_hunter: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(items_price=((10, Mineral.diamond),), shop_region=Region.volcano_dwarf_shop),
        ),
        Book.queen_of_sauce_cookbook: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=50000, shop_region=LogicRegion.bookseller_2, other_requirements=(WalnutRequirement(100),)),),  # Worst book ever
    },
    fishes=(
        # TODO override region so no need to add inaccessible regions in logic
        fish_data.blue_discus,
        fish_data.lionfish,
        fish_data.midnight_carp,
        fish_data.pufferfish,
        fish_data.stingray,
        fish_data.super_cucumber,
        fish_data.tilapia,
        fish_data.tuna
    ),
    villagers=(
        villagers_data.leo,
    ),
    animals=(
        Animal(AnimalName.ostrich,
               required_building=Building.barn,
               sources=(
                   OstrichIncubatorSource(AnimalProduct.ostrich_egg_starter),
               )),
    ),
    hat_sources={
        Hats.infinity_crown.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                              other_requirements=(ForgeInfinityWeaponRequirement(),)),),
        Hats.archers_cap.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                           other_requirements=(CookedRecipesRequirement(9999),)),),
        Hats.chef_hat.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                        other_requirements=(CookedRecipesRequirement(9999),)),),
        Hats.gnomes_cap.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                          other_requirements=(CraftedItemsRequirement(9999),)),),
        Hats.eye_patch.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                         other_requirements=(CaughtFishRequirement(9999, unique=True),)),),
        Hats.cowpoke_hat.name: (ShopSource(price=1000, shop_region=LogicRegion.hat_mouse,
                                           other_requirements=(FullShipmentRequirement(),)),),
        Hats.goblin_mask.name: (ShopSource(price=10000, shop_region=LogicRegion.hat_mouse,
                                           other_requirements=(FullShipmentRequirement(),)),),
        Hats.elegant_turban.name: (ShopSource(price=50000, shop_region=LogicRegion.hat_mouse,
                                              other_requirements=(AllAchievementsRequirement(),)),),
        Hats.junimo_hat.name: (ShopSource(price=25000, shop_region=LogicRegion.hat_mouse,
                                          other_requirements=(PerfectionPercentRequirement(100),)),),
        Hats.paper_hat.name: (ShopSource(price=10000, shop_region=LogicRegion.hat_mouse,
                                         other_requirements=(RegionRequirement(Region.island_south),)),),
        Hats.pageboy_cap.name: (ShopSource(price=5000, shop_region=LogicRegion.hat_mouse,
                                           other_requirements=(ReadAllBooksRequirement(),)),),

        Hats.concerned_ape_mask.name: (ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                                  other_requirements=(PerfectionPercentRequirement(100), RegionRequirement(Region.volcano_floor_10))),),
        Hats.golden_helmet.name: (ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                             other_requirements=(RegionRequirement(Region.blacksmith), HasItemRequirement(Geode.golden_coconut),)),),

        Hats.tiger_hat: (MonsterSource(monsters=(Monster.tiger_slime,), amount_tier=MAX_MONTHS),),
        Hats.deluxe_pirate_hat: (ForagingSource(regions=(Region.volcano, Region.volcano_floor_5, Region.volcano_floor_10,), require_all_regions=True),),
    },
)
