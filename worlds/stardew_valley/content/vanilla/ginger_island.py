from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack, StardewContent
from ...data import villagers_data, fish_data
from ...data.animal import Animal, AnimalName, OstrichIncubatorSource
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.fish_data import FishingSource
from ...data.game_item import ItemTag, Tag, CustomRuleSource
from ...data.harvest import ForagingSource, HarvestFruitTreeSource, HarvestCropSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.recipe_source import FriendshipSource, MasterySource, ArchipelagoSource, SpecialOrderSource, QuestSource, SkillSource
from ...data.requirement import WalnutRequirement, CookedRecipesRequirement, \
    CaughtFishRequirement, FullShipmentRequirement, RegionRequirement, \
    AllAchievementsRequirement, PerfectionPercentRequirement, ReadAllBooksRequirement, HasItemRequirement, ToolRequirement
from ...data.shop import ShopSource, HatMouseSource
from ...logic.tailoring_logic import TailoringSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.animal_product_names import AnimalProduct
from ...strings.artisan_good_names import ArtisanGood
from ...strings.book_names import Book
from ...strings.building_names import Building
from ...strings.craftable_names import WildSeeds, Craftable, Consumable, Fishing, Ring
from ...strings.crop_names import Fruit, Vegetable
from ...strings.currency_names import Currency
from ...strings.fertilizer_names import SpeedGro, RetainingSoil
from ...strings.fish_names import Fish
from ...strings.flower_names import Flower
from ...strings.food_names import Beverage, Meal
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.geode_names import Geode
from ...strings.ingredient_names import Ingredient
from ...strings.machine_names import Machine
from ...strings.material_names import Material
from ...strings.metal_names import Fossil, Mineral, MetalBar, Ore
from ...strings.monster_drop_names import Loot
from ...strings.monster_names import Monster
from ...strings.quest_names import Quest
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed
from ...strings.skill_names import Skill
from ...strings.special_order_names import SpecialOrder
from ...strings.tool_names import Tool
from ...strings.villager_names import NPC


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
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.volcano_floor_10,)),
        ),
        Forageable.ginger: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.island_west,),
                           other_requirements=(ToolRequirement(Tool.hoe),)),
        ),
        Mushroom.magma_cap: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.volcano_floor_5,)),
        ),

        # Fruit tree
        Fruit.banana: (HarvestFruitTreeSource(sapling=Sapling.banana, seasons=(Season.summer,)),),
        Fruit.mango: (HarvestFruitTreeSource(sapling=Sapling.mango, seasons=(Season.summer,)),),

        # Crop
        Vegetable.taro_root: (HarvestCropSource(seed=Seed.taro, seasons=(Season.summer,)),),
        Fruit.pineapple: (HarvestCropSource(seed=Seed.pineapple, seasons=(Season.summer,)),),

        # Temporary animal stuff, will be moved once animal products are properly content-packed
        AnimalProduct.ostrich_egg_starter: (CustomRuleSource(lambda logic: logic.tool.can_forage(Generic.any, Region.island_north, True) & logic.has(Forageable.journal_scrap) & logic.region.can_reach(Region.volcano_floor_5)),),
        AnimalProduct.ostrich_egg: (CustomRuleSource(lambda logic: logic.has(AnimalProduct.ostrich_egg_starter) | logic.animal.has_animal(AnimalName.ostrich)),),

    },
    shop_sources={
        Seed.taro: (ShopSource(price=0, currency=Currency.money, items_price=((2, Fossil.bone_fragment),), shop_region=Region.island_trader),),
        Seed.pineapple: (ShopSource(price=0, currency=Currency.money, items_price=((1, Mushroom.magma_cap),), shop_region=Region.island_trader),),
        Sapling.banana: (ShopSource(price=0, currency=Currency.money, items_price=((5, Forageable.dragon_tooth),), shop_region=Region.island_trader),),
        Sapling.mango: (ShopSource(price=0, currency=Currency.money, items_price=((75, Fish.mussel_node),), shop_region=Region.island_trader),),

        # This one is 10 diamonds, should maybe add time?
        Book.the_diamond_hunter: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(items_price=((10, Mineral.diamond),), shop_region=Region.volcano_dwarf_shop),
        ),
        Book.queen_of_sauce_cookbook: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=50000, shop_region=LogicRegion.bookseller_permanent, other_requirements=(WalnutRequirement(100),)),),  # Worst book ever

        Beverage.pina_colada: (ShopSource(price=600, currency=Currency.money, shop_region=Region.island_resort),),
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
        Hats.archers_cap: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(CookedRecipesRequirement(9999),)),),
        Hats.chef_hat: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(CookedRecipesRequirement(9999),)),),
        Hats.eye_patch: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(CaughtFishRequirement(9999, unique=True),)),),
        Hats.cowpoke_hat: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(FullShipmentRequirement(),)),),
        Hats.goblin_mask: (Tag(ItemTag.HAT), HatMouseSource(price=10000, unlock_requirements=(FullShipmentRequirement(),)),),
        Hats.elegant_turban: (Tag(ItemTag.HAT), HatMouseSource(price=50000, unlock_requirements=(AllAchievementsRequirement(),)),),
        Hats.junimo_hat: (Tag(ItemTag.HAT), HatMouseSource(price=25000, unlock_requirements=(PerfectionPercentRequirement(100),)),),
        Hats.paper_hat: (Tag(ItemTag.HAT), HatMouseSource(price=10000, unlock_requirements=(RegionRequirement(Region.island_south),)),),
        Hats.pageboy_cap: (Tag(ItemTag.HAT), HatMouseSource(price=5000, unlock_requirements=(ReadAllBooksRequirement(),)),),

        Hats.concerned_ape_mask: (Tag(ItemTag.HAT), ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                                               other_requirements=(
                                                               PerfectionPercentRequirement(100), RegionRequirement(Region.volcano_floor_10))),),
        Hats.golden_helmet: (Tag(ItemTag.HAT), ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                                          other_requirements=(
                                                          RegionRequirement(Region.blacksmith), HasItemRequirement(Geode.golden_coconut),)),),
        Hats.bluebird_mask: (
        Tag(ItemTag.HAT), ShopSource(price=0, currency=Currency.money, items_price=((30, Vegetable.taro_root),), shop_region=Region.island_trader),),
        Hats.deluxe_cowboy_hat: (
        Tag(ItemTag.HAT), ShopSource(price=0, currency=Currency.money, items_price=((30, Vegetable.taro_root),), shop_region=Region.island_trader),),
        Hats.small_cap: (
        Tag(ItemTag.HAT), ShopSource(price=0, currency=Currency.money, items_price=((30, Vegetable.taro_root),), shop_region=Region.island_trader),),
        Hats.mr_qis_hat: (Tag(ItemTag.HAT), ShopSource(price=5, currency=Currency.qi_gem, shop_region=Region.qi_walnut_room),),
        Hats.pink_bow: (Tag(ItemTag.HAT), ShopSource(price=10000, shop_region=Region.volcano_dwarf_shop),),

        Hats.tiger_hat: (Tag(ItemTag.HAT), MonsterSource(monsters=(Monster.tiger_slime,), amount_tier=MAX_MONTHS,
                                                         other_requirements=(RegionRequirement(region=Region.adventurer_guild),)),),
        Hats.deluxe_pirate_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.volcano, Region.volcano_floor_5, Region.volcano_floor_10,),
                                                                  require_all_regions=True),),

        Hats.foragers_hat: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Forageable.ginger,)),),
        Hats.sunglasses: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Material.cinder_shard,)),),
        Hats.swashbuckler_hat: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Forageable.dragon_tooth,)),),
        Hats.warrior_helmet: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(AnimalProduct.ostrich_egg,)),),

        Hats.frog_hat: (Tag(ItemTag.HAT), FishingSource(region=Region.gourmand_frog_cave, ),),
    },
    cooking_recipes=(
        CookingRecipe(name=Meal.banana_pudding, ingredients=((Fruit.banana, 1), (AnimalProduct.cow_milk, 1), (Ingredient.sugar, 1),), sources=(ShopSource(shop_region=Region.island_trader, items_price=((30, Fossil.bone_fragment),)),),),
        CookingRecipe(name=Beverage.ginger_ale, ingredients=((Forageable.ginger, 3), (Ingredient.sugar, 1),), sources=(ShopSource(shop_region=Region.volcano_dwarf_shop, price=1000),),),
        CookingRecipe(name=Meal.mango_sticky_rice, ingredients=((Fruit.mango, 1), (Forageable.coconut, 1), (Ingredient.rice, 1),), sources=(FriendshipSource(friend=NPC.leo, hearts=7),),),
        CookingRecipe(name=Meal.poi, ingredients=((Vegetable.taro_root, 4),), sources=(FriendshipSource(friend=NPC.leo, hearts=3),),),
        CookingRecipe(name=Meal.tropical_curry, ingredients=((Forageable.coconut, 1), (Fruit.pineapple, 1), (Fruit.hot_pepper, 1),), sources=(ShopSource(shop_region=Region.island_resort, price=2000),),),
    ),
    crafting_recipes=(
        CraftingRecipe(name=SpeedGro.hyper, ingredients=((Ore.radioactive, 1), (Fossil.bone_fragment, 3), (Loot.solar_essence, 1),), sources=(ArchipelagoSource(ap_items=(f"{SpeedGro.hyper} Recipe",)),),),
        CraftingRecipe(name=RetainingSoil.deluxe, ingredients=((Material.stone, 5), (Material.fiber, 3), (Material.clay, 1),), sources=(ShopSource(shop_region=Region.island_trader, items_price=((50, Currency.cinder_shard),)),),),
        CraftingRecipe(name=WildSeeds.blue_grass_starter, ingredients=((Material.fiber, 25), (Material.moss, 10), (ArtisanGood.mystic_syrup, 1),), sources=(ArchipelagoSource(ap_items=(f"{WildSeeds.blue_grass_starter} Recipe",)),),),
        CraftingRecipe(name=Fishing.magic_bait, ingredients=((Ore.radioactive, 1), (Loot.bug_meat, 3),), sources=(ArchipelagoSource(ap_items=(f"{Fishing.magic_bait} Recipe",)),),),
        CraftingRecipe(name=Ring.thorns_ring, ingredients=((Fossil.bone_fragment, 50), (Material.stone, 50), (MetalBar.gold, 1),), sources=(SkillSource(skill=Skill.combat, level=7),),),
        CraftingRecipe(name=Consumable.fairy_dust, ingredients=((Mineral.diamond, 1), (Flower.fairy_rose, 1),), sources=(QuestSource(quest=Quest.the_pirates_wife),),),
        CraftingRecipe(name=Consumable.warp_totem_island, ingredients=((Material.hardwood, 5), (Forageable.dragon_tooth, 1), (Forageable.ginger, 1),), sources=(ShopSource(shop_region=Region.volcano_dwarf_shop, price=10000),),),
        CraftingRecipe(name=Machine.heavy_tapper, ingredients=((Material.hardwood, 30), (MetalBar.radioactive, 1),), sources=(ArchipelagoSource(ap_items=(f"{Machine.heavy_tapper} Recipe",)),),),
        CraftingRecipe(name=Machine.ostrich_incubator, ingredients=((Fossil.bone_fragment, 50), (Material.hardwood, 50), (Currency.cinder_shard, 20),), sources=(ArchipelagoSource(ap_items=(f"{Machine.ostrich_incubator} Recipe",)),),),
        CraftingRecipe(name=Machine.solar_panel, ingredients=((MetalBar.quartz, 10), (MetalBar.iron, 5), (MetalBar.gold, 5),), sources=(SpecialOrderSource(special_order=SpecialOrder.island_ingredients),),), # #, content_pack=ginger_island_content_pack.name) # If set this as a ginger island only recipe, the rule for battery packs will fail. It does OR on lightning rod and solar panel, even when GI is off
        CraftingRecipe(name=Craftable.hopper, ingredients=((Material.hardwood, 10), (MetalBar.iridium, 1), (MetalBar.radioactive, 1),), sources=(ArchipelagoSource(ap_items=(f"{Craftable.hopper} Recipe",)),),),
        CraftingRecipe(name=Machine.mini_forge, ingredients=((Forageable.dragon_tooth, 5), (MetalBar.iron, 10), (MetalBar.gold, 10), (MetalBar.iridium, 5),), sources=(MasterySource(skill=Skill.combat),),),
    ),
)
