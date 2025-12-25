import itertools
import logging
from dataclasses import dataclass
from typing import List, Dict, Set

from BaseClasses import MultiWorld, CollectionState
from worlds.generic.Rules import set_rule as _set_rule
from . import locations
from .bundles.bundle_room import BundleRoom
from .content import StardewContent
from .content.feature import friendsanity
from .content.vanilla.ginger_island import ginger_island_content_pack
from .content.vanilla.qi_board import qi_board_content_pack
from .data.craftable_data import all_crafting_recipes_by_name
from .data.game_item import ItemTag
from .data.harvest import HarvestCropSource, HarvestFruitTreeSource
from .data.museum_data import all_museum_items, dwarf_scrolls, skeleton_front, skeleton_middle, skeleton_back, \
    all_museum_items_by_name, all_museum_minerals, \
    all_museum_artifacts, Artifact
from .data.recipe_data import all_cooking_recipes_by_name
from .data.secret_note_data import gift_requirements, SecretNote
from .locations import LocationTags
from .logic.logic import StardewLogic
from .logic.time_logic import MAX_MONTHS
from .logic.tool_logic import tool_upgrade_prices
from .mods.mod_data import ModNames
from .options import SpecialOrderLocations, Museumsanity, BackpackProgression, Shipsanity, \
    Monstersanity, Chefsanity, Craftsanity, ArcadeMachineLocations, Cooksanity, StardewValleyOptions, Walnutsanity
from .options.options import FarmType, Moviesanity, Eatsanity, Friendsanity, ExcludeGingerIsland, \
    IncludeEndgameLocations
from .stardew_rule import And, StardewRule, true_
from .stardew_rule.indirect_connection import look_for_indirect_connection
from .stardew_rule.rule_explain import explain
from .strings.animal_product_names import AnimalProduct
from .strings.ap_names.ap_option_names import WalnutsanityOptionName, SecretsanityOptionName, StartWithoutOptionName
from .strings.ap_names.community_upgrade_names import CommunityUpgrade, Bookseller
from .strings.ap_names.mods.mod_items import SVEQuestItem, SVERunes
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.backpack_tiers import Backpack
from .strings.building_names import Building, WizardBuilding
from .strings.bundle_names import CCRoom
from .strings.calendar_names import Weekday
from .strings.craftable_names import Bomb, Furniture, Consumable, Craftable
from .strings.crop_names import Fruit, Vegetable
from .strings.currency_names import Currency
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, \
    DeepWoodsEntrance, AlecEntrance, \
    SVEEntrance, LaceyEntrance, BoardingHouseEntrance, LogicEntrance
from .strings.fish_names import Fish
from .strings.food_names import Meal
from .strings.forageable_names import Forageable
from .strings.generic_names import Generic
from .strings.geode_names import Geode
from .strings.gift_names import Gift
from .strings.machine_names import Machine
from .strings.material_names import Material
from .strings.metal_names import Artifact as ArtifactName, MetalBar, Mineral
from .strings.monster_names import Monster
from .strings.performance_names import Performance
from .strings.quest_names import Quest
from .strings.region_names import Region, LogicRegion
from .strings.season_names import Season
from .strings.skill_names import Skill
from .strings.special_item_names import SpecialItem
from .strings.special_order_names import SpecialOrder
from .strings.tool_names import Tool, ToolMaterial, FishingRod
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StardewRuleCollector:
    multiworld: MultiWorld
    player: int
    content: StardewContent

    def set_entrance_rule(self, entrance_name: str, rule: StardewRule) -> None:
        try:
            potentially_required_regions = look_for_indirect_connection(rule)
            if potentially_required_regions:
                for region in potentially_required_regions:
                    logger.debug(f"Registering indirect condition for {region} -> {entrance_name}")
                    self.multiworld.register_indirect_condition(self.multiworld.get_region(region, self.player),
                                                                self.multiworld.get_entrance(entrance_name, self.player))

            _set_rule(self.multiworld.get_entrance(entrance_name, self.player), rule)
        except KeyError as ex:
            logger.error(f"""Failed to evaluate indirect connection in: {explain(rule, CollectionState(self.multiworld))}""")
            raise ex

    def set_island_entrance_rule(self, entrance_name: str, rule: StardewRule) -> None:
        if not self.content.is_enabled(ginger_island_content_pack):
            return
        self.set_entrance_rule(entrance_name, rule)

    def set_many_island_entrances_rules(self, entrance_rules: dict[str, StardewRule]) -> None:
        if not self.content.is_enabled(ginger_island_content_pack):
            return
        for entrance, rule in entrance_rules.items():
            self.set_entrance_rule(entrance, rule)

    def set_location_rule(self, location_name: str, rule: StardewRule) -> None:
        _set_rule(self.multiworld.get_location(location_name, self.player), rule)


def set_rules(world):
    world_options = world.options
    world_content = world.content
    rule_collector = StardewRuleCollector(world.multiworld, world.player, world_content)
    logic = world.logic
    bundle_rooms: List[BundleRoom] = world.modified_bundles
    trash_bear_requests: Dict[str, List[str]] = world.trash_bear_requests

    all_location_names = set(location.name for location in world.multiworld.get_locations(world.player))

    set_entrance_rules(logic, rule_collector, bundle_rooms, world_options, world_content)
    set_ginger_island_rules(logic, rule_collector, world_options, world_content)

    set_tool_rules(logic, rule_collector, world_content)
    set_skills_rules(logic, rule_collector, world_content)
    set_bundle_rules(bundle_rooms, logic, rule_collector, world_options)
    set_building_rules(logic, rule_collector, world_content)
    set_cropsanity_rules(logic, rule_collector, world_content)
    set_story_quests_rules(all_location_names, logic, rule_collector, world_options)
    set_special_order_rules(all_location_names, logic, rule_collector, world_options, world_content)
    set_help_wanted_quests_rules(logic, rule_collector, world_options)
    set_fishsanity_rules(all_location_names, logic, rule_collector)
    set_museumsanity_rules(all_location_names, logic, rule_collector, world_options)

    set_friendsanity_rules(logic, rule_collector, world_content)
    set_backpack_rules(logic, rule_collector, world_options, world_content)
    set_festival_rules(all_location_names, logic, rule_collector)
    set_monstersanity_rules(all_location_names, logic, rule_collector, world_options)
    set_shipsanity_rules(all_location_names, logic, rule_collector, world_options)
    set_cooksanity_rules(all_location_names, logic, rule_collector, world_options)
    set_chefsanity_rules(all_location_names, logic, rule_collector, world_options)
    set_craftsanity_rules(all_location_names, logic, rule_collector, world_options)
    set_booksanity_rules(logic, rule_collector, world_content)
    set_isolated_locations_rules(logic, rule_collector, trash_bear_requests)
    set_arcade_machine_rules(logic, rule_collector, world_options)
    set_movie_rules(logic, rule_collector, world_options, world_content)
    set_secrets_rules(logic, rule_collector, world_options, world_content)
    set_hatsanity_rules(logic, rule_collector, world_content)
    set_eatsanity_rules(all_location_names, logic, rule_collector, world_options)
    set_endgame_locations_rules(logic, rule_collector, world_options)

    set_deepwoods_rules(logic, rule_collector, world_content)
    set_magic_spell_rules(logic, rule_collector, world_content)
    set_sve_rules(logic, rule_collector, world_content)


def set_isolated_locations_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, trash_bear_requests: Dict[str, List[str]]):
    rule_collector.set_location_rule("Beach Bridge Repair", logic.grind.can_grind_item(300, "Wood"))
    rule_collector.set_location_rule("Grim Reaper Statue", logic.combat.can_fight_at_level(Performance.decent) & logic.tool.has_tool(Tool.pickaxe))
    rule_collector.set_location_rule("Galaxy Sword Shrine", logic.has("Prismatic Shard"))
    rule_collector.set_location_rule("Krobus Stardrop", logic.money.can_spend(20000))
    rule_collector.set_location_rule("Demetrius's Breakthrough", logic.money.can_have_earned_total(25000))
    for request_type in trash_bear_requests:
        location = f"Trash Bear {request_type}"
        items = trash_bear_requests[request_type]
        rule_collector.set_location_rule(location, logic.bundle.can_feed_trash_bear(*items))


def set_tool_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    tool_progression = content.features.tool_progression
    if not tool_progression.is_progressive:
        return

    rule_collector.set_location_rule("Purchase Fiberglass Rod", (logic.skill.has_level(Skill.fishing, 2) & logic.money.can_spend(1800)))
    rule_collector.set_location_rule("Purchase Iridium Rod", (logic.skill.has_level(Skill.fishing, 6) & logic.money.can_spend(7500)))

    rule_collector.set_location_rule("Copper Pan Cutscene", logic.received("Glittering Boulder Removed"))

    # Pan has no basic tier, so it is removed from materials.
    pan_materials = ToolMaterial.materials[1:]
    for previous, material in itertools.product(pan_materials[:-1], pan_materials[1:]):
        location_name = tool_progression.to_upgrade_location_name(Tool.pan, material)
        # You need to receive the previous tool to be able to upgrade it.
        rule_collector.set_location_rule(location_name, logic.tool.has_pan(previous))

    materials = ToolMaterial.materials
    tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.trash_can]
    for (previous, material), tool in itertools.product(zip(materials[:-1], materials[1:]), tool):
        location_name = tool_progression.to_upgrade_location_name(tool, material)
        # You need to receive the previous tool to be able to upgrade it.
        rule_collector.set_location_rule(location_name, logic.tool.has_tool(tool, previous))


