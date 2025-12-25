from ..game_content import ContentPack
from ...data import villagers_data, fish_data
from ...data.building import Building
from ...data.game_item import GenericSource, ItemTag, Tag, CustomRuleSource, AllRegionsSource
from ...data.harvest import ForagingSource, SeasonalForagingSource, ArtifactSpotSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.requirement import ToolRequirement, BookRequirement, SkillRequirement, YearRequirement, \
    GrangeDisplayRequirement, EggHuntRequirement, MuseumCompletionRequirement, BuildingRequirement, \
    NumberOfFriendsRequirement, HelpWantedRequirement, FishingCompetitionRequirement, MovieRequirement, LuauDelightRequirementRequirement, \
    ReceivedRaccoonsRequirement, \
    PrizeMachineRequirement, SpecificFriendRequirement, RegionRequirement, CatalogueRequirement
from ...data.shop import ShopSource, MysteryBoxSource, ArtifactTroveSource, PrizeMachineSource, \
    FishingTreasureChestSource, HatMouseSource
from ...logic.tailoring_logic import TailoringSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.artisan_good_names import ArtisanGood
from ...strings.book_names import Book
from ...strings.building_names import Building as BuildingNames
from ...strings.catalogue_names import Catalogue
from ...strings.craftable_names import Furniture
from ...strings.crop_names import Fruit
from ...strings.currency_names import Currency
from ...strings.fish_names import WaterItem, Fish
from ...strings.food_names import Beverage, Meal
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar
from ...strings.monster_names import Monster
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed, TreeSeed
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import NPC

