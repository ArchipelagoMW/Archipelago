from ..game_content import ContentPack
from ...data import villagers_data, fish_data
from ...data.building import Building
from ...data.cooking_recipe import CookingRecipe
from ...data.festival_data import all_festival_data
from ...data.game_item import GenericSource, ItemTag, Tag, CustomRuleSource, AllRegionsSource
from ...data.harvest import ForagingSource, SeasonalForagingSource, ArtifactSpotSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.recipe_source import FriendshipSource, QueenOfSauceSource
from ...data.requirement import ToolRequirement, BookRequirement, SkillRequirement, YearRequirement, \
    GrangeDisplayRequirement, EggHuntRequirement, MuseumCompletionRequirement, BuildingRequirement, \
    NumberOfFriendsRequirement, HelpWantedRequirement, FishingCompetitionRequirement, MovieRequirement, LuauDelightRequirementRequirement, \
    ReceivedRaccoonsRequirement, \
    PrizeMachineRequirement, SpecificFriendRequirement, RegionRequirement, EndgameItemReceivedRequirement, MasteryRequirement, ReceivedRequirement, \
    BachelorFriendRequirement, SeasonRequirement, SpeakJunimoRequirement, FestivalItemReceivedRequirement, MuseumArtifactsRequirement
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
from ...strings.craftable_names import Furniture, Consumable, Fishing, WildSeeds
from ...strings.crop_names import Fruit, Vegetable
from ...strings.currency_names import Currency
from ...strings.fertilizer_names import Fertilizer, RetainingSoil, SpeedGro
from ...strings.festival_check_names import FestivalCheck
from ...strings.fish_names import WaterItem, Fish, Trash
from ...strings.food_names import Beverage, Meal
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.generic_names import Generic
from ...strings.geode_names import Geode
from ...strings.gift_names import Gift
from ...strings.ingredient_names import Ingredient
from ...strings.machine_names import Machine
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar, Ore
from ...strings.monster_names import Monster
from ...strings.region_names import Region, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import Seed, TreeSeed
from ...strings.skill_names import Skill
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

