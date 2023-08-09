import itertools
from typing import Dict, List

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from . import options, locations
from .bundles import Bundle
from .data.monster_data import all_monsters_by_category, all_monsters, all_monsters_by_name
from .logic.logic import StardewLogic
from .logic.tool_logic import tool_upgrade_prices
from .stardew_rule import And
from .strings.building_names import Building
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, DeepWoodsEntrance, AlecEntrance, MagicEntrance
from .data.museum_data import all_museum_items, all_mineral_items, all_artifact_items, dwarf_scrolls, skeleton_front, skeleton_middle, skeleton_back, \
    all_museum_items_by_name
from .strings.performance_names import Performance
from .strings.region_names import Region
from .mods.mod_data import ModNames
from .locations import LocationTags
from .options import StardewOptions
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.calendar_names import Weekday
from .strings.craftable_names import Craftable
from .strings.material_names import Material
from .strings.metal_names import MetalBar
from .strings.season_names import Season
from .strings.skill_names import ModSkill, Skill
from .strings.tool_names import Tool, ToolMaterial
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet


def set_rules(multi_world: MultiWorld, player: int, world_options: StardewOptions, logic: StardewLogic,
              current_bundles: Dict[str, Bundle]):
    all_location_names = list(location.name for location in multi_world.get_locations(player))
    # 22.756 - 23.789
    set_entrance_rules(logic, multi_world, player, world_options)
    # 34.761 - 35.568
    set_ginger_island_rules(logic, multi_world, player, world_options)
    # 36.281 - 38.453

    set_tool_rules(logic, multiworld, player, world_options)
    set_skills_rules(logic, multiworld, player, world_options)
    set_bundle_rules(current_bundles, logic, multiworld, player)
    set_building_rules(logic, multiworld, player, world_options)
    set_cropsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_story_quests_rules(all_location_names, logic, multiworld, player, world_options)
    set_special_order_rules(all_location_names, logic, multiworld, player, world_options)
    set_help_wanted_quests_rules(logic, multiworld, player, world_options)
    set_fishsanity_rules(all_location_names, logic, multiworld, player)
    set_museumsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_friendsanity_rules(all_location_names, logic, multiworld, player)
    set_backpack_rules(logic, multiworld, player, world_options)
    set_festival_rules(all_location_names, logic, multiworld, player)
    set_monstersanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_isolated_locations_rules(logic, multiworld, player)
    set_traveling_merchant_rules(logic, multiworld, player)
    set_arcade_machine_rules(logic, multiworld, player, world_options)
    set_deepwoods_rules(logic, multiworld, player, world_options)
    set_magic_spell_rules(logic, multiworld, player, world_options)
    # 1min52 - 1min53 # These times are for TestOptions
    # 1min36 - 1min38 # After the combat not duplicating a bunch of stuff
    # 1min28 - 1min30 # with the caching of combat rules
    # 1min25 - 1min26 # after caching seasons
    # 1min19 - 1min25 # moved some progression items to useful
    # 1min30 - 1min32 # with the flattening
    # 1min25 - 1min36 # with zero flattening
    # 1min36 - 1min40 # with complex flattening only in simplify


def set_isolated_locations_rules(logic: StardewLogic, multiworld, player):
    MultiWorldRules.add_rule(multiworld.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Have a Baby", player),
                             logic.relationship.can_reproduce(1).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Have Another Baby", player),
                             logic.relationship.can_reproduce(2).simplify())


def set_tool_rules(logic: StardewLogic, multiworld, player, world_options):
    # Those checks do not exist if ToolProgression is vanilla
    if world_options.tool_progression == ToolProgression.option_vanilla:
        return

    MultiWorldRules.add_rule(multiworld.get_location("Purchase Fiberglass Rod", player),
                             (logic.skill.has_level(Skill.fishing, 2) & logic.money.can_spend(1800)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Purchase Iridium Rod", player),
                             (logic.skill.has_level(Skill.fishing, 6) & logic.money.can_spend(7500)).simplify())

    materials = [None, "Copper", "Iron", "Gold", "Iridium"]
    tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.watering_can, Tool.trash_can]
    for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
        if previous is None:
            continue
        tool_upgrade_location = multiworld.get_location(f"{material} {tool} Upgrade", player)
        MultiWorldRules.set_rule(tool_upgrade_location, logic.has_tool(tool, previous).simplify())