def set_building_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        if building.name in building_progression.starting_buildings:
            continue

        location_name = building_progression.to_location_name(building.name)

        rule_collector.set_location_rule(location_name, logic.building.can_build(building.name))


def set_bundle_rules(bundle_rooms: List[BundleRoom], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    for bundle_room in bundle_rooms:
        if bundle_room.name == CCRoom.raccoon_requests:
            # The rule for the raccoon bundles are placed on their entrance, not on the location itself.
            continue

        room_rules = []
        for bundle in bundle_room.bundles:
            bundle_rules = logic.bundle.can_complete_bundle(bundle)
            room_rules.append(bundle_rules)
            rule_collector.set_location_rule(bundle.name, bundle_rules)
        if bundle_room.name == CCRoom.abandoned_joja_mart or bundle_room.name == CCRoom.raccoon_requests:
            continue
        room_location = f"Complete {bundle_room.name}"
        rule_collector.set_location_rule(room_location, And(*room_rules))


def set_skills_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    skill_progression = content.features.skill_progression
    if not skill_progression.is_progressive:
        return

    for skill in content.skills.values():
        for level, level_name in skill_progression.get_randomized_level_names_by_level(skill):
            rule = logic.skill.can_earn_level(skill.name, level)
            rule_collector.set_location_rule(level_name, rule)

        if skill_progression.is_mastery_randomized(skill):
            rule = logic.skill.can_earn_mastery(skill.name)
            rule_collector.set_location_rule(skill.mastery_name, rule)


def set_entrance_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, bundle_rooms: List[BundleRoom], world_options: StardewValleyOptions,
                       content: StardewContent):
    set_mines_floor_entrance_rules(logic, rule_collector)
    set_skull_cavern_floor_entrance_rules(logic, rule_collector)
    set_blacksmith_entrance_rules(logic, rule_collector)
    set_skill_entrance_rules(logic, rule_collector, content)
    set_traveling_merchant_day_entrance_rules(logic, rule_collector)
    set_dangerous_mine_rules(logic, rule_collector, content)

    rule_collector.set_entrance_rule(Entrance.enter_tide_pools, logic.received("Beach Bridge") | logic.mod.magic.can_blink())
    rule_collector.set_entrance_rule(Entrance.mountain_to_outside_adventure_guild, logic.received("Landslide Removed"))
    rule_collector.set_entrance_rule(Entrance.enter_quarry,
                                     (logic.received("Bridge Repair") | logic.mod.magic.can_blink()) & logic.tool.has_tool(Tool.pickaxe))
    rule_collector.set_entrance_rule(Entrance.enter_secret_woods, logic.tool.has_tool(Tool.axe, ToolMaterial.iron) | (logic.mod.magic.can_blink()))
    rule_collector.set_entrance_rule(Entrance.town_to_community_center, logic.received("Community Center Key"))
    rule_collector.set_entrance_rule(Entrance.forest_to_wizard_tower, logic.received("Wizard Invitation"))
    rule_collector.set_entrance_rule(Entrance.forest_to_sewer, logic.wallet.has_rusty_key())
    rule_collector.set_entrance_rule(Entrance.town_to_sewer, logic.wallet.has_rusty_key())
    # The money requirement is just in case Joja got replaced by a theater, you need to buy a ticket.
    # We do not put directly a ticket requirement, because we don't want to place an indirect theater requirement only
    # for the safeguard "in case you get a theater"
    rule_collector.set_entrance_rule(Entrance.town_to_jojamart, logic.money.can_spend(1000))
    rule_collector.set_entrance_rule(Entrance.enter_abandoned_jojamart, logic.has_abandoned_jojamart())
    movie_theater_rule = logic.has_movie_theater()
    rule_collector.set_entrance_rule(Entrance.purchase_movie_ticket, movie_theater_rule)
    rule_collector.set_entrance_rule(Entrance.enter_movie_theater, movie_theater_rule & logic.has(Gift.movie_ticket))
    rule_collector.set_entrance_rule(Entrance.take_bus_to_desert, logic.received(Transportation.bus_repair) & logic.money.can_spend(500))
    rule_collector.set_entrance_rule(Entrance.enter_skull_cavern, logic.received(Wallet.skull_key))
    rule_collector.set_entrance_rule(LogicEntrance.talk_to_mines_dwarf,
                                     logic.wallet.can_speak_dwarf() & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_traveling_merchant, logic.traveling_merchant.has_days() & logic.money.can_spend(1200))
    set_raccoon_rules(logic, rule_collector, bundle_rooms, world_options)

    rule_collector.set_entrance_rule(LogicEntrance.fish_in_waterfall,
                                     logic.skill.has_level(Skill.fishing, 5) & logic.tool.has_fishing_rod(FishingRod.bamboo))

    set_farm_buildings_entrance_rules(logic, rule_collector)

    rule_collector.set_entrance_rule(Entrance.mountain_to_railroad, logic.received("Railroad Boulder Removed"))
    rule_collector.set_entrance_rule(Entrance.enter_witch_warp_cave, logic.quest.has_dark_talisman() | (logic.mod.magic.can_blink()))
    rule_collector.set_entrance_rule(Entrance.enter_witch_hut, (logic.quest.can_complete_quest(Quest.goblin_problem) | logic.mod.magic.can_blink()))
    rule_collector.set_entrance_rule(Entrance.enter_mutant_bug_lair,
                                     (logic.wallet.has_rusty_key() & logic.region.can_reach(Region.railroad) & logic.relationship.can_meet(NPC.krobus))
                                     | logic.mod.magic.can_blink())
    rule_collector.set_entrance_rule(Entrance.enter_casino, logic.quest.has_club_card())

    set_bedroom_entrance_rules(logic, rule_collector, content)
    set_festival_entrance_rules(logic, rule_collector)
    
    # I can't remember why this was here, but clearly we do not need kitchen rules for island cooking....
    # rule_collector.set_island_entrance_rule(LogicEntrance.island_cooking, logic.cooking.can_cook_in_kitchen)
    rule_collector.set_entrance_rule(LogicEntrance.farmhouse_cooking, logic.cooking.can_cook_in_kitchen)
    rule_collector.set_entrance_rule(LogicEntrance.shipping, logic.shipping.can_use_shipping_bin)
    rule_collector.set_entrance_rule(LogicEntrance.find_secret_notes,
                                     logic.quest.has_magnifying_glass() & (logic.ability.can_chop_trees() | logic.mine.can_mine_in_the_mines_floor_1_40()))
    rule_collector.set_entrance_rule(LogicEntrance.watch_queen_of_sauce, logic.action.can_watch(Channel.queen_of_sauce))
    rule_collector.set_entrance_rule(Entrance.forest_to_mastery_cave, logic.skill.can_enter_mastery_cave)
    set_bookseller_rules(logic, rule_collector)
    rule_collector.set_entrance_rule(Entrance.adventurer_guild_to_bedroom, logic.monster.can_kill_max(Generic.any))
    if world_options.include_endgame_locations == IncludeEndgameLocations.option_true:
        rule_collector.set_entrance_rule(LogicEntrance.purchase_wizard_blueprints, logic.quest.has_magic_ink())
    rule_collector.set_entrance_rule(LogicEntrance.search_garbage_cans, logic.time.has_lived_months(MAX_MONTHS / 2))

    rule_collector.set_entrance_rule(Entrance.forest_beach_shortcut, logic.received("Forest To Beach Shortcut"))
    rule_collector.set_entrance_rule(Entrance.mountain_jojamart_shortcut, logic.received("Mountain Shortcuts"))
    rule_collector.set_entrance_rule(Entrance.mountain_town_shortcut, logic.received("Mountain Shortcuts"))
    rule_collector.set_entrance_rule(Entrance.town_tidepools_shortcut, logic.received("Town To Tide Pools Shortcut"))
    rule_collector.set_entrance_rule(Entrance.tunnel_backwoods_shortcut, logic.received("Tunnel To Backwoods Shortcut"))
    rule_collector.set_entrance_rule(Entrance.mountain_lake_to_outside_adventure_guild_shortcut, logic.received("Mountain Shortcuts"))

    rule_collector.set_entrance_rule(Entrance.feed_trash_bear, logic.received("Trash Bear Arrival"))
    rule_collector.set_entrance_rule(Entrance.enter_shorts_maze, logic.has(Craftable.staircase))

    rule_collector.set_entrance_rule(Entrance.enter_mens_locker_room, logic.wallet.has_mens_locker_key())
    rule_collector.set_entrance_rule(Entrance.enter_womens_locker_room, logic.wallet.has_womens_locker_key())


