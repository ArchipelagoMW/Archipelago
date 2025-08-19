import itertools
import logging
from typing import List, Dict, Set

from BaseClasses import MultiWorld, CollectionState
from worlds.generic.Rules import set_rule
from . import locations
from .bundles.bundle_room import BundleRoom
from .content import StardewContent
from .content.feature import friendsanity
from .data.craftable_data import all_crafting_recipes_by_name
from .data.game_item import ItemTag
from .data.harvest import HarvestCropSource, HarvestFruitTreeSource
from .data.museum_data import all_museum_items, dwarf_scrolls, skeleton_front, skeleton_middle, skeleton_back, all_museum_items_by_name, all_museum_minerals, \
    all_museum_artifacts, Artifact
from .data.recipe_data import all_cooking_recipes_by_name
from .locations import LocationTags
from .logic.logic import StardewLogic
from .logic.time_logic import MAX_MONTHS
from .logic.tool_logic import tool_upgrade_prices
from .mods.mod_data import ModNames
from .options import ExcludeGingerIsland, SpecialOrderLocations, Museumsanity, BackpackProgression, Shipsanity, \
    Monstersanity, Chefsanity, Craftsanity, ArcadeMachineLocations, Cooksanity, StardewValleyOptions, Walnutsanity
from .stardew_rule import And, StardewRule, true_
from .stardew_rule.indirect_connection import look_for_indirect_connection
from .stardew_rule.rule_explain import explain
from .strings.ap_names.ap_option_names import WalnutsanityOptionName
from .strings.ap_names.community_upgrade_names import CommunityUpgrade
from .strings.ap_names.mods.mod_items import SVEQuestItem, SVERunes
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.building_names import Building
from .strings.bundle_names import CCRoom
from .strings.calendar_names import Weekday
from .strings.craftable_names import Bomb, Furniture
from .strings.crop_names import Fruit, Vegetable
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, DeepWoodsEntrance, AlecEntrance, \
    SVEEntrance, LaceyEntrance, BoardingHouseEntrance, LogicEntrance
from .strings.forageable_names import Forageable
from .strings.generic_names import Generic
from .strings.geode_names import Geode
from .strings.material_names import Material
from .strings.metal_names import MetalBar, Mineral
from .strings.monster_names import Monster
from .strings.performance_names import Performance
from .strings.quest_names import Quest
from .strings.region_names import Region
from .strings.season_names import Season
from .strings.skill_names import Skill
from .strings.tool_names import Tool, ToolMaterial
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet

logger = logging.getLogger(__name__)


def set_rules(world):
    multiworld = world.multiworld
    world_options = world.options
    world_content = world.content
    player = world.player
    logic = world.logic
    bundle_rooms: List[BundleRoom] = world.modified_bundles

    all_location_names = set(location.name for location in multiworld.get_locations(player))

    set_entrance_rules(logic, multiworld, player, world_options)
    set_ginger_island_rules(logic, multiworld, player, world_options)

    set_tool_rules(logic, multiworld, player, world_content)
    set_skills_rules(logic, multiworld, player, world_content)
    set_bundle_rules(bundle_rooms, logic, multiworld, player, world_options)
    set_building_rules(logic, multiworld, player, world_content)
    set_cropsanity_rules(logic, multiworld, player, world_content)
    set_story_quests_rules(all_location_names, logic, multiworld, player, world_options)
    set_special_order_rules(all_location_names, logic, multiworld, player, world_options)
    set_help_wanted_quests_rules(logic, multiworld, player, world_options)
    set_fishsanity_rules(all_location_names, logic, multiworld, player)
    set_museumsanity_rules(all_location_names, logic, multiworld, player, world_options)

    set_friendsanity_rules(logic, multiworld, player, world_content)
    set_backpack_rules(logic, multiworld, player, world_options)
    set_festival_rules(all_location_names, logic, multiworld, player)
    set_monstersanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_shipsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_cooksanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_chefsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_craftsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_booksanity_rules(logic, multiworld, player, world_content)
    set_isolated_locations_rules(logic, multiworld, player)
    set_traveling_merchant_day_rules(logic, multiworld, player)
    set_arcade_machine_rules(logic, multiworld, player, world_options)

    set_deepwoods_rules(logic, multiworld, player, world_options)
    set_magic_spell_rules(logic, multiworld, player, world_options)
    set_sve_rules(logic, multiworld, player, world_options)


def set_isolated_locations_rules(logic: StardewLogic, multiworld, player):
    set_rule(multiworld.get_location("Old Master Cannoli", player),
             logic.has(Fruit.sweet_gem_berry))
    set_rule(multiworld.get_location("Galaxy Sword Shrine", player),
             logic.has("Prismatic Shard"))
    set_rule(multiworld.get_location("Krobus Stardrop", player),
             logic.money.can_spend(20000))
    set_rule(multiworld.get_location("Demetrius's Breakthrough", player),
             logic.money.can_have_earned_total(25000))
    set_rule(multiworld.get_location("Pot Of Gold", player),
             logic.season.has(Season.spring))


def set_tool_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    if not content.features.tool_progression.is_progressive:
        return

    set_rule(multiworld.get_location("Purchase Fiberglass Rod", player),
             (logic.skill.has_level(Skill.fishing, 2) & logic.money.can_spend(1800)))
    set_rule(multiworld.get_location("Purchase Iridium Rod", player),
             (logic.skill.has_level(Skill.fishing, 6) & logic.money.can_spend(7500)))

    set_rule(multiworld.get_location("Copper Pan Cutscene", player), logic.received("Glittering Boulder Removed"))

    materials = [None, "Copper", "Iron", "Gold", "Iridium"]
    tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.trash_can, Tool.pan]
    for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
        if previous is None:
            continue
        tool_upgrade_location = multiworld.get_location(f"{material} {tool} Upgrade", player)
        set_rule(tool_upgrade_location, logic.tool.has_tool(tool, previous))


def set_building_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        if building.name in building_progression.starting_buildings:
            continue

        location_name = building_progression.to_location_name(building.name)

        set_rule(multiworld.get_location(location_name, player),
                 logic.building.can_build(building.name))