def set_building_rules(logic: StardewLogic, multi_world, player, world_options):
    if world_options[options.BuildingProgression] != options.BuildingProgression.option_vanilla:
        for building in locations.locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            if building.mod_name is not None and building.mod_name not in world_options[options.Mods]:
                continue
            MultiWorldRules.set_rule(multi_world.get_location(building.name, player),
                                     logic.buildings.building_rules[building.name.replace(" Blueprint", "")].simplify())


def set_bundle_rules(current_bundles, logic: StardewLogic, multi_world, player):
    for bundle in current_bundles.values():
        location = multi_world.get_location(bundle.get_name_with_bundle(), player)
        rules = logic.can_complete_bundle(bundle.requirements, bundle.number_required)
        simplified_rules = rules.simplify()
        MultiWorldRules.set_rule(location, simplified_rules)
    MultiWorldRules.add_rule(multi_world.get_location("Complete Crafts Room", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.CRAFTS_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Pantry", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.PANTRY_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Fish Tank", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.FISH_TANK_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Boiler Room", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.BOILER_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Bulletin Board", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle
                                 in locations.locations_by_tag[LocationTags.BULLETIN_BOARD_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Vault", player),
                             And(logic.region.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.VAULT_BUNDLE]).simplify())


def set_skills_rules(logic: StardewLogic, multi_world, player, world_options):
    mods = world_options[options.Mods]
    if world_options[options.SkillProgression] == options.SkillProgression.option_vanilla:
        return
    for i in range(1, 11):
        set_vanilla_skill_rule_for_level(logic, multi_world, player, i)
        set_modded_skill_rule_for_level(logic, multi_world, player, mods, i)


def set_vanilla_skill_rule_for_level(logic: StardewLogic, multi_world, player, level: int):
    set_vanilla_skill_rule(logic, multi_world, player, Skill.farming, level)
    set_vanilla_skill_rule(logic, multi_world, player, Skill.fishing, level)
    set_vanilla_skill_rule(logic, multi_world, player, Skill.foraging, level)
    set_vanilla_skill_rule(logic, multi_world, player, Skill.mining, level)
    set_vanilla_skill_rule(logic, multi_world, player, Skill.combat, level)


def set_modded_skill_rule_for_level(logic: StardewLogic, multi_world, player, mods, level: int):
    if ModNames.luck_skill in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.luck, level)
    if ModNames.magic in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.magic, level)
    if ModNames.binning_skill in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.binning, level)
    if ModNames.cooking_skill in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.cooking, level)
    if ModNames.socializing_skill in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.socializing, level)
    if ModNames.archaeology in mods:
        set_modded_skill_rule(logic, multi_world, player, ModSkill.archaeology, level)


def get_skill_level_location(multi_world, player, skill: str, level: int):
    location_name = f"Level {level} {skill}"
    return multi_world.get_location(location_name, player)


def set_vanilla_skill_rule(logic: StardewLogic, multi_world, player, skill: str, level: int):
    rule = logic.skill.can_earn_level(skill, level).simplify()
    MultiWorldRules.set_rule(get_skill_level_location(multi_world, player, skill, level), rule.simplify())


def set_modded_skill_rule(logic: StardewLogic, multi_world, player, skill: str, level: int):
    rule = logic.mod.skill.can_earn_mod_skill_level(skill, level).simplify()
    MultiWorldRules.set_rule(get_skill_level_location(multi_world, player, skill, level), rule.simplify())


