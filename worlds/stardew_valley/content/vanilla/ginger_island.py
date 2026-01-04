from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack, StardewContent
from ...data import villagers_data, fish_data
from ...data.animal import Animal, AnimalName, OstrichIncubatorSource
from ...data.game_item import ItemTag, Tag, CustomRuleSource
from ...data.harvest import ForagingSource, HarvestFruitTreeSource, HarvestCropSource
from ...data.requirement import WalnutRequirement
from ...data.shop import ShopSource
from ...strings.animal_product_names import AnimalProduct
from ...strings.book_names import Book
from ...strings.building_names import Building
from ...strings.crop_names import Fruit, Vegetable
from ...strings.fish_names import Fish
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.metal_names import Fossil, Mineral
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
            ShopSource(money_price=50000, shop_region=LogicRegion.bookseller_2, other_requirements=(WalnutRequirement(100),)),),  # Worst book ever

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
    )
)