def set_bundle_rules(bundle_rooms: List[BundleRoom], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    for bundle_room in bundle_rooms:
        room_rules = []
        for bundle in bundle_room.bundles:
            location = multiworld.get_location(bundle.name, player)
            bundle_rules = logic.bundle.can_complete_bundle(bundle)
            if bundle_room.name == CCRoom.raccoon_requests:
                num = int(bundle.name[-1])
                extra_raccoons = 1 if world_options.quest_locations.has_story_quests() else 0
                extra_raccoons = extra_raccoons + num
                bundle_rules = logic.received(CommunityUpgrade.raccoon, extra_raccoons) & bundle_rules
                if num > 1:
                    previous_bundle_name = f"Raccoon Request {num - 1}"
                    bundle_rules = bundle_rules & logic.region.can_reach_location(previous_bundle_name)
            room_rules.append(bundle_rules)
            set_rule(location, bundle_rules)
        if bundle_room.name == CCRoom.abandoned_joja_mart or bundle_room.name == CCRoom.raccoon_requests:
            continue
        room_location = f"Complete {bundle_room.name}"
        set_rule(multiworld.get_location(room_location, player), And(*room_rules))


def set_skills_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    skill_progression = content.features.skill_progression
    if not skill_progression.is_progressive:
        return

    for skill in content.skills.values():
        for level, level_name in skill_progression.get_randomized_level_names_by_level(skill):
            rule = logic.skill.can_earn_level(skill.name, level)
            location = multiworld.get_location(level_name, player)
            set_rule(location, rule)

        if skill_progression.is_mastery_randomized(skill):
            rule = logic.skill.can_earn_mastery(skill.name)
            location = multiworld.get_location(skill.mastery_name, player)
            set_rule(location, rule)


def set_entrance_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    set_mines_floor_entrance_rules(logic, multiworld, player)
    set_skull_cavern_floor_entrance_rules(logic, multiworld, player)
    set_blacksmith_entrance_rules(logic, multiworld, player)
    set_skill_entrance_rules(logic, multiworld, player, world_options)
    set_traveling_merchant_day_rules(logic, multiworld, player)
    set_dangerous_mine_rules(logic, multiworld, player, world_options)

    set_entrance_rule(multiworld, player, Entrance.enter_tide_pools, logic.received("Beach Bridge") | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_quarry, logic.received("Bridge Repair") | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_secret_woods, logic.tool.has_tool(Tool.axe, "Iron") | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.forest_to_wizard_tower, logic.region.can_reach(Region.community_center))
    set_entrance_rule(multiworld, player, Entrance.forest_to_sewer, logic.wallet.has_rusty_key())
    set_entrance_rule(multiworld, player, Entrance.town_to_sewer, logic.wallet.has_rusty_key())
    set_entrance_rule(multiworld, player, Entrance.enter_abandoned_jojamart, logic.has_abandoned_jojamart())
    movie_theater_rule = logic.has_movie_theater()
    set_entrance_rule(multiworld, player, Entrance.enter_movie_theater, movie_theater_rule)
    set_entrance_rule(multiworld, player, Entrance.purchase_movie_ticket, movie_theater_rule)
    set_entrance_rule(multiworld, player, Entrance.take_bus_to_desert, logic.received("Bus Repair") & logic.money.can_spend(500))
    set_entrance_rule(multiworld, player, Entrance.enter_skull_cavern, logic.received(Wallet.skull_key))
    set_entrance_rule(multiworld, player, LogicEntrance.talk_to_mines_dwarf,
                      logic.wallet.can_speak_dwarf() & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, LogicEntrance.buy_from_traveling_merchant, logic.traveling_merchant.has_days())
    set_entrance_rule(multiworld, player, LogicEntrance.buy_from_raccoon, logic.quest.has_raccoon_shop())
    set_entrance_rule(multiworld, player, LogicEntrance.fish_in_waterfall,
                      logic.skill.has_level(Skill.fishing, 5) & logic.tool.has_fishing_rod(2))

    set_farm_buildings_entrance_rules(logic, multiworld, player)

    set_entrance_rule(multiworld, player, Entrance.mountain_to_railroad, logic.received("Railroad Boulder Removed"))
    set_entrance_rule(multiworld, player, Entrance.enter_witch_warp_cave, logic.quest.has_dark_talisman() | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_witch_hut, (logic.quest.can_complete_quest(Quest.goblin_problem) | logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_mutant_bug_lair,
                      (logic.wallet.has_rusty_key() & logic.region.can_reach(Region.railroad) & logic.relationship.can_meet(
                          NPC.krobus)) | logic.mod.magic.can_blink())
    set_entrance_rule(multiworld, player, Entrance.enter_casino, logic.quest.has_club_card())

    set_bedroom_entrance_rules(logic, multiworld, player, world_options)
    set_festival_entrance_rules(logic, multiworld, player)
    set_island_entrance_rule(multiworld, player, LogicEntrance.island_cooking, logic.cooking.can_cook_in_kitchen, world_options)
    set_entrance_rule(multiworld, player, LogicEntrance.farmhouse_cooking, logic.cooking.can_cook_in_kitchen)
    set_entrance_rule(multiworld, player, LogicEntrance.shipping, logic.shipping.can_use_shipping_bin)
    set_entrance_rule(multiworld, player, LogicEntrance.watch_queen_of_sauce, logic.action.can_watch(Channel.queen_of_sauce))
    set_entrance_rule(multiworld, player, Entrance.forest_to_mastery_cave, logic.skill.can_enter_mastery_cave)
    set_entrance_rule(multiworld, player, LogicEntrance.buy_experience_books, logic.time.has_lived_months(2))
    set_entrance_rule(multiworld, player, LogicEntrance.buy_year1_books, logic.time.has_year_two)
    set_entrance_rule(multiworld, player, LogicEntrance.buy_year3_books, logic.time.has_year_three)
    set_entrance_rule(multiworld, player, Entrance.adventurer_guild_to_bedroom, logic.monster.can_kill_max(Generic.any))


def set_dangerous_mine_rules(logic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    dangerous_mine_rule = logic.mine.has_mine_elevator_to_floor(120) & logic.region.can_reach(Region.qi_walnut_room)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_20, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_60, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_100, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.enter_dangerous_skull_cavern,
                      (logic.received(Wallet.skull_key) & logic.region.can_reach(Region.qi_walnut_room)))


def set_farm_buildings_entrance_rules(logic, multiworld, player):
    set_entrance_rule(multiworld, player, Entrance.downstairs_to_cellar, logic.building.has_building(Building.cellar))
    set_entrance_rule(multiworld, player, Entrance.use_desert_obelisk, logic.can_use_obelisk(Transportation.desert_obelisk))
    set_entrance_rule(multiworld, player, Entrance.enter_greenhouse, logic.received("Greenhouse"))
    set_entrance_rule(multiworld, player, Entrance.enter_coop, logic.building.has_building(Building.coop))
    set_entrance_rule(multiworld, player, Entrance.enter_barn, logic.building.has_building(Building.barn))
    set_entrance_rule(multiworld, player, Entrance.enter_shed, logic.building.has_building(Building.shed))
    set_entrance_rule(multiworld, player, Entrance.enter_slime_hutch, logic.building.has_building(Building.slime_hutch))


def set_bedroom_entrance_rules(logic, multiworld, player, world_options: StardewValleyOptions):
    set_entrance_rule(multiworld, player, Entrance.enter_harvey_room, logic.relationship.has_hearts(NPC.harvey, 2))
    set_entrance_rule(multiworld, player, Entrance.mountain_to_maru_room, logic.relationship.has_hearts(NPC.maru, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_sebastian_room, (logic.relationship.has_hearts(NPC.sebastian, 2) | logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.forest_to_leah_cottage, logic.relationship.has_hearts(NPC.leah, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_elliott_house, logic.relationship.has_hearts(NPC.elliott, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_sunroom, logic.relationship.has_hearts(NPC.caroline, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_wizard_basement, logic.relationship.has_hearts(NPC.wizard, 4))
    if ModNames.alec in world_options.mods:
        set_entrance_rule(multiworld, player, AlecEntrance.petshop_to_bedroom, (logic.relationship.has_hearts(ModNPC.alec, 2) | logic.mod.magic.can_blink()))
    if ModNames.lacey in world_options.mods:
        set_entrance_rule(multiworld, player, LaceyEntrance.forest_to_hat_house, logic.relationship.has_hearts(ModNPC.lacey, 2))


def set_mines_floor_entrance_rules(logic, multiworld, player):
    for floor in range(5, 120 + 5, 5):
        rule = logic.mine.has_mine_elevator_to_floor(floor - 10)
        if floor == 5 or floor == 45 or floor == 85:
            rule = rule & logic.mine.can_progress_in_the_mines_from_floor(floor)
        set_entrance_rule(multiworld, player, dig_to_mines_floor(floor), rule)


def set_skull_cavern_floor_entrance_rules(logic, multiworld, player):
    for floor in range(25, 200 + 25, 25):
        rule = logic.mod.elevator.has_skull_cavern_elevator_to_floor(floor - 25)
        if floor == 25 or floor == 75 or floor == 125:
            rule = rule & logic.mine.can_progress_in_the_skull_cavern_from_floor(floor)
        set_entrance_rule(multiworld, player, dig_to_skull_floor(floor), rule)


def set_skill_entrance_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    set_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops, logic.farming.has_farming_tools & logic.season.has_spring)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops, logic.farming.has_farming_tools & logic.season.has_summer)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops, logic.farming.has_farming_tools & logic.season.has_fall)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_indoor_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops_on_island, logic.farming.has_farming_tools, world_options)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops_on_island, logic.farming.has_farming_tools, world_options)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops_on_island, logic.farming.has_farming_tools, world_options)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_indoor_crops_on_island, logic.farming.has_farming_tools, world_options)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_fall_crops_in_summer, true_)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_fall_crops_in_fall, true_)

    set_entrance_rule(multiworld, player, LogicEntrance.fishing, logic.fishing.can_fish_anywhere())


