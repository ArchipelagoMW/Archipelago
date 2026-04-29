from .ginger_island import ginger_island_content_pack as ginger_island_content_pack
from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack, StardewContent
from ...data import fish_data
from ...data.game_item import GenericSource, ItemTag, Tag
from ...data.harvest import HarvestCropSource
from ...data.hats_data import Hats
from ...data.requirement import DangerousMinesRequirement, CraftedItemsRequirement, ReceivedRequirement, ForgeInfinityWeaponRequirement
from ...data.shop import HatMouseSource, ShopSource
from ...logic.tailoring_logic import TailoringSource
from ...strings.animal_product_names import AnimalProduct
from ...strings.craftable_names import Furniture
from ...strings.crop_names import Fruit
from ...strings.currency_names import Currency
from ...strings.ingredient_names import Ingredient
from ...strings.machine_names import Machine
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region
from ...strings.seed_names import Seed, TreeSeed


class QiBoardContentPack(ContentPack):
    def harvest_source_hook(self, content: StardewContent):
        content.untag_item(Seed.qi_bean, ItemTag.CROPSANITY_SEED)


qi_board_content_pack = QiBoardContentPack(
    "Qi Board (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
        ginger_island_content_pack.name,
    ),
    harvest_sources={
        # This one is a bit special, because it's only available during the special order, but it can be found from like, everywhere.
        Seed.qi_bean: (GenericSource(regions=(Region.qi_walnut_room,)),),
        Fruit.qi_fruit: (HarvestCropSource(seed=Seed.qi_bean),),
    },
    shop_sources={
        Furniture.exotic_double_bed: (ShopSource(price=50, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        Ingredient.qi_seasoning: (ShopSource(price=10, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        Machine.enricher: (ShopSource(price=20, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        Machine.pressure_nozzle: (ShopSource(price=20, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        TreeSeed.mushroom: (ShopSource(price=5, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        "Galaxy Soul": (ShopSource(price=40, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        AnimalProduct.golden_egg_starter: (ShopSource(price=100, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room,
                                                      other_requirements=(ReceivedRequirement(AnimalProduct.golden_egg),)),),
    },
    fishes=(
        fish_data.ms_angler,
        fish_data.son_of_crimsonfish,
        fish_data.glacierfish_jr,
        fish_data.legend_ii,
        fish_data.radioactive_carp,
    ),
    hat_sources={
        Hats.infinity_crown: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(ForgeInfinityWeaponRequirement(),)),),
        Hats.space_helmet: (HatMouseSource(price=20000, unlock_requirements=(DangerousMinesRequirement(120),)),),
        Hats.qi_mask: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Fruit.qi_fruit,)),),
        Hats.radioactive_goggles: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(MetalBar.radioactive,)),),
        Hats.gnomes_cap: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(CraftedItemsRequirement(9999),)),),
        Hats.star_helmet: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(TreeSeed.mushroom,)),),
    },
)