def set_bookseller_rules(logic, rule_collector):
    rule_collector.set_entrance_rule(LogicEntrance.buy_books, logic.received(Bookseller.days))
    rule_collector.set_entrance_rule(LogicEntrance.buy_experience_books, logic.received(Bookseller.stock_experience_books))
    rule_collector.set_entrance_rule(LogicEntrance.buy_permanent_books, logic.received(Bookseller.stock_permanent_books))
    rare_books_rule = (logic.received(Bookseller.days, 4) & logic.received(Bookseller.stock_rare_books)) | \
                      (logic.received(Bookseller.days, 2) & logic.received(Bookseller.stock_rare_books, 2))
    rule_collector.set_entrance_rule(LogicEntrance.buy_rare_books, rare_books_rule)


def set_raccoon_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, bundle_rooms: List[BundleRoom], world_options: StardewValleyOptions):
    rule_collector.set_entrance_rule(LogicEntrance.has_giant_stump, logic.received(CommunityUpgrade.raccoon))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_1, logic.quest.has_raccoon_shop())
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_2, logic.quest.has_raccoon_shop(2))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_3, logic.quest.has_raccoon_shop(3))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_4, logic.quest.has_raccoon_shop(4))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_5, logic.quest.has_raccoon_shop(5))
    rule_collector.set_entrance_rule(LogicEntrance.buy_from_raccoon_6, logic.quest.has_raccoon_shop(6))

    raccoon_room = next(iter(room for room in bundle_rooms if room.name == CCRoom.raccoon_requests))
    extra_raccoons = 1 if world_options.quest_locations.has_story_quests() else 0

    for bundle in raccoon_room.bundles:
        num = int(bundle.name[-1])
        bundle_rules = logic.received(CommunityUpgrade.raccoon, num + extra_raccoons) & logic.bundle.can_complete_bundle(bundle)
        rule_collector.set_entrance_rule("Can Complete " + bundle.name, bundle_rules)


def set_dangerous_mine_rules(logic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    dangerous_mine_rule = logic.mine.has_mine_elevator_to_floor(120) & logic.region.can_reach(Region.qi_walnut_room)
    rule_collector.set_entrance_rule(Entrance.dig_to_dangerous_mines_20, dangerous_mine_rule)
    rule_collector.set_entrance_rule(Entrance.dig_to_dangerous_mines_60, dangerous_mine_rule)
    rule_collector.set_entrance_rule(Entrance.dig_to_dangerous_mines_100, dangerous_mine_rule)
    rule_collector.set_entrance_rule(Entrance.enter_dangerous_skull_cavern,
                                     (logic.received(Wallet.skull_key) & logic.region.can_reach(Region.qi_walnut_room)))


def set_farm_buildings_entrance_rules(logic, rule_collector: StardewRuleCollector):
    rule_collector.set_entrance_rule(Entrance.downstairs_to_cellar, logic.building.has_building(Building.cellar))
    rule_collector.set_entrance_rule(Entrance.use_desert_obelisk, logic.can_use_obelisk(Transportation.desert_obelisk))
    rule_collector.set_entrance_rule(Entrance.enter_greenhouse, logic.received("Greenhouse"))
    rule_collector.set_entrance_rule(Entrance.enter_coop, logic.building.has_building(Building.coop))
    rule_collector.set_entrance_rule(Entrance.enter_barn, logic.building.has_building(Building.barn))
    rule_collector.set_entrance_rule(Entrance.enter_shed, logic.building.has_building(Building.shed))
    rule_collector.set_entrance_rule(Entrance.enter_slime_hutch, logic.building.has_building(Building.slime_hutch))


def set_bedroom_entrance_rules(logic, rule_collector: StardewRuleCollector, content: StardewContent):
    rule_collector.set_entrance_rule(Entrance.enter_harvey_room, logic.relationship.has_hearts(NPC.harvey, 2))
    rule_collector.set_entrance_rule(Entrance.mountain_to_maru_room, logic.relationship.has_hearts(NPC.maru, 2))
    rule_collector.set_entrance_rule(Entrance.enter_sebastian_room, (logic.relationship.has_hearts(NPC.sebastian, 2) | logic.mod.magic.can_blink()))
    rule_collector.set_entrance_rule(Entrance.forest_to_leah_cottage, logic.relationship.has_hearts(NPC.leah, 2))
    rule_collector.set_entrance_rule(Entrance.enter_elliott_house, logic.relationship.has_hearts(NPC.elliott, 2))
    rule_collector.set_entrance_rule(Entrance.enter_sunroom, logic.relationship.has_hearts(NPC.caroline, 2))
    rule_collector.set_entrance_rule(Entrance.enter_wizard_basement, logic.relationship.has_hearts(NPC.wizard, 4))
    rule_collector.set_entrance_rule(Entrance.enter_lewis_bedroom, logic.relationship.has_hearts(NPC.lewis, 2))
    if content.is_enabled(ModNames.alec):
        rule_collector.set_entrance_rule(AlecEntrance.petshop_to_bedroom, (logic.relationship.has_hearts(ModNPC.alec, 2) | logic.mod.magic.can_blink()))
    if content.is_enabled(ModNames.lacey):
        rule_collector.set_entrance_rule(LaceyEntrance.forest_to_hat_house, logic.relationship.has_hearts(ModNPC.lacey, 2))


def set_mines_floor_entrance_rules(logic, rule_collector: StardewRuleCollector):
    for floor in range(5, 120 + 5, 5):
        rule = logic.mine.has_mine_elevator_to_floor(floor - 10)
        if floor == 5 or floor == 45 or floor == 85:
            rule = rule & logic.mine.can_progress_in_the_mines_from_floor(floor)
        rule_collector.set_entrance_rule(dig_to_mines_floor(floor), rule)


def set_skull_cavern_floor_entrance_rules(logic, rule_collector: StardewRuleCollector):
    rule_collector.set_entrance_rule(Entrance.mine_in_skull_cavern, logic.mine.can_progress_in_the_mines_from_floor(120))

    for floor in range(25, 200 + 25, 25):
        rule = logic.mod.elevator.has_skull_cavern_elevator_to_floor(floor - 25)
        if floor == 25 or floor == 75 or floor == 125:
            rule = rule & logic.mine.can_progress_in_the_skull_cavern_from_floor(floor)
        rule_collector.set_entrance_rule(dig_to_skull_floor(floor), rule)


def set_skill_entrance_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    rule_collector.set_entrance_rule(LogicEntrance.grow_spring_crops, logic.farming.has_farming_tools & logic.season.has_spring)
    rule_collector.set_entrance_rule(LogicEntrance.grow_summer_crops, logic.farming.has_farming_tools & logic.season.has_summer)
    rule_collector.set_entrance_rule(LogicEntrance.grow_fall_crops, logic.farming.has_farming_tools & logic.season.has_fall)
    rule_collector.set_entrance_rule(LogicEntrance.grow_winter_crops, logic.farming.has_farming_tools & logic.season.has_winter)
    rule_collector.set_entrance_rule(LogicEntrance.grow_spring_crops_in_greenhouse, logic.farming.has_farming_tools)
    rule_collector.set_entrance_rule(LogicEntrance.grow_summer_crops_in_greenhouse, logic.farming.has_farming_tools)
    rule_collector.set_entrance_rule(LogicEntrance.grow_fall_crops_in_greenhouse, logic.farming.has_farming_tools)
    rule_collector.set_entrance_rule(LogicEntrance.grow_winter_crops_in_greenhouse, logic.farming.has_farming_tools)
    rule_collector.set_entrance_rule(LogicEntrance.grow_indoor_crops_in_greenhouse, logic.farming.has_farming_tools)
    rule_collector.set_island_entrance_rule(LogicEntrance.grow_spring_crops_on_island, logic.farming.has_farming_tools)
    rule_collector.set_island_entrance_rule(LogicEntrance.grow_summer_crops_on_island, logic.farming.has_farming_tools)
    rule_collector.set_island_entrance_rule(LogicEntrance.grow_fall_crops_on_island, logic.farming.has_farming_tools)
    rule_collector.set_island_entrance_rule(LogicEntrance.grow_winter_crops_on_island, logic.farming.has_farming_tools)
    rule_collector.set_island_entrance_rule(LogicEntrance.grow_indoor_crops_on_island, logic.farming.has_farming_tools)
    rule_collector.set_entrance_rule(LogicEntrance.grow_summer_fall_crops_in_summer, true_)
    rule_collector.set_entrance_rule(LogicEntrance.grow_summer_fall_crops_in_fall, true_)

    rule_collector.set_entrance_rule(LogicEntrance.fishing, logic.fishing.can_fish_anywhere())


def set_blacksmith_entrance_rules(logic, rule_collector: StardewRuleCollector):
    set_blacksmith_upgrade_rule(logic, rule_collector, LogicEntrance.blacksmith_copper, MetalBar.copper, ToolMaterial.copper)
    set_blacksmith_upgrade_rule(logic, rule_collector, LogicEntrance.blacksmith_iron, MetalBar.iron, ToolMaterial.iron)
    set_blacksmith_upgrade_rule(logic, rule_collector, LogicEntrance.blacksmith_gold, MetalBar.gold, ToolMaterial.gold)
    set_blacksmith_upgrade_rule(logic, rule_collector, LogicEntrance.blacksmith_iridium, MetalBar.iridium, ToolMaterial.iridium)


def set_blacksmith_upgrade_rule(logic, rule_collector: StardewRuleCollector, entrance_name: str, item_name: str, tool_material: str):
    upgrade_rule = logic.has(item_name) & logic.money.can_spend(tool_upgrade_prices[tool_material])
    rule_collector.set_entrance_rule(entrance_name, upgrade_rule)


def set_festival_entrance_rules(logic, rule_collector: StardewRuleCollector):
    rule_collector.set_entrance_rule(LogicEntrance.attend_egg_festival, logic.season.has(Season.spring))
    rule_collector.set_entrance_rule(LogicEntrance.attend_desert_festival, logic.season.has(Season.spring) & logic.received(Transportation.bus_repair))
    rule_collector.set_entrance_rule(LogicEntrance.attend_flower_dance, logic.season.has(Season.spring))

    rule_collector.set_entrance_rule(LogicEntrance.attend_luau, logic.season.has(Season.summer))
    rule_collector.set_entrance_rule(LogicEntrance.attend_trout_derby,
                                     logic.season.has(Season.summer) & logic.fishing.can_use_specific_bait(Fish.rainbow_trout))
    rule_collector.set_entrance_rule(LogicEntrance.attend_moonlight_jellies, logic.season.has(Season.summer))

    rule_collector.set_entrance_rule(LogicEntrance.attend_fair, logic.season.has(Season.fall))
    rule_collector.set_entrance_rule(LogicEntrance.attend_spirit_eve, logic.season.has(Season.fall))

    rule_collector.set_entrance_rule(LogicEntrance.attend_festival_of_ice, logic.season.has(Season.winter))
    rule_collector.set_entrance_rule(LogicEntrance.attend_squidfest, logic.season.has(Season.winter) & logic.fishing.can_use_specific_bait(Fish.squid))
    rule_collector.set_entrance_rule(LogicEntrance.attend_night_market, logic.season.has(Season.winter))
    rule_collector.set_entrance_rule(LogicEntrance.attend_winter_star, logic.season.has(Season.winter))


def set_ginger_island_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions, content: StardewContent):
    set_island_entrances_rules(logic, rule_collector, content)
    if not content.is_enabled(ginger_island_content_pack):
        return

    set_boat_repair_rules(logic, rule_collector)
    set_island_parrot_rules(logic, rule_collector)
    rule_collector.set_location_rule("Open Professor Snail Cave", logic.has(Bomb.cherry_bomb))
    rule_collector.set_location_rule("Complete Island Field Office", logic.walnut.can_complete_field_office())
    set_walnut_rules(logic, rule_collector, world_options)