def set_entrance_rules(logic: StardewLogic, multi_world, player, world_options: StardewOptions):
    set_mines_floor_entrance_rules(logic, multiworld, player)
    set_skull_cavern_floor_entrance_rules(logic, multiworld, player)
    set_blacksmith_entrance_rules(logic, multiworld, player)
    set_skill_entrance_rules(logic, multiworld, player)
    set_traveling_merchant_day_rules(logic, multiworld, player)

    dangerous_mine_rule = logic.mine.has_mine_elevator_to_floor(120) & logic.region.can_reach(Region.qi_walnut_room)
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.dig_to_dangerous_mines_20, player),
                             dangerous_mine_rule.simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.dig_to_dangerous_mines_60, player),
                             dangerous_mine_rule.simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.dig_to_dangerous_mines_100, player),
                             dangerous_mine_rule.simplify())

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_tide_pools, player),
                             logic.received("Beach Bridge") | (logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_quarry, player),
                             logic.received("Bridge Repair") | (logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_secret_woods, player),
                             logic.tool.has_tool(Tool.axe, "Iron") | (logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.forest_to_sewer, player),
                             logic.wallet.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.town_to_sewer, player),
                             logic.wallet.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.take_bus_to_desert, player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_skull_cavern, player),
                             logic.received(Wallet.skull_key).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_dangerous_skull_cavern, player),
                             (logic.received(Wallet.skull_key) & logic.region.can_reach(Region.qi_walnut_room)).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_mines_dwarf, player),
                             logic.wallet.can_speak_dwarf() & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron))

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_desert_obelisk, player),
                             logic.received(Transportation.desert_obelisk).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_island_obelisk, player),
                             logic.received(Transportation.island_obelisk).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_farm_obelisk, player),
                             logic.received(Transportation.farm_obelisk).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.buy_from_traveling_merchant, player),
                             logic.has_traveling_merchant())

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_greenhouse, player),
                             logic.received("Greenhouse"))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_coop, player),
                             logic.buildings.has_building(Building.coop))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_barn, player),
                             logic.buildings.has_building(Building.barn))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_shed, player),
                             logic.buildings.has_building(Building.shed))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_slime_hutch, player),
                             logic.buildings.has_building(Building.slime_hutch))

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_adventurer_guild, player),
                             logic.received("Adventurer's Guild"))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_railroad, player),
                             logic.time.has_lived_months(2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_witch_warp_cave, player),
                             logic.received(Wallet.dark_talisman) | (logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_witch_hut, player),
                             (logic.has(ArtisanGood.void_mayonnaise) | logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_mutant_bug_lair, player),
                             ((logic.wallet.has_rusty_key() & logic.region.can_reach(Region.railroad) &
                               logic.relationship.can_meet(NPC.krobus) | logic.mod.magic.can_blink()).simplify()))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_casino, player),
                             logic.received("Club Card"))

    set_festival_entrance_rules(logic, multiworld, player)

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_harvey_room, player),
                             logic.relationship.has_hearts(NPC.harvey, 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_maru_room, player),
                             logic.relationship.has_hearts(NPC.maru, 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_sebastian_room, player),
                             (logic.relationship.has_hearts(NPC.sebastian, 2) | logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.forest_to_leah_cottage, player),
                             logic.relationship.has_hearts(NPC.leah, 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_elliott_house, player),
                             logic.relationship.has_hearts(NPC.elliott, 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_sunroom, player),
                             logic.relationship.has_hearts(NPC.caroline, 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_wizard_basement, player),
                             logic.relationship.has_hearts(NPC.wizard, 4))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_leo_treehouse, player),
                             logic.received("Treehouse"))
    if ModNames.alec in world_options[options.Mods]:
        MultiWorldRules.set_rule(multi_world.get_entrance(AlecEntrance.petshop_to_bedroom, player),
                                 (logic.relationship.has_hearts(ModNPC.alec, 2) | logic.mod.magic.can_blink()).simplify())


def set_mines_floor_entrance_rules(logic, multiworld, player):
    for floor in range(5, 120 + 5, 5):
        rule = logic.has_mine_elevator_to_floor(floor - 10)
        if floor == 5 or floor == 45 or floor == 85:
            rule = rule & logic.can_progress_in_the_mines_from_floor(floor)
        entrance = multiworld.get_entrance(dig_to_mines_floor(floor), player)
        MultiWorldRules.set_rule(entrance, rule.simplify())


def set_skull_cavern_floor_entrance_rules(logic, multiworld, player):
    for floor in range(25, 200 + 25, 25):
        rule = has_skull_cavern_elevator_to_floor(logic, floor - 25)
        if floor == 5 or floor == 45 or floor == 85:
            rule = rule & logic.can_progress_in_the_skull_cavern_from_floor(floor)
        entrance = multiworld.get_entrance(dig_to_skull_floor(floor), player)
        MultiWorldRules.set_rule(entrance, rule.simplify())