def set_blacksmith_entrance_rules(logic, multiworld, player):
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_copper, MetalBar.copper, ToolMaterial.copper)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_iron, MetalBar.iron, ToolMaterial.iron)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_gold, MetalBar.gold, ToolMaterial.gold)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_iridium, MetalBar.iridium, ToolMaterial.iridium)


def set_blacksmith_upgrade_rule(logic, multiworld, player, entrance_name: str, item_name: str, tool_material: str):
    upgrade_rule = logic.has(item_name) & logic.money.can_spend(tool_upgrade_prices[tool_material])
    set_entrance_rule(multiworld, player, entrance_name, upgrade_rule)


def set_festival_entrance_rules(logic, multiworld, player):
    set_entrance_rule(multiworld, player, LogicEntrance.attend_egg_festival, logic.season.has(Season.spring))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_desert_festival, logic.season.has(Season.spring) & logic.received("Bus Repair"))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_flower_dance, logic.season.has(Season.spring))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_luau, logic.season.has(Season.summer))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_trout_derby, logic.season.has(Season.summer))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_moonlight_jellies, logic.season.has(Season.summer))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_fair, logic.season.has(Season.fall))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_spirit_eve, logic.season.has(Season.fall))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_festival_of_ice, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_squidfest, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_night_market, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_winter_star, logic.season.has(Season.winter))


def set_ginger_island_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    set_island_entrances_rules(logic, multiworld, player, world_options)
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    set_boat_repair_rules(logic, multiworld, player)
    set_island_parrot_rules(logic, multiworld, player)
    set_rule(multiworld.get_location("Open Professor Snail Cave", player),
             logic.has(Bomb.cherry_bomb))
    set_rule(multiworld.get_location("Complete Island Field Office", player),
             logic.walnut.can_complete_field_office())
    set_walnut_rules(logic, multiworld, player, world_options)


def set_boat_repair_rules(logic: StardewLogic, multiworld, player):
    set_rule(multiworld.get_location("Repair Boat Hull", player),
             logic.has(Material.hardwood))
    set_rule(multiworld.get_location("Repair Boat Anchor", player),
             logic.has(MetalBar.iridium))
    set_rule(multiworld.get_location("Repair Ticket Machine", player),
             logic.has(ArtisanGood.battery_pack))


