from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ..override import override
from ..vanilla.ginger_island import ginger_island_content_pack as ginger_island_content_pack
from ...data import villagers_data, fish_data
from ...data.game_item import ItemTag, Tag
from ...data.harvest import ForagingSource, HarvestCropSource
from ...data.requirement import YearRequirement, CombatRequirement, RelationshipRequirement, ToolRequirement, SkillRequirement, FishingRequirement
from ...data.shop import ShopSource
from ...mods.mod_data import ModNames
from ...strings.craftable_names import ModEdible
from ...strings.crop_names import Fruit, SVEVegetable, SVEFruit
from ...strings.fish_names import WaterItem, SVEFish, SVEWaterItem
from ...strings.flower_names import Flower
from ...strings.food_names import SVEMeal, SVEBeverage
from ...strings.forageable_names import Mushroom, Forageable, SVEForage
from ...strings.gift_names import SVEGift
from ...strings.metal_names import Ore
from ...strings.monster_drop_names import ModLoot, Loot
from ...strings.performance_names import Performance
from ...strings.region_names import Region, SVERegion, LogicRegion
from ...strings.season_names import Season
from ...strings.seed_names import SVESeed
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import ModNPC


class SVEContentPack(ContentPack):

    def fish_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            content.fishes.pop(fish_data.baby_lunaloo.name)
            content.fishes.pop(fish_data.clownfish.name)
            content.fishes.pop(fish_data.lunaloo.name)
            content.fishes.pop(fish_data.seahorse.name)
            content.fishes.pop(fish_data.shiny_lunaloo.name)
            content.fishes.pop(fish_data.starfish.name)
            content.fishes.pop(fish_data.sea_sponge.name)

            # Remove Highlands fishes at it requires 2 Lance hearts for the quest to access it
            content.fishes.pop(fish_data.daggerfish.name)
            content.fishes.pop(fish_data.gemfish.name)

            # Remove Fable Reef fishes at it requires 8 Lance hearts for the event to access it
            content.fishes.pop(fish_data.torpedo_trout.name)

    def villager_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            # Remove Lance if Ginger Island is not in content since he is first encountered in Volcano Forge
            content.villagers.pop(villagers_data.lance.name)

    def harvest_source_hook(self, content: StardewContent):
        content.untag_item(SVESeed.shrub, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.fungus, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.slime, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.stalk, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.void, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.ancient_fern, tag=ItemTag.CROPSANITY_SEED)
        if ginger_island_content_pack.name not in content.registered_packs:
            # Remove Highlands seeds as these are behind Lance existing.
            content.game_items.pop(SVESeed.void)
            content.game_items.pop(SVEVegetable.void_root)
            content.game_items.pop(SVESeed.stalk)
            content.game_items.pop(SVEFruit.monster_fruit)
            content.game_items.pop(SVESeed.fungus)
            content.game_items.pop(SVEVegetable.monster_mushroom)
            content.game_items.pop(SVESeed.slime)
            content.game_items.pop(SVEFruit.slime_berry)