def set_blacksmith_entrance_rules(logic, multiworld, player):
    set_blacksmith_upgrade_rule(logic, multiworld, player, Entrance.blacksmith_copper, MetalBar.copper, ToolMaterial.copper)
    set_blacksmith_upgrade_rule(logic, multiworld, player, Entrance.blacksmith_iron, MetalBar.iron, ToolMaterial.iron)
    set_blacksmith_upgrade_rule(logic, multiworld, player, Entrance.blacksmith_gold, MetalBar.gold, ToolMaterial.gold)
    set_blacksmith_upgrade_rule(logic, multiworld, player, Entrance.blacksmith_iridium, MetalBar.iridium, ToolMaterial.iridium)


def set_skill_entrance_rules(logic, multiworld, player):
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.farming, player),
                             logic.can_get_farming_xp().simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.fishing, player),
                             logic.can_get_fishing_xp().simplify())


def set_blacksmith_upgrade_rule(logic, multiworld, player, entrance_name: str, item_name: str, tool_material: str):
    material_entrance = multiworld.get_entrance(entrance_name, player)
    upgrade_rule = logic.has(item_name) & logic.can_spend_money(tool_upgrade_prices[tool_material])
    MultiWorldRules.set_rule(material_entrance, upgrade_rule.simplify())


def set_festival_entrance_rules(logic, multiworld, player):
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_egg_festival, player), logic.has_season(Season.spring))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_flower_dance, player), logic.has_season(Season.spring))

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_luau, player), logic.has_season(Season.summer))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_moonlight_jellies, player), logic.has_season(Season.summer))

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_fair, player), logic.has_season(Season.fall))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_spirit_eve, player), logic.has_season(Season.fall))

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_festival_of_ice, player), logic.has_season(Season.winter))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_night_market, player), logic.has_season(Season.winter))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.attend_winter_star, player), logic.has_season(Season.winter))


def set_ginger_island_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    set_island_entrances_rules(logic, multiworld, player)
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    set_boat_repair_rules(logic, multi_world, player)
    set_island_parrot_rules(logic, multi_world, player)
    MultiWorldRules.add_rule(multi_world.get_location("Open Professor Snail Cave", player),
                             logic.has(Craftable.cherry_bomb).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Island Field Office", player),
                             logic.can_complete_field_office().simplify())


def set_boat_repair_rules(logic: StardewLogic, multi_world, player):
    MultiWorldRules.add_rule(multi_world.get_location("Repair Boat Hull", player),
                             logic.has(Material.hardwood).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Repair Boat Anchor", player),
                             logic.has(MetalBar.iridium).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Repair Ticket Machine", player),
                             logic.has(ArtisanGood.battery_pack).simplify())


def set_island_entrances_rules(logic: StardewLogic, multi_world, player):
    boat_repaired = logic.received(Transportation.boat_repair).simplify()
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.fish_shop_to_boat_tunnel, player),
                             boat_repaired)
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.boat_to_ginger_island, player),
                             boat_repaired)
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_south_to_west, player),
                             logic.received("Island West Turtle").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_south_to_north, player),
                             logic.received("Island North Turtle").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_west_to_islandfarmhouse, player),
                             logic.received("Island Farmhouse").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_west_to_gourmand_cave, player),
                             logic.received("Island Farmhouse").simplify())
    dig_site_rule = logic.received("Dig Site Bridge").simplify()
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_north_to_dig_site, player), dig_site_rule)
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.dig_site_to_professor_snail_cave, player),
                             logic.received("Open Professor Snail Cave").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_island_trader, player),
                             logic.received("Island Trader").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_south_to_southeast, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_island_resort, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_west_to_qi_walnut_room, player),
                             logic.received("Qi Walnut Room").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_north_to_volcano, player),
                             (logic.tool.can_water(0) | logic.received("Volcano Bridge") |
                              logic.mod.magic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.volcano_to_secret_beach, player),
                             logic.tool.can_water(2).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.climb_to_volcano_5, player),
                             (logic.ability.can_mine_perfectly() & logic.tool.can_water(1)).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_volcano_dwarf, player),
                             logic.wallet.can_speak_dwarf())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.climb_to_volcano_10, player),
                             (logic.ability.can_mine_perfectly() & logic.tool.can_water(1)).simplify())
    parrots = [Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_jungle_to_volcano,
               Entrance.parrot_express_dig_site_to_volcano, Entrance.parrot_express_docks_to_dig_site,
               Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_volcano_to_dig_site,
               Entrance.parrot_express_docks_to_jungle, Entrance.parrot_express_dig_site_to_jungle,
               Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_jungle_to_docks,
               Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_volcano_to_docks]
    parrot_express_rule = logic.received(Transportation.parrot_express).simplify()
    parrot_express_to_dig_site_rule = dig_site_rule & parrot_express_rule
    for parrot in parrots:
        if "Dig Site" in parrot:
            MultiWorldRules.set_rule(multiworld.get_entrance(parrot, player), parrot_express_to_dig_site_rule)
        else:
            MultiWorldRules.set_rule(multiworld.get_entrance(parrot, player), parrot_express_rule)