CookingRecipe(name=Meal.algae_soup, ingredients=((WaterItem.green_algae, 4),), sources=(FriendshipSource(friend=NPC.clint, hearts=3),),),
CookingRecipe(name=Meal.artichoke_dip, ingredients=((Vegetable.artichoke, 4), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=28),),),
CookingRecipe(name=Meal.autumn_bounty, ingredients=((Vegetable.yam, 1), (Vegetable.pumpkin, 1),), sources=(FriendshipSource(friend=NPC.demetrius, hearts=7),),),
CookingRecipe(name=Meal.baked_fish, ingredients=((Fish.sunfish, 1), (Fish.bream, 1), (Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=7),),),
# banana_pudding = shop_trade_recipe(Meal.banana_pudding, Region.island_trader, Fossil.bone_fragment, 30, {Fruit.banana: 1, AnimalProduct.cow_milk: 1, Ingredient.sugar: 1}, content_pack=ginger_island_content_pack.name)
CookingRecipe(name=Meal.bean_hotpot, ingredients=((Vegetable.green_bean, 2),), sources=(FriendshipSource(friend=NPC.clint, hearts=7),),),
# blackberry_cobbler_ingredients = {Forageable.blackberry: 2, Ingredient.sugar: 1, Ingredient.wheat_flour: 1}
# blackberry_cobbler_qos = queen_of_sauce_recipe(Meal.blackberry_cobbler, 2, Season.fall, 14, blackberry_cobbler_ingredients)
# blueberry_tart_ingredients = {Fruit.blueberry: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.any_egg: 1}
# blueberry_tart = friendship_recipe(Meal.blueberry_tart, NPC.pierre, 3, blueberry_tart_ingredients)
CookingRecipe(name=Meal.bread, ingredients=((Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=28),),),
CookingRecipe(name=Meal.bruschetta, ingredients=((Meal.bread, 1), (Ingredient.oil, 1), (Vegetable.tomato, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=21),),),
CookingRecipe(name=Meal.carp_surprise, ingredients=((Fish.carp, 4),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=7),),),
CookingRecipe(name=Meal.cheese_cauliflower, ingredients=((Vegetable.cauliflower, 1), (ArtisanGood.cheese, 1),), sources=(FriendshipSource(friend=NPC.pam, hearts=3),),),
# chocolate_cake_ingredients = {Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1}
# chocolate_cake_qos = queen_of_sauce_recipe(Meal.chocolate_cake, 1, Season.winter, 14, chocolate_cake_ingredients)
CookingRecipe(name=Meal.chowder, ingredients=((Fish.clam, 1), (AnimalProduct.cow_milk, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=3),),),
CookingRecipe(name=Meal.coleslaw, ingredients=((Vegetable.red_cabbage, 1), (Ingredient.vinegar, 1), (ArtisanGood.mayonnaise, 1),), sources=(QueenOfSauceSource(year=14, season=Season.spring, day=14),),),
# complete_breakfast_ingredients = {Meal.fried_egg: 1, AnimalProduct.milk: 1, Meal.hashbrowns: 1, Meal.pancakes: 1}
# complete_breakfast = queen_of_sauce_recipe(Meal.complete_breakfast, 2, Season.spring, 21, complete_breakfast_ingredients)
CookingRecipe(name=Meal.cookie, ingredients=((Ingredient.wheat_flour, 1), (Ingredient.sugar, 1), (AnimalProduct.chicken_egg, 1),), sources=(FriendshipSource(friend=NPC.evelyn, hearts=4),),),
# crab_cakes_ingredients = {Fish.crab: 1, Ingredient.wheat_flour: 1, AnimalProduct.chicken_egg: 1, Ingredient.oil: 1}
# crab_cakes_qos = queen_of_sauce_recipe(Meal.crab_cakes, 2, Season.fall, 21, crab_cakes_ingredients)
CookingRecipe(name=Meal.cranberry_candy, ingredients=((Fruit.cranberries, 1), (Fruit.apple, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=28),),),
CookingRecipe(name=Meal.cranberry_sauce, ingredients=((Fruit.cranberries, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.gus, hearts=7),),),
CookingRecipe(name=Meal.crispy_bass, ingredients=((Fish.largemouth_bass, 1), (Ingredient.wheat_flour, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.kent, hearts=3),),),
# dish_o_the_sea = skill_recipe(Meal.dish_o_the_sea, Skill.fishing, 3, {Fish.sardine: 2, Meal.hashbrowns: 1})
CookingRecipe(name=Meal.eggplant_parmesan, ingredients=((Vegetable.eggplant, 1), (Vegetable.tomato, 1),), sources=(FriendshipSource(friend=NPC.lewis, hearts=7),),),
CookingRecipe(name=Meal.escargot, ingredients=((Fish.snail, 1), (Vegetable.garlic, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=5),),),
# farmer_lunch = skill_recipe(Meal.farmer_lunch, Skill.farming, 3, {Meal.omelet: 2, Vegetable.parsnip: 1})
CookingRecipe(name=Meal.fiddlehead_risotto, ingredients=((Ingredient.oil, 1), (Forageable.fiddlehead_fern, 1), (Vegetable.garlic, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=28),),),
CookingRecipe(name=Meal.fish_stew, ingredients=((Fish.crayfish, 1), (Fish.mussel, 1), (Fish.periwinkle, 1), (Vegetable.tomato, 1),), sources=(FriendshipSource(friend=NPC.willy, hearts=7),),),
CookingRecipe(name=Meal.fish_taco, ingredients=((Fish.tuna, 1), (Meal.tortilla, 1), (Vegetable.red_cabbage, 1), (ArtisanGood.mayonnaise, 1),), sources=(FriendshipSource(friend=NPC.linus, hearts=7),),),
CookingRecipe(name=Meal.fried_calamari, ingredients=((Fish.squid, 1), (Ingredient.wheat_flour, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.jodi, hearts=3),),),
CookingRecipe(name=Meal.fried_eel, ingredients=((Fish.eel, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.george, hearts=3),),),
# fried_egg = starter_recipe(Meal.fried_egg, {AnimalProduct.chicken_egg: 1})
CookingRecipe(name=Meal.fried_mushroom, ingredients=((Mushroom.common, 1), (Mushroom.morel, 1), (Ingredient.oil, 1),), sources=(FriendshipSource(friend=NPC.demetrius, hearts=3),),),
CookingRecipe(name=Meal.fruit_salad, ingredients=((Fruit.blueberry, 1), (Fruit.melon, 1), (Fruit.apricot, 1),), sources=(QueenOfSauceSource(year=2, season=Season.fall, day=7),),),
# ginger_ale = shop_recipe(Beverage.ginger_ale, Region.volcano_dwarf_shop, 1000, {Forageable.ginger: 3, Ingredient.sugar: 1}, content_pack=ginger_island_content_pack.name)
CookingRecipe(name=Meal.glazed_yams, ingredients=((Vegetable.yam, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=21),),),
CookingRecipe(name=Meal.hashbrowns, ingredients=((Vegetable.potato, 1), (Ingredient.oil, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=14),),),
CookingRecipe(name=Meal.ice_cream, ingredients=((AnimalProduct.cow_milk, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.jodi, hearts=7),),),
# lobster_bisque_ingredients = {Fish.lobster: 1, AnimalProduct.cow_milk: 1}
# lobster_bisque_friend = friendship_recipe(Meal.lobster_bisque, NPC.willy, 9, lobster_bisque_ingredients)
# lobster_bisque_qos = queen_of_sauce_recipe(Meal.lobster_bisque, 2, Season.winter, 14, lobster_bisque_ingredients)
CookingRecipe(name=Meal.lucky_lunch, ingredients=((Fish.sea_cucumber, 1), (Meal.tortilla, 1), (Flower.blue_jazz, 1),), sources=(QueenOfSauceSource(year=2, season=Season.spring, day=28),),),
CookingRecipe(name=Meal.maki_roll, ingredients=((Fish.any, 1), (WaterItem.seaweed, 1), (Ingredient.rice, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=21),),),
# mango_sticky_rice = friendship_recipe(Meal.mango_sticky_rice, NPC.leo, 7, {Fruit.mango: 1, Forageable.coconut: 1, Ingredient.rice: 1}, content_pack=ginger_island_content_pack.name)
CookingRecipe(name=Meal.maple_bar, ingredients=((ArtisanGood.maple_syrup, 1), (Ingredient.sugar, 1), (Ingredient.wheat_flour, 1),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=14),),),
# miners_treat = skill_recipe(Meal.miners_treat, Skill.mining, 3, {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1})
# moss_soup = skill_recipe(Meal.moss_soup, Skill.foraging, 3, {Material.moss: 20})
CookingRecipe(name=Meal.omelet, ingredients=((AnimalProduct.chicken_egg, 1), (AnimalProduct.cow_milk, 1),), sources=(QueenOfSauceSource(year=1, season=Season.spring, day=28),),),
CookingRecipe(name=Meal.pale_broth, ingredients=((WaterItem.white_algae, 2),), sources=(FriendshipSource(friend=NPC.marnie, hearts=3),),),
CookingRecipe(name=Meal.pancakes, ingredients=((Ingredient.wheat_flour, 1), (AnimalProduct.chicken_egg, 1),), sources=(QueenOfSauceSource(year=1, season=Season.summer, day=14),),),
CookingRecipe(name=Meal.parsnip_soup, ingredients=((Vegetable.parsnip, 1), (AnimalProduct.cow_milk, 1), (Ingredient.vinegar, 1),), sources=(FriendshipSource(friend=NPC.caroline, hearts=3),),),
CookingRecipe(name=Meal.pepper_poppers, ingredients=((Fruit.hot_pepper, 1), (ArtisanGood.cheese, 1),), sources=(FriendshipSource(friend=NPC.shane, hearts=3),),),
# pink_cake_ingredients = {Fruit.melon: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1}
# pink_cake_qos = queen_of_sauce_recipe(Meal.pink_cake, 2, Season.summer, 21, pink_cake_ingredients)
# pizza_ingredients = {Ingredient.wheat_flour: 1, Vegetable.tomato: 1, ArtisanGood.cheese: 1}
# pizza_qos = queen_of_sauce_recipe(Meal.pizza, 2, Season.spring, 7, pizza_ingredients)
# pizza_saloon = shop_recipe(Meal.pizza, Region.saloon, 150, pizza_ingredients)
CookingRecipe(name=Meal.plum_pudding, ingredients=((Forageable.wild_plum, 2), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=1, season=Season.winter, day=7),),),
# poi = friendship_recipe(Meal.poi, NPC.leo, 3, {Vegetable.taro_root: 4}, content_pack=ginger_island_content_pack.name)
CookingRecipe(name=Meal.poppyseed_muffin, ingredients=((Flower.poppy, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=7),),),
# pumpkin_pie_ingredients = {Vegetable.pumpkin: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1}
# pumpkin_pie_qos = queen_of_sauce_recipe(Meal.pumpkin_pie, 1, Season.winter, 21, pumpkin_pie_ingredients)
CookingRecipe(name=Meal.pumpkin_soup, ingredients=((Vegetable.pumpkin, 1), (AnimalProduct.cow_milk, 1),), sources=(FriendshipSource(friend=NPC.robin, hearts=7),),),
CookingRecipe(name=Meal.radish_salad, ingredients=((Ingredient.oil, 1), (Ingredient.vinegar, 1), (Vegetable.radish, 1),), sources=(QueenOfSauceSource(year=1, season=Season.spring, day=21),),),
CookingRecipe(name=Meal.red_plate, ingredients=((Vegetable.red_cabbage, 1), (Vegetable.radish, 1),), sources=(FriendshipSource(friend=NPC.emily, hearts=7),),),
CookingRecipe(name=Meal.rhubarb_pie, ingredients=((Fruit.rhubarb, 1), (Ingredient.wheat_flour, 1), (Ingredient.sugar, 1),), sources=(FriendshipSource(friend=NPC.marnie, hearts=7),),),
CookingRecipe(name=Meal.rice_pudding, ingredients=((AnimalProduct.milk, 1), (Ingredient.sugar, 1), (Ingredient.rice, 1),), sources=(FriendshipSource(friend=NPC.evelyn, hearts=7),),),
CookingRecipe(name=Meal.roasted_hazelnuts, ingredients=((Forageable.hazelnut, 3),), sources=(QueenOfSauceSource(year=2, season=Season.summer, day=28),),),
# roots_platter = skill_recipe(Meal.roots_platter, Skill.combat, 3, {Forageable.cave_carrot: 1, Forageable.winter_root: 1})
CookingRecipe(name=Meal.salad, ingredients=((Forageable.leek, 1), (Forageable.dandelion, 1), (Ingredient.vinegar, 1),), sources=(FriendshipSource(friend=NPC.emily, hearts=3),),),
CookingRecipe(name=Meal.salmon_dinner, ingredients=((Fish.salmon, 1), (Vegetable.amaranth, 1), (Vegetable.kale, 1),), sources=(FriendshipSource(friend=NPC.gus, hearts=3),),),
CookingRecipe(name=Meal.sashimi, ingredients=((Fish.any, 1),), sources=(FriendshipSource(friend=NPC.linus, hearts=3),),),
# seafoam_pudding = skill_recipe(Meal.seafoam_pudding, Skill.fishing, 9, {Fish.flounder: 1, Fish.midnight_carp: 1, AnimalProduct.squid_ink: 1})
CookingRecipe(name=Meal.shrimp_cocktail, ingredients=((Vegetable.tomato, 1), (Fish.shrimp, 1), (Forageable.wild_horseradish, 1),), sources=(QueenOfSauceSource(year=2, season=Season.winter, day=28),),),
CookingRecipe(name=Meal.spaghetti, ingredients=((Vegetable.tomato, 1), (Ingredient.wheat_flour, 1),), sources=(FriendshipSource(friend=NPC.lewis, hearts=3),),),
CookingRecipe(name=Meal.spicy_eel, ingredients=((Fish.eel, 1), (Fruit.hot_pepper, 1),), sources=(FriendshipSource(friend=NPC.george, hearts=7),),),
# squid_ink_ravioli = skill_recipe(Meal.squid_ink_ravioli, Skill.combat, 9, {AnimalProduct.squid_ink: 1, Ingredient.wheat_flour: 1, Vegetable.tomato: 1})
# stir_fry_ingredients = {Forageable.cave_carrot: 1, Mushroom.common: 1, Vegetable.kale: 1, Ingredient.sugar: 1}
# stir_fry_qos = queen_of_sauce_recipe(Meal.stir_fry, 1, Season.spring, 7, stir_fry_ingredients)
CookingRecipe(name=Meal.strange_bun, ingredients=((Ingredient.wheat_flour, 1), (Fish.periwinkle, 1), (ArtisanGood.void_mayonnaise, 1),), sources=(FriendshipSource(friend=NPC.shane, hearts=7),),),
CookingRecipe(name=Meal.stuffing, ingredients=((Meal.bread, 1), (Fruit.cranberries, 1), (Forageable.hazelnut, 1),), sources=(FriendshipSource(friend=NPC.pam, hearts=7),),),
CookingRecipe(name=Meal.super_meal, ingredients=((Vegetable.bok_choy, 1), (Fruit.cranberries, 1), (Vegetable.artichoke, 1),), sources=(FriendshipSource(friend=NPC.kent, hearts=7),),),
#
# survival_burger = skill_recipe(Meal.survival_burger, Skill.foraging, 8, {Meal.bread: 1, Forageable.cave_carrot: 1, Vegetable.eggplant: 1})
CookingRecipe(name=Meal.tom_kha_soup, ingredients=((Forageable.coconut, 1), (Fish.shrimp, 1), (Mushroom.common, 1),), sources=(FriendshipSource(friend=NPC.sandy, hearts=7),),),
# tortilla_ingredients = {Vegetable.corn: 1}
# tortilla_qos = queen_of_sauce_recipe(Meal.tortilla, 1, Season.fall, 7, tortilla_ingredients)
# tortilla_saloon = shop_recipe(Meal.tortilla, Region.saloon, 100, tortilla_ingredients)
# triple_shot_espresso = shop_recipe(Beverage.triple_shot_espresso, Region.saloon, 5000, {Beverage.coffee: 3})
# tropical_curry = shop_recipe(Meal.tropical_curry, Region.island_resort, 2000, {Forageable.coconut: 1, Fruit.pineapple: 1, Fruit.hot_pepper: 1}, content_pack=ginger_island_content_pack.name)
CookingRecipe(name=Meal.trout_soup, ingredients=((Fish.rainbow_trout, 1), (WaterItem.green_algae, 1),), sources=(QueenOfSauceSource(year=1, season=Season.fall, day=14),),),
CookingRecipe(name=Meal.vegetable_medley, ingredients=((Vegetable.tomato, 1), (Vegetable.beet, 1),), sources=(FriendshipSource(friend=NPC.caroline, hearts=7),),),
#
# magic_elixir = shop_recipe(ModEdible.magic_elixir, Region.adventurer_guild, 3000, {Edible.life_elixir: 1, Mushroom.purple: 1}, content_pack=ModNames.magic)
#
# baked_berry_oatmeal = shop_recipe(SVEMeal.baked_berry_oatmeal, SVERegion.bear_shop, 0, {Forageable.salmonberry: 15, Forageable.blackberry: 15, Ingredient.sugar: 1, Ingredient.wheat_flour: 2}, content_pack=ModNames.sve)
# big_bark_burger = friendship_and_shop_recipe(SVEMeal.big_bark_burger, NPC.gus, 5, Region.saloon, 5500, {SVEFish.puppyfish: 1, Meal.bread: 1, Ingredient.oil: 1}, content_pack=ModNames.sve)
# flower_cookie = shop_recipe(SVEMeal.flower_cookie, SVERegion.bear_shop, 0, {SVEForage.ferngill_primrose: 1, SVEForage.goldenrod: 1, SVEForage.winter_star_rose: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.large_egg: 1}, content_pack=ModNames.sve)
# frog_legs = shop_recipe(SVEMeal.frog_legs, Region.adventurer_guild, 2000, {SVEFish.frog: 1, Ingredient.oil: 1, Ingredient.wheat_flour: 1}, content_pack=ModNames.sve)
# glazed_butterfish = friendship_and_shop_recipe(SVEMeal.glazed_butterfish, NPC.gus, 10, Region.saloon, 4000, {SVEFish.butterfish: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1}, content_pack=ModNames.sve)
# mixed_berry_pie = shop_recipe(SVEMeal.mixed_berry_pie, Region.saloon, 3500, {Fruit.strawberry: 6, SVEFruit.salal_berry: 6, Forageable.blackberry: 6, SVEForage.bearberry: 6, Ingredient.sugar: 1, Ingredient.wheat_flour: 1}, content_pack=ModNames.sve)
# mushroom_berry_rice = friendship_and_shop_recipe(SVEMeal.mushroom_berry_rice, ModNPC.marlon, 6, Region.adventurer_guild, 1500, {SVEForage.poison_mushroom: 3, SVEForage.red_baneberry: 10, Ingredient.rice: 1, Ingredient.sugar: 2}, content_pack=ModNames.sve)
# seaweed_salad = shop_recipe(SVEMeal.seaweed_salad, Region.fish_shop, 1250, {SVEWaterItem.dulse_seaweed: 2, WaterItem.seaweed: 2, Ingredient.oil: 1}, content_pack=ModNames.sve)
# void_delight = friendship_and_shop_recipe(SVEMeal.void_delight, NPC.krobus, 10, Region.sewer, 5000, {SVEFish.void_eel: 1, Loot.void_essence: 50, Loot.solar_essence: 20}, content_pack=ModNames.sve)
# void_salmon_sushi = friendship_and_shop_recipe(SVEMeal.void_salmon_sushi, NPC.krobus, 10, Region.sewer, 5000, {Fish.void_salmon: 1, ArtisanGood.void_mayonnaise: 1, WaterItem.seaweed: 3}, content_pack=ModNames.sve)
#
# mushroom_kebab = friendship_recipe(DistantLandsMeal.mushroom_kebab, ModNPC.goblin, 2, {Mushroom.chanterelle: 1, Mushroom.common: 1, Mushroom.red: 1, Material.wood: 1}, content_pack=ModNames.distant_lands)
# void_mint_tea = friendship_recipe(DistantLandsMeal.void_mint_tea, ModNPC.goblin, 4, {DistantLandsCrop.void_mint: 1}, content_pack=ModNames.distant_lands)
# crayfish_soup = friendship_recipe(DistantLandsMeal.crayfish_soup, ModNPC.goblin, 6, {Forageable.cave_carrot: 1, Fish.crayfish: 1, DistantLandsFish.purple_algae: 1, WaterItem.white_algae: 1}, content_pack=ModNames.distant_lands)
# pemmican = friendship_recipe(DistantLandsMeal.pemmican, ModNPC.goblin, 8, {Loot.bug_meat: 1, Fish.any: 1, Forageable.salmonberry: 3, Material.stone: 2}, content_pack=ModNames.distant_lands)
#
# special_pumpkin_soup = friendship_recipe(BoardingHouseMeal.special_pumpkin_soup, ModNPC.joel, 6, {Vegetable.pumpkin: 2, AnimalProduct.large_goat_milk: 1, Vegetable.garlic: 1}, content_pack=ModNames.boarding_house)
# diggers_delight = skill_recipe(ArchaeologyMeal.diggers_delight, ModSkill.archaeology, 3, {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.milk: 1}, content_pack=ModNames.archaeology)
# rocky_root = skill_recipe(ArchaeologyMeal.rocky_root, ModSkill.archaeology, 7, {Forageable.cave_carrot: 3, Seed.coffee: 1, Material.stone: 1}, content_pack=ModNames.archaeology)
# ancient_jello = skill_recipe(ArchaeologyMeal.ancient_jello, ModSkill.archaeology, 9, {WaterItem.cave_jelly: 6, Ingredient.sugar: 5, AnimalProduct.egg: 1, AnimalProduct.milk: 1, Artifact.chipped_amphora: 1}, content_pack=ModNames.archaeology)
#
# grilled_cheese = skill_recipe(TrashyMeal.grilled_cheese, ModSkill.binning, 1, {Meal.bread: 1, ArtisanGood.cheese: 1}, content_pack=ModNames.binning_skill)
# fish_casserole = skill_recipe(TrashyMeal.fish_casserole, ModSkill.binning, 8, {Fish.any: 1, AnimalProduct.milk: 1, Vegetable.carrot: 1}, content_pack=ModNames.binning_skill)
    ),
)
