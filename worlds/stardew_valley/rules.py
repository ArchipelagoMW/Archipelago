import itertools
from typing import Dict, List

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from . import options, locations
from .bundles import Bundle
from worlds.stardew_valley.strings.entrance_names import dig_to_mines_floor, Entrance, move_to_woods_depth, DeepWoodsEntrance, AlecEntrance
from .data.museum_data import all_museum_items, all_mineral_items, all_artifact_items, \
    dwarf_scrolls, skeleton_front, \
    skeleton_middle, skeleton_back, all_museum_items_by_name
from worlds.stardew_valley.strings.region_names import Region
from .mods.mod_data import ModNames
from .locations import LocationTags
from .logic import StardewLogic, And, tool_upgrade_prices
from .options import StardewOptions
from .strings.calendar_names import Weekday
from .strings.skill_names import ModSkill, Skill
from .strings.tool_names import Tool, ToolMaterial


def set_rules(multi_world: MultiWorld, player: int, world_options: StardewOptions, logic: StardewLogic,
              current_bundles: Dict[str, Bundle]):
    all_location_names = list(location.name for location in multi_world.get_locations(player))

    set_entrance_rules(logic, multi_world, player, world_options)

    set_ginger_island_rules(logic, multi_world, player, world_options)

    # Those checks do not exist if ToolProgression is vanilla
    if world_options[options.ToolProgression] != options.ToolProgression.option_vanilla:
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Fiberglass Rod", player),
                                 (logic.has_skill_level(Skill.fishing, 2) & logic.can_spend_money(1800)).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Iridium Rod", player),
                                 (logic.has_skill_level(Skill.fishing, 6) & logic.can_spend_money(7500)).simplify())

        materials = [None, "Copper", "Iron", "Gold", "Iridium"]
        tool = ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]
        for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
            if previous is None:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") &
                                          logic.can_spend_money(tool_upgrade_prices[material])).simplify())
            else:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") & logic.has_tool(tool, previous) &
                                          logic.can_spend_money(tool_upgrade_prices[material])).simplify())

    set_skills_rules(logic, multi_world, player, world_options)

    # Bundles
    for bundle in current_bundles.values():
        location = multi_world.get_location(bundle.get_name_with_bundle(), player)
        rules = logic.can_complete_bundle(bundle.requirements, bundle.number_required)
        simplified_rules = rules.simplify()
        MultiWorldRules.set_rule(location, simplified_rules)
    MultiWorldRules.add_rule(multi_world.get_location("Complete Crafts Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.CRAFTS_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Pantry", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.PANTRY_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Fish Tank", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.FISH_TANK_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Boiler Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.BOILER_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Bulletin Board", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle
                                 in locations.locations_by_tag[LocationTags.BULLETIN_BOARD_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Vault", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.VAULT_BUNDLE]).simplify())

    # Buildings
    if world_options[options.BuildingProgression] != options.BuildingProgression.option_vanilla:
        for building in locations.locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            if building.mod_name is not None and building.mod_name not in world_options[options.Mods]:
                continue
            MultiWorldRules.set_rule(multi_world.get_location(building.name, player),
                                     logic.building_rules[building.name.replace(" Blueprint", "")].simplify())

    set_story_quests_rules(all_location_names, logic, multi_world, player, world_options)
    set_special_order_rules(all_location_names, logic, multi_world, player, world_options)
    set_help_wanted_quests_rules(logic, multi_world, player, world_options)
    set_fishsanity_rules(all_location_names, logic, multi_world, player)
    set_museumsanity_rules(all_location_names, logic, multi_world, player, world_options)
    set_friendsanity_rules(all_location_names, logic, multi_world, player)
    set_backpack_rules(logic, multi_world, player, world_options)
    set_festival_rules(all_location_names, logic, multi_world, player)

    MultiWorldRules.add_rule(multi_world.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())

    set_traveling_merchant_rules(logic, multi_world, player)
    set_arcade_machine_rules(logic, multi_world, player, world_options)
    set_deepwoods_rules(logic, multi_world, player, world_options)


def set_skills_rules(logic, multi_world, player, world_options):
    # Skills
    if world_options[options.SkillProgression] != options.SkillProgression.option_vanilla:
        for i in range(1, 11):
            set_skill_rule(logic, multi_world, player, Skill.farming, i)
            set_skill_rule(logic, multi_world, player, Skill.fishing, i)
            set_skill_rule(logic, multi_world, player, Skill.foraging, i)
            set_skill_rule(logic, multi_world, player, Skill.mining, i)
            set_skill_rule(logic, multi_world, player, Skill.combat, i)

            # Modded Skills
            if ModNames.luck_skill in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.luck, i)
            if ModNames.magic in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.magic, i)
            if ModNames.binning_skill in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.binning, i)
            if ModNames.cooking_skill in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.cooking, i)
            if ModNames.socializing_skill in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.socializing, i)
            if ModNames.archaeology in world_options[options.Mods]:
                set_skill_rule(logic, multi_world, player, ModSkill.archaeology, i)