def set_boat_repair_rules(logic: StardewLogic, rule_collector: StardewRuleCollector):
    rule_collector.set_location_rule("Repair Boat Hull", logic.has(Material.hardwood))
    rule_collector.set_location_rule("Repair Boat Anchor", logic.has(MetalBar.iridium))
    rule_collector.set_location_rule("Repair Ticket Machine", logic.has(ArtisanGood.battery_pack))


def set_island_entrances_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
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
        Entrance.island_north_to_volcano: logic.tool.can_water() | logic.received("Volcano Bridge") | logic.mod.magic.can_blink(),
        Entrance.volcano_to_secret_beach: logic.tool.can_water(3),
        Entrance.climb_to_volcano_5: logic.ability.can_mine_perfectly() & logic.tool.can_water(2),
        Entrance.talk_to_volcano_dwarf: logic.wallet.can_speak_dwarf(),
        Entrance.climb_to_volcano_10: logic.ability.can_mine_perfectly() & logic.tool.can_water(2),
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

    rule_collector.set_many_island_entrances_rules(entrance_rules)


def set_island_parrot_rules(logic: StardewLogic, rule_collector: StardewRuleCollector):
    # Logic rules require more walnuts than in reality, to allow the player to spend them "wrong"
    has_walnut = logic.walnut.has_walnut(5)
    has_5_walnut = logic.walnut.has_walnut(15)
    has_10_walnut = logic.walnut.has_walnut(40)
    has_20_walnut = logic.walnut.has_walnut(60)
    rule_collector.set_location_rule("Leo's Parrot", has_walnut)
    rule_collector.set_location_rule("Island West Turtle", has_10_walnut & logic.received("Island North Turtle"))
    rule_collector.set_location_rule("Island Farmhouse", has_20_walnut)
    rule_collector.set_location_rule("Island Mailbox", has_5_walnut & logic.received("Island Farmhouse"))
    rule_collector.set_location_rule(Transportation.farm_obelisk, has_20_walnut & logic.received("Island Mailbox"))
    rule_collector.set_location_rule("Dig Site Bridge", has_10_walnut & logic.received("Island West Turtle"))
    rule_collector.set_location_rule("Island Trader", has_10_walnut & logic.received("Island Farmhouse"))
    rule_collector.set_location_rule("Volcano Bridge",
                                     has_5_walnut & logic.received("Island West Turtle") & logic.region.can_reach(Region.volcano_floor_10))
    rule_collector.set_location_rule("Volcano Exit Shortcut", has_5_walnut & logic.received("Island West Turtle"))
    rule_collector.set_location_rule("Island Resort", has_20_walnut & logic.received("Island Farmhouse"))
    rule_collector.set_location_rule(Transportation.parrot_express, has_10_walnut)


def set_walnut_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    if world_options.walnutsanity == Walnutsanity.preset_none:
        return

    set_walnut_puzzle_rules(logic, rule_collector, world_options)
    set_walnut_bushes_rules(logic, rule_collector, world_options)
    set_walnut_dig_spot_rules(logic, rule_collector, world_options)
    set_walnut_repeatable_rules(logic, rule_collector, world_options)


def set_walnut_puzzle_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options):
    if WalnutsanityOptionName.puzzles not in world_options.walnutsanity:
        return

    rule_collector.set_location_rule("Walnutsanity: Open Golden Coconut", logic.has(Geode.golden_coconut))
    rule_collector.set_location_rule("Walnutsanity: Banana Altar", logic.has(Fruit.banana))
    rule_collector.set_location_rule("Walnutsanity: Leo's Tree", logic.tool.has_tool(Tool.axe))
    rule_collector.set_location_rule("Walnutsanity: Gem Birds Shrine",
                                     logic.has_all(Mineral.amethyst, Mineral.aquamarine, Mineral.emerald, Mineral.ruby, Mineral.topaz)
                                     & logic.region.can_reach_all(Region.island_north, Region.island_west, Region.island_east, Region.island_south))
    rule_collector.set_location_rule("Walnutsanity: Gourmand Frog Melon", logic.has(Fruit.melon) & logic.region.can_reach(Region.island_west))
    rule_collector.set_location_rule("Walnutsanity: Gourmand Frog Wheat",
                                     logic.has(Vegetable.wheat) & logic.region.can_reach(Region.island_west)
                                     & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Melon"))
    rule_collector.set_location_rule("Walnutsanity: Gourmand Frog Garlic",
                                     logic.has(Vegetable.garlic) & logic.region.can_reach(Region.island_west)
                                     & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Wheat"))
    rule_collector.set_location_rule("Walnutsanity: Whack A Mole", logic.tool.has_tool(Tool.watering_can, ToolMaterial.iridium))
    rule_collector.set_location_rule("Walnutsanity: Complete Large Animal Collection", logic.walnut.can_complete_large_animal_collection())
    rule_collector.set_location_rule("Walnutsanity: Complete Snake Collection", logic.walnut.can_complete_snake_collection())
    rule_collector.set_location_rule("Walnutsanity: Complete Mummified Frog Collection", logic.walnut.can_complete_frog_collection())
    rule_collector.set_location_rule("Walnutsanity: Complete Mummified Bat Collection", logic.walnut.can_complete_bat_collection())
    rule_collector.set_location_rule("Walnutsanity: Purple Flowers Island Survey", logic.walnut.can_start_field_office)
    rule_collector.set_location_rule("Walnutsanity: Purple Starfish Island Survey", logic.walnut.can_start_field_office)
    rule_collector.set_location_rule("Walnutsanity: Protruding Tree Walnut", logic.combat.has_slingshot)
    rule_collector.set_location_rule("Walnutsanity: Starfish Tide Pool", logic.tool.has_fishing_rod())
    rule_collector.set_location_rule("Walnutsanity: Mermaid Song", logic.has(Furniture.flute_block))


def set_walnut_bushes_rules(logic, rule_collector: StardewRuleCollector, world_options):
    if WalnutsanityOptionName.bushes not in world_options.walnutsanity:
        return
    # I don't think any of the bushes require something special, but that might change with ER
    return


def set_walnut_dig_spot_rules(logic, rule_collector: StardewRuleCollector, world_options):
    if WalnutsanityOptionName.dig_spots not in world_options.walnutsanity:
        return

    for dig_spot_walnut in locations.locations_by_tag[LocationTags.WALNUTSANITY_DIG]:
        rule = logic.tool.has_tool(Tool.hoe)
        if "Journal Scrap" in dig_spot_walnut.name:
            rule = rule & logic.has(Forageable.journal_scrap)
        if "Starfish Diamond" in dig_spot_walnut.name:
            rule = rule & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron)
        rule_collector.set_location_rule(dig_spot_walnut.name, rule)


def set_walnut_repeatable_rules(logic, rule_collector: StardewRuleCollector, world_options):
    if WalnutsanityOptionName.repeatables not in world_options.walnutsanity:
        return
    for i in range(1, 6):
        rule_collector.set_location_rule(f"Walnutsanity: Fishing Walnut {i}", logic.tool.has_fishing_rod())
        rule_collector.set_location_rule(f"Walnutsanity: Harvesting Walnut {i}", logic.skill.can_get_farming_xp)
        rule_collector.set_location_rule(f"Walnutsanity: Mussel Node Walnut {i}", logic.tool.has_tool(Tool.pickaxe))
        rule_collector.set_location_rule(f"Walnutsanity: Volcano Rocks Walnut {i}", logic.tool.has_tool(Tool.pickaxe))
        rule_collector.set_location_rule(f"Walnutsanity: Volcano Monsters Walnut {i}", logic.combat.has_galaxy_weapon)
        rule_collector.set_location_rule(f"Walnutsanity: Volcano Crates Walnut {i}", logic.combat.has_any_weapon)
    rule_collector.set_location_rule(f"Walnutsanity: Tiger Slime Walnut", logic.monster.can_kill(Monster.tiger_slime))


def set_cropsanity_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_content: StardewContent):
    if not world_content.features.cropsanity.is_enabled:
        return

    for item in world_content.find_tagged_items(ItemTag.CROPSANITY):
        location = world_content.features.cropsanity.to_location_name(item.name)
        harvest_sources = (source for source in item.sources if isinstance(source, (HarvestFruitTreeSource, HarvestCropSource)))
        rule_collector.set_location_rule(location, logic.source.has_access_to_any(harvest_sources))