register_mod_content_pack(SVEContentPack(
    ModNames.sve,
    weak_dependencies=(
        ginger_island_content_pack.name,
        ModNames.jasper,  # To override Marlon and Gunther
    ),
    shop_sources={
        SVEGift.aged_blue_moon_wine: (ShopSource(money_price=28000, shop_region=SVERegion.blue_moon_vineyard),),
        SVEGift.blue_moon_wine: (ShopSource(money_price=3000, shop_region=SVERegion.blue_moon_vineyard),),
        ModEdible.lightning_elixir: (ShopSource(money_price=12000, shop_region=SVERegion.galmoran_outpost),),
        ModEdible.barbarian_elixir: (ShopSource(money_price=22000, shop_region=SVERegion.galmoran_outpost),),
        ModEdible.gravity_elixir: (ShopSource(money_price=4000, shop_region=SVERegion.galmoran_outpost),),
        SVEMeal.grampleton_orange_chicken: (ShopSource(money_price=650, shop_region=Region.saloon, other_requirements=(RelationshipRequirement(ModNPC.sophia, 6),)),),
        ModEdible.hero_elixir: (ShopSource(money_price=8000, shop_region=SVERegion.isaac_shop),),
        ModEdible.aegis_elixir: (ShopSource(money_price=28000, shop_region=SVERegion.galmoran_outpost),),
        SVEBeverage.sports_drink: (ShopSource(money_price=750, shop_region=Region.hospital),),
        SVEMeal.stamina_capsule: (ShopSource(money_price=4000, shop_region=Region.hospital),),
    },
    harvest_sources={
        Mushroom.red: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.summer, Season.fall)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.purple: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave, SVERegion.junimo_woods), )
        ),
        Mushroom.morel: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.chanterelle: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Flower.tulip: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.blue_jazz: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.summer_spangle: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.sunflower: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.fairy_rose: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.fall,)),),
        Fruit.ancient_fruit: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=Season.not_winter, other_requirements=(YearRequirement(3),)),
            ForagingSource(regions=(SVERegion.sprite_spring_cave,)),
        ),
        Fruit.sweet_gem_berry: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=Season.not_winter, other_requirements=(YearRequirement(3),)),
        ),

        # New items

        ModLoot.green_mushroom: (ForagingSource(regions=(SVERegion.highlands_pond,), seasons=Season.not_winter),),
        ModLoot.ornate_treasure_chest: (ForagingSource(regions=(SVERegion.highlands_outside,),
                                                       other_requirements=(CombatRequirement(Performance.galaxy), ToolRequirement(Tool.axe, ToolMaterial.iron))),),
        ModLoot.swirl_stone: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.galaxy),)),),
        ModLoot.void_soul: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEForage.winter_star_rose: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.winter,)),),
        SVEForage.bearberry: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.winter,)),),
        SVEForage.poison_mushroom: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.summer, Season.fall)),),
        SVEForage.red_baneberry: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.summer, Season.summer)),),
        SVEForage.ferngill_primrose: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.spring,)),),
        SVEForage.goldenrod: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.summer, Season.fall)),),
        SVEForage.conch: (ForagingSource(regions=(Region.beach, SVERegion.fable_reef,)),),
        SVEForage.dewdrop_berry: (ForagingSource(regions=(SVERegion.enchanted_grove,)),),
        SVEForage.sand_dollar: (ForagingSource(regions=(Region.beach, SVERegion.fable_reef,), seasons=(Season.spring, Season.summer)),),
        SVEForage.golden_ocean_flower: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        SVEForage.four_leaf_clover: (ForagingSource(regions=(Region.secret_woods, SVERegion.forest_west,), seasons=(Season.summer, Season.fall)),),
        SVEForage.mushroom_colony: (ForagingSource(regions=(Region.secret_woods, SVERegion.junimo_woods, SVERegion.forest_west,), seasons=(Season.fall,)),),
        SVEForage.rusty_blade: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.great),)),),
        SVEForage.rafflesia: (ForagingSource(regions=(Region.secret_woods,), seasons=Season.not_winter),),
        SVEForage.thistle: (ForagingSource(regions=(SVERegion.summit,)),),
        ModLoot.void_pebble: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.great),)),),
        ModLoot.void_shard: (ForagingSource(regions=(SVERegion.crimson_badlands,),
                                            other_requirements=(CombatRequirement(Performance.galaxy), SkillRequirement(Skill.combat, 10), YearRequirement(3),)),),
        SVEWaterItem.dulse_seaweed: (ForagingSource(regions=(Region.beach,), other_requirements=(FishingRequirement(Region.beach),)),),

        # Fable Reef
        WaterItem.coral: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        Forageable.rainbow_shell: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        WaterItem.sea_urchin: (ForagingSource(regions=(SVERegion.fable_reef,)),),

        # Crops
        SVESeed.shrub: (ForagingSource(regions=(Region.secret_woods,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.salal_berry: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.shrub, seasons=(Season.spring,)),),
        SVESeed.slime: (ForagingSource(regions=(SVERegion.highlands_outside,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.slime_berry: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.slime, seasons=(Season.spring,)),),
        SVESeed.ancient_fern: (ForagingSource(regions=(Region.secret_woods,)),),
        SVEVegetable.ancient_fiber: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.ancient_fern, seasons=(Season.summer,)),),
        SVESeed.stalk: (ForagingSource(regions=(SVERegion.highlands_outside,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.monster_fruit: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.stalk, seasons=(Season.summer,)),),
        SVESeed.fungus: (ForagingSource(regions=(SVERegion.highlands_pond,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEVegetable.monster_mushroom: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.fungus, seasons=(Season.fall,)),),
        SVESeed.void: (ForagingSource(regions=(SVERegion.highlands_cavern,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEVegetable.void_root: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.void, seasons=(Season.winter,)),),

    },
    fishes=(
        fish_data.baby_lunaloo,  # Removed when no ginger island
        fish_data.bonefish,
        fish_data.bull_trout,
        fish_data.butterfish,
        fish_data.clownfish,  # Removed when no ginger island
        fish_data.daggerfish,
        fish_data.frog,
        fish_data.gemfish,
        fish_data.goldenfish,
        fish_data.grass_carp,
        fish_data.king_salmon,
        fish_data.kittyfish,
        fish_data.lunaloo,  # Removed when no ginger island
        fish_data.meteor_carp,
        fish_data.minnow,
        fish_data.puppyfish,
        fish_data.radioactive_bass,
        fish_data.seahorse,  # Removed when no ginger island
        fish_data.shiny_lunaloo,  # Removed when no ginger island
        fish_data.snatcher_worm,
        fish_data.starfish,  # Removed when no ginger island
        fish_data.torpedo_trout,
        fish_data.undeadfish,
        fish_data.void_eel,
        fish_data.water_grub,
        fish_data.sea_sponge,  # Removed when no ginger island

    ),
    villagers=(
        villagers_data.claire,
        villagers_data.lance,  # Removed when no ginger island
        villagers_data.mommy,
        villagers_data.sophia,
        villagers_data.victor,
        villagers_data.andy,
        villagers_data.apples,
        villagers_data.gunther,
        villagers_data.martin,
        villagers_data.marlon,
        villagers_data.morgan,
        villagers_data.scarlett,
        villagers_data.susan,
        villagers_data.morris,
        # The wizard leaves his tower on sunday, for like 1 hour... Good enough for entrance rando!
        override(villagers_data.wizard, locations=(Region.wizard_tower, Region.forest), bachelor=True, mod_name=ModNames.sve),
    )
))