def set_skill_rule(logic, multi_world, player, skill: str, level: int):
    location_name = f"Level {level} {skill}"
    location = multi_world.get_location(location_name, player)
    rule = logic.can_earn_skill_level(skill, level).simplify()
    MultiWorldRules.set_rule(location, rule)


def set_entrance_rules(logic, multi_world, player, world_options: StardewOptions):
    for floor in range(5, 120 + 5, 5):
        MultiWorldRules.set_rule(multi_world.get_entrance(dig_to_mines_floor(floor), player),
                                 logic.can_mine_to_floor(floor).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_tide_pools, player),
                             logic.received("Beach Bridge") | (logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_quarry, player),
                             logic.received("Bridge Repair") | (logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_secret_woods, player),
                             logic.has_tool("Axe", "Iron") | (logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.forest_to_sewers, player),
                             logic.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.town_to_sewers, player),
                             logic.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.take_bus_to_desert, player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_skull_cavern, player),
                             logic.received("Skull Key").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mine_to_skull_cavern_floor_100, player),
                             logic.can_mine_perfectly_in_the_skull_cavern().simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_mines_dwarf, player),
                             logic.can_speak_dwarf() & logic.has_tool(Tool.pickaxe, ToolMaterial.iron))

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_desert_obelisk, player),
                             logic.received("Desert Obelisk").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_island_obelisk, player),
                             logic.received("Island Obelisk").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_farm_obelisk, player),
                             logic.received("Farm Obelisk").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.buy_from_traveling_merchant, player),
                             logic.has_traveling_merchant())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_greenhouse, player),
                             logic.received("Greenhouse"))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_adventurer_guild, player),
                             logic.received("Adventurer's Guild"))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_railroad, player),
                             logic.has_lived_months(2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_witch_warp_cave, player),
                             logic.received("Dark Talisman") | (logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_witch_hut, player),
                             (logic.has("Void Mayonnaise") | logic.can_blink()).simplify())

    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_harvey_room, player),
                             logic.has_relationship("Harvey", 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.mountain_to_maru_room, player),
                             logic.has_relationship("Maru", 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_sebastian_room, player),
                             (logic.has_relationship("Sebastian", 2) | logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.forest_to_leah_cottage, player),
                             logic.has_relationship("Leah", 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_elliott_house, player),
                             logic.has_relationship("Elliott", 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_sunroom, player),
                             logic.has_relationship("Caroline", 2))
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.enter_wizard_basement, player),
                             logic.has_relationship("Wizard", 4))
    if ModNames.alec in world_options[options.Mods]:
        MultiWorldRules.set_rule(multi_world.get_entrance(AlecEntrance.petshop_to_bedroom, player),
                                 (logic.has_relationship("Alec", 2) | logic.can_blink()).simplify())


def set_ginger_island_rules(logic: StardewLogic, multi_world, player, world_options: StardewOptions):
    set_island_entrances_rules(logic, multi_world, player)
    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        return

    set_boat_repair_rules(logic, multi_world, player)
    set_island_parrot_rules(logic, multi_world, player)