def set_island_parrot_rules(logic: StardewLogic, multi_world, player):
    has_walnut = logic.has_walnut(1).simplify()
    has_5_walnut = logic.has_walnut(5).simplify()
    has_10_walnut = logic.has_walnut(10).simplify()
    has_20_walnut = logic.has_walnut(20).simplify()
    MultiWorldRules.add_rule(multi_world.get_location("Leo's Parrot", player),
                             has_walnut)
    MultiWorldRules.add_rule(multi_world.get_location("Island West Turtle", player),
                             has_10_walnut & logic.received("Island North Turtle"))
    MultiWorldRules.add_rule(multi_world.get_location("Island Farmhouse", player),
                             has_20_walnut)
    MultiWorldRules.add_rule(multi_world.get_location("Island Mailbox", player),
                             has_5_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multi_world.get_location(Transportation.farm_obelisk, player),
                             has_20_walnut & logic.received("Island Mailbox"))
    MultiWorldRules.add_rule(multi_world.get_location("Dig Site Bridge", player),
                             has_10_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multi_world.get_location("Island Trader", player),
                             has_10_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multi_world.get_location("Volcano Bridge", player),
                             has_5_walnut & logic.received("Island West Turtle") &
                             logic.region.can_reach(Region.volcano_floor_10))
    MultiWorldRules.add_rule(multi_world.get_location("Volcano Exit Shortcut", player),
                             has_5_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multi_world.get_location("Island Resort", player),
                             has_20_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multi_world.get_location(Transportation.parrot_express, player),
                             has_10_walnut)


def set_cropsanity_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, world_options: StardewOptions):
    if world_options[options.Cropsanity] == options.Cropsanity.option_disabled:
        return

    harvest_prefix = "Harvest "
    harvest_prefix_length = len(harvest_prefix)
    for harvest_location in locations.locations_by_tag[LocationTags.CROPSANITY]:
        if harvest_location.name in all_location_names and (harvest_location.mod_name is None or harvest_location.mod_name in world_options[options.Mods]):
            crop_name = harvest_location.name[harvest_prefix_length:]
            MultiWorldRules.set_rule(multi_world.get_location(harvest_location.name, player),
                                     logic.has(crop_name).simplify())


def set_story_quests_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, world_options: StardewOptions):
    for quest in locations.locations_by_tag[LocationTags.QUEST]:
        if quest.name in all_location_names and (quest.mod_name is None or quest.mod_name in world_options[options.Mods]):
            MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                     logic.quest_rules[quest.name].simplify())