def set_story_quests_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    if world_options.quest_locations.has_no_story_quests():
        return
    for quest_location in locations.locations_by_tag[LocationTags.STORY_QUEST]:
        quest_location_name = quest_location.name
        if quest_location_name in all_location_names:
            quest_prefix = "Quest: "
            quest_name = quest_location_name[len(quest_prefix):]
            rule_collector.set_location_rule(quest_location_name, logic.registry.quest_rules[quest_name])


def set_special_order_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector,
                            world_options: StardewValleyOptions, content: StardewContent):
    if world_options.special_order_locations & SpecialOrderLocations.option_board:
        board_rule = logic.received("Special Order Board") & logic.time.has_lived_months(4)
        for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
            if board_order.name in all_location_names:
                order_rule = board_rule & logic.registry.special_order_rules[board_order.name]
                rule_collector.set_location_rule(board_order.name, order_rule)

    if content.is_enabled(qi_board_content_pack):
        qi_rule = logic.region.can_reach(Region.qi_walnut_room) & logic.time.has_lived_months(8)
        for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
            if qi_order.name in all_location_names:
                order_rule = qi_rule & logic.registry.special_order_rules[qi_order.name]
                rule_collector.set_location_rule(qi_order.name, order_rule)


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
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
            set_help_wanted_delivery_rule(logic, rule_collector, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(logic, rule_collector, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(logic, rule_collector, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(logic, rule_collector, month_rule, quest_number)


def set_help_wanted_delivery_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    rule_collector.set_location_rule(location_name, logic.quest.can_do_item_delivery_quest() & month_rule)


def set_help_wanted_gathering_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    rule_collector.set_location_rule(location_name, logic.quest.can_do_gathering_quest() & month_rule)


def set_help_wanted_fishing_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    rule_collector.set_location_rule(location_name, logic.quest.can_do_fishing_quest() & month_rule)


def set_help_wanted_slay_monsters_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    rule_collector.set_location_rule(location_name, logic.quest.can_do_slaying_quest() & month_rule)


def set_fishsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            rule_collector.set_location_rule(fish_location.name, logic.has(fish_name))


def set_museumsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    museum_prefix = "Museumsanity: "
    if world_options.museumsanity == Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, rule_collector, museum_milestone, museum_prefix)
    elif world_options.museumsanity != Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, rule_collector, museum_prefix)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, rule_collector: StardewRuleCollector, museum_prefix: str):
    all_donations = sorted(locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 3 // number_donations
            rule = logic.museum.can_find_museum_item(all_museum_items_by_name[donation_name]) & logic.received(Wallet.metal_detector, required_detectors)
            rule_collector.set_location_rule(museum_location.name, rule)
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, museum_milestone, museum_prefix: str):
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
    rule_collector.set_location_rule(museum_milestone.name, rule)


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = Wallet.metal_detector
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 3 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions, content: StardewContent):
    if world_options.backpack_progression == BackpackProgression.option_vanilla:
        return

    num_per_tier = world_options.backpack_size.count_per_tier()
    start_without_backpack = bool(StartWithoutOptionName.backpack in world_options.start_without)
    backpack_tier_names = Backpack.get_purchasable_tiers(content.is_enabled(ModNames.big_backpack), start_without_backpack)
    previous_backpacks = 0
    for tier in backpack_tier_names:
        for i in range(1, num_per_tier + 1):
            loc_name = f"{tier} {i}"
            if num_per_tier == 1:
                loc_name = tier
            price = Backpack.prices_per_tier[tier]
            rule_collector.set_location_rule(loc_name, logic.money.can_spend(price) & logic.received("Progressive Backpack", previous_backpacks))
            previous_backpacks += 1


def set_festival_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector):
    festival_locations = []
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            rule_collector.set_location_rule(festival.name, logic.registry.festival_rules[festival.name])


monster_eradication_prefix = "Monster Eradication: "


def set_monstersanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    monstersanity_option = world_options.monstersanity
    if monstersanity_option == Monstersanity.option_none:
        return

    if monstersanity_option == Monstersanity.option_one_per_monster or monstersanity_option == Monstersanity.option_split_goals:
        set_monstersanity_monster_rules(all_location_names, logic, rule_collector, monstersanity_option)
        return

    if monstersanity_option == Monstersanity.option_progressive_goals:
        set_monstersanity_progressive_category_rules(all_location_names, logic, rule_collector)
        return

    set_monstersanity_category_rules(all_location_names, logic, rule_collector, monstersanity_option)


def set_monstersanity_monster_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, monstersanity_option):
    for monster_name in logic.monster.all_monsters_by_name:
        location_name = f"{monster_eradication_prefix}{monster_name}"
        if location_name not in all_location_names:
            continue
        if monstersanity_option == Monstersanity.option_split_goals:
            rule = logic.monster.can_kill_many(logic.monster.all_monsters_by_name[monster_name])
        else:
            rule = logic.monster.can_kill(logic.monster.all_monsters_by_name[monster_name])
        rule_collector.set_location_rule(location_name, rule)


def set_monstersanity_progressive_category_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector):
    for monster_category in logic.monster.all_monsters_by_category:
        set_monstersanity_progressive_single_category_rules(all_location_names, logic, rule_collector, monster_category)


def set_monstersanity_progressive_single_category_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector,
                                                        monster_category: str):
    location_names = [name for name in all_location_names if name.startswith(monster_eradication_prefix) and name.endswith(monster_category)]
    if not location_names:
        return
    location_names = sorted(location_names, key=lambda name: get_monster_eradication_number(name, monster_category))
    for i in range(5):
        location_name = location_names[i]
        set_monstersanity_progressive_category_rule(all_location_names, logic, rule_collector, monster_category, location_name, i)


def set_monstersanity_progressive_category_rule(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector,
                                                monster_category: str, location_name: str, goal_index):
    if location_name not in all_location_names:
        return
    if goal_index < 3:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index + 1)
    else:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index * 2)
    rule_collector.set_location_rule(location_name, rule)


def get_monster_eradication_number(location_name, monster_category) -> int:
    number = location_name[len(monster_eradication_prefix):-len(monster_category)]
    number = number.strip()
    if number.isdigit():
        return int(number)
    return 1000


def set_monstersanity_category_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, monstersanity_option):
    for monster_category in logic.monster.all_monsters_by_category:
        location_name = f"{monster_eradication_prefix}{monster_category}"
        if location_name not in all_location_names:
            continue
        if monstersanity_option == Monstersanity.option_one_per_category:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category])
        else:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], MAX_MONTHS)
        rule_collector.set_location_rule(location_name, rule)


def set_shipsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    shipsanity_option = world_options.shipsanity
    if shipsanity_option == Shipsanity.option_none:
        return

    shipsanity_prefix = "Shipsanity: "
    for location in locations.locations_by_tag[LocationTags.SHIPSANITY]:
        if location.name not in all_location_names:
            continue
        item_to_ship = location.name[len(shipsanity_prefix):]
        rule_collector.set_location_rule(location.name, logic.shipping.can_ship(item_to_ship))


def set_cooksanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
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
        rule_collector.set_location_rule(location.name, cook_rule)


def set_chefsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    chefsanity_option = world_options.chefsanity
    if chefsanity_option == Chefsanity.preset_none:
        return

    chefsanity_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CHEFSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[:-len(chefsanity_suffix)]
        recipe = all_cooking_recipes_by_name[recipe_name]
        learn_rule = logic.cooking.can_learn_recipe(recipe.source)
        rule_collector.set_location_rule(location.name, learn_rule)


def set_craftsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
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
        rule_collector.set_location_rule(location.name, craft_rule)


