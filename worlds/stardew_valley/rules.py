import itertools
from typing import Dict

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from . import options, locations
from .bundles import Bundle
from .locations import LocationTags
from .logic import StardewLogic, _And, season_per_skill_level, tool_prices, week_days

help_wanted_per_season = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter",
    5: "Year Two",
    6: "Year Two",
    7: "Year Two",
    8: "Year Two",
    9: "Year Two",
    10: "Year Two",
}


def set_rules(multi_world: MultiWorld, player: int, world_options: options.StardewOptions, logic: StardewLogic,
              current_bundles: Dict[str, Bundle]):
    summer = multi_world.get_location("Summer", player)
    all_location_names = list(location.name for location in multi_world.get_locations(player))

    for floor in range(5, 120 + 5, 5):
        MultiWorldRules.add_rule(multi_world.get_entrance(f"Dig to The Mines - Floor {floor}", player),
                                 logic.can_mine_to_floor(floor).simplify())

    MultiWorldRules.add_rule(multi_world.get_entrance("Enter Quarry", player),
                             logic.received("Bridge Repair").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Enter Secret Woods", player),
                             logic.has_tool("Axe", "Iron").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Take Bus to Desert", player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Enter Skull Cavern", player),
                             logic.received("Skull Key").simplify())

    MultiWorldRules.add_rule(multi_world.get_entrance("Use Desert Obelisk", player),
                             logic.received("Desert Obelisk").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Use Island Obelisk", player),
                             logic.received("Island Obelisk").simplify())

    # Those checks do not exist if ToolProgression is vanilla
    if world_options[options.ToolProgression] != options.ToolProgression.option_vanilla:
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Fiberglass Rod", player),
                                 (logic.has_skill_level("Fishing", 2) & logic.can_spend_money(1800)).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Iridium Rod", player),
                                 (logic.has_skill_level("Fishing", 6) & logic.can_spend_money(7500)).simplify())

        materials = [None, "Copper", "Iron", "Gold", "Iridium"]
        tool = ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]
        for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
            if previous is None:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") &
                                          logic.can_spend_money(tool_prices[material])).simplify())
            else:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") & logic.has_tool(tool, previous) &
                                          logic.can_spend_money(tool_prices[material])).simplify())

    # Skills
    if world_options[options.SkillProgression] != options.SkillProgression.option_vanilla:
        for i in range(1, 11):
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Farming", player),
                                     (logic.received(season_per_skill_level["Farming", i])).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Fishing", player),
                                     (logic.can_get_fishing_xp() &
                                      logic.received(season_per_skill_level["Fishing", i])).simplify())
            MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                     logic.received(season_per_skill_level["Foraging", i]).simplify())
            if i >= 6:
                MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                         logic.has_tool("Axe", "Iron").simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Mining", player),
                                     logic.received(season_per_skill_level["Mining", i]).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Combat", player),
                                     (logic.received(season_per_skill_level["Combat", i]) &
                                      logic.has_any_weapon()).simplify())

    # Bundles
    for bundle in current_bundles.values():
        MultiWorldRules.set_rule(multi_world.get_location(bundle.get_name_with_bundle(), player),
                                 logic.can_complete_bundle(bundle.requirements, bundle.number_required).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Crafts Room", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.CRAFTS_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Pantry", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.PANTRY_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Fish Tank", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.FISH_TANK_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Boiler Room", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.BOILER_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Bulletin Board", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.BULLETIN_BOARD_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Vault", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.locations_by_tag[LocationTags.VAULT_BUNDLE]).simplify())

    # Buildings
    if world_options[options.BuildingProgression] != options.BuildingProgression.option_vanilla:
        for building in locations.locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            MultiWorldRules.set_rule(multi_world.get_location(building.name, player),
                                     logic.building_rules[building.name.replace(" Blueprint", "")].simplify())

    # Story Quests
    for quest in locations.locations_by_tag[LocationTags.QUEST]:
        MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                 logic.quest_rules[quest.name].simplify())

    # Help Wanted Quests
    desired_number_help_wanted: int = world_options[options.HelpWantedLocations] // 7
    for i in range(1, desired_number_help_wanted + 1):
        prefix = "Help Wanted:"
        delivery = "Item Delivery"
        rule = logic.received(help_wanted_per_season[min(5, i)])
        fishing_rule = rule & logic.can_fish()
        slay_rule = rule & logic.has_any_weapon()
        for j in range(i, i + 4):
            MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} {delivery} {j}", player),
                                     rule.simplify())

        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Gathering {i}", player),
                                 rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Fishing {i}", player),
                                 fishing_rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Slay Monsters {i}", player),
                                 slay_rule.simplify())

    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            MultiWorldRules.set_rule(multi_world.get_location(fish_location.name, player),
                                     logic.has(fish_name).simplify())

    if world_options[options.BuildingProgression] == options.BuildingProgression.option_progressive_early_shipping_bin:
        summer.access_rule = summer.access_rule & logic.received("Shipping Bin")

    # Backpacks
    if world_options[options.BackpackProgression] != options.BackpackProgression.option_vanilla:
        MultiWorldRules.add_rule(multi_world.get_location("Large Pack", player),
                                 logic.can_spend_money(2000).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Deluxe Pack", player),
                                 logic.can_spend_money(10000).simplify())

    if world_options[options.BackpackProgression] == options.BackpackProgression.option_early_progressive:
        summer.access_rule = summer.access_rule & logic.received("Progressive Backpack")
        MultiWorldRules.add_rule(multi_world.get_location("Winter", player),
                                 logic.received("Progressive Backpack", 2).simplify())

    MultiWorldRules.add_rule(multi_world.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())

    # Traveling Merchant
    for day in week_days:
        item_for_day = f"Traveling Merchant: {day}"
        for i in range(1, 4):
            location_name = f"Traveling Merchant {day} Item {i}"
            MultiWorldRules.set_rule(multi_world.get_location(location_name, player),
                                     logic.received(item_for_day))

    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Junimo Kart", player),
                                 (logic.received("Skull Key") & logic.has("Junimo Kart Small Buff")).simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 2", player),
                                 logic.has("Junimo Kart Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 3", player),
                                 logic.has("Junimo Kart Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Junimo Kart: Sunset Speedway (Victory)", player),
                                 logic.has("Junimo Kart Max Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Journey of the Prairie King", player),
                                 logic.has("JotPK Small Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 2", player),
                                 logic.has("JotPK Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 3", player),
                                 logic.has("JotPK Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Journey of the Prairie King Victory", player),
                                 logic.has("JotPK Max Buff").simplify())