pelican_town = ContentPack(
    "Pelican Town (Vanilla)",
    harvest_sources={
        # Spring
        Forageable.daffodil: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.bus_stop, Region.town, Region.railroad)),
        ),
        Forageable.dandelion: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.bus_stop, Region.forest, Region.railroad)),
        ),
        Forageable.leek: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.railroad)),
        ),
        Forageable.wild_horseradish: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.backwoods, Region.mountain, Region.forest, Region.secret_woods)),
        ),
        Forageable.salmonberry: (
            Tag(ItemTag.FORAGE),
            SeasonalForagingSource(season=Season.spring, days=(15, 16, 17, 18),
                                   regions=(Region.backwoods, Region.mountain, Region.town, Region.forest, Region.tunnel_entrance, Region.railroad)),
        ),
        Forageable.spring_onion: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.forest,)),
        ),

        # Summer
        Fruit.grape: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer,), regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.railroad)),
        ),
        Forageable.spice_berry: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer,), regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.forest, Region.railroad)),
        ),
        Forageable.sweet_pea: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer,), regions=(Region.bus_stop, Region.town, Region.forest, Region.railroad)),
        ),
        Forageable.fiddlehead_fern: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer,), regions=(Region.secret_woods,)),
        ),

        # Fall
        Forageable.blackberry: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.fall,), regions=(Region.backwoods, Region.town, Region.forest, Region.railroad)),
            SeasonalForagingSource(season=Season.fall, days=(8, 9, 10, 11),
                                   regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.tunnel_entrance,
                                            Region.railroad)),
        ),
        Forageable.hazelnut: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.fall,), regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.railroad)),
        ),
        Forageable.wild_plum: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.fall,), regions=(Region.mountain, Region.bus_stop, Region.railroad)),
        ),

        # Winter
        Forageable.crocus: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,),
                           regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.secret_woods)),
        ),
        Forageable.crystal_fruit: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,),
                           regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.railroad)),
        ),
        Forageable.holly: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,),
                           regions=(Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.railroad)),
        ),
        Forageable.snow_yam: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,),
                           regions=(Region.farm, Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.railroad,
                                    Region.secret_woods, Region.beach),
                           other_requirements=(ToolRequirement(Tool.hoe),)),
        ),
        Forageable.winter_root: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,),
                           regions=(Region.farm, Region.backwoods, Region.mountain, Region.bus_stop, Region.town, Region.forest, Region.railroad,
                                    Region.secret_woods, Region.beach),
                           other_requirements=(ToolRequirement(Tool.hoe),)),
        ),

        # Mushrooms
        Mushroom.common: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring,), regions=(Region.secret_woods,)),
            ForagingSource(seasons=(Season.fall,), regions=(Region.backwoods, Region.mountain, Region.forest)),
        ),
        Mushroom.chanterelle: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.fall,), regions=(Region.secret_woods,)),
        ),
        Mushroom.morel: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.spring, Season.fall), regions=(Region.secret_woods,)),
        ),
        Mushroom.red: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer, Season.fall), regions=(Region.secret_woods,)),
        ),

        # Beach
        WaterItem.coral: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.tide_pools,)),
            SeasonalForagingSource(season=Season.summer, days=(12, 13, 14), regions=(Region.beach,)),
        ),
        WaterItem.nautilus_shell: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.winter,), regions=(Region.beach,)),
        ),
        Forageable.rainbow_shell: (
            Tag(ItemTag.FORAGE),
            ForagingSource(seasons=(Season.summer,), regions=(Region.beach,)),
        ),
        WaterItem.sea_urchin: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.tide_pools,)),
        ),

        Seed.mixed: (
            ForagingSource(seasons=(Season.spring, Season.summer, Season.fall,), regions=(Region.town, Region.farm, Region.forest)),
        ),

        Seed.mixed_flower: (
            ForagingSource(seasons=(Season.summer,), regions=(Region.town, Region.farm, Region.forest)),
        ),

        # Books
        Book.jack_be_nimble_jack_be_thick: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ArtifactSpotSource(amount=22),),  # After 22 spots, there are 50.48% chances player received the book.
        Book.woodys_secret: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            GenericSource(regions=(Region.forest, Region.mountain),
                          other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.iron), SkillRequirement(Skill.foraging, 5))),),
    },
    shop_sources={
        # Saplings
        Sapling.apple: (ShopSource(price=4000, shop_region=Region.pierre_store),),
        Sapling.apricot: (ShopSource(price=2000, shop_region=Region.pierre_store),),
        Sapling.cherry: (ShopSource(price=3400, shop_region=Region.pierre_store),),
        Sapling.orange: (ShopSource(price=4000, shop_region=Region.pierre_store),),
        Sapling.peach: (ShopSource(price=6000, shop_region=Region.pierre_store),),
        Sapling.pomegranate: (ShopSource(price=6000, shop_region=Region.pierre_store),),

        # Crop seeds, assuming they are bought in season, otherwise price is different with missing stock list.
        Seed.parsnip: (ShopSource(price=20, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.bean: (ShopSource(price=60, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.cauliflower: (ShopSource(price=80, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.potato: (ShopSource(price=50, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.tulip: (ShopSource(price=20, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.kale: (ShopSource(price=70, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.jazz: (ShopSource(price=30, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.garlic: (ShopSource(price=40, shop_region=Region.pierre_store, seasons=(Season.spring,)),),
        Seed.rice: (ShopSource(price=40, shop_region=Region.pierre_store, seasons=(Season.spring,)),),

        Seed.melon: (ShopSource(price=80, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.tomato: (ShopSource(price=50, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.blueberry: (ShopSource(price=80, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.pepper: (ShopSource(price=40, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.wheat: (ShopSource(price=10, shop_region=Region.pierre_store, seasons=(Season.summer, Season.fall)),),
        Seed.radish: (ShopSource(price=40, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.poppy: (ShopSource(price=100, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.spangle: (ShopSource(price=50, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.hops: (ShopSource(price=60, shop_region=Region.pierre_store, seasons=(Season.summer,)),),
        Seed.corn: (ShopSource(price=150, shop_region=Region.pierre_store, seasons=(Season.summer, Season.fall)),),
        Seed.sunflower: (ShopSource(price=200, shop_region=Region.pierre_store, seasons=(Season.summer, Season.fall)),),
        Seed.red_cabbage: (ShopSource(price=100, shop_region=Region.pierre_store, seasons=(Season.summer,)),),

        Seed.eggplant: (ShopSource(price=20, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.pumpkin: (ShopSource(price=100, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.bok_choy: (ShopSource(price=50, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.yam: (ShopSource(price=60, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.cranberry: (ShopSource(price=240, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.fairy: (ShopSource(price=200, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.amaranth: (ShopSource(price=70, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.grape: (ShopSource(price=60, shop_region=Region.pierre_store, seasons=(Season.fall,)),),
        Seed.artichoke: (ShopSource(price=30, shop_region=Region.pierre_store, seasons=(Season.fall,)),),

        Seed.broccoli: (ShopSource(items_price=((5, Material.moss),), shop_region=LogicRegion.raccoon_shop_1),),
        Seed.carrot: (ShopSource(items_price=((1, TreeSeed.maple),), shop_region=LogicRegion.raccoon_shop_1),),
        Seed.powdermelon: (ShopSource(items_price=((2, TreeSeed.acorn),), shop_region=LogicRegion.raccoon_shop_1),),
        Seed.summer_squash: (ShopSource(items_price=((15, Material.sap),), shop_region=LogicRegion.raccoon_shop_1),),

        Seed.strawberry: (ShopSource(price=100, shop_region=LogicRegion.egg_festival, seasons=(Season.spring,)),),
        Seed.rare_seed: (ShopSource(price=1000, shop_region=LogicRegion.traveling_cart, seasons=(Season.spring, Season.summer)),),

        # Saloon
        Beverage.beer: (ShopSource(price=400, shop_region=Region.saloon),),
        Meal.salad: (ShopSource(price=220, shop_region=Region.saloon),),
        Meal.bread: (ShopSource(price=100, shop_region=Region.saloon),),
        Meal.spaghetti: (ShopSource(price=240, shop_region=Region.saloon),),
        Meal.pizza: (ShopSource(price=600, shop_region=Region.saloon),),
        Beverage.coffee: (ShopSource(price=300, shop_region=Region.saloon),),

        # Books
        Book.animal_catalogue: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=5000, shop_region=Region.ranch, other_requirements=(YearRequirement(2),)),),
        Book.book_of_mysteries: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            MysteryBoxSource(amount=50),),  # After 38 boxes, there are 49.99% chances player received the book.
        Book.dwarvish_safety_manual: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=4000, shop_region=LogicRegion.mines_dwarf_shop),),
        #   ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),  # Repeatable, so no need for bookseller
        Book.friendship_101: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            PrizeMachineSource(amount=9),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.horse_the_book: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=25000, shop_region=LogicRegion.bookseller_permanent),),
        Book.jack_be_nimble_jack_be_thick: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.jewels_of_the_sea: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            FishingTreasureChestSource(amount=25),  # After 21 chests, there are 49.44% chances player received the book.
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.mapping_cave_systems: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            AllRegionsSource(regions=(Region.adventurer_guild_bedroom, LogicRegion.bookseller_rare,)),
            # Disabling the shop source for better game design.
            # ShopSource(price=20000, shop_region=LogicRegion.bookseller_3),
        ),
        Book.monster_compendium: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            CustomRuleSource(create_rule=lambda logic: logic.monster.can_kill_many(Generic.any)),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.ol_slitherlegs: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=25000, shop_region=LogicRegion.bookseller_permanent),),
        Book.price_catalogue: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=3000, shop_region=LogicRegion.bookseller_permanent),),
        Book.the_alleyway_buffet: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            GenericSource(regions=(Region.town,),
                          other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.iron), ToolRequirement(Tool.pickaxe, ToolMaterial.iron))),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.the_art_o_crabbing: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            CustomRuleSource(create_rule=lambda logic: logic.festival.has_squidfest_day_1_iridium_reward()),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.treasure_appraisal_guide: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ArtifactTroveSource(amount=20),  # After 18 troves, there is 49,88% chances player received the book.
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),
        Book.raccoon_journal: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            #  ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),  # Repeatable, so no need for bookseller
            ShopSource(items_price=((999, Material.fiber),), shop_region=LogicRegion.raccoon_shop_2),),
        Book.way_of_the_wind_pt_1: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=15000, shop_region=LogicRegion.bookseller_permanent),),
        Book.way_of_the_wind_pt_2: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=35000, shop_region=LogicRegion.bookseller_permanent, other_requirements=(BookRequirement(Book.way_of_the_wind_pt_1),)),),
        Book.woodys_secret: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(price=20000, shop_region=LogicRegion.bookseller_rare),),

        # Experience Books
        Book.book_of_stars: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_permanent),),
        Book.bait_and_bobber: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_experience),),
        Book.combat_quarterly: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_experience),),
        Book.mining_monthly: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_experience),),
        Book.stardew_valley_almanac: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_experience),),
        Book.woodcutters_weekly: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(price=5000, shop_region=LogicRegion.bookseller_experience),),

        # Catalogues
        Catalogue.wizard: (ShopSource(price=150000, shop_region=Region.sewer, other_requirements=(CatalogueRequirement(Catalogue.wizard),)),),
        Catalogue.furniture: (ShopSource(price=200000, shop_region=Region.carpenter, other_requirements=(CatalogueRequirement(Catalogue.furniture),BuildingRequirement(BuildingNames.kitchen),)),),

        # Furniture
        Furniture.single_bed: (ShopSource(price=500, shop_region=Region.carpenter),),
        Furniture.crane_game_house_plant: (ShopSource(price=500, shop_region=Region.movie_theater),),
        Furniture.cursed_mannequin: (MonsterSource(monsters=(Monster.haunted_skull,), amount_tier=MAX_MONTHS),),
    },
    fishes=(
        fish_data.albacore,
        fish_data.anchovy,
        fish_data.bream,
        fish_data.bullhead,
        fish_data.carp,
        fish_data.catfish,
        fish_data.chub,
        fish_data.dorado,
        fish_data.eel,
        fish_data.flounder,
        fish_data.goby,
        fish_data.halibut,
        fish_data.herring,
        fish_data.largemouth_bass,
        fish_data.lingcod,
        fish_data.midnight_carp,  # Ginger island override
        fish_data.octopus,
        fish_data.perch,
        fish_data.pike,
        fish_data.pufferfish,  # Ginger island override
        fish_data.rainbow_trout,
        fish_data.red_mullet,
        fish_data.red_snapper,
        fish_data.salmon,
        fish_data.sardine,
        fish_data.sea_cucumber,
        fish_data.shad,
        fish_data.slimejack,
        fish_data.smallmouth_bass,
        fish_data.squid,
        fish_data.sturgeon,
        fish_data.sunfish,
        fish_data.super_cucumber,  # Ginger island override
        fish_data.tiger_trout,
        fish_data.tilapia,  # Ginger island override
        fish_data.tuna,  # Ginger island override
        fish_data.void_salmon,
        fish_data.walleye,
        fish_data.woodskip,
        fish_data.blobfish,
        fish_data.midnight_squid,
        fish_data.spook_fish,

        # Legendaries
        fish_data.angler,
        fish_data.crimsonfish,
        fish_data.glacierfish,
        fish_data.legend,
        fish_data.mutant_carp,

        # Crab pot
        fish_data.clam,
        fish_data.cockle,
        fish_data.crab,
        fish_data.crayfish,
        fish_data.lobster,
        fish_data.mussel,
        fish_data.oyster,
        fish_data.periwinkle,
        fish_data.shrimp,
        fish_data.snail,
    ),
    villagers=(
        villagers_data.josh,
        villagers_data.elliott,
        villagers_data.harvey,
        villagers_data.sam,
        villagers_data.sebastian,
        villagers_data.shane,
        villagers_data.abigail,
        villagers_data.emily,
        villagers_data.haley,
        villagers_data.leah,
        villagers_data.maru,
        villagers_data.penny,
        villagers_data.caroline,
        villagers_data.clint,
        villagers_data.demetrius,
        villagers_data.evelyn,
        villagers_data.george,
        villagers_data.gus,
        villagers_data.jas,
        villagers_data.jodi,
        villagers_data.kent,
        villagers_data.krobus,
        villagers_data.lewis,
        villagers_data.linus,
        villagers_data.marnie,
        villagers_data.pam,
        villagers_data.pierre,
        villagers_data.robin,
        villagers_data.vincent,
        villagers_data.willy,
        villagers_data.wizard,
    ),
    farm_buildings=(
        Building(
            BuildingNames.barn,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=6000,
                    items_price=((350, Material.wood), (150, Material.stone))
                ),
            ),
        ),
        Building(
            BuildingNames.big_barn,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=12_000,
                    items_price=((450, Material.wood), (200, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.barn,
        ),
        Building(
            BuildingNames.deluxe_barn,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=25_000,
                    items_price=((550, Material.wood), (300, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.big_barn,
        ),
        Building(
            BuildingNames.coop,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=4000,
                    items_price=((300, Material.wood), (100, Material.stone))
                ),
            ),
        ),
        Building(
            BuildingNames.big_coop,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=10_000,
                    items_price=((400, Material.wood), (150, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.coop,
        ),
        Building(
            BuildingNames.deluxe_coop,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=20_000,
                    items_price=((500, Material.wood), (200, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.big_coop,
        ),
        Building(
            BuildingNames.fish_pond,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=5000,
                    items_price=((200, Material.stone), (5, WaterItem.seaweed), (5, WaterItem.green_algae))
                ),
            ),
        ),
        Building(
            BuildingNames.mill,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=2500,
                    items_price=((50, Material.stone), (150, Material.wood), (4, ArtisanGood.cloth))
                ),
            ),
        ),
        Building(
            BuildingNames.shed,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=15_000,
                    items_price=((300, Material.wood),)
                ),
            ),
        ),
        Building(
            BuildingNames.big_shed,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=20_000,
                    items_price=((550, Material.wood), (300, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.shed,
        ),
        Building(
            BuildingNames.silo,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=100,
                    items_price=((100, Material.stone), (10, Material.clay), (5, MetalBar.copper))
                ),
            ),
        ),
        Building(
            BuildingNames.slime_hutch,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=10_000,
                    items_price=((500, Material.stone), (10, MetalBar.quartz), (1, MetalBar.iridium))
                ),
            ),
        ),
        Building(
            BuildingNames.stable,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=10_000,
                    items_price=((100, Material.hardwood), (5, MetalBar.iron))
                ),
            ),
        ),
        Building(
            BuildingNames.well,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=1000,
                    items_price=((75, Material.stone),)
                ),
            ),
        ),
        Building(
            BuildingNames.shipping_bin,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=250,
                    items_price=((150, Material.wood),)
                ),
            ),
        ),
        Building(
            BuildingNames.pet_bowl,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=5000,
                    items_price=((25, Material.hardwood),)
                ),
            ),
        ),
        Building(
            BuildingNames.kitchen,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=10_000,
                    items_price=((450, Material.wood),)
                ),
            ),
            upgrade_from=BuildingNames.farm_house,
        ),
        Building(
            BuildingNames.kids_room,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=65_000,
                    items_price=((100, Material.hardwood),)
                ),
            ),
            upgrade_from=BuildingNames.kitchen,
        ),
        Building(
            BuildingNames.cellar,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=100_000,
                ),
            ),
            upgrade_from=BuildingNames.kids_room,
        ),
        # Building(
        #     WizardBuilding.earth_obelisk,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=500_000,
        #             items_price=((10, MetalBar.iridium), (10, Mineral.earth_crystal),)
        #         ),
        #     ),
        # ),
        # Building(
        #     WizardBuilding.water_obelisk,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=500_000,
        #             items_price=((5, MetalBar.iridium), (10, Fish.clam), (10, WaterItem.coral),)
        #         ),
        #     ),
        # ),
        # Building(
        #     WizardBuilding.desert_obelisk,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=1_000_000,
        #             items_price=((20, MetalBar.iridium), (10, Forageable.coconut), (10, Forageable.cactus_fruit),)
        #         ),
        #     ),
        # ),
        # Building(
        #     WizardBuilding.island_obelisk,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=1_000_000,
        #             items_price=((10, MetalBar.iridium), (10, Forageable.dragon_tooth), (10, Fruit.banana),)
        #         ),
        #     ),
        # ),
        # Building(
        #     WizardBuilding.junimo_hut,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=20_000,
        #             items_price=((200, Material.stone), (9, Fruit.starfruit), (100, Material.fiber),)
        #         ),
        #     ),
        # ),
        # Building(
        #     WizardBuilding.gold_clock,
        #     sources=(
        #         ShopSource(
        #             shop_region=Region.wizard_tower,
        #             price=10_000_000,
        #         ),
        #     ),
        # ),
    ),
    hat_sources={
        # Hats from the Hat Mouse
        Hats.blue_ribbon: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(GrangeDisplayRequirement(),)),),
        Hats.blue_bonnet: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(MuseumCompletionRequirement(40),)),),
        Hats.cowboy: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(MuseumCompletionRequirement(),)),),
        Hats.butterfly_bow: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(1, 5),)),),
        Hats.mouse_ears: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(1, 10),)),),
        Hats.cat_ears: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(8, 10),)),),
        Hats.tiara: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(4, 5),)),),
        Hats.santa_hat: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(10, 5),)),),
        Hats.earmuffs: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(NumberOfFriendsRequirement(20, 5),)),),
        Hats.tropiclip: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(BuildingRequirement(BuildingNames.kitchen),)),),
        Hats.hunters_cap: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(BuildingRequirement(BuildingNames.cellar),)),),
        Hats.polka_bow: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(HelpWantedRequirement(10),)),),
        Hats.chicken_mask: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(HelpWantedRequirement(40),)),),
        Hats.straw: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(EggHuntRequirement(),)),),
        Hats.sailors_cap: (Tag(ItemTag.HAT), HatMouseSource(price=1000, unlock_requirements=(FishingCompetitionRequirement(),)),),
        Hats.jester_hat: (Tag(ItemTag.HAT), HatMouseSource(price=25000, unlock_requirements=(MovieRequirement(),)),),
        Hats.governors_hat: (Tag(ItemTag.HAT), HatMouseSource(price=5000, unlock_requirements=(LuauDelightRequirementRequirement(),)),),
        Hats.white_bow: (Tag(ItemTag.HAT), HatMouseSource(price=5000, unlock_requirements=(ReceivedRaccoonsRequirement(8),)),),
        Hats.sports_cap: (Tag(ItemTag.HAT), HatMouseSource(price=5000, unlock_requirements=(PrizeMachineRequirement(11),)),),

        Hats.emilys_magic_hat: (Tag(ItemTag.HAT), ShopSource(price=10000, shop_region=LogicRegion.lost_items_shop,
                                                             other_requirements=(
                                                                 SpecificFriendRequirement(NPC.emily, 14), RegionRequirement(Region.farm))),),
        Hats.fedora: (Tag(ItemTag.HAT), ShopSource(price=500, currency=Currency.star_token, shop_region=LogicRegion.fair),),
        Hats.cone_hat: (Tag(ItemTag.HAT), ShopSource(price=5000, shop_region=LogicRegion.night_market),),
        Hats.red_fez: (Tag(ItemTag.HAT), ShopSource(price=8000, shop_region=LogicRegion.traveling_cart),),

        Hats.garbage_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.town,), grind_months=12),),
        Hats.mystery_hat: (Tag(ItemTag.HAT), MysteryBoxSource(amount=100),),

        Hats.fishing_hat: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Fish.stonefish, Fish.ice_pip, Fish.scorpion_carp, Fish.spook_fish,
                                                                              Fish.midnight_squid, Fish.void_salmon, Fish.slimejack,)),),
        Hats.bucket_hat: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.hat.has_bucket_hat),),

        Hats.leprechaun_hat: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.forest,), seasons=(Season.spring,), ),),
        Hats.mushroom_cap: (Tag(ItemTag.HAT), ForagingSource(regions=(Region.farm,), seasons=(Season.fall,),
                                                             other_requirements=(ToolRequirement(Tool.axe),),),),

        Hats.raccoon_hat: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.quest.has_raccoon_shop(3) &
                                                                                        logic.region.can_reach(LogicRegion.raccoon_shop_3)),),

        Hats.squid_hat: (Tag(ItemTag.HAT), CustomRuleSource(create_rule=lambda logic: logic.festival.can_squidfest_iridium_reward()),),

    }
)