def set_booksanity_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    for book in content.find_tagged_items(ItemTag.BOOK):
        if booksanity.is_included(book):
            rule_collector.set_location_rule(booksanity.to_location_name(book.name), logic.has(book.name))

    for i, book in enumerate(booksanity.get_randomized_lost_books()):
        if i <= 0:
            continue
        rule_collector.set_location_rule(booksanity.to_location_name(book), logic.received(booksanity.progressive_lost_book, i))


def set_traveling_merchant_day_entrance_rules(logic: StardewLogic, rule_collector: StardewRuleCollector):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        entrance_name = f"Buy from Traveling Merchant {day}"
        rule_collector.set_entrance_rule(entrance_name, logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    play_junimo_kart_rule = logic.received(Wallet.skull_key)

    if world_options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
        rule_collector.set_entrance_rule(Entrance.play_junimo_kart, play_junimo_kart_rule)
        return

    rule_collector.set_entrance_rule(Entrance.play_junimo_kart, play_junimo_kart_rule & logic.has("Junimo Kart Small Buff"))
    rule_collector.set_entrance_rule(Entrance.reach_junimo_kart_2, logic.has("Junimo Kart Medium Buff"))
    rule_collector.set_entrance_rule(Entrance.reach_junimo_kart_3, logic.has("Junimo Kart Big Buff"))
    rule_collector.set_entrance_rule(Entrance.reach_junimo_kart_4, logic.has("Junimo Kart Max Buff"))
    rule_collector.set_entrance_rule(Entrance.play_journey_of_the_prairie_king, logic.has("JotPK Small Buff"))
    rule_collector.set_entrance_rule(Entrance.reach_jotpk_world_2, logic.has("JotPK Medium Buff"))
    rule_collector.set_entrance_rule(Entrance.reach_jotpk_world_3, logic.has("JotPK Big Buff"))
    rule_collector.set_location_rule("Journey of the Prairie King Victory", logic.has("JotPK Max Buff"))


def set_movie_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions, content: StardewContent):
    moviesanity = world_options.moviesanity.value
    if moviesanity <= Moviesanity.option_none:
        return

    if moviesanity >= Moviesanity.option_all_movies:
        watch_prefix = "Watch "
        for movie_location in locations.locations_by_tag[LocationTags.MOVIE]:
            movie_name = movie_location.name[len(watch_prefix):]
            if moviesanity == Moviesanity.option_all_movies:
                rule = logic.movie.can_watch_movie(movie_name)
            elif moviesanity == Moviesanity.option_all_movies_loved or moviesanity == Moviesanity.option_all_movies_and_all_snacks:
                rule = logic.movie.can_watch_movie_with_loving_npc(movie_name)
            else:
                rule = logic.movie.can_watch_movie_with_loving_npc_and_snack(movie_name)
            rule_collector.set_location_rule(movie_location.name, rule)
    if moviesanity >= Moviesanity.option_all_movies_and_all_snacks:
        snack_prefix = "Share "
        for snack_location in locations.locations_by_tag[LocationTags.MOVIE_SNACK]:
            snack_name = snack_location.name[len(snack_prefix):]
            if moviesanity == Moviesanity.option_all_movies_and_all_loved_snacks:
                rule = logic.movie.can_buy_snack_for_someone_who_loves_it(snack_name)
            else:
                rule = logic.movie.can_buy_snack(snack_name)
            rule_collector.set_location_rule(snack_location.name, rule)


def set_secrets_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions, content: StardewContent):
    if not world_options.secretsanity:
        return

    if SecretsanityOptionName.easy in world_options.secretsanity:
        rule_collector.set_location_rule("Old Master Cannoli", logic.has(Fruit.sweet_gem_berry))
        rule_collector.set_location_rule("Pot Of Gold", logic.season.has(Season.spring))
        rule_collector.set_location_rule("Poison The Governor", logic.has(SpecialItem.lucky_purple_shorts))
        rule_collector.set_location_rule("Grange Display Bribe", logic.has(SpecialItem.lucky_purple_shorts))
        rule_collector.set_location_rule("Purple Lettuce", logic.has(SpecialItem.lucky_purple_shorts))
        rule_collector.set_location_rule("Make Marnie Laugh", logic.has(SpecialItem.trimmed_purple_shorts) & logic.relationship.can_meet(NPC.marnie))
        rule_collector.set_location_rule("Jumpscare Lewis", logic.has(SpecialItem.trimmed_purple_shorts) & logic.relationship.can_meet(NPC.lewis))
        rule_collector.set_location_rule("Confront Marnie", logic.gifts.can_gift_to(NPC.marnie, SpecialItem.lucky_purple_shorts))
        rule_collector.set_location_rule("Lucky Purple Bobber", logic.fishing.can_use_tackle(SpecialItem.lucky_purple_shorts))
        rule_collector.set_location_rule("Something For Santa", logic.season.has(Season.winter) & logic.has_any(AnimalProduct.any_milk, Meal.cookie))
        cc_rewards = ["Bridge Repair", "Greenhouse", "Glittering Boulder Removed", "Minecarts Repair", Transportation.bus_repair, "Friendship Bonus (2 <3)"]
        rule_collector.set_location_rule("Jungle Junimo", logic.action.can_speak_junimo() & logic.and_(*[logic.received(reward) for reward in cc_rewards]))
        rule_collector.set_location_rule("??HMTGF??", logic.has(Fish.super_cucumber))
        rule_collector.set_location_rule("??Pinky Lemon??", logic.has(ArtisanGood.duck_mayonnaise))
        rule_collector.set_location_rule("??Foroguemon??", logic.has(Meal.strange_bun) & logic.relationship.has_hearts(NPC.vincent, 2))
        rule_collector.set_location_rule("Galaxies Will Heed Your Cry", logic.wallet.can_speak_dwarf())
        rule_collector.set_location_rule("Summon Bone Serpent", logic.has(ArtifactName.ancient_doll))
        rule_collector.set_location_rule("Meowmere", logic.has(SpecialItem.far_away_stone) & logic.region.can_reach(Region.wizard_basement))
        rule_collector.set_location_rule("A Familiar Tune", logic.relationship.can_meet(NPC.elliott))
        rule_collector.set_location_rule("Flubber Experiment",
                                         logic.relationship.can_get_married() & logic.building.has_building(Building.slime_hutch)
                                         & logic.has_all(Machine.slime_incubator, AnimalProduct.slime_egg_green))
        rule_collector.set_location_rule("Seems Fishy", logic.money.can_spend_at(Region.wizard_basement, 500))
        rule_collector.set_location_rule("What kind of monster is this?", logic.gifts.can_gift_to(NPC.willy, Fish.mutant_carp))
        rule_collector.set_location_rule("My mouth is watering already", logic.gifts.can_gift_to(NPC.abigail, Meal.magic_rock_candy))
        rule_collector.set_location_rule("A gift of lovely perfume", logic.gifts.can_gift_to(NPC.krobus, Consumable.monster_musk))
        rule_collector.set_location_rule("Where exactly does this juice come from?", logic.gifts.can_gift_to(NPC.dwarf, AnimalProduct.cow_milk))
        rule_collector.set_location_rule("Thank the Devs", logic.received("Stardrop") & logic.money.can_spend_at(Region.wizard_basement, 500))
        if content.is_enabled(ginger_island_content_pack) and content.is_enabled(qi_board_content_pack):
            rule_collector.set_location_rule("Obtain my precious fruit whenever you like",
                                             logic.special_order.can_complete_special_order(SpecialOrder.qis_crop) &
                                             logic.tool.has_tool(Tool.axe))

    if SecretsanityOptionName.fishing in world_options.secretsanity:
        if world_options.farm_type == FarmType.option_beach:
            rule_collector.set_location_rule("'Boat'", logic.fishing.can_fish_at(Region.farm))
        if content.is_enabled(ginger_island_content_pack):
            rule_collector.set_location_rule("Foliage Print", logic.fishing.can_fish_with_cast_distance(Region.island_north, 5))
            rule_collector.set_location_rule("Frog Hat", logic.fishing.can_fish_at(Region.gourmand_frog_cave))
            rule_collector.set_location_rule("Gourmand Statue", logic.fishing.can_fish_at(Region.pirate_cove))
            rule_collector.set_location_rule("'Physics 101'", logic.fishing.can_fish_at(Region.volcano_floor_10))
            rule_collector.set_location_rule("Lifesaver", logic.fishing.can_fish_at(Region.boat_tunnel))
            rule_collector.set_location_rule("Squirrel Figurine", logic.fishing.can_fish_at(Region.volcano_secret_beach))
        rule_collector.set_location_rule("Decorative Trash Can", logic.fishing.can_fish_at(Region.town))
        rule_collector.set_location_rule("Iridium Krobus", logic.fishing.can_fish_with_cast_distance(Region.forest, 7))
        rule_collector.set_location_rule("Pyramid Decal", logic.fishing.can_fish_with_cast_distance(Region.desert, 4))
        rule_collector.set_location_rule("'Vista'", logic.fishing.can_fish_at(Region.railroad) & logic.season.has_any_not_winter())
        rule_collector.set_location_rule("Wall Basket", logic.fishing.can_fish_at(Region.secret_woods))

    if SecretsanityOptionName.difficult in world_options.secretsanity:
        rule_collector.set_location_rule("Free The Forsaken Souls", logic.action.can_watch(Channel.sinister_signal))
        rule_collector.set_location_rule("Annoy the Moon Man", logic.shipping.can_use_shipping_bin & logic.time.has_lived_months(6))
        rule_collector.set_location_rule("Strange Sighting", logic.region.can_reach_all(Region.bus_stop, Region.town) & logic.time.has_lived_months(6))
        rule_collector.set_location_rule("Sea Monster Sighting", logic.region.can_reach(Region.beach) & logic.time.has_lived_months(2))
        rule_collector.set_location_rule("...Bigfoot?",
                                         logic.region.can_reach_all(Region.forest, Region.town, Region.secret_woods) & logic.time.has_lived_months(4))
        rule_collector.set_location_rule("'Me me me me me me me me me me me me me me me me'",
                                         logic.region.can_reach(Region.railroad) & logic.tool.has_scythe())
        rule_collector.set_location_rule("Secret Iridium Stackmaster Trophy", logic.grind.can_grind_item(10000, Material.wood))

    if SecretsanityOptionName.secret_notes in world_options.secretsanity:
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_1)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_2)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_3)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_4)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_5)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_6)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_7)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_8)
        set_secret_note_gift_rule(logic, rule_collector, SecretNote.note_9)
        rule_collector.set_location_rule(SecretNote.note_10, logic.registry.quest_rules[Quest.cryptic_note])
        rule_collector.set_location_rule(SecretNote.note_11, logic.relationship.can_meet_all(NPC.marnie, NPC.jas, ))
        rule_collector.set_location_rule(SecretNote.note_12, logic.region.can_reach(Region.town))
        rule_collector.set_location_rule(SecretNote.note_13, logic.time.has_lived_months(1) & logic.region.can_reach(Region.town))
        rule_collector.set_location_rule(SecretNote.note_14, logic.region.can_reach(Region.town) & logic.season.has(Season.spring))
        rule_collector.set_location_rule(SecretNote.note_15, logic.region.can_reach(LogicRegion.night_market))
        rule_collector.set_location_rule(SecretNote.note_16, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.railroad))
        rule_collector.set_location_rule(SecretNote.note_17, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.town))
        rule_collector.set_location_rule(SecretNote.note_18, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.desert))
        rule_collector.set_location_rule(SecretNote.note_19_part_1, logic.region.can_reach(Region.town))
        rule_collector.set_location_rule(SecretNote.note_19_part_2, logic.region.can_reach(Region.town) & logic.has(SpecialItem.solid_gold_lewis))
        rule_collector.set_location_rule(SecretNote.note_20, logic.region.can_reach(Region.town) & logic.has(AnimalProduct.rabbit_foot))
        rule_collector.set_location_rule(SecretNote.note_21, logic.region.can_reach(Region.town))
        rule_collector.set_location_rule(SecretNote.note_22, logic.registry.quest_rules[Quest.the_mysterious_qi])
        rule_collector.set_location_rule(SecretNote.note_23, logic.registry.quest_rules[Quest.strange_note])
        rule_collector.set_location_rule(SecretNote.note_24,
                                         logic.building.has_wizard_building(WizardBuilding.junimo_hut) & logic.has(Mineral.any_gem)
                                         & logic.season.has_any_not_winter())
        rule_collector.set_location_rule(SecretNote.note_25, logic.season.has_any_not_winter() & logic.fishing.can_fish_at(Region.railroad)
                                         & logic.relationship.can_meet_any(NPC.abigail, NPC.caroline, ))
        rule_collector.set_location_rule(SecretNote.note_26,
                                         logic.building.has_wizard_building(WizardBuilding.junimo_hut) & logic.has(ArtisanGood.raisins)
                                         & logic.season.has_any_not_winter())
        rule_collector.set_location_rule(SecretNote.note_27, logic.region.can_reach(Region.mastery_cave))