def set_island_entrances_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    boat_repaired = logic.received(Transportation.boat_repair)
    dig_site_rule = logic.received("Dig Site Bridge")
    entrance_rules = {
        Entrance.use_island_obelisk: logic.can_use_obelisk(Transportation.island_obelisk),
        Entrance.use_farm_obelisk: logic.can_use_obelisk(Transportation.farm_obelisk),
        Entrance.fish_shop_to_boat_tunnel: boat_repaired,
        Entrance.boat_to_ginger_island: boat_repaired & logic.money.can_spend(1000),
        Entrance.island_south_to_west: logic.received("Island West Turtle"),
        Entrance.island_south_to_north: logic.received("Island North Turtle"),
        Entrance.island_west_to_islandfarmhouse: logic.received("Island Farmhouse"),
        Entrance.island_west_to_gourmand_cave: logic.received("Island Farmhouse"),
        Entrance.island_north_to_dig_site: dig_site_rule,
        Entrance.dig_site_to_professor_snail_cave: logic.received("Open Professor Snail Cave"),
        Entrance.talk_to_island_trader: logic.received("Island Trader"),
        Entrance.island_south_to_southeast: logic.received("Island Resort"),
        Entrance.use_island_resort: logic.received("Island Resort"),
        Entrance.island_west_to_qi_walnut_room: logic.received("Qi Walnut Room"),
        Entrance.island_north_to_volcano: logic.tool.can_water(0) | logic.received("Volcano Bridge") | logic.mod.magic.can_blink(),
        Entrance.volcano_to_secret_beach: logic.tool.can_water(2),
        Entrance.climb_to_volcano_5: logic.ability.can_mine_perfectly() & logic.tool.can_water(1),
        Entrance.talk_to_volcano_dwarf: logic.wallet.can_speak_dwarf(),
        Entrance.climb_to_volcano_10: logic.ability.can_mine_perfectly() & logic.tool.can_water(1),
        Entrance.mountain_to_leo_treehouse: logic.received("Treehouse"),
    }
    parrots = [Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_jungle_to_volcano,
               Entrance.parrot_express_dig_site_to_volcano, Entrance.parrot_express_docks_to_dig_site,
               Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_volcano_to_dig_site,
               Entrance.parrot_express_docks_to_jungle, Entrance.parrot_express_dig_site_to_jungle,
               Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_jungle_to_docks,
               Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_volcano_to_docks]
    parrot_express_rule = logic.received(Transportation.parrot_express)
    parrot_express_to_dig_site_rule = dig_site_rule & parrot_express_rule
    for parrot in parrots:
        if "Dig Site" in parrot:
            entrance_rules[parrot] = parrot_express_to_dig_site_rule
        else:
            entrance_rules[parrot] = parrot_express_rule

    set_many_island_entrances_rules(multiworld, player, entrance_rules, world_options)


def set_island_parrot_rules(logic: StardewLogic, multiworld, player):
    # Logic rules require more walnuts than in reality, to allow the player to spend them "wrong"
    has_walnut = logic.walnut.has_walnut(5)
    has_5_walnut = logic.walnut.has_walnut(15)
    has_10_walnut = logic.walnut.has_walnut(40)
    has_20_walnut = logic.walnut.has_walnut(60)
    set_rule(multiworld.get_location("Leo's Parrot", player),
             has_walnut)
    set_rule(multiworld.get_location("Island West Turtle", player),
             has_10_walnut & logic.received("Island North Turtle"))
    set_rule(multiworld.get_location("Island Farmhouse", player),
             has_20_walnut)
    set_rule(multiworld.get_location("Island Mailbox", player),
             has_5_walnut & logic.received("Island Farmhouse"))
    set_rule(multiworld.get_location(Transportation.farm_obelisk, player),
             has_20_walnut & logic.received("Island Mailbox"))
    set_rule(multiworld.get_location("Dig Site Bridge", player),
             has_10_walnut & logic.received("Island West Turtle"))
    set_rule(multiworld.get_location("Island Trader", player),
             has_10_walnut & logic.received("Island Farmhouse"))
    set_rule(multiworld.get_location("Volcano Bridge", player),
             has_5_walnut & logic.received("Island West Turtle") &
             logic.region.can_reach(Region.volcano_floor_10))
    set_rule(multiworld.get_location("Volcano Exit Shortcut", player),
             has_5_walnut & logic.received("Island West Turtle"))
    set_rule(multiworld.get_location("Island Resort", player),
             has_20_walnut & logic.received("Island Farmhouse"))
    set_rule(multiworld.get_location(Transportation.parrot_express, player),
             has_10_walnut)


def set_walnut_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.walnutsanity == Walnutsanity.preset_none:
        return

    set_walnut_puzzle_rules(logic, multiworld, player, world_options)
    set_walnut_bushes_rules(logic, multiworld, player, world_options)
    set_walnut_dig_spot_rules(logic, multiworld, player, world_options)
    set_walnut_repeatable_rules(logic, multiworld, player, world_options)