def set_special_order_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player,
                            world_options: StardewOptions):
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_disabled:
        return
    board_rule = logic.received("Special Order Board") & logic.time.has_lived_months(4)
    for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
        if board_order.name in all_location_names:
            order_rule = board_rule & logic.special_order.special_order_rules[board_order.name]
            MultiWorldRules.set_rule(multi_world.get_location(board_order.name, player), order_rule.simplify())

    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        return
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_board_only:
        return
    qi_rule = logic.region.can_reach(Region.qi_walnut_room) & logic.time.has_lived_months(8)
    for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
        if qi_order.name in all_location_names:
            order_rule = qi_rule & logic.special_order.special_order_rules[qi_order.name]
            MultiWorldRules.set_rule(multi_world.get_location(qi_order.name, player), order_rule.simplify())


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, multi_world, player, world_options):
    help_wanted_number = world_options[options.HelpWantedLocations]
    for i in range(0, help_wanted_number):
        set_number = i // 7
        month_rule = logic.time.has_lived_months(set_number).simplify()
        quest_number = set_number + 1
        quest_number_in_set = i % 7
        if quest_number_in_set < 4:
            quest_number = set_number * 4 + quest_number_in_set + 1
            set_help_wanted_delivery_rule(multi_world, player, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(multi_world, player, month_rule, quest_number)


def set_help_wanted_delivery_rule(multi_world, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    MultiWorldRules.set_rule(multi_world.get_location(location_name, player), month_rule)


def set_help_wanted_gathering_rule(multi_world, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    MultiWorldRules.set_rule(multi_world.get_location(location_name, player), month_rule)


def set_help_wanted_fishing_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), month_rule.simplify())


def set_help_wanted_slay_monsters_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), month_rule.simplify())


def set_fishsanity_rules(all_location_names: List[str], logic: StardewLogic, multi_world: MultiWorld, player: int):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            MultiWorldRules.set_rule(multi_world.get_location(fish_location.name, player),
                                     logic.has(fish_name).simplify())


def set_museumsanity_rules(all_location_names: List[str], logic: StardewLogic, multi_world: MultiWorld, player: int,
                           world_options: StardewOptions):
    museum_prefix = "Museumsanity: "
    if world_options[options.Museumsanity] == options.Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, multi_world, museum_milestone, museum_prefix, player)
    elif world_options[options.Museumsanity] != options.Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, multi_world, museum_prefix, player)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, multi_world, museum_prefix, player):
    all_donations = sorted(locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 5 // number_donations
            rule = logic.can_find_museum_item(all_museum_items_by_name[donation_name]) & logic.received("Traveling Merchant Metal Detector",
                                                                                                          required_detectors)
            MultiWorldRules.set_rule(multiworld.get_location(museum_location.name, player),
                                     rule.simplify())
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, multi_world: MultiWorld, museum_milestone, museum_prefix: str,
                              player: int):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    metal_detector = "Traveling Merchant Metal Detector"
    rule = None
    if milestone_name.endswith(donations_suffix):
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items, logic.can_find_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_museum_minerals, logic.can_find_museum_minerals)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_museum_artifacts, logic.can_find_museum_artifacts)
    elif milestone_name == "Dwarf Scrolls":
        rule = And([logic.can_find_museum_item(item) for item in dwarf_scrolls]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Front":
        rule = And([logic.can_find_museum_item(item) for item in skeleton_front]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Middle":
        rule = And([logic.can_find_museum_item(item) for item in skeleton_middle]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Back":
        rule = And([logic.can_find_museum_item(item) for item in skeleton_back]) & logic.received(metal_detector, 4)
    elif milestone_name == "Ancient Seed":
        rule = logic.can_find_museum_item(Artifact.ancient_seed) & logic.received(metal_detector, 4)
    if rule is None:
        return
    MultiWorldRules.set_rule(multi_world.get_location(museum_milestone.name, player), rule.simplify())


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = "Traveling Merchant Metal Detector"
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 5 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    if world_options[options.BackpackProgression] != options.BackpackProgression.option_vanilla:
        MultiWorldRules.set_rule(multi_world.get_location("Large Pack", player),
                                 logic.money.can_spend(2000).simplify())
        MultiWorldRules.set_rule(multi_world.get_location("Deluxe Pack", player),
                                 (logic.money.can_spend(10000) & logic.received("Progressive Backpack")).simplify())
        if ModNames.big_backpack in world_options[options.Mods]:
            MultiWorldRules.set_rule(multi_world.get_location("Premium Pack", player),
                                     (logic.money.can_spend(150000) &
                                      logic.received("Progressive Backpack", 2)).simplify())


def set_festival_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player):
    festival_locations = []
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            MultiWorldRules.set_rule(multi_world.get_location(festival.name, player),
                                     logic.festival_rules[festival.name].simplify())


monster_eradication_prefix = "Monster Eradication: "


def set_monstersanity_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, world_options):
    monstersanity_option = world_options[options.Monstersanity]
    if monstersanity_option == options.Monstersanity.option_none:
        return

    if monstersanity_option == options.Monstersanity.option_one_per_monster or monstersanity_option == options.Monstersanity.option_split_goals:
        set_monstersanity_monster_rules(all_location_names, logic, multi_world, player, monstersanity_option)
        return

    if monstersanity_option == options.Monstersanity.option_progressive_goals:
        set_monstersanity_progressive_category_rules(all_location_names, logic, multi_world, player, monstersanity_option)
        return

    set_monstersanity_category_rules(all_location_names, logic, multi_world, player, monstersanity_option)


def set_monstersanity_monster_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, monstersanity_option):
    for monster_name in all_monsters_by_name:
        location_name = f"{monster_eradication_prefix}{monster_name}"
        if location_name not in all_location_names:
            continue
        location = multi_world.get_location(location_name, player)
        rule = logic.combat.can_kill_monster(all_monsters_by_name[monster_name])
        if monstersanity_option == options.Monstersanity.option_split_goals:
            rule = rule & logic.time.has_lived_max_months()
        MultiWorldRules.set_rule(location, rule.simplify())