def set_secret_note_gift_rule(logic: StardewLogic, rule_collector: StardewRuleCollector, secret_note_location: str) -> None:
    rule_collector.set_location_rule(secret_note_location, logic.gifts.can_fulfill(gift_requirements[secret_note_location]))


def set_hatsanity_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    hatsanity = content.features.hatsanity

    for hat in content.hats.values():
        if not hatsanity.is_included(hat):
            continue

        rule_collector.set_location_rule(hatsanity.to_location_name(hat), logic.hat.can_wear(hat))


def set_eatsanity_rules(all_location_names: Set[str], logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    if world_options.eatsanity == Eatsanity.preset_none:
        return
    for eat_location in locations.locations_by_tag[LocationTags.EATSANITY]:
        if eat_location.name not in all_location_names:
            continue
        eat_prefix = "Eat "
        drink_prefix = "Drink "
        if eat_location.name.startswith(eat_prefix):
            item_name = eat_location.name[len(eat_prefix):]
        elif eat_location.name.startswith(drink_prefix):
            item_name = eat_location.name[len(drink_prefix):]
        else:
            raise Exception(f"Eatsanity Location does not have a recognized prefix: '{eat_location.name}'")
        rule_collector.set_location_rule(eat_location.name, logic.has(item_name))


def set_endgame_locations_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, world_options: StardewValleyOptions):
    if not world_options.include_endgame_locations:
        return

    rule_collector.set_location_rule("Earth Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.earth_obelisk))
    rule_collector.set_location_rule("Water Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.water_obelisk))
    rule_collector.set_location_rule("Desert Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.desert_obelisk))
    rule_collector.set_location_rule("Junimo Hut Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.junimo_hut))
    rule_collector.set_location_rule("Gold Clock Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.gold_clock))
    rule_collector.set_location_rule("Purchase Return Scepter", logic.money.can_spend_at(Region.sewer, 2_000_000))
    rule_collector.set_location_rule("Pam House Blueprint",
                                     logic.money.can_spend_at(Region.carpenter, 500_000) & logic.grind.can_grind_item(950, Material.wood))
    rule_collector.set_location_rule("Forest To Beach Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    rule_collector.set_location_rule("Mountain Shortcuts Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    rule_collector.set_location_rule("Town To Tide Pools Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    rule_collector.set_location_rule("Tunnel To Backwoods Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    rule_collector.set_location_rule("Purchase Statue Of Endless Fortune", logic.can_purchase_statue_of_endless_fortune())
    rule_collector.set_location_rule("Purchase Catalogue", logic.money.can_spend_at(Region.pierre_store, 30_000))
    rule_collector.set_location_rule("Purchase Furniture Catalogue", logic.money.can_spend_at(Region.carpenter, 200_000))
    rule_collector.set_location_rule("Purchase Joja Furniture Catalogue",
                                     logic.action.can_speak_junimo() & logic.money.can_spend_at(Region.movie_theater, 25_000))
    rule_collector.set_location_rule("Purchase Junimo Catalogue",
                                     logic.action.can_speak_junimo() & logic.money.can_spend_at(LogicRegion.traveling_cart, 70_000))
    rule_collector.set_location_rule("Purchase Retro Catalogue", logic.money.can_spend_at(LogicRegion.traveling_cart, 110_000))
    # rule_collector.set_location_rule( "Find Trash Catalogue", logic) # No need, the region is enough
    rule_collector.set_location_rule("Purchase Wizard Catalogue", logic.money.can_spend_at(Region.sewer, 150_000))
    rule_collector.set_location_rule("Purchase Tea Set", logic.money.can_spend_at(LogicRegion.traveling_cart, 1_000_000) & logic.time.has_lived_max_months)
    if world_options.friendsanity == Friendsanity.option_all_with_marriage:
        rule_collector.set_location_rule("Purchase Abigail Portrait", logic.relationship.can_purchase_portrait(NPC.abigail))
        rule_collector.set_location_rule("Purchase Alex Portrait", logic.relationship.can_purchase_portrait(NPC.alex))
        rule_collector.set_location_rule("Purchase Elliott Portrait", logic.relationship.can_purchase_portrait(NPC.elliott))
        rule_collector.set_location_rule("Purchase Emily Portrait", logic.relationship.can_purchase_portrait(NPC.emily))
        rule_collector.set_location_rule("Purchase Haley Portrait", logic.relationship.can_purchase_portrait(NPC.haley))
        rule_collector.set_location_rule("Purchase Harvey Portrait", logic.relationship.can_purchase_portrait(NPC.harvey))
        rule_collector.set_location_rule("Purchase Krobus Portrait", logic.relationship.can_purchase_portrait(NPC.krobus))
        rule_collector.set_location_rule("Purchase Leah Portrait", logic.relationship.can_purchase_portrait(NPC.leah))
        rule_collector.set_location_rule("Purchase Maru Portrait", logic.relationship.can_purchase_portrait(NPC.maru))
        rule_collector.set_location_rule("Purchase Penny Portrait", logic.relationship.can_purchase_portrait(NPC.penny))
        rule_collector.set_location_rule("Purchase Sam Portrait", logic.relationship.can_purchase_portrait(NPC.sam))
        rule_collector.set_location_rule("Purchase Sebastian Portrait", logic.relationship.can_purchase_portrait(NPC.sebastian))
        rule_collector.set_location_rule("Purchase Shane Portrait", logic.relationship.can_purchase_portrait(NPC.shane))
    elif world_options.friendsanity != Friendsanity.option_none:
        rule_collector.set_location_rule("Purchase Spouse Portrait", logic.relationship.can_purchase_portrait())
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        rule_collector.set_location_rule("Island Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.island_obelisk))
        if world_options.special_order_locations == SpecialOrderLocations.option_board_qi:
            rule_collector.set_location_rule("Purchase Horse Flute", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            rule_collector.set_location_rule("Purchase Pierre's Missing Stocklist", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            rule_collector.set_location_rule("Purchase Key To The Town", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20))
            rule_collector.set_location_rule("Purchase Mini-Shipping Bin", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 60))
            rule_collector.set_location_rule("Purchase Exotic Double Bed", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            rule_collector.set_location_rule("Purchase Golden Egg", logic.received(AnimalProduct.golden_egg) & logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 100))


def set_friendsanity_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.features.friendsanity.is_enabled:
        return
    rule_collector.set_location_rule("Spouse Stardrop", logic.relationship.has_hearts_with_any_bachelor(13))
    rule_collector.set_location_rule("Have a Baby", logic.relationship.can_reproduce(1))
    rule_collector.set_location_rule("Have Another Baby", logic.relationship.can_reproduce(2))

    for villager in content.villagers.values():
        for heart in content.features.friendsanity.get_randomized_hearts(villager):
            rule = logic.relationship.can_earn_relationship(villager.name, heart)
            location_name = friendsanity.to_location_name(villager.name, heart)
            rule_collector.set_location_rule(location_name, rule)

    for heart in content.features.friendsanity.get_pet_randomized_hearts():
        rule = logic.pet.can_befriend_pet(heart)
        location_name = friendsanity.to_location_name(NPC.pet, heart)
        rule_collector.set_location_rule(location_name, rule)


def set_deepwoods_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ModNames.deepwoods):
        return

    rule_collector.set_location_rule("Breaking Up Deep Woods Gingerbread House", logic.tool.has_tool(Tool.axe, ToolMaterial.gold))
    rule_collector.set_location_rule("Chop Down a Deep Woods Iridium Tree", logic.tool.has_tool(Tool.axe, ToolMaterial.iridium))
    rule_collector.set_entrance_rule(DeepWoodsEntrance.use_woods_obelisk, logic.received("Woods Obelisk"))
    for depth in range(10, 100 + 10, 10):
        rule_collector.set_entrance_rule(move_to_woods_depth(depth), logic.mod.deepwoods.can_chop_to_depth(depth))
    rule_collector.set_location_rule("The Sword in the Stone", logic.mod.deepwoods.can_pull_sword() & logic.mod.deepwoods.can_chop_to_depth(100))


def set_magic_spell_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ModNames.magic):
        return

    rule_collector.set_location_rule("Analyze: Clear Debris", logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe))
    rule_collector.set_location_rule("Analyze: Till", logic.tool.has_tool(Tool.hoe))
    rule_collector.set_location_rule("Analyze: Water", logic.tool.has_tool(Tool.watering_can))
    rule_collector.set_location_rule("Analyze All Toil School Locations",
                                     logic.tool.has_tool(Tool.watering_can)
                                     & logic.tool.has_tool(Tool.hoe)
                                     & (logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe)))
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    rule_collector.set_location_rule("Analyze: Evac", logic.ability.can_mine_perfectly())
    rule_collector.set_location_rule("Analyze: Haste", logic.has("Coffee"))
    rule_collector.set_location_rule("Analyze: Heal", logic.has("Life Elixir"))
    rule_collector.set_location_rule("Analyze All Life School Locations",
                                     logic.has_all("Coffee", "Life Elixir") & logic.ability.can_mine_perfectly())
    rule_collector.set_location_rule("Analyze: Descend", logic.region.can_reach(Region.mines))
    rule_collector.set_location_rule("Analyze: Fireball", logic.has("Fire Quartz"))
    rule_collector.set_location_rule("Analyze: Frostbolt", logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    rule_collector.set_location_rule("Analyze All Elemental School Locations",
                                     logic.has("Fire Quartz") & logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    # rule_collector.set_location_rule( "Analyze: Lantern", player),)
    rule_collector.set_location_rule("Analyze: Tendrils", logic.region.can_reach(Region.farm))
    rule_collector.set_location_rule("Analyze: Shockwave", logic.has("Earth Crystal"))
    rule_collector.set_location_rule("Analyze All Nature School Locations", logic.has("Earth Crystal") & logic.region.can_reach("Farm")),
    rule_collector.set_location_rule("Analyze: Meteor", logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)),
    rule_collector.set_location_rule("Analyze: Lucksteal", logic.region.can_reach(Region.witch_hut))
    rule_collector.set_location_rule("Analyze: Bloodmana", logic.region.can_reach(Region.mines_floor_100))
    rule_collector.set_location_rule("Analyze All Eldritch School Locations",
                                     logic.region.can_reach_all(Region.witch_hut, Region.mines_floor_100, Region.farm) & logic.time.has_lived_months(12))
    rule_collector.set_location_rule("Analyze Every Magic School Location",
                                     logic.tool.has_tool(Tool.watering_can)
                                     & logic.tool.has_tool(Tool.hoe)
                                     & (logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe))
                                     & logic.has_all("Coffee", "Life Elixir", "Earth Crystal", "Fire Quartz")
                                     & logic.ability.can_mine_perfectly()
                                     & logic.fishing.can_fish(85)
                                     & logic.region.can_reach_all(Region.witch_hut, Region.mines_floor_100, Region.farm)
                                     & logic.time.has_lived_months(12))


def set_sve_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ModNames.sve):
        return

    rule_collector.set_entrance_rule(SVEEntrance.forest_to_lost_woods, logic.bundle.can_complete_community_center)
    rule_collector.set_entrance_rule(SVEEntrance.enter_summit, logic.mod.sve.has_iridium_bomb())
    rule_collector.set_entrance_rule(SVEEntrance.backwoods_to_grove, logic.mod.sve.has_any_rune())
    rule_collector.set_entrance_rule(SVEEntrance.badlands_to_cave, logic.has("Aegis Elixir") | logic.combat.can_fight_at_level(Performance.maximum))
    rule_collector.set_entrance_rule(SVEEntrance.forest_west_to_spring, logic.quest.can_complete_quest(Quest.magic_ink))
    rule_collector.set_entrance_rule(SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    rule_collector.set_entrance_rule(SVEEntrance.secret_woods_to_west, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    rule_collector.set_entrance_rule(SVEEntrance.grandpa_shed_to_interior, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    rule_collector.set_entrance_rule(SVEEntrance.aurora_warp_to_aurora, logic.received(SVERunes.nexus_aurora))
    rule_collector.set_entrance_rule(SVEEntrance.farm_warp_to_farm, logic.received(SVERunes.nexus_farm))
    rule_collector.set_entrance_rule(SVEEntrance.guild_warp_to_guild, logic.received(SVERunes.nexus_guild))
    rule_collector.set_entrance_rule(SVEEntrance.junimo_warp_to_junimo, logic.received(SVERunes.nexus_junimo))
    rule_collector.set_entrance_rule(SVEEntrance.spring_warp_to_spring, logic.received(SVERunes.nexus_spring))
    rule_collector.set_entrance_rule(SVEEntrance.outpost_warp_to_outpost, logic.received(SVERunes.nexus_outpost))
    rule_collector.set_entrance_rule(SVEEntrance.wizard_warp_to_wizard, logic.received(SVERunes.nexus_wizard))
    rule_collector.set_entrance_rule(SVEEntrance.use_purple_junimo, logic.relationship.has_hearts(ModNPC.apples, 10))
    rule_collector.set_entrance_rule(SVEEntrance.grandpa_interior_to_upstairs, logic.mod.sve.has_grandpa_shed_repaired())
    rule_collector.set_entrance_rule(SVEEntrance.use_bear_shop, (logic.mod.sve.can_buy_bear_recipe()))
    rule_collector.set_entrance_rule(SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    rule_collector.set_entrance_rule(SVEEntrance.museum_to_gunther_bedroom, logic.relationship.has_hearts(ModNPC.gunther, 2))
    rule_collector.set_entrance_rule(SVEEntrance.to_aurora_basement, logic.mod.quest.has_completed_aurora_vineyard_bundle())
    logic.mod.sve.initialize_rules()
    for location in logic.registry.sve_location_rules:
        rule_collector.set_location_rule(location, logic.registry.sve_location_rules[location])
    set_sve_ginger_island_rules(logic, rule_collector, content)
    set_boarding_house_rules(logic, rule_collector, content)


def set_sve_ginger_island_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    rule_collector.set_entrance_rule(SVEEntrance.summit_to_highlands, logic.mod.sve.has_marlon_boat())
    rule_collector.set_entrance_rule(SVEEntrance.wizard_to_fable_reef, logic.received(SVEQuestItem.fable_reef_portal))
    rule_collector.set_entrance_rule(SVEEntrance.highlands_to_cave,
                                     logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron) & logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    rule_collector.set_entrance_rule(SVEEntrance.highlands_to_pond, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))


def set_boarding_house_rules(logic: StardewLogic, rule_collector: StardewRuleCollector, content: StardewContent):
    if not content.is_enabled(ModNames.boarding_house):
        return
    rule_collector.set_entrance_rule(BoardingHouseEntrance.the_lost_valley_to_lost_valley_ruins, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
