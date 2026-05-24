from ..game_content import ContentPack
from ...data import villagers_data, fish_data
from ...data.building import Building
from ...data.cooking_recipe import CookingRecipe
from ...data.craftable_data import CraftingRecipe
from ...data.festival_data import all_festival_data
from ...data.game_item import GenericSource, ItemTag, Tag, CustomRuleSource, AllRegionsSource
from ...data.harvest import ForagingSource, SeasonalForagingSource, ArtifactSpotSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.recipe_source import FriendshipSource, QueenOfSauceSource, SkillSource, StarterSource, SpecialOrderSource, ArchipelagoSource, CutsceneSource, \
    MasterySource
from ...data.requirement import ToolRequirement, BookRequirement, SkillRequirement, YearRequirement, \
    GrangeDisplayRequirement, EggHuntRequirement, MuseumCompletionRequirement, BuildingRequirement, \
    NumberOfFriendsRequirement, HelpWantedRequirement, FishingCompetitionRequirement, MovieRequirement, LuauDelightRequirementRequirement, \
    ReceivedRaccoonsRequirement, \
    PrizeMachineRequirement, SpecificFriendRequirement, RegionRequirement, EndgameItemReceivedRequirement, MasteryRequirement, ReceivedRequirement, \
    BachelorFriendRequirement, SeasonRequirement, SpeakJunimoRequirement, FestivalItemReceivedRequirement, MuseumArtifactsRequirement, \
    CraftedSpecificItemRequirement
from ...data.shop import ShopSource, MysteryBoxSource, ArtifactTroveSource, PrizeMachineSource, \
    FishingTreasureChestSource, HatMouseSource
from ...data.tool import ToolUpgrade, StartingToolSource
from ...logic.tailoring_logic import TailoringSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.animal_product_names import AnimalProduct
from ...strings.ap_names.shop_location_names import ShopLocation
from ...strings.artisan_good_names import ArtisanGood
from ...strings.book_names import Book
from ...strings.building_names import Building as BuildingNames
from ...strings.catalogue_names import Catalogue
from ...strings.craftable_names import Furniture, Consumable, Fishing, WildSeeds, Bomb, Fence, Sprinkler, Floor, Edible, Ring, Lighting, Storage, Sign, \
    Craftable, Statue