def set_monstersanity_progressive_category_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, monstersanity_option):
    for monster_category in all_monsters_by_category:
        location_names = [name for name in all_location_names if name.startswith(monster_eradication_prefix) and name.endswith(monster_category)]
        if not location_names:
            continue
        location_names = sorted(location_names, key=lambda name: get_monster_eradication_number(name, monster_category))
        for i in range(5):
            location_name = location_names[i]
            if location_name not in all_location_names:
                continue
            location = multi_world.get_location(location_name, player)
            if i < 3:
                rule = logic.combat.can_kill_any_monster(all_monsters_by_category[monster_category]) & logic.time.has_lived_months((i+1) * 2)
            else:
                rule = logic.combat.can_kill_all_monsters(all_monsters_by_category[monster_category]) & logic.time.has_lived_months(i * 3)
            MultiWorldRules.set_rule(location, rule.simplify())


def get_monster_eradication_number(location_name, monster_category) -> int:
    number = location_name[len(monster_eradication_prefix):-len(monster_category)]
    number = number.strip()
    if number.isdigit():
        return int(number)
    return 1000


def set_monstersanity_category_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player, monstersanity_option):
    for monster_category in all_monsters_by_category:
        location_name = f"{monster_eradication_prefix}{monster_category}"
        if location_name not in all_location_names:
            continue
        location = multi_world.get_location(location_name, player)
        if monstersanity_option == options.Monstersanity.option_one_per_category:
            rule = logic.combat.can_kill_any_monster(all_monsters_by_category[monster_category])
        else:
            rule = logic.combat.can_kill_all_monsters(all_monsters_by_category[monster_category]) & logic.time.has_lived_max_months()
        MultiWorldRules.set_rule(location, rule.simplify())