def set_boat_repair_rules(logic: StardewLogic, multi_world, player):
    MultiWorldRules.add_rule(multi_world.get_location("Repair Boat Hull", player),
                             logic.has("Hardwood").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Repair Boat Anchor", player),
                             logic.has("Iridium Bar").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Repair Ticket Machine", player),
                             logic.has("Battery Pack").simplify())


def set_island_entrances_rules(logic: StardewLogic, multi_world, player):
    boat_repaired = logic.received("Boat Repair").simplify()
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
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_north_to_dig_site, player),
                             logic.received("Dig Site Bridge").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_island_trader, player),
                             logic.received("Island Trader").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_south_to_southeast, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.use_island_resort, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_west_to_qi_walnut_room, player),
                             logic.received("Qi Walnut Room").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.island_north_to_volcano, player),
                             (logic.can_water(0) | logic.received("Volcano Bridge") |
                              logic.can_blink()).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.volcano_to_secret_beach, player),
                             logic.can_water(2).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.climb_to_volcano_5, player),
                             (logic.can_mine_perfectly() & logic.can_water(1)).simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.talk_to_volcano_dwarf, player),
                             logic.can_speak_dwarf())
    MultiWorldRules.set_rule(multi_world.get_entrance(Entrance.climb_to_volcano_10, player),
                             (logic.can_mine_perfectly() & logic.can_water(1) & logic.received("Volcano Exit Shortcut")).simplify())
    parrots = [Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_jungle_to_volcano,
               Entrance.parrot_express_dig_site_to_volcano, Entrance.parrot_express_docks_to_dig_site,
               Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_volcano_to_dig_site,
               Entrance.parrot_express_docks_to_jungle, Entrance.parrot_express_dig_site_to_jungle,
               Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_jungle_to_docks,
               Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_volcano_to_docks]
    for parrot in parrots:
        MultiWorldRules.set_rule(multi_world.get_entrance(parrot, player), logic.received("Parrot Express").simplify())


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
    MultiWorldRules.add_rule(multi_world.get_location("Farm Obelisk", player),
                             has_20_walnut & logic.received("Island Mailbox"))
    MultiWorldRules.add_rule(multi_world.get_location("Dig Site Bridge", player),
                             has_10_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multi_world.get_location("Island Trader", player),
                             has_10_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multi_world.get_location("Volcano Bridge", player),
                             has_5_walnut & logic.received("Island West Turtle") &
                             logic.can_reach_region(Region.volcano_floor_10))
    MultiWorldRules.add_rule(multi_world.get_location("Volcano Exit Shortcut", player),
                             has_5_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multi_world.get_location("Island Resort", player),
                             has_20_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multi_world.get_location("Parrot Express", player),
                             has_10_walnut)


def set_story_quests_rules(all_location_names: List[str], logic, multi_world, player, world_options: StardewOptions):
    for quest in locations.locations_by_tag[LocationTags.QUEST]:
        if quest.name in all_location_names and (quest.mod_name is None or quest.mod_name in world_options[options.Mods]):
            MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                     logic.quest_rules[quest.name].simplify())


def set_special_order_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player,
                            world_options: StardewOptions):
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_disabled:
        return
    board_rule = logic.received("Special Order Board") & logic.has_lived_months(4)
    for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
        if board_order.name in all_location_names:
            order_rule = board_rule & logic.special_order_rules[board_order.name]
            MultiWorldRules.set_rule(multi_world.get_location(board_order.name, player), order_rule.simplify())

    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        return
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_board_only:
        return
    qi_rule = logic.can_reach_region(Region.qi_walnut_room) & logic.has_lived_months(8)
    for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
        if qi_order.name in all_location_names:
            order_rule = qi_rule & logic.special_order_rules[qi_order.name]
            MultiWorldRules.set_rule(multi_world.get_location(qi_order.name, player), order_rule.simplify())