def set_walnut_puzzle_rules(logic: StardewLogic, multiworld, player, world_options):
    if WalnutsanityOptionName.puzzles not in world_options.walnutsanity:
        return

    set_rule(multiworld.get_location("Walnutsanity: Open Golden Coconut", player), logic.has(Geode.golden_coconut))
    set_rule(multiworld.get_location("Walnutsanity: Banana Altar", player), logic.has(Fruit.banana))
    set_rule(multiworld.get_location("Walnutsanity: Leo's Tree", player), logic.tool.has_tool(Tool.axe))
    set_rule(multiworld.get_location("Walnutsanity: Gem Birds Shrine", player), logic.has(Mineral.amethyst) & logic.has(Mineral.aquamarine) &
             logic.has(Mineral.emerald) & logic.has(Mineral.ruby) & logic.has(Mineral.topaz) &
             logic.region.can_reach_all((Region.island_north, Region.island_west, Region.island_east, Region.island_south)))
    set_rule(multiworld.get_location("Walnutsanity: Gourmand Frog Melon", player), logic.has(Fruit.melon) & logic.region.can_reach(Region.island_west))
    set_rule(multiworld.get_location("Walnutsanity: Gourmand Frog Wheat", player), logic.has(Vegetable.wheat) &
             logic.region.can_reach(Region.island_west) & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Melon"))
    set_rule(multiworld.get_location("Walnutsanity: Gourmand Frog Garlic", player), logic.has(Vegetable.garlic) &
             logic.region.can_reach(Region.island_west) & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Wheat"))
    set_rule(multiworld.get_location("Walnutsanity: Whack A Mole", player), logic.tool.has_tool(Tool.watering_can, ToolMaterial.iridium))
    set_rule(multiworld.get_location("Walnutsanity: Complete Large Animal Collection", player), logic.walnut.can_complete_large_animal_collection())
    set_rule(multiworld.get_location("Walnutsanity: Complete Snake Collection", player), logic.walnut.can_complete_snake_collection())
    set_rule(multiworld.get_location("Walnutsanity: Complete Mummified Frog Collection", player), logic.walnut.can_complete_frog_collection())
    set_rule(multiworld.get_location("Walnutsanity: Complete Mummified Bat Collection", player), logic.walnut.can_complete_bat_collection())
    set_rule(multiworld.get_location("Walnutsanity: Purple Flowers Island Survey", player), logic.walnut.can_start_field_office)
    set_rule(multiworld.get_location("Walnutsanity: Purple Starfish Island Survey", player), logic.walnut.can_start_field_office)
    set_rule(multiworld.get_location("Walnutsanity: Protruding Tree Walnut", player), logic.combat.has_slingshot)
    set_rule(multiworld.get_location("Walnutsanity: Starfish Tide Pool", player), logic.tool.has_fishing_rod(1))
    set_rule(multiworld.get_location("Walnutsanity: Mermaid Song", player), logic.has(Furniture.flute_block))


def set_walnut_bushes_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.bushes not in world_options.walnutsanity:
        return
    # I don't think any of the bushes require something special, but that might change with ER
    return


def set_walnut_dig_spot_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.dig_spots not in world_options.walnutsanity:
        return

    for dig_spot_walnut in locations.locations_by_tag[LocationTags.WALNUTSANITY_DIG]:
        rule = logic.tool.has_tool(Tool.hoe)
        if "Journal Scrap" in dig_spot_walnut.name:
            rule = rule & logic.has(Forageable.journal_scrap)
        if "Starfish Diamond" in dig_spot_walnut.name:
            rule = rule & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron)
        set_rule(multiworld.get_location(dig_spot_walnut.name, player), rule)


def set_walnut_repeatable_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.repeatables not in world_options.walnutsanity:
        return
    for i in range(1, 6):
        set_rule(multiworld.get_location(f"Walnutsanity: Fishing Walnut {i}", player), logic.tool.has_fishing_rod(1))
        set_rule(multiworld.get_location(f"Walnutsanity: Harvesting Walnut {i}", player), logic.skill.can_get_farming_xp)
        set_rule(multiworld.get_location(f"Walnutsanity: Mussel Node Walnut {i}", player), logic.tool.has_tool(Tool.pickaxe))
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Rocks Walnut {i}", player), logic.tool.has_tool(Tool.pickaxe))
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Monsters Walnut {i}", player), logic.combat.has_galaxy_weapon)
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Crates Walnut {i}", player), logic.combat.has_any_weapon)
    set_rule(multiworld.get_location(f"Walnutsanity: Tiger Slime Walnut", player), logic.monster.can_kill(Monster.tiger_slime))


def set_cropsanity_rules(logic: StardewLogic, multiworld, player, world_content: StardewContent):
    if not world_content.features.cropsanity.is_enabled:
        return

    for item in world_content.find_tagged_items(ItemTag.CROPSANITY):
        location = world_content.features.cropsanity.to_location_name(item.name)
        harvest_sources = (source for source in item.sources if isinstance(source, (HarvestFruitTreeSource, HarvestCropSource)))
        set_rule(multiworld.get_location(location, player), logic.source.has_access_to_any(harvest_sources))


def set_story_quests_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.quest_locations.has_no_story_quests():
        return
    for quest in locations.locations_by_tag[LocationTags.STORY_QUEST]:
        if quest.name in all_location_names and (quest.mod_name is None or quest.mod_name in world_options.mods):
            set_rule(multiworld.get_location(quest.name, player),
                     logic.registry.quest_rules[quest.name])


def set_special_order_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player,
                            world_options: StardewValleyOptions):
    if world_options.special_order_locations & SpecialOrderLocations.option_board:
        board_rule = logic.received("Special Order Board") & logic.time.has_lived_months(4)
        for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
            if board_order.name in all_location_names:
                order_rule = board_rule & logic.registry.special_order_rules[board_order.name]
                set_rule(multiworld.get_location(board_order.name, player), order_rule)

    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    if world_options.special_order_locations & SpecialOrderLocations.value_qi:
        qi_rule = logic.region.can_reach(Region.qi_walnut_room) & logic.time.has_lived_months(8)
        for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
            if qi_order.name in all_location_names:
                order_rule = qi_rule & logic.registry.special_order_rules[qi_order.name]
                set_rule(multiworld.get_location(qi_order.name, player), order_rule)


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.quest_locations.has_no_story_quests():
        return
    help_wanted_number = world_options.quest_locations.value
    for i in range(0, help_wanted_number):
        set_number = i // 7
        month_rule = logic.time.has_lived_months(set_number)
        quest_number = set_number + 1
        quest_number_in_set = i % 7
        if quest_number_in_set < 4:
            quest_number = set_number * 4 + quest_number_in_set + 1
            set_help_wanted_delivery_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(multiworld, player, month_rule, quest_number)


def set_help_wanted_delivery_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), month_rule)


def set_help_wanted_gathering_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), month_rule)


def set_help_wanted_fishing_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), month_rule)


def set_help_wanted_slay_monsters_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), month_rule)


def set_fishsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            set_rule(multiworld.get_location(fish_location.name, player),
                     logic.has(fish_name))