from ...strings.crop_names import Fruit, Vegetable
from ...strings.currency_names import Currency
from ...strings.fertilizer_names import Fertilizer, RetainingSoil, SpeedGro
from ...strings.festival_check_names import FestivalCheck
from ...strings.fish_names import WaterItem, Fish, Trash
from ...strings.flower_names import Flower
from ...strings.food_names import Beverage, Meal
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.geode_names import Geode
from ...strings.gift_names import Gift
from ...strings.ingredient_names import Ingredient
from ...strings.machine_names import Machine
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar, Ore, Fossil, Mineral, Artifact
from ...strings.monster_drop_names import Loot
from ...strings.monster_names import Monster
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed, TreeSeed
from ...strings.skill_names import Skill
from ...strings.special_order_names import SpecialOrder
from ...strings.tool_names import Tool, ToolMaterial, FishingRod
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
            ForagingSource(seasons=(Season.spring,), regions=(Region.secret_woods,)),
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
        Seed.powdermelon: (ShopSource(items_price=((2, TreeSeed.pine),), shop_region=LogicRegion.raccoon_shop_1),),
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
        Catalogue.catalogue: (ShopSource(price=30_000, shop_region=Region.pierre_store, other_requirements=(EndgameItemReceivedRequirement(Catalogue.catalogue),)),),
        Catalogue.furniture: (ShopSource(price=200_000, shop_region=Region.carpenter, other_requirements=(EndgameItemReceivedRequirement(Catalogue.furniture), BuildingRequirement(BuildingNames.kitchen),)),),
        Catalogue.joja: (ShopSource(price=25_000, shop_region=Region.movie_theater, other_requirements=(SpeakJunimoRequirement(), EndgameItemReceivedRequirement(Catalogue.joja),)),),
        Catalogue.junimo: (ShopSource(price=70_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpeakJunimoRequirement(), EndgameItemReceivedRequirement(Catalogue.junimo),)),),
        Catalogue.retro: (ShopSource(price=110_000, shop_region=LogicRegion.traveling_cart, other_requirements=(EndgameItemReceivedRequirement(Catalogue.retro),)),),
        Catalogue.wizard: (ShopSource(price=150000, shop_region=Region.sewer, other_requirements=(EndgameItemReceivedRequirement(Catalogue.wizard),)),),

        # Furniture
        Furniture.single_bed: (ShopSource(price=500, shop_region=Region.carpenter),),
        Furniture.crane_game_house_plant: (ShopSource(price=500, shop_region=Region.movie_theater),),
        Furniture.cursed_mannequin: (MonsterSource(monsters=(Monster.haunted_skull,), amount_tier=MAX_MONTHS),),

        # Other shop stuff
        Fertilizer.basic: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        Fertilizer.quality: (ShopSource(price=150, currency=Currency.money, shop_region=Region.pierre_store,
                                        other_requirements=(YearRequirement(2),)),),
        Ingredient.oil: (ShopSource(price=200, currency=Currency.money, shop_region=Region.pierre_store),),
        Ingredient.rice: (ShopSource(price=200, currency=Currency.money, shop_region=Region.pierre_store),),
        Ingredient.sugar: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        Ingredient.vinegar: (ShopSource(price=200, currency=Currency.money, shop_region=Region.pierre_store),),
        Ingredient.wheat_flour: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        RetainingSoil.basic: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        RetainingSoil.quality: (ShopSource(price=150, currency=Currency.money, shop_region=Region.pierre_store,
                                           other_requirements=(YearRequirement(2),)),),
        SpeedGro.basic: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        SpeedGro.deluxe: (ShopSource(price=150, currency=Currency.money, shop_region=Region.pierre_store,
                                     other_requirements=(YearRequirement(2),)),),
        WildSeeds.grass_starter: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store),),
        Gift.bouquet: (ShopSource(price=100, currency=Currency.money, shop_region=Region.pierre_store,
                                  other_requirements=(BachelorFriendRequirement(8),)),),

        Machine.crab_pot: (ShopSource(price=1500, currency=Currency.money, shop_region=Region.fish_shop,
                                      other_requirements=(SkillRequirement(Skill.fishing, 3),)),),
        Fishing.lead_bobber: (ShopSource(price=200, currency=Currency.money, shop_region=Region.fish_shop,
                                         other_requirements=(SkillRequirement(Skill.fishing, 6),)),),

        "Energy Tonic": (ShopSource(price=1000, currency=Currency.money, shop_region=Region.hospital),),
        "Muscle Remedy": (ShopSource(price=1000, currency=Currency.money, shop_region=Region.hospital),),

        Trash.joja_cola: (ShopSource(price=75, currency=Currency.money, shop_region=Region.saloon),),

        AnimalProduct.void_egg_starter: (ShopSource(price=5000, currency=Currency.money, shop_region=Region.sewer),),
        Consumable.butterfly_powder: (ShopSource(price=20000, currency=Currency.money, shop_region=Region.sewer),),
        ShopLocation.krobus_stardrop: (ShopSource(price=20000, currency=Currency.money, shop_region=Region.sewer),),
        Tool.return_scepter: (ShopSource(price=2_000_000, currency=Currency.money, shop_region=Region.sewer),),

        AnimalProduct.golden_egg_starter:  (ShopSource(price=100000, currency=Currency.money, shop_region=Region.ranch,
                                                       other_requirements=(ReceivedRequirement(AnimalProduct.golden_egg),)),),

        Gift.movie_ticket: (ShopSource(price=1000, currency=Currency.money, shop_region=Region.movie_ticket_stand),),

        Meal.ice_cream: (ShopSource(price=250, currency=Currency.money, shop_region=Region.town,
                                       other_requirements=(SeasonRequirement(Season.summer),)),),

        f"{NPC.abigail} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.abigail, 14),)),),
        f"{NPC.alex} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.alex, 14),)),),
        f"{NPC.elliott} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.elliott, 14),)),),
        f"{NPC.emily} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.emily, 14),)),),
        f"{NPC.haley} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.haley, 14),)),),
        f"{NPC.harvey} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.harvey, 14),)),),
        f"{NPC.krobus} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.krobus, 14),)),),
        f"{NPC.leah} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.leah, 14),)),),
        f"{NPC.maru} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.maru, 14),)),),
        f"{NPC.penny} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.penny, 14),)),),
        f"{NPC.sam} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.sam, 14),)),),
        f"{NPC.sebastian} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.sebastian, 14),)),),
        f"{NPC.shane} Portrait": (ShopSource(price=30_000, shop_region=LogicRegion.traveling_cart, other_requirements=(SpecificFriendRequirement(NPC.shane, 14),)),),
        Gift.tea_set: (ShopSource(price=1_000_000, shop_region=LogicRegion.traveling_cart, other_requirements=(YearRequirement(10), RegionRequirement(LogicRegion.winter_star))),),

        Furniture.tub_o_flowers: (ShopSource(price=250, shop_region=LogicRegion.flower_dance),),
        f"{Furniture.tub_o_flowers} Recipe": (ShopSource(price=1000, shop_region=LogicRegion.flower_dance),),
        FestivalCheck.rarecrow_5: (ShopSource(price=2500, shop_region=LogicRegion.flower_dance, other_requirements=(FestivalItemReceivedRequirement("Rarecrow #5"),)),),
        FestivalCheck.moonlight_jellies_banner: (ShopSource(price=800, shop_region=LogicRegion.moonlight_jellies),),
        FestivalCheck.starport_decal: (ShopSource(price=1000, shop_region=LogicRegion.moonlight_jellies),),
        FestivalCheck.rarecrow_1: (ShopSource(price=800, currency=Currency.star_token, shop_region=LogicRegion.fair, other_requirements=(FestivalItemReceivedRequirement("Rarecrow #1"),)),),
        FestivalCheck.fair_stardrop: (ShopSource(price=2000, currency=Currency.star_token, shop_region=LogicRegion.fair),),
        FestivalCheck.jack_o_lantern: (ShopSource(price=2000, shop_region=LogicRegion.spirit_eve),),
        FestivalCheck.rarecrow_2: (ShopSource(price=5000, shop_region=LogicRegion.spirit_eve, other_requirements=(FestivalItemReceivedRequirement("Rarecrow #2"),)),),
        FestivalCheck.rarecrow_4: (ShopSource(price=5000, shop_region=LogicRegion.festival_of_ice, other_requirements=(FestivalItemReceivedRequirement("Rarecrow #4"),)),),
        FestivalCheck.iridium_fireplace: (ShopSource(price=15000, shop_region=LogicRegion.night_market),),
        FestivalCheck.rarecrow_7: (ShopSource(price=5000, shop_region=LogicRegion.night_market,
                                              other_requirements=(FestivalItemReceivedRequirement("Rarecrow #7"),
                                                                  MuseumArtifactsRequirement(20),)),),
        FestivalCheck.rarecrow_8: (ShopSource(price=5000, shop_region=LogicRegion.night_market,
                                              other_requirements=(FestivalItemReceivedRequirement("Rarecrow #8"),
                                                                  MuseumCompletionRequirement(40),)),),
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
        fish_data.flounder,  # Ginger island override
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
                    items_price=((350, Material.wood), (150, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
                ),
            ),
        ),
        Building(
            BuildingNames.big_barn,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=12_000,
                    items_price=((450, Material.wood), (200, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
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
                    items_price=((550, Material.wood), (300, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
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
                    items_price=((300, Material.wood), (100, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
                ),
            ),
        ),
        Building(
            BuildingNames.big_coop,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=10_000,
                    items_price=((400, Material.wood), (150, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
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
                    items_price=((500, Material.wood), (200, Material.stone)),
                    forbidden_items=(AnimalProduct.wool, ArtisanGood.cloth),
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
    tool_upgrades=(
        ToolUpgrade(
            tool_name=Tool.pickaxe,
            tool_material=ToolMaterial.basic,
            sources=(StartingToolSource(),),
        ),
        ToolUpgrade(
            tool_name=Tool.pickaxe,
            tool_material=ToolMaterial.copper,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=2000,
                    items_price=((5, MetalBar.copper),),
                    other_requirements=(ToolRequirement(Tool.pickaxe, ToolMaterial.basic),),
                    forbidden_items=(MetalBar.iron, Ore.iron, Geode.frozen, MetalBar.gold, Ore.gold, Geode.magma, MetalBar.iridium, Ore.iridium, Geode.omni,),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pickaxe,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5000,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.pickaxe, ToolMaterial.copper),),
                    forbidden_items=(MetalBar.gold, Ore.gold, Geode.magma, MetalBar.iridium, Ore.iridium, Geode.omni,),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pickaxe,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=10_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.pickaxe, ToolMaterial.iron),),
                    forbidden_items=(MetalBar.iridium, Ore.iridium, Geode.omni,),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pickaxe,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=25_000,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.pickaxe, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.axe,
            tool_material=ToolMaterial.basic,
            sources=(StartingToolSource(),),
        ),
        ToolUpgrade(
            tool_name=Tool.axe,
            tool_material=ToolMaterial.copper,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=2000,
                    items_price=((5, MetalBar.copper),),
                    other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.basic),),
                    forbidden_items=(Material.hardwood, Geode.omni,),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.axe,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5000,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.copper),),
                    forbidden_items=(Material.hardwood, Geode.omni,),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.axe,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=10_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.iron),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.axe,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=25_000,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.axe, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.watering_can,
            tool_material=ToolMaterial.basic,
            sources=(StartingToolSource(),),
        ),
        ToolUpgrade(
            tool_name=Tool.watering_can,
            tool_material=ToolMaterial.copper,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=2000,
                    items_price=((5, MetalBar.copper),),
                    other_requirements=(ToolRequirement(Tool.watering_can, ToolMaterial.basic),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.watering_can,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5000,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.watering_can, ToolMaterial.copper),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.watering_can,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=10_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.watering_can, ToolMaterial.iron),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.watering_can,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=25_000,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.watering_can, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.basic,
            sources=(StartingToolSource(),),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.copper,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=2000,
                    items_price=((5, MetalBar.copper),),
                    other_requirements=(ToolRequirement(Tool.hoe, ToolMaterial.basic),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5000,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.hoe, ToolMaterial.copper),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=10_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.hoe, ToolMaterial.iron),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=25_000,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.hoe, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.hoe,
            tool_material=ToolMaterial.basic,
            sources=(GenericSource(),),
        ),
        ToolUpgrade(
            tool_name=Tool.trash_can,
            tool_material=ToolMaterial.copper,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=1000,
                    items_price=((5, MetalBar.copper),),
                    other_requirements=(ToolRequirement(Tool.trash_can, ToolMaterial.basic),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.trash_can,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=2500,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.trash_can, ToolMaterial.copper),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.trash_can,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.trash_can, ToolMaterial.iron),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.trash_can,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=12_500,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.trash_can, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pan,
            tool_material=ToolMaterial.iron,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=5000,
                    items_price=((5, MetalBar.iron),),
                    other_requirements=(ToolRequirement(Tool.pan, ToolMaterial.copper),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pan,
            tool_material=ToolMaterial.gold,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=10_000,
                    items_price=((5, MetalBar.gold),),
                    other_requirements=(ToolRequirement(Tool.pan, ToolMaterial.iron),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.pan,
            tool_material=ToolMaterial.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.blacksmith,
                    price=25_000,
                    items_price=((5, MetalBar.iridium),),
                    other_requirements=(ToolRequirement(Tool.pan, ToolMaterial.gold),),
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.fishing_rod,
            full_name=FishingRod.training,
            sources=(
                ShopSource(
                    shop_region=Region.fish_shop,
                    price=5,
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.fishing_rod,
            full_name=FishingRod.bamboo,
            sources=(
                ShopSource(
                    shop_region=Region.fish_shop,
                    price=500,
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.fishing_rod,
            full_name=FishingRod.fiberglass,
            sources=(
                ShopSource(
                    shop_region=Region.fish_shop,
                    price=1800,
                    other_requirements=(SkillRequirement(Skill.fishing, 2),)
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.fishing_rod,
            full_name=FishingRod.iridium,
            sources=(
                ShopSource(
                    shop_region=Region.fish_shop,
                    price=7500,
                    other_requirements=(SkillRequirement(Skill.fishing, 6),)
                ),
            ),
        ),
        ToolUpgrade(
            tool_name=Tool.fishing_rod,
            full_name=FishingRod.advanced_iridium,
            sources=(
                ShopSource(
                    shop_region=Region.fish_shop,
                    price=25_000,
                    other_requirements=(MasteryRequirement(Skill.fishing),)
                ),
            ),
        ),
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

    },
    festivals=(
        all_festival_data[LogicRegion.egg_festival],
        all_festival_data[LogicRegion.flower_dance],
        all_festival_data[LogicRegion.luau],
        all_festival_data[LogicRegion.moonlight_jellies],
        all_festival_data[LogicRegion.fair],
        all_festival_data[LogicRegion.spirit_eve],
        all_festival_data[LogicRegion.festival_of_ice],
        all_festival_data[LogicRegion.winter_star],
        all_festival_data[LogicRegion.night_market],
        all_festival_data[LogicRegion.trout_derby],
        all_festival_data[LogicRegion.squidfest],
    ),
    cooking_recipes=(
        CookingRecipe(name=Meal.algae_soup, ingredients=((WaterItem.green_algae, 4),), sources=(FriendshipSource(friend=NPC.clint, hearts=3),),),
        CookingRecipe(name=Meal.artichoke_dip, ingredients=((Vegetable.artichoke, 4), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=28),),),
        CookingRecipe(name=Meal.autumn_bounty, ingredients=((Vegetable.yam, 1), (Vegetable.pumpkin, 1),), sources=(FriendshipSource(friend=NPC.demetrius, hearts=7),),),
        CookingRecipe(name=Meal.baked_fish, ingredients=((Fish.sunfish, 1), (Fish.bream, 1), (Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=7),),),
        CookingRecipe(name=Meal.bean_hotpot, ingredients=((Vegetable.green_bean, 2),), sources=(FriendshipSource(friend=NPC.clint, hearts=7),),),
        CookingRecipe(name=Meal.blackberry_cobbler, ingredients=((Forageable.blackberry, 2), (Ingredient.sugar, 1), (Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=14),),),
        CookingRecipe(name=Meal.blueberry_tart, ingredients=((Fruit.blueberry, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.any_egg, 1),), sources=(FriendshipSource(friend=NPC.pierre, hearts=3),),),
        CookingRecipe(name=Meal.bread, ingredients=((Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=28),),),
        CookingRecipe(name=Meal.bruschetta, ingredients=((Meal.bread, 1), (Ingredient.oil, 1), (Vegetable.tomato, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=21),),),
        CookingRecipe(name=Meal.carp_surprise, ingredients=((Fish.carp, 4),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=7),),),
        CookingRecipe(name=Meal.cheese_cauliflower, ingredients=((Vegetable.cauliflower, 1), (ArtisanGood.cheese, 1),), sources=(FriendshipSource(friend=NPC.pam, hearts=3),),),
        CookingRecipe(name=Meal.chocolate_cake, ingredients=((Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.chicken_egg, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=14),),),
        CookingRecipe(name=Meal.chowder, ingredients=((Fish.clam, 1), (AnimalProduct.cow_milk, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=3),),),
        CookingRecipe(name=Meal.coleslaw, ingredients=((Vegetable.red_cabbage, 1), (Ingredient.vinegar, 1), (ArtisanGood.mayonnaise, 1),), sources=(QueenOfSauceSource(year=14, season=Season.spring, day=14),),),
        CookingRecipe(name=Meal.complete_breakfast, ingredients=((Meal.fried_egg, 1), (AnimalProduct.milk, 1), (Meal.hashbrowns, 1), (Meal.pancakes, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=21),),),
        CookingRecipe(name=Meal.cookie, ingredients=((Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.chicken_egg, 1),), sources=(FriendshipSource(friend=NPC.evelyn, hearts=4),),),
        CookingRecipe(name=Meal.crab_cakes, ingredients=((Fish.crab, 1), (Ingredient.wheat_flour, 1), (AnimalProduct.chicken_egg, 1), (Ingredient.oil, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=21),),),
        CookingRecipe(name=Meal.cranberry_candy, ingredients=((Fruit.cranberries, 1), (Fruit.apple, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=28),),),
        CookingRecipe(name=Meal.cranberry_sauce, ingredients=((Fruit.cranberries, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.gus, hearts=7),),),
        CookingRecipe(name=Meal.crispy_bass, ingredients=((Fish.largemouth_bass, 1), (Ingredient.wheat_flour, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.kent, hearts=3),),),
        CookingRecipe(name=Meal.dish_o_the_sea, ingredients=((Fish.sardine, 2), (Meal.hashbrowns, 1),), sources=(SkillSource(skill=Skill.fishing, level=3),),),
        CookingRecipe(name=Meal.eggplant_parmesan, ingredients=((Vegetable.eggplant, 1), (Vegetable.tomato, 1),), sources=(FriendshipSource(friend=NPC.lewis, hearts=7),),),
        CookingRecipe(name=Meal.escargot, ingredients=((Fish.snail, 1), (Vegetable.garlic, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=5),),),
        CookingRecipe(name=Meal.farmer_lunch, ingredients=((Meal.omelet, 2), (Vegetable.parsnip, 1),), sources=(SkillSource(skill=Skill.farming, level=3),),),
        CookingRecipe(name=Meal.fiddlehead_risotto, ingredients=((Ingredient.oil, 1), (Forageable.fiddlehead_fern, 1), (Vegetable.garlic, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=28),),),
        CookingRecipe(name=Meal.fish_stew, ingredients=((Fish.crayfish, 1), (Fish.mussel, 1), (Fish.periwinkle, 1), (Vegetable.tomato, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=7),),),
        CookingRecipe(name=Meal.fish_taco, ingredients=((Fish.tuna, 1), (Meal.tortilla, 1), (Vegetable.red_cabbage, 1), (ArtisanGood.mayonnaise, 1),), sources=(FriendshipSource(friend=NPC.linus, hearts=7),),),
        CookingRecipe(name=Meal.fried_calamari, ingredients=((Fish.squid, 1), (Ingredient.wheat_flour, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.jodi, hearts=3),),),
        CookingRecipe(name=Meal.fried_eel, ingredients=((Fish.eel, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.george, hearts=3),),),
        CookingRecipe(name=Meal.fried_egg, ingredients=((AnimalProduct.chicken_egg, 1),), sources=(StarterSource(),),),
        CookingRecipe(name=Meal.fried_mushroom, ingredients=((Mushroom.common, 1), (Mushroom.morel, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.demetrius, hearts=3),),),
        CookingRecipe(name=Meal.fruit_salad, ingredients=((Fruit.blueberry, 1), (Fruit.melon, 1), (Fruit.apricot, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=7),),),
        CookingRecipe(name=Meal.glazed_yams, ingredients=((Vegetable.yam, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=21),),),
        CookingRecipe(name=Meal.hashbrowns, ingredients=((Vegetable.potato, 1), (Ingredient.oil, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=14),),),
        CookingRecipe(name=Meal.ice_cream, ingredients=((AnimalProduct.cow_milk, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.jodi, hearts=7),),),
        CookingRecipe(name=Meal.lobster_bisque, ingredients=((Fish.lobster, 1), (AnimalProduct.cow_milk, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=9),),),
        CookingRecipe(name=Meal.lobster_bisque, ingredients=((Fish.lobster, 1), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=14),),),
        CookingRecipe(name=Meal.lucky_lunch, ingredients=((Fish.sea_cucumber, 1), (Meal.tortilla, 1), (Flower.blue_jazz, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=28),),),
        CookingRecipe(name=Meal.maki_roll, ingredients=((Fish.any, 1), (WaterItem.seaweed, 1), (Ingredient.rice, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=21),),),
        CookingRecipe(name=Meal.maple_bar, ingredients=((ArtisanGood.maple_syrup, 1), (Ingredient.sugar, 1), (Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=14),),),
        CookingRecipe(name=Meal.miners_treat, ingredients=((Forageable.cave_carrot, 2), (Ingredient.sugar, 1), (AnimalProduct.cow_milk, 1),), sources=(SkillSource(skill=Skill.mining, level=3),),),
        CookingRecipe(name=Meal.moss_soup, ingredients=((Material.moss, 20),), sources=(SkillSource(skill=Skill.foraging, level=3),),),
        CookingRecipe(name=Meal.omelet, ingredients=((AnimalProduct.chicken_egg, 1), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=1, season=Season.spring, day=28),),),
        CookingRecipe(name=Meal.pale_broth, ingredients=((WaterItem.white_algae, 2),), sources=(FriendshipSource(friend=NPC.marnie, hearts=3),),),
        CookingRecipe(name=Meal.pancakes, ingredients=((Ingredient.wheat_flour, 1), (AnimalProduct.chicken_egg, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=14),),),
        CookingRecipe(name=Meal.parsnip_soup, ingredients=((Vegetable.parsnip, 1), (AnimalProduct.cow_milk, 1), (Ingredient.vinegar, 1),), sources=(FriendshipSource(friend=NPC.caroline, hearts=3),),),
        CookingRecipe(name=Meal.pepper_poppers, ingredients=((Fruit.hot_pepper, 1), (ArtisanGood.cheese, 1),), sources=(FriendshipSource(friend=NPC.shane, hearts=3),),),
        CookingRecipe(name=Meal.pink_cake, ingredients=((Fruit.melon, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.chicken_egg, 1),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=21),),),
        CookingRecipe(name=Meal.pizza, ingredients=((Ingredient.wheat_flour, 1), (Vegetable.tomato, 1), (ArtisanGood.cheese, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=7),),),
        CookingRecipe(name=Meal.pizza, ingredients=((Ingredient.wheat_flour, 1), (Vegetable.tomato, 1), (ArtisanGood.cheese, 1),), sources=(ShopSource(shop_region=Region.saloon, price=150),),),
        CookingRecipe(name=Meal.plum_pudding, ingredients=((Forageable.wild_plum, 2), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=7),),),
        CookingRecipe(name=Meal.poppyseed_muffin, ingredients=((Flower.poppy, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=7),),),
        CookingRecipe(name=Meal.pumpkin_pie, ingredients=((Vegetable.pumpkin, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=21),),),
        CookingRecipe(name=Meal.pumpkin_soup, ingredients=((Vegetable.pumpkin, 1), (AnimalProduct.cow_milk, 1),), sources=(FriendshipSource(friend=NPC.robin, hearts=7),),),
        CookingRecipe(name=Meal.radish_salad, ingredients=((Ingredient.oil, 1), (Ingredient.vinegar, 1), (Vegetable.radish, 1),), sources=(QueenOfSauceSource(year=1, season=Season.spring, day=21),),),
        CookingRecipe(name=Meal.red_plate, ingredients=((Vegetable.red_cabbage, 1), (Vegetable.radish, 1),), sources=(FriendshipSource(friend=NPC.emily, hearts=7),),),
        CookingRecipe(name=Meal.rhubarb_pie, ingredients=((Fruit.rhubarb, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.marnie, hearts=7),),),
        CookingRecipe(name=Meal.rice_pudding, ingredients=((AnimalProduct.milk, 1), (Ingredient.sugar, 1), (Ingredient.rice, 1),), sources=(FriendshipSource(friend=NPC.evelyn, hearts=7),),),
        CookingRecipe(name=Meal.roasted_hazelnuts, ingredients=((Forageable.hazelnut, 3),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=28),),),
        CookingRecipe(name=Meal.roots_platter, ingredients=((Forageable.cave_carrot, 1), (Forageable.winter_root, 1),), sources=(SkillSource(skill=Skill.combat, level=3),),),
        CookingRecipe(name=Meal.salad, ingredients=((Forageable.leek, 1), (Forageable.dandelion, 1), (Ingredient.vinegar, 1),), sources=(FriendshipSource(friend=NPC.emily, hearts=3),),),
        CookingRecipe(name=Meal.salmon_dinner, ingredients=((Fish.salmon, 1), (Vegetable.amaranth, 1), (Vegetable.kale, 1),), sources=(FriendshipSource(friend=NPC.gus, hearts=3),),),
        CookingRecipe(name=Meal.sashimi, ingredients=((Fish.any, 1),), sources=(FriendshipSource(friend=NPC.linus, hearts=3),),),
        CookingRecipe(name=Meal.seafoam_pudding, ingredients=((Fish.flounder, 1), (Fish.midnight_carp, 1), (AnimalProduct.squid_ink, 1),), sources=(SkillSource(skill=Skill.fishing, level=9),),),
        CookingRecipe(name=Meal.shrimp_cocktail, ingredients=((Vegetable.tomato, 1), (Fish.shrimp, 1), (Forageable.wild_horseradish, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=28),),),
        CookingRecipe(name=Meal.spaghetti, ingredients=((Vegetable.tomato, 1), (Ingredient.wheat_flour, 1),), sources=(FriendshipSource(friend=NPC.lewis, hearts=3),),),
        CookingRecipe(name=Meal.spicy_eel, ingredients=((Fish.eel, 1), (Fruit.hot_pepper, 1),), sources=(FriendshipSource(friend=NPC.george, hearts=7),),),
        CookingRecipe(name=Meal.squid_ink_ravioli, ingredients=((AnimalProduct.squid_ink, 1), (Ingredient.wheat_flour, 1), (Vegetable.tomato, 1),), sources=(SkillSource(skill=Skill.combat, level=9),),),
        CookingRecipe(name=Meal.stir_fry, ingredients=((Forageable.cave_carrot, 1), (Mushroom.common, 1), (Vegetable.kale, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.spring, day=7),),),
        CookingRecipe(name=Meal.strange_bun, ingredients=((Ingredient.wheat_flour, 1), (Fish.periwinkle, 1), (ArtisanGood.void_mayonnaise, 1),), sources=(FriendshipSource(friend=NPC.shane, hearts=7),),),
        CookingRecipe(name=Meal.stuffing, ingredients=((Meal.bread, 1), (Fruit.cranberries, 1), (Forageable.hazelnut, 1),), sources=(FriendshipSource(friend=NPC.pam, hearts=7),),),
        CookingRecipe(name=Meal.super_meal, ingredients=((Vegetable.bok_choy, 1), (Fruit.cranberries, 1), (Vegetable.artichoke, 1),), sources=(FriendshipSource(friend=NPC.kent, hearts=7),),),
        CookingRecipe(name=Meal.survival_burger, ingredients=((Meal.bread, 1), (Forageable.cave_carrot, 1), (Vegetable.eggplant, 1),), sources=(SkillSource(skill=Skill.foraging, level=8),),),
        CookingRecipe(name=Meal.tom_kha_soup, ingredients=((Forageable.coconut, 1), (Fish.shrimp, 1), (Mushroom.common, 1),), sources=(FriendshipSource(friend=NPC.sandy, hearts=7),),),
        CookingRecipe(name=Meal.tortilla, ingredients=((Vegetable.corn, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=7),),),
        CookingRecipe(name=Meal.tortilla, ingredients=((Vegetable.corn, 1),), sources=(ShopSource(shop_region=Region.saloon, price=100),),),
        CookingRecipe(name=Beverage.triple_shot_espresso, ingredients=((Beverage.coffee, 3),), sources=(ShopSource(shop_region=Region.saloon, price=5000),),),
        CookingRecipe(name=Meal.trout_soup, ingredients=((Fish.rainbow_trout, 1), (WaterItem.green_algae, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=14),),),
        CookingRecipe(name=Meal.vegetable_medley, ingredients=((Vegetable.tomato, 1), (Vegetable.beet, 1),), sources=(FriendshipSource(friend=NPC.caroline, hearts=7),),),
    ),
    crafting_recipes=(
        CraftingRecipe(name=Bomb.cherry_bomb, ingredients=((Ore.copper, 4), (Material.coal, 1),), sources=(SkillSource(skill=Skill.mining, level=1),),),
        CraftingRecipe(name=Bomb.bomb, ingredients=((Ore.iron, 4), (Material.coal, 1),), sources=(SkillSource(skill=Skill.mining, level=6),),),
        CraftingRecipe(name=Bomb.mega_bomb, ingredients=((Ore.gold, 4), (Loot.solar_essence, 1), (Loot.void_essence, 1),), sources=(SkillSource(skill=Skill.mining, level=8),),),

        CraftingRecipe(name=Fence.gate, ingredients=((Material.wood, 10),), sources=(StarterSource(),),),
        CraftingRecipe(name=Fence.wood, ingredients=((Material.wood, 2),), sources=(StarterSource(),),),
        CraftingRecipe(name=Fence.stone, ingredients=((Material.stone, 2),), sources=(SkillSource(skill=Skill.farming, level=2),),),
        CraftingRecipe(name=Fence.iron, ingredients=((MetalBar.iron, 2),), sources=(SkillSource(skill=Skill.farming, level=4),),),
        CraftingRecipe(name=Fence.hardwood, ingredients=((Material.hardwood, 2),), sources=(SkillSource(skill=Skill.farming, level=6),),),

        CraftingRecipe(name=Sprinkler.basic, ingredients=((MetalBar.copper, 1), (MetalBar.iron, 1),), sources=(SkillSource(skill=Skill.farming, level=2),),),
        CraftingRecipe(name=Sprinkler.quality, ingredients=((MetalBar.iron, 1), (MetalBar.gold, 1), (MetalBar.quartz, 1),), sources=(SkillSource(skill=Skill.farming, level=6),),),
        CraftingRecipe(name=Sprinkler.iridium, ingredients=((MetalBar.gold, 1), (MetalBar.iridium, 1), (ArtisanGood.battery_pack, 1),), sources=(SkillSource(skill=Skill.farming, level=9),),),

        CraftingRecipe(name=Machine.bee_house, ingredients=((Material.wood, 40), (Material.coal, 8), (MetalBar.iron, 1), (ArtisanGood.maple_syrup, 1),), sources=(SkillSource(skill=Skill.farming, level=3),),),
        CraftingRecipe(name=Machine.cask, ingredients=((Material.wood, 40), (Material.hardwood, 1),), sources=(CutsceneSource(region=Region.cellar, friend=NPC.robin, hearts=0, other_requirements=(BuildingRequirement(BuildingNames.cellar),)),),),
        CraftingRecipe(name=Machine.cheese_press, ingredients=((Material.wood, 45), (Material.stone, 45), (Material.hardwood, 10), (MetalBar.copper, 1),), sources=(SkillSource(skill=Skill.farming, level=6),),),
        CraftingRecipe(name=Machine.keg, ingredients=((Material.wood, 30), (MetalBar.copper, 1), (MetalBar.iron, 1), (ArtisanGood.oak_resin, 1),), sources=(SkillSource(skill=Skill.farming, level=8),),),
        CraftingRecipe(name=Machine.loom, ingredients=((Material.wood, 60), (Material.fiber, 30), (ArtisanGood.pine_tar, 1),), sources=(SkillSource(skill=Skill.farming, level=7),),),
        CraftingRecipe(name=Machine.mayonnaise_machine, ingredients=((Material.wood, 15), (Material.stone, 15), (Mineral.earth_crystal, 10), (MetalBar.copper, 1),), sources=(SkillSource(skill=Skill.farming, level=2),),),
        CraftingRecipe(name=Machine.oil_maker, ingredients=((Loot.slime, 50), (Material.hardwood, 20), (MetalBar.gold, 1),), sources=(SkillSource(skill=Skill.farming, level=8),),),
        CraftingRecipe(name=Machine.preserves_jar, ingredients=((Material.wood, 50), (Material.stone, 40), (Material.coal, 8),), sources=(SkillSource(skill=Skill.farming, level=4),),),
        CraftingRecipe(name=Machine.fish_smoker, ingredients=((Material.hardwood, 10), (WaterItem.sea_jelly, 1), (WaterItem.river_jelly, 1), (WaterItem.cave_jelly, 1),), sources=(ShopSource(shop_region=Region.fish_shop, price=10000),),),
        CraftingRecipe(name=Machine.dehydrator, ingredients=((Material.wood, 30), (Material.clay, 2), (Mineral.fire_quartz, 1),), sources=(ShopSource(shop_region=Region.pierre_store, price=10000),),),

        CraftingRecipe(name=Fertilizer.basic, ingredients=((Material.sap, 2),), sources=(SkillSource(skill=Skill.farming, level=1),),),

        CraftingRecipe(name=Fertilizer.quality, ingredients=((Material.sap, 4), (Fish.any, 1),), sources=(SkillSource(skill=Skill.farming, level=9),),),
        CraftingRecipe(name=Fertilizer.deluxe, ingredients=((MetalBar.iridium, 1), (Material.sap, 40),), sources=(ArchipelagoSource(ap_items=(f"{Fertilizer.deluxe} Recipe",)),),),

        CraftingRecipe(name=SpeedGro.basic, ingredients=((ArtisanGood.pine_tar, 1), (Material.moss, 5),), sources=(SkillSource(skill=Skill.farming, level=3),),),
        CraftingRecipe(name=SpeedGro.deluxe, ingredients=((ArtisanGood.oak_resin, 1), (Fossil.bone_fragment, 5),), sources=(SkillSource(skill=Skill.farming, level=8),),),
        CraftingRecipe(name=RetainingSoil.basic, ingredients=((Material.stone, 2),), sources=(SkillSource(skill=Skill.farming, level=4),),),
        CraftingRecipe(name=RetainingSoil.quality, ingredients=((Material.stone, 3), (Material.clay, 1),), sources=(SkillSource(skill=Skill.farming, level=7),),),
        CraftingRecipe(name=Fertilizer.tree, ingredients=((Material.fiber, 5), (Material.stone, 5),), sources=(SkillSource(skill=Skill.foraging, level=7),),),

        CraftingRecipe(name=WildSeeds.spring, ingredients=((Forageable.wild_horseradish, 1), (Forageable.daffodil, 1), (Forageable.leek, 1), (Forageable.dandelion, 1),), sources=(SkillSource(skill=Skill.foraging, level=1),),),
        CraftingRecipe(name=WildSeeds.summer, ingredients=((Forageable.spice_berry, 1), (Fruit.grape, 1), (Forageable.sweet_pea, 1),), sources=(SkillSource(skill=Skill.foraging, level=4),),),
        CraftingRecipe(name=WildSeeds.fall, ingredients=((Mushroom.common, 1), (Forageable.wild_plum, 1), (Forageable.hazelnut, 1), (Forageable.blackberry, 1),), sources=(SkillSource(skill=Skill.foraging, level=6),),),
        CraftingRecipe(name=WildSeeds.winter, ingredients=((Forageable.winter_root, 1), (Forageable.crystal_fruit, 1), (Forageable.snow_yam, 1), (Forageable.crocus, 1),), sources=(SkillSource(skill=Skill.foraging, level=7),),),
        CraftingRecipe(name=WildSeeds.ancient, ingredients=((Artifact.ancient_seed, 1),), sources=(ArchipelagoSource(ap_items=(f"{WildSeeds.ancient} Recipe",)),),),
        CraftingRecipe(name=WildSeeds.grass_starter, ingredients=((Material.fiber, 10),), sources=(ShopSource(shop_region=Region.pierre_store, price=1000),),),
        CraftingRecipe(name=WildSeeds.tea_sapling, ingredients=(((WildSeeds.spring, WildSeeds.summer, WildSeeds.fall, WildSeeds.winter), 2), (Material.fiber, 5), (Material.wood, 5),), sources=(CutsceneSource(region=Region.sunroom, friend=NPC.caroline, hearts=2),),),
        CraftingRecipe(name=WildSeeds.fiber, ingredients=((Seed.mixed, 1), (Material.sap, 5), (Material.clay, 1),), sources=(SpecialOrderSource(special_order=SpecialOrder.community_cleanup),),),

        CraftingRecipe(name=Floor.wood, ingredients=((Material.wood, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=100),),),
        CraftingRecipe(name=Floor.rustic, ingredients=((Material.wood, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=200),),),
        CraftingRecipe(name=Floor.straw, ingredients=((Material.wood, 1), (Material.fiber, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=200),),),
        CraftingRecipe(name=Floor.weathered, ingredients=((Material.wood, 1),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=500),),),
        CraftingRecipe(name=Floor.crystal, ingredients=((MetalBar.quartz, 1),), sources=(ShopSource(shop_region=Region.sewer, price=500),),),
        CraftingRecipe(name=Floor.stone, ingredients=((Material.stone, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=100),),),
        CraftingRecipe(name=Floor.stone_walkway, ingredients=((Material.stone, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=200),),),
        CraftingRecipe(name=Floor.brick, ingredients=((Material.clay, 2), (Material.stone, 5),), sources=(ShopSource(shop_region=Region.carpenter, price=500),),),
        CraftingRecipe(name=Floor.wood_path, ingredients=((Material.wood, 1),), sources=(StarterSource(),),),
        CraftingRecipe(name=Floor.gravel_path, ingredients=((Material.stone, 1),), sources=(StarterSource(),),),
        CraftingRecipe(name=Floor.cobblestone_path, ingredients=((Material.stone, 1),), sources=(StarterSource(),),),
        CraftingRecipe(name=Floor.stepping_stone_path, ingredients=((Material.stone, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=100),),),
        CraftingRecipe(name=Floor.crystal_path, ingredients=((MetalBar.quartz, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=200),),),

        CraftingRecipe(name=Fishing.spinner, ingredients=((MetalBar.iron, 2),), sources=(SkillSource(skill=Skill.fishing, level=6),),),
        CraftingRecipe(name=Fishing.trap_bobber, ingredients=((MetalBar.copper, 1), (Material.sap, 10),), sources=(SkillSource(skill=Skill.fishing, level=6),),),
        CraftingRecipe(name=Fishing.sonar_bobber, ingredients=((MetalBar.iron, 1), (MetalBar.quartz, 2),), sources=(SkillSource(skill=Skill.fishing, level=6),),),
        CraftingRecipe(name=Fishing.cork_bobber, ingredients=((Material.wood, 10), (Material.hardwood, 5), (Loot.slime, 10),), sources=(SkillSource(skill=Skill.fishing, level=7),),),
        CraftingRecipe(name=Fishing.quality_bobber, ingredients=((MetalBar.copper, 1), (Material.sap, 20), (Loot.solar_essence, 5),), sources=(SpecialOrderSource(special_order=SpecialOrder.juicy_bugs_wanted),),),
        CraftingRecipe(name=Fishing.treasure_hunter, ingredients=((MetalBar.gold, 2),), sources=(SkillSource(skill=Skill.fishing, level=7),),),
        CraftingRecipe(name=Fishing.dressed_spinner, ingredients=((MetalBar.iron, 2), (ArtisanGood.cloth, 1),), sources=(SkillSource(skill=Skill.fishing, level=8),),),
        CraftingRecipe(name=Fishing.barbed_hook, ingredients=((MetalBar.copper, 1), (MetalBar.iron, 1), (MetalBar.gold, 1),), sources=(SkillSource(skill=Skill.fishing, level=8),),),
        CraftingRecipe(name=Fishing.magnet, ingredients=((MetalBar.iron, 1),), sources=(SkillSource(skill=Skill.fishing, level=9),),),
        CraftingRecipe(name=Fishing.bait, ingredients=((Loot.bug_meat, 1),), sources=(SkillSource(skill=Skill.fishing, level=2),),),
        CraftingRecipe(name=Fishing.deluxe_bait, ingredients=((Fishing.bait, 5), (Material.moss, 2),), sources=(SkillSource(skill=Skill.fishing, level=4),),),
        CraftingRecipe(name=Fishing.wild_bait, ingredients=((Material.fiber, 10), (Loot.bug_meat, 5), (Loot.slime, 5),), sources=(CutsceneSource(region=Region.tent, friend=NPC.linus, hearts=4),),),
        CraftingRecipe(name=Machine.crab_pot, ingredients=((Material.wood, 40), (MetalBar.iron, 3),), sources=(SkillSource(skill=Skill.fishing, level=3),),),

        CraftingRecipe(name=Ring.sturdy_ring, ingredients=((MetalBar.copper, 2), (Loot.bug_meat, 25), (Loot.slime, 25),), sources=(SkillSource(skill=Skill.combat, level=1),),),
        CraftingRecipe(name=Ring.warrior_ring, ingredients=((MetalBar.iron, 10), (Material.coal, 25), (Mineral.frozen_tear, 10),), sources=(SkillSource(skill=Skill.combat, level=4),),),
        CraftingRecipe(name=Ring.ring_of_yoba, ingredients=((MetalBar.gold, 5), (MetalBar.iron, 5), (Mineral.diamond, 1),), sources=(SkillSource(skill=Skill.combat, level=7),),),
        CraftingRecipe(name=Ring.glowstone_ring, ingredients=((Loot.solar_essence, 5), (MetalBar.iron, 5),), sources=(SkillSource(skill=Skill.mining, level=4),),),
        CraftingRecipe(name=Ring.iridium_band, ingredients=((MetalBar.iridium, 5), (Loot.solar_essence, 50), (Loot.void_essence, 50),), sources=(SkillSource(skill=Skill.combat, level=9),),),
        CraftingRecipe(name=Ring.wedding_ring, ingredients=((MetalBar.iridium, 5), (Mineral.prismatic_shard, 1),), sources=(ShopSource(shop_region=LogicRegion.traveling_cart, price=500),),),

        CraftingRecipe(name=Edible.field_snack, ingredients=((TreeSeed.acorn, 1), (TreeSeed.maple, 1), (TreeSeed.pine, 1),), sources=(SkillSource(skill=Skill.foraging, level=1),),),
        CraftingRecipe(name=Edible.bug_steak, ingredients=((Loot.bug_meat, 10),), sources=(SkillSource(skill=Skill.combat, level=1),),),
        CraftingRecipe(name=Edible.life_elixir, ingredients=((Mushroom.red, 1), (Mushroom.purple, 1), (Mushroom.morel, 1), (Mushroom.chanterelle, 1),), sources=(SkillSource(skill=Skill.combat, level=2),),),
        CraftingRecipe(name=Edible.oil_of_garlic, ingredients=((Vegetable.garlic, 10), (Ingredient.oil, 1),), sources=(SkillSource(skill=Skill.combat, level=6),),),

        CraftingRecipe(name=Consumable.monster_musk, ingredients=((Loot.bat_wing, 30), (Loot.slime, 30),), sources=(SpecialOrderSource(special_order=SpecialOrder.prismatic_jelly),),),
        CraftingRecipe(name=Consumable.warp_totem_beach, ingredients=((Material.hardwood, 1), (WaterItem.coral, 2), (Material.fiber, 10),), sources=(SkillSource(skill=Skill.foraging, level=6),),),
        CraftingRecipe(name=Consumable.warp_totem_mountains, ingredients=((Material.hardwood, 1), (MetalBar.iron, 1), (Material.stone, 25),), sources=(SkillSource(skill=Skill.foraging, level=7),),),
        CraftingRecipe(name=Consumable.warp_totem_farm, ingredients=((Material.hardwood, 1), (ArtisanGood.honey, 1), (Material.fiber, 20),), sources=(SkillSource(skill=Skill.foraging, level=8),),),
        CraftingRecipe(name=Consumable.warp_totem_desert, ingredients=((Material.hardwood, 2), (Forageable.coconut, 1), (Ore.iridium, 4),), sources=(ShopSource(shop_region=Region.desert, items_price=((10, MetalBar.iridium),)),),),
        CraftingRecipe(name=Consumable.rain_totem, ingredients=((Material.hardwood, 1), (ArtisanGood.truffle_oil, 1), (ArtisanGood.pine_tar, 5),), sources=(SkillSource(skill=Skill.foraging, level=9),),),

        CraftingRecipe(name=Lighting.torch, ingredients=((Material.wood, 1), (Material.sap, 2),), sources=(StarterSource(),),),
        CraftingRecipe(name=Lighting.campfire, ingredients=((Material.stone, 10), (Material.wood, 10), (Material.fiber, 10),), sources=(StarterSource(),),),
        CraftingRecipe(name=Lighting.wooden_brazier, ingredients=((Material.wood, 10), (Material.coal, 1), (Material.fiber, 5),), sources=(ShopSource(shop_region=Region.carpenter, price=250),),),
        CraftingRecipe(name=Lighting.stone_brazier, ingredients=((Material.stone, 10), (Material.coal, 1), (Material.fiber, 5),), sources=(ShopSource(shop_region=Region.carpenter, price=400),),),
        CraftingRecipe(name=Lighting.gold_brazier, ingredients=((MetalBar.gold, 1), (Material.coal, 1), (Material.fiber, 5),), sources=(ShopSource(shop_region=Region.carpenter, price=1000),),),
        CraftingRecipe(name=Lighting.carved_brazier, ingredients=((Material.hardwood, 10), (Material.coal, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=2000),),),
        CraftingRecipe(name=Lighting.stump_brazier, ingredients=((Material.hardwood, 5), (Material.coal, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=800),),),
        CraftingRecipe(name=Lighting.barrel_brazier, ingredients=((Material.wood, 50), (Loot.solar_essence, 1), (Material.coal, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=800),),),
        CraftingRecipe(name=Lighting.skull_brazier, ingredients=((Fossil.bone_fragment, 10),), sources=(ShopSource(shop_region=Region.carpenter, price=3000),),),
        CraftingRecipe(name=Lighting.marble_brazier, ingredients=((Mineral.marble, 1), (Mineral.aquamarine, 1), (Material.stone, 100),), sources=(ShopSource(shop_region=Region.carpenter, price=5000),),),
        CraftingRecipe(name=Lighting.wood_lamp_post, ingredients=((Material.wood, 50), (ArtisanGood.battery_pack, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=500),),),
        CraftingRecipe(name=Lighting.iron_lamp_post, ingredients=((MetalBar.iron, 1), (ArtisanGood.battery_pack, 1),), sources=(ShopSource(shop_region=Region.carpenter, price=1000),),),
        CraftingRecipe(name=Lighting.jack_o_lantern, ingredients=((Vegetable.pumpkin, 1), (Lighting.torch, 1),), sources=(ShopSource(shop_region=LogicRegion.spirit_eve, price=2000),),),

        CraftingRecipe(name=Machine.bone_mill, ingredients=((Fossil.bone_fragment, 10), (Material.clay, 3), (Material.stone, 20),), sources=(SpecialOrderSource(special_order=SpecialOrder.fragments_of_the_past),),),
        CraftingRecipe(name=Machine.bait_maker, ingredients=((MetalBar.iron, 3), (WaterItem.coral, 3), (WaterItem.sea_urchin, 1),), sources=(SkillSource(skill=Skill.fishing, level=6),),),

        CraftingRecipe(name=Machine.charcoal_kiln, ingredients=((Material.wood, 20), (MetalBar.copper, 2),), sources=(SkillSource(skill=Skill.foraging, level=2),),),

        CraftingRecipe(name=Machine.crystalarium, ingredients=((Material.stone, 99), (MetalBar.gold, 5), (MetalBar.iridium, 2), (ArtisanGood.battery_pack, 1),), sources=(SkillSource(skill=Skill.mining, level=9),),),

        # # In-Game, the Furnace recipe is completely unique. It is the only recipe that is obtained in a cutscene after doing a skill-related action.
        # # So it has a custom source that needs both the craftsanity item from AP and the skill, if craftsanity is enabled.
        CraftingRecipe(name=Machine.furnace, ingredients=((Ore.copper, 20), (Material.stone, 25),), sources=(StarterSource(other_requirements=(SkillRequirement(skill=Skill.mining, level=1), RegionRequirement(region=Region.mines_floor_5),)),),),

        CraftingRecipe(name=Machine.geode_crusher, ingredients=((MetalBar.gold, 2), (Material.stone, 50), (Mineral.diamond, 1),), sources=(SpecialOrderSource(special_order=SpecialOrder.cave_patrol),),),
        CraftingRecipe(name=Machine.mushroom_log, ingredients=((Material.hardwood, 10), (Material.moss, 10),), sources=(SkillSource(skill=Skill.foraging, level=4),),),
        CraftingRecipe(name=Machine.lightning_rod, ingredients=((MetalBar.iron, 1), (MetalBar.quartz, 1), (Loot.bat_wing, 5),), sources=(SkillSource(skill=Skill.foraging, level=6),),),
        CraftingRecipe(name=Machine.recycling_machine, ingredients=((Material.wood, 25), (Material.stone, 25), (MetalBar.iron, 1),), sources=(SkillSource(skill=Skill.fishing, level=4),),),
        CraftingRecipe(name=Machine.seed_maker, ingredients=((Material.wood, 25), (Material.coal, 10), (MetalBar.gold, 1),), sources=(SkillSource(skill=Skill.farming, level=9),),),
        CraftingRecipe(name=Machine.slime_egg_press, ingredients=((Material.coal, 25), (Mineral.fire_quartz, 1), (ArtisanGood.battery_pack, 1),), sources=(SkillSource(skill=Skill.combat, level=6),),),
        CraftingRecipe(name=Machine.slime_incubator, ingredients=((MetalBar.iridium, 2), (Loot.slime, 100),), sources=(SkillSource(skill=Skill.combat, level=8),),),

        CraftingRecipe(name=Machine.tapper, ingredients=((Material.wood, 40), (MetalBar.copper, 2),), sources=(SkillSource(skill=Skill.foraging, level=4),),),

        CraftingRecipe(name=Machine.worm_bin, ingredients=((Material.hardwood, 25), (MetalBar.gold, 1), (MetalBar.iron, 1), (Material.fiber, 50),), sources=(SkillSource(skill=Skill.fishing, level=4),),),
        CraftingRecipe(name=Machine.deluxe_worm_bin, ingredients=((Machine.worm_bin, 1), (Material.moss, 30),), sources=(SkillSource(skill=Skill.fishing, level=8),),),

        CraftingRecipe(name=Furniture.tub_o_flowers, ingredients=((Material.wood, 25), (Seed.tulip, 1), (Seed.jazz, 1), (Seed.poppy, 1), (Seed.spangle, 1),), sources=(ShopSource(shop_region=LogicRegion.flower_dance, price=2000),),),
        CraftingRecipe(name=Furniture.wicked_statue, ingredients=((Material.stone, 25), (Material.coal, 5),), sources=(ShopSource(shop_region=Region.sewer, price=1000),),),
        CraftingRecipe(name=Furniture.flute_block, ingredients=((Material.wood, 10), (Ore.copper, 2), (Material.fiber, 20),), sources=(CutsceneSource(region=Region.carpenter, friend=NPC.robin, hearts=6),),),
        CraftingRecipe(name=Furniture.drum_block, ingredients=((Material.stone, 10), (Ore.copper, 2), (Material.fiber, 20),), sources=(CutsceneSource(region=Region.carpenter, friend=NPC.robin, hearts=6),),),

        CraftingRecipe(name=Storage.chest, ingredients=((Material.wood, 50),), sources=(StarterSource(),),),
        CraftingRecipe(name=Storage.stone_chest, ingredients=((Material.stone, 50),), sources=(SpecialOrderSource(special_order=SpecialOrder.robins_resource_rush),),),
        CraftingRecipe(name=Storage.big_chest, ingredients=((Material.wood, 120), (MetalBar.copper, 2),), sources=(ShopSource(shop_region=Region.carpenter, price=5000),),),
        CraftingRecipe(name=Storage.big_stone_chest, ingredients=((Material.stone, 250),), sources=(ShopSource(shop_region=LogicRegion.mines_dwarf_shop, price=5000, other_requirements=(CraftedSpecificItemRequirement(Storage.stone_chest),)),),),

        CraftingRecipe(name=Sign.wood, ingredients=((Material.wood, 25),), sources=(StarterSource(),),),
        CraftingRecipe(name=Sign.stone, ingredients=((Material.stone, 25),), sources=(StarterSource(),),),
        CraftingRecipe(name=Sign.dark, ingredients=((Loot.bat_wing, 5), (Fossil.bone_fragment, 5),), sources=(FriendshipSource(friend=NPC.krobus, hearts=3),),),
        CraftingRecipe(name=Sign.text, ingredients=((Material.wood, 25),), sources=(StarterSource(),),),

        CraftingRecipe(name=Craftable.garden_pot, ingredients=((Material.clay, 1), (Material.stone, 10), (MetalBar.quartz, 1),), sources=(ArchipelagoSource(ap_items=("Greenhouse",)),),), # $8
        CraftingRecipe(name=Craftable.scarecrow, ingredients=((Material.wood, 50), (Material.coal, 1), (Material.fiber, 20),), sources=(SkillSource(skill=Skill.farming, level=1),),),
        CraftingRecipe(name=Craftable.deluxe_scarecrow, ingredients=((Material.wood, 50), (Material.fiber, 40), (Ore.iridium, 1),), sources=(ArchipelagoSource(ap_items=(f"{Craftable.deluxe_scarecrow} Recipe",)),),),
        CraftingRecipe(name=Craftable.staircase, ingredients=((Material.stone, 99),), sources=(SkillSource(skill=Skill.mining, level=2),),),
        CraftingRecipe(name=Craftable.explosive_ammo, ingredients=((MetalBar.iron, 1), (Material.coal, 2),), sources=(SkillSource(skill=Skill.combat, level=8),),),
        CraftingRecipe(name=Craftable.transmute_fe, ingredients=((MetalBar.copper, 3),), sources=(SkillSource(skill=Skill.mining, level=4),),),
        CraftingRecipe(name=Craftable.transmute_au, ingredients=((MetalBar.iron, 2),), sources=(SkillSource(skill=Skill.mining, level=7),),),
        CraftingRecipe(name=Craftable.mini_jukebox, ingredients=((MetalBar.iron, 2), (ArtisanGood.battery_pack, 1),), sources=(CutsceneSource(region=Region.saloon, friend=NPC.gus, hearts=5),),),
        CraftingRecipe(name=Craftable.mini_obelisk, ingredients=((Material.hardwood, 30), (Loot.solar_essence, 20), (MetalBar.gold, 3),), sources=(SpecialOrderSource(special_order=SpecialOrder.a_curious_substance),),),
        CraftingRecipe(name=Craftable.farm_computer, ingredients=((Artifact.dwarf_gadget, 1), (ArtisanGood.battery_pack, 1), (MetalBar.quartz, 10),), sources=(SpecialOrderSource(special_order=SpecialOrder.aquatic_overpopulation),),),

        CraftingRecipe(name=Craftable.cookout_kit, ingredients=((Material.wood, 15), (Material.fiber, 10), (Material.coal, 3),), sources=(SkillSource(skill=Skill.foraging, level=3),),),
        CraftingRecipe(name=Craftable.tent_kit, ingredients=((Material.hardwood, 10), (Material.fiber, 25), (ArtisanGood.cloth, 1),), sources=(SkillSource(skill=Skill.foraging, level=8),),),

        CraftingRecipe(name=Statue.blessings, ingredients=((Material.sap, 999), (Material.fiber, 999), (Material.stone, 999), (Material.moss, 333),), sources=(MasterySource(skill=Skill.farming),),),
        CraftingRecipe(name=Statue.dwarf_king, ingredients=((MetalBar.iridium, 20),), sources=(MasterySource(skill=Skill.mining),),),
        CraftingRecipe(name=Machine.heavy_furnace, ingredients=((Machine.furnace, 2), (MetalBar.iron, 3), (Material.stone, 50),), sources=(MasterySource(skill=Skill.mining),),),
        CraftingRecipe(name=TreeSeed.mystic, ingredients=((TreeSeed.acorn, 5), (TreeSeed.maple, 5), (TreeSeed.pine, 5), (TreeSeed.mahogany, 5),), sources=(MasterySource(skill=Skill.foraging),),),
        CraftingRecipe(name=Consumable.treasure_totem, ingredients=((Material.hardwood, 5), (ArtisanGood.mystic_syrup, 1), (Material.moss, 10),), sources=(MasterySource(skill=Skill.foraging),),),
        CraftingRecipe(name=Fishing.challenge_bait, ingredients=((Fossil.bone_fragment, 5), (Material.moss, 2),), sources=(MasterySource(skill=Skill.fishing),),),
        CraftingRecipe(name=Machine.anvil, ingredients=((MetalBar.iron, 50),), sources=(MasterySource(skill=Skill.combat),),),
    ),
)