def set_help_wanted_quests_rules(logic: StardewLogic, multi_world, player, world_options):
    desired_number_help_wanted: int = world_options[options.HelpWantedLocations] // 7
    for i in range(0, desired_number_help_wanted):
        prefix = "Help Wanted:"
        delivery = "Item Delivery"
        rule = logic.received("Month End", i)
        fishing_rule = rule & logic.can_fish()
        slay_rule = rule & logic.can_do_combat_at_level("Basic")
        item_delivery_index = (i * 4) + 1
        for j in range(item_delivery_index, item_delivery_index + 4):
            location_name = f"{prefix} {delivery} {j}"
            MultiWorldRules.set_rule(multi_world.get_location(location_name, player), rule.simplify())

        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Gathering {i + 1}", player),
                                 rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Fishing {i + 1}", player),
                                 fishing_rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Slay Monsters {i + 1}", player),
                                 slay_rule.simplify())


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
            rule = logic.has(donation_name) & logic.received("Traveling Merchant Metal Detector", required_detectors)
            MultiWorldRules.set_rule(multi_world.get_location(museum_location.name, player),
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
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_mineral_items)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_artifact_items)
    elif milestone_name == "Dwarf Scrolls":
        rule = logic.has([item.name for item in dwarf_scrolls]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Front":
        rule = logic.has([item.name for item in skeleton_front]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Middle":
        rule = logic.has([item.name for item in skeleton_middle]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Back":
        rule = logic.has([item.name for item in skeleton_back]) & logic.received(metal_detector, 4)
    elif milestone_name == "Ancient Seed":
        rule = logic.has("Ancient Seed") & logic.received(metal_detector, 4)
    if rule is None:
        return
    MultiWorldRules.set_rule(multi_world.get_location(museum_milestone.name, player), rule.simplify())


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items):
    metal_detector = "Traveling Merchant Metal Detector"
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 5 // len(accepted_items)
    rule = logic.has([item.name for item in accepted_items], num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    if world_options[options.BackpackProgression] != options.BackpackProgression.option_vanilla:
        MultiWorldRules.set_rule(multi_world.get_location("Large Pack", player),
                                 logic.can_spend_money(2000).simplify())
        MultiWorldRules.set_rule(multi_world.get_location("Deluxe Pack", player),
                                 (logic.can_spend_money(10000) & logic.received("Progressive Backpack")).simplify())
        if ModNames.big_backpack in world_options[options.Mods]:
            MultiWorldRules.set_rule(multi_world.get_location("Premium Pack", player),
                                     (logic.can_spend_money(150000) &
                                      logic.received("Progressive Backpack", 2)).simplify())


def set_festival_rules(all_location_names: List[str], logic: StardewLogic, multi_world, player):
    for festival in locations.locations_by_tag[LocationTags.FESTIVAL]:
        if festival.name in all_location_names:
            MultiWorldRules.set_rule(multi_world.get_location(festival.name, player),
                                     logic.festival_rules[festival.name].simplify())


def set_traveling_merchant_rules(logic: StardewLogic, multi_world: MultiWorld, player: int):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        for i in range(1, 4):
            location_name = f"Traveling Merchant {day} Item {i}"
            MultiWorldRules.set_rule(multi_world.get_location(location_name, player),
                                     logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        MultiWorldRules.add_rule(multi_world.get_entrance(Entrance.play_junimo_kart, player),
                                 (logic.received("Skull Key") & logic.has("Junimo Kart Small Buff")).simplify())
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
                                 logic.can_earn_relationship(friend_name, num_hearts).simplify())


def set_deepwoods_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options: StardewOptions):
    if ModNames.deepwoods in world_options[options.Mods]:
        MultiWorldRules.add_rule(multi_world.get_location("Breaking Up Deep Woods Gingerbread House", player),
                                 logic.has_tool("Axe", "Gold") & logic.can_reach_woods_depth(50).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Chop Down a Deep Woods Iridium Tree", player),
                                 logic.has_tool("Axe", "Iridium").simplify())
        for depth in {10, 30, 50, 70, 90, 100}:
            MultiWorldRules.set_rule(multi_world.get_entrance(move_to_woods_depth(depth), player),
                                     logic.can_reach_woods_depth(depth).simplify())
        MultiWorldRules.set_rule(multi_world.get_entrance(DeepWoodsEntrance.use_woods_obelisk, player),
                                 logic.received("Woods Obelisk").simplify())