def set_museumsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int,
                           world_options: StardewValleyOptions):
    museum_prefix = "Museumsanity: "
    if world_options.museumsanity == Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, multiworld, museum_milestone, museum_prefix, player)
    elif world_options.museumsanity != Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, multiworld, museum_prefix, player)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, multiworld, museum_prefix, player):
    all_donations = sorted(locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 3 // number_donations
            rule = logic.museum.can_find_museum_item(all_museum_items_by_name[donation_name]) & logic.received(Wallet.metal_detector, required_detectors)
            set_rule(multiworld.get_location(museum_location.name, player),
                     rule)
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, multiworld: MultiWorld, museum_milestone, museum_prefix: str,
                              player: int):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    metal_detector = Wallet.metal_detector
    rule = None
    if milestone_name.endswith(donations_suffix):
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items, logic.museum.can_find_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_museum_minerals, logic.museum.can_find_museum_minerals)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_museum_artifacts, logic.museum.can_find_museum_artifacts)
    elif milestone_name == "Dwarf Scrolls":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in dwarf_scrolls)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Front":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_front)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Middle":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_middle)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Back":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_back)) & logic.received(metal_detector, 2)
    elif milestone_name == "Ancient Seed":
        rule = logic.museum.can_find_museum_item(Artifact.ancient_seed) & logic.received(metal_detector, 2)
    if rule is None:
        return
    set_rule(multiworld.get_location(museum_milestone.name, player), rule)


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = Wallet.metal_detector
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 3 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if world_options.backpack_progression != BackpackProgression.option_vanilla:
        set_rule(multiworld.get_location("Large Pack", player),
                 logic.money.can_spend(2000))
        set_rule(multiworld.get_location("Deluxe Pack", player),
                 (logic.money.can_spend(10000) & logic.received("Progressive Backpack")))
        if ModNames.big_backpack in world_options.mods:
            set_rule(multiworld.get_location("Premium Pack", player),
                     (logic.money.can_spend(150000) &
                      logic.received("Progressive Backpack", 2)))


def set_festival_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player):
    festival_locations = []
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            set_rule(multiworld.get_location(festival.name, player),
                     logic.registry.festival_rules[festival.name])


monster_eradication_prefix = "Monster Eradication: "


def set_monstersanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    monstersanity_option = world_options.monstersanity
    if monstersanity_option == Monstersanity.option_none:
        return

    if monstersanity_option == Monstersanity.option_one_per_monster or monstersanity_option == Monstersanity.option_split_goals:
        set_monstersanity_monster_rules(all_location_names, logic, multiworld, player, monstersanity_option)
        return

    if monstersanity_option == Monstersanity.option_progressive_goals:
        set_monstersanity_progressive_category_rules(all_location_names, logic, multiworld, player)
        return

    set_monstersanity_category_rules(all_location_names, logic, multiworld, player, monstersanity_option)


def set_monstersanity_monster_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monstersanity_option):
    for monster_name in logic.monster.all_monsters_by_name:
        location_name = f"{monster_eradication_prefix}{monster_name}"
        if location_name not in all_location_names:
            continue
        location = multiworld.get_location(location_name, player)
        if monstersanity_option == Monstersanity.option_split_goals:
            rule = logic.monster.can_kill_many(logic.monster.all_monsters_by_name[monster_name])
        else:
            rule = logic.monster.can_kill(logic.monster.all_monsters_by_name[monster_name])
        set_rule(location, rule)


def set_monstersanity_progressive_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player):
    for monster_category in logic.monster.all_monsters_by_category:
        set_monstersanity_progressive_single_category_rules(all_location_names, logic, multiworld, player, monster_category)


def set_monstersanity_progressive_single_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monster_category: str):
    location_names = [name for name in all_location_names if name.startswith(monster_eradication_prefix) and name.endswith(monster_category)]
    if not location_names:
        return
    location_names = sorted(location_names, key=lambda name: get_monster_eradication_number(name, monster_category))
    for i in range(5):
        location_name = location_names[i]
        set_monstersanity_progressive_category_rule(all_location_names, logic, multiworld, player, monster_category, location_name, i)


def set_monstersanity_progressive_category_rule(all_location_names: Set[str], logic: StardewLogic, multiworld, player,
                                                monster_category: str, location_name: str, goal_index):
    if location_name not in all_location_names:
        return
    location = multiworld.get_location(location_name, player)
    if goal_index < 3:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index + 1)
    else:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index * 2)
    set_rule(location, rule)


def get_monster_eradication_number(location_name, monster_category) -> int:
    number = location_name[len(monster_eradication_prefix):-len(monster_category)]
    number = number.strip()
    if number.isdigit():
        return int(number)
    return 1000


def set_monstersanity_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monstersanity_option):
    for monster_category in logic.monster.all_monsters_by_category:
        location_name = f"{monster_eradication_prefix}{monster_category}"
        if location_name not in all_location_names:
            continue
        location = multiworld.get_location(location_name, player)
        if monstersanity_option == Monstersanity.option_one_per_category:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category])
        else:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], MAX_MONTHS)
        set_rule(location, rule)


def set_shipsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    shipsanity_option = world_options.shipsanity
    if shipsanity_option == Shipsanity.option_none:
        return

    shipsanity_prefix = "Shipsanity: "
    for location in locations.locations_by_tag[LocationTags.SHIPSANITY]:
        if location.name not in all_location_names:
            continue
        item_to_ship = location.name[len(shipsanity_prefix):]
        set_rule(multiworld.get_location(location.name, player), logic.shipping.can_ship(item_to_ship))