def set_traveling_merchant_day_rules(logic: StardewLogic, multi_world: MultiWorld, player: int):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        entrance_name = f"Buy from Traveling Merchant {day}"
        MultiWorldRules.set_rule(multiworld.get_entrance(entrance_name, player), logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.play_junimo_kart, player),
                             logic.received(Wallet.skull_key).simplify())
    if world_options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
        return

    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.play_junimo_kart, player),
                             logic.has("Junimo Kart Small Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.reach_junimo_kart_2, player),
                             logic.has("Junimo Kart Medium Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.reach_junimo_kart_3, player),
                             logic.has("Junimo Kart Big Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Junimo Kart: Sunset Speedway (Victory)", player),
                             logic.has("Junimo Kart Max Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.play_journey_of_the_prairie_king, player),
                             logic.has("JotPK Small Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.reach_jotpk_world_2, player),
                             logic.has("JotPK Medium Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.reach_jotpk_world_3, player),
                             logic.has("JotPK Big Buff").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Journey of the Prairie King Victory", player),
                             logic.has("JotPK Max Buff").simplify())


def set_friendsanity_rules(all_location_names: List[str], logic: StardewLogic, multi_world: MultiWorld, player: int):
    friend_prefix = "Friendsanity: "
    friend_suffix = " <3"
    for friend_location in locations.locations_by_tag[LocationTags.FRIENDSANITY]:
        if not friend_location.name in all_location_names:
            continue
        friend_location_without_prefix = friend_location.name[len(friend_prefix):]
        friend_location_trimmed = friend_location_without_prefix[:friend_location_without_prefix.index(friend_suffix)]
        split_index = friend_location_trimmed.rindex(" ")
        friend_name = friend_location_trimmed[:split_index]
        num_hearts = int(friend_location_trimmed[split_index + 1:])
        MultiWorldRules.set_rule(multi_world.get_location(friend_location.name, player),
                                 logic.relationship.can_earn_relationship(friend_name, num_hearts).simplify())


def set_deepwoods_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options: StardewOptions):
    if ModNames.deepwoods in world_options[options.Mods]:
        MultiWorldRules.add_rule(multi_world.get_location("Breaking Up Deep Woods Gingerbread House", player),
                                 logic.tool.has_tool(Tool.axe, "Gold") & logic.mod.deepwoods.can_reach_woods_depth(50).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Chop Down a Deep Woods Iridium Tree", player),
                                 logic.tool.has_tool(Tool.axe, "Iridium").simplify())
        MultiWorldRules.set_rule(multi_world.get_entrance(DeepWoodsEntrance.use_woods_obelisk, player),
                                 logic.received("Woods Obelisk").simplify())
        for depth in range(10, 100 + 10, 10):
            MultiWorldRules.set_rule(multi_world.get_entrance(move_to_woods_depth(depth), player),
                                     logic.mod.deepwoods.can_chop_to_depth(depth).simplify())


def set_magic_spell_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options: StardewOptions):
    if ModNames.magic not in world_options[options.Mods]:
        return

    MultiWorldRules.set_rule(multiworld.get_entrance(MagicEntrance.store_to_altar, player),
                             (logic.relationship.has_hearts(NPC.wizard, 3) &
                              logic.region.can_reach(Region.wizard_tower)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Clear Debris", player),
                             (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Till", player),
                             logic.tool.has_tool("Hoe", "Basic").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Water", player),
                             logic.tool.has_tool("Watering Can", "Basic").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Toil School Locations", player),
                             (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
                              & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic"))).simplify())
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Evac", player),
                             logic.ability.can_mine_perfectly().simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Haste", player),
                             logic.has("Coffee").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Heal", player),
                             logic.has("Life Elixir").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Life School Locations", player),
                             (logic.has("Coffee") & logic.has("Life Elixir")
                              & logic.ability.can_mine_perfectly()).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Descend", player),
                             logic.region.can_reach(Region.mines).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Fireball", player),
                             logic.has("Fire Quartz").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Frostbite", player),
                             (logic.region.can_reach(Region.mines_floor_60) & logic.skill.can_fish(85)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Elemental School Locations", player),
                             (logic.has("Fire Quartz") & logic.region.can_reach(Region.mines_floor_60) & logic.skill.can_fish(85)).simplify())
    # MultiWorldRules.add_rule(multiworld.get_location("Analyze: Lantern", player),)
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Tendrils", player),
                             logic.region.can_reach(Region.farm).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Shockwave", player),
                             logic.has("Earth Crystal").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Nature School Locations", player),
                             (logic.has("Earth Crystal") & logic.region.can_reach("Farm")).simplify()),
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Meteor", player),
                             (logic.region.can_reach(Region.farm) & logic.has_lived_months(12)).simplify()),
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Lucksteal", player),
                             logic.region.can_reach(Region.witch_hut).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Bloodmana", player),
                             logic.region.can_reach(Region.mines_floor_100).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Eldritch School Locations", player),
                             (logic.region.can_reach(Region.witch_hut) &
                              logic.region.can_reach(Region.mines_floor_100) &
                              logic.region.can_reach(Region.farm) & logic.has_lived_months(12)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze Every Magic School Location", player),
                             (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
                              & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")) &
                              logic.has("Coffee") & logic.has("Life Elixir")
                              & logic.ability.can_mine_perfectly() & logic.has("Earth Crystal") &
                              logic.has("Fire Quartz") & logic.skill.can_fish(85) &
                              logic.region.can_reach(Region.witch_hut) &
                              logic.region.can_reach(Region.mines_floor_100) &
                              logic.region.can_reach(Region.farm) & logic.has_lived_months(12)).simplify())