def set_cooksanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    cooksanity_option = world_options.cooksanity
    if cooksanity_option == Cooksanity.option_none:
        return

    cooksanity_prefix = "Cook "
    for location in locations.locations_by_tag[LocationTags.COOKSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[len(cooksanity_prefix):]
        recipe = all_cooking_recipes_by_name[recipe_name]
        cook_rule = logic.cooking.can_cook(recipe)
        set_rule(multiworld.get_location(location.name, player), cook_rule)


def set_chefsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    chefsanity_option = world_options.chefsanity
    if chefsanity_option == Chefsanity.option_none:
        return

    chefsanity_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CHEFSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[:-len(chefsanity_suffix)]
        recipe = all_cooking_recipes_by_name[recipe_name]
        learn_rule = logic.cooking.can_learn_recipe(recipe.source)
        set_rule(multiworld.get_location(location.name, player), learn_rule)


def set_craftsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    craftsanity_option = world_options.craftsanity
    if craftsanity_option == Craftsanity.option_none:
        return

    craft_prefix = "Craft "
    craft_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CRAFTSANITY]:
        if location.name not in all_location_names:
            continue
        if location.name.endswith(craft_suffix):
            recipe_name = location.name[:-len(craft_suffix)]
            recipe = all_crafting_recipes_by_name[recipe_name]
            craft_rule = logic.crafting.can_learn_recipe(recipe)
        else:
            recipe_name = location.name[len(craft_prefix):]
            recipe = all_crafting_recipes_by_name[recipe_name]
            craft_rule = logic.crafting.can_craft(recipe)
        set_rule(multiworld.get_location(location.name, player), craft_rule)


def set_booksanity_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    for book in content.find_tagged_items(ItemTag.BOOK):
        if booksanity.is_included(book):
            set_rule(multiworld.get_location(booksanity.to_location_name(book.name), player), logic.has(book.name))

    for i, book in enumerate(booksanity.get_randomized_lost_books()):
        if i <= 0:
            continue
        set_rule(multiworld.get_location(booksanity.to_location_name(book), player), logic.received(booksanity.progressive_lost_book, i))


def set_traveling_merchant_day_rules(logic: StardewLogic, multiworld: MultiWorld, player: int):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        entrance_name = f"Buy from Traveling Merchant {day}"
        set_entrance_rule(multiworld, player, entrance_name, logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    play_junimo_kart_rule = logic.received(Wallet.skull_key)

    if world_options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
        set_entrance_rule(multiworld, player, Entrance.play_junimo_kart, play_junimo_kart_rule)
        return

    set_entrance_rule(multiworld, player, Entrance.play_junimo_kart, play_junimo_kart_rule & logic.has("Junimo Kart Small Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_2, logic.has("Junimo Kart Medium Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_3, logic.has("Junimo Kart Big Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_4, logic.has("Junimo Kart Max Buff"))
    set_entrance_rule(multiworld, player, Entrance.play_journey_of_the_prairie_king, logic.has("JotPK Small Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_jotpk_world_2, logic.has("JotPK Medium Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_jotpk_world_3, logic.has("JotPK Big Buff"))
    set_rule(multiworld.get_location("Journey of the Prairie King Victory", player),
             logic.has("JotPK Max Buff"))


def set_friendsanity_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.features.friendsanity.is_enabled:
        return
    set_rule(multiworld.get_location("Spouse Stardrop", player),
             logic.relationship.has_hearts_with_any_bachelor(13) & logic.relationship.can_get_married())
    set_rule(multiworld.get_location("Have a Baby", player),
             logic.relationship.can_reproduce(1))
    set_rule(multiworld.get_location("Have Another Baby", player),
             logic.relationship.can_reproduce(2))

    for villager in content.villagers.values():
        for heart in content.features.friendsanity.get_randomized_hearts(villager):
            rule = logic.relationship.can_earn_relationship(villager.name, heart)
            location_name = friendsanity.to_location_name(villager.name, heart)
            set_rule(multiworld.get_location(location_name, player), rule)

    for heart in content.features.friendsanity.get_pet_randomized_hearts():
        rule = logic.pet.can_befriend_pet(heart)
        location_name = friendsanity.to_location_name(NPC.pet, heart)
        set_rule(multiworld.get_location(location_name, player), rule)


def set_deepwoods_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.deepwoods in world_options.mods:
        set_rule(multiworld.get_location("Breaking Up Deep Woods Gingerbread House", player),
                 logic.tool.has_tool(Tool.axe, "Gold"))
        set_rule(multiworld.get_location("Chop Down a Deep Woods Iridium Tree", player),
                 logic.tool.has_tool(Tool.axe, "Iridium"))
        set_entrance_rule(multiworld, player, DeepWoodsEntrance.use_woods_obelisk, logic.received("Woods Obelisk"))
        for depth in range(10, 100 + 10, 10):
            set_entrance_rule(multiworld, player, move_to_woods_depth(depth), logic.mod.deepwoods.can_chop_to_depth(depth))
        set_rule(multiworld.get_location("The Sword in the Stone", player),
                 logic.mod.deepwoods.can_pull_sword() & logic.mod.deepwoods.can_chop_to_depth(100))


def set_magic_spell_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.magic not in world_options.mods:
        return

    set_rule(multiworld.get_location("Analyze: Clear Debris", player),
             (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")))
    set_rule(multiworld.get_location("Analyze: Till", player),
             logic.tool.has_tool("Hoe", "Basic"))
    set_rule(multiworld.get_location("Analyze: Water", player),
             logic.tool.has_tool("Watering Can", "Basic"))
    set_rule(multiworld.get_location("Analyze All Toil School Locations", player),
             (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
              & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic"))))
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    set_rule(multiworld.get_location("Analyze: Evac", player),
             logic.ability.can_mine_perfectly())
    set_rule(multiworld.get_location("Analyze: Haste", player),
             logic.has("Coffee"))
    set_rule(multiworld.get_location("Analyze: Heal", player),
             logic.has("Life Elixir"))
    set_rule(multiworld.get_location("Analyze All Life School Locations", player),
             (logic.has("Coffee") & logic.has("Life Elixir")
              & logic.ability.can_mine_perfectly()))
    set_rule(multiworld.get_location("Analyze: Descend", player),
             logic.region.can_reach(Region.mines))
    set_rule(multiworld.get_location("Analyze: Fireball", player),
             logic.has("Fire Quartz"))
    set_rule(multiworld.get_location("Analyze: Frostbolt", player),
             logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    set_rule(multiworld.get_location("Analyze All Elemental School Locations", player),
             logic.has("Fire Quartz") & logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    # set_rule(multiworld.get_location("Analyze: Lantern", player),)
    set_rule(multiworld.get_location("Analyze: Tendrils", player),
             logic.region.can_reach(Region.farm))
    set_rule(multiworld.get_location("Analyze: Shockwave", player),
             logic.has("Earth Crystal"))
    set_rule(multiworld.get_location("Analyze All Nature School Locations", player),
             (logic.has("Earth Crystal") & logic.region.can_reach("Farm"))),
    set_rule(multiworld.get_location("Analyze: Meteor", player),
             (logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12))),
    set_rule(multiworld.get_location("Analyze: Lucksteal", player),
             logic.region.can_reach(Region.witch_hut))
    set_rule(multiworld.get_location("Analyze: Bloodmana", player),
             logic.region.can_reach(Region.mines_floor_100))
    set_rule(multiworld.get_location("Analyze All Eldritch School Locations", player),
             (logic.region.can_reach(Region.witch_hut) &
              logic.region.can_reach(Region.mines_floor_100) &
              logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)))
    set_rule(multiworld.get_location("Analyze Every Magic School Location", player),
             (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
              & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")) &
              logic.has("Coffee") & logic.has("Life Elixir")
              & logic.ability.can_mine_perfectly() & logic.has("Earth Crystal") &
              logic.has("Fire Quartz") & logic.fishing.can_fish(85) &
              logic.region.can_reach(Region.witch_hut) &
              logic.region.can_reach(Region.mines_floor_100) &
              logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)))


def set_sve_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.sve not in world_options.mods:
        return
    set_entrance_rule(multiworld, player, SVEEntrance.forest_to_lost_woods, logic.bundle.can_complete_community_center)
    set_entrance_rule(multiworld, player, SVEEntrance.enter_summit, logic.mod.sve.has_iridium_bomb())
    set_entrance_rule(multiworld, player, SVEEntrance.backwoods_to_grove, logic.mod.sve.has_any_rune())
    set_entrance_rule(multiworld, player, SVEEntrance.badlands_to_cave, logic.has("Aegis Elixir") | logic.combat.can_fight_at_level(Performance.maximum))
    set_entrance_rule(multiworld, player, SVEEntrance.forest_west_to_spring, logic.quest.can_complete_quest(Quest.magic_ink))
    set_entrance_rule(multiworld, player, SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    set_entrance_rule(multiworld, player, SVEEntrance.secret_woods_to_west, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.grandpa_shed_to_interior, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.aurora_warp_to_aurora, logic.received(SVERunes.nexus_aurora))
    set_entrance_rule(multiworld, player, SVEEntrance.farm_warp_to_farm, logic.received(SVERunes.nexus_farm))
    set_entrance_rule(multiworld, player, SVEEntrance.guild_warp_to_guild, logic.received(SVERunes.nexus_guild))
    set_entrance_rule(multiworld, player, SVEEntrance.junimo_warp_to_junimo, logic.received(SVERunes.nexus_junimo))
    set_entrance_rule(multiworld, player, SVEEntrance.spring_warp_to_spring, logic.received(SVERunes.nexus_spring))
    set_entrance_rule(multiworld, player, SVEEntrance.outpost_warp_to_outpost, logic.received(SVERunes.nexus_outpost))
    set_entrance_rule(multiworld, player, SVEEntrance.wizard_warp_to_wizard, logic.received(SVERunes.nexus_wizard))
    set_entrance_rule(multiworld, player, SVEEntrance.use_purple_junimo, logic.relationship.has_hearts(ModNPC.apples, 10))
    set_entrance_rule(multiworld, player, SVEEntrance.grandpa_interior_to_upstairs, logic.mod.sve.has_grandpa_shed_repaired())
    set_entrance_rule(multiworld, player, SVEEntrance.use_bear_shop, (logic.mod.sve.can_buy_bear_recipe()))
    set_entrance_rule(multiworld, player, SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    set_entrance_rule(multiworld, player, SVEEntrance.museum_to_gunther_bedroom, logic.relationship.has_hearts(ModNPC.gunther, 2))
    set_entrance_rule(multiworld, player, SVEEntrance.to_aurora_basement, logic.mod.quest.has_completed_aurora_vineyard_bundle())
    logic.mod.sve.initialize_rules()
    for location in logic.registry.sve_location_rules:
        set_rule(multiworld.get_location(location, player),
                 logic.registry.sve_location_rules[location])
    set_sve_ginger_island_rules(logic, multiworld, player, world_options)
    set_boarding_house_rules(logic, multiworld, player, world_options)


def set_sve_ginger_island_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    set_entrance_rule(multiworld, player, SVEEntrance.summit_to_highlands, logic.mod.sve.has_marlon_boat())
    set_entrance_rule(multiworld, player, SVEEntrance.wizard_to_fable_reef, logic.received(SVEQuestItem.fable_reef_portal))
    set_entrance_rule(multiworld, player, SVEEntrance.highlands_to_cave,
                      logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron) & logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.highlands_to_pond, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))


def set_boarding_house_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.boarding_house not in world_options.mods:
        return
    set_entrance_rule(multiworld, player, BoardingHouseEntrance.the_lost_valley_to_lost_valley_ruins, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))


def set_entrance_rule(multiworld, player, entrance: str, rule: StardewRule):
    try:
        potentially_required_regions = look_for_indirect_connection(rule)
        if potentially_required_regions:
            for region in potentially_required_regions:
                logger.debug(f"Registering indirect condition for {region} -> {entrance}")
                multiworld.register_indirect_condition(multiworld.get_region(region, player), multiworld.get_entrance(entrance, player))

        set_rule(multiworld.get_entrance(entrance, player), rule)
    except KeyError as ex:
        logger.error(f"""Failed to evaluate indirect connection in: {explain(rule, CollectionState(multiworld))}""")
        raise ex


def set_island_entrance_rule(multiworld, player, entrance: str, rule: StardewRule, world_options: StardewValleyOptions):
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    set_entrance_rule(multiworld, player, entrance, rule)


def set_many_island_entrances_rules(multiworld, player, entrance_rules: Dict[str, StardewRule], world_options: StardewValleyOptions):
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    for entrance, rule in entrance_rules.items():
        set_entrance_rule(multiworld, player, entrance, rule)
