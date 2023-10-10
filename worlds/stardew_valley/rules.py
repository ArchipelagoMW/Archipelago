import itertools
from typing import List

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from .options import StardewValleyOptions, ToolProgression, BuildingProgression, SkillProgression, ExcludeGingerIsland, Cropsanity, SpecialOrderLocations, Museumsanity, \
    BackpackProgression, ArcadeMachineLocations
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, \
    DeepWoodsEntrance, AlecEntrance, MagicEntrance
from .data.museum_data import all_museum_items, all_museum_minerals, all_museum_artifacts, \
    dwarf_scrolls, skeleton_front, \
    skeleton_middle, skeleton_back, all_museum_items_by_name, Artifact
from .strings.region_names import Region
from .mods.mod_data import ModNames
from .mods.logic import magic, deepwoods
from .locations import LocationTags, locations_by_tag
from .logic import StardewLogic, And, tool_upgrade_prices
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.calendar_names import Weekday
from .strings.craftable_names import Craftable
from .strings.material_names import Material
from .strings.metal_names import MetalBar
from .strings.skill_names import ModSkill, Skill
from .strings.tool_names import Tool, ToolMaterial
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet


def set_rules(world):
    multiworld = world.multiworld
    world_options = world.options
    player = world.player
    logic = world.logic
    current_bundles = world.modified_bundles
    
    all_location_names = list(location.name for location in multiworld.get_locations(player))

    set_entrance_rules(logic, multiworld, player, world_options)

    set_ginger_island_rules(logic, multiworld, player, world_options)

    # Those checks do not exist if ToolProgression is vanilla
    if world_options.tool_progression != ToolProgression.option_vanilla:
        MultiWorldRules.add_rule(multiworld.get_location("Purchase Fiberglass Rod", player),
                                 (logic.has_skill_level(Skill.fishing, 2) & logic.can_spend_money(1800)).simplify())
        MultiWorldRules.add_rule(multiworld.get_location("Purchase Iridium Rod", player),
                                 (logic.has_skill_level(Skill.fishing, 6) & logic.can_spend_money(7500)).simplify())

        materials = [None, "Copper", "Iron", "Gold", "Iridium"]
        tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.watering_can, Tool.trash_can]
        for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
            if previous is None:
                MultiWorldRules.add_rule(multiworld.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") &
                                          logic.can_spend_money(tool_upgrade_prices[material])).simplify())
            else:
                MultiWorldRules.add_rule(multiworld.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") & logic.has_tool(tool, previous) &
                                          logic.can_spend_money(tool_upgrade_prices[material])).simplify())

    set_skills_rules(logic, multiworld, player, world_options)

    # Bundles
    for bundle in current_bundles.values():
        location = multiworld.get_location(bundle.get_name_with_bundle(), player)
        rules = logic.can_complete_bundle(bundle.requirements, bundle.number_required)
        simplified_rules = rules.simplify()
        MultiWorldRules.set_rule(location, simplified_rules)
    MultiWorldRules.add_rule(multiworld.get_location("Complete Crafts Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations_by_tag[LocationTags.CRAFTS_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Pantry", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations_by_tag[LocationTags.PANTRY_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Fish Tank", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations_by_tag[LocationTags.FISH_TANK_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Boiler Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations_by_tag[LocationTags.BOILER_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Bulletin Board", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle
                                 in locations_by_tag[LocationTags.BULLETIN_BOARD_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Vault", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations_by_tag[LocationTags.VAULT_BUNDLE]).simplify())

    # Buildings
    if world_options.building_progression != BuildingProgression.option_vanilla:
        for building in locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            if building.mod_name is not None and building.mod_name not in world_options.mods:
                continue
            MultiWorldRules.set_rule(multiworld.get_location(building.name, player),
                                     logic.building_rules[building.name.replace(" Blueprint", "")].simplify())

    set_cropsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_story_quests_rules(all_location_names, logic, multiworld, player, world_options)
    set_special_order_rules(all_location_names, logic, multiworld, player, world_options)
    set_help_wanted_quests_rules(logic, multiworld, player, world_options)
    set_fishsanity_rules(all_location_names, logic, multiworld, player)
    set_museumsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_friendsanity_rules(all_location_names, logic, multiworld, player)
    set_backpack_rules(logic, multiworld, player, world_options)
    set_festival_rules(all_location_names, logic, multiworld, player)

    MultiWorldRules.add_rule(multiworld.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Have a Baby", player),
                             logic.can_reproduce(1).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Have Another Baby", player),
                             logic.can_reproduce(2).simplify())

    set_traveling_merchant_rules(logic, multiworld, player)
    set_arcade_machine_rules(logic, multiworld, player, world_options)
    set_deepwoods_rules(logic, multiworld, player, world_options)
    set_magic_spell_rules(logic, multiworld, player, world_options)


def set_skills_rules(logic, multiworld, player, world_options):
    # Skills
    if world_options.skill_progression != SkillProgression.option_vanilla:
        for i in range(1, 11):
            set_skill_rule(logic, multiworld, player, Skill.farming, i)
            set_skill_rule(logic, multiworld, player, Skill.fishing, i)
            set_skill_rule(logic, multiworld, player, Skill.foraging, i)
            set_skill_rule(logic, multiworld, player, Skill.mining, i)
            set_skill_rule(logic, multiworld, player, Skill.combat, i)

            # Modded Skills
            if ModNames.luck_skill in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.luck, i)
            if ModNames.magic in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.magic, i)
            if ModNames.binning_skill in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.binning, i)
            if ModNames.cooking_skill in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.cooking, i)
            if ModNames.socializing_skill in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.socializing, i)
            if ModNames.archaeology in world_options.mods:
                set_skill_rule(logic, multiworld, player, ModSkill.archaeology, i)


def set_skill_rule(logic, multiworld, player, skill: str, level: int):
    location_name = f"Level {level} {skill}"
    location = multiworld.get_location(location_name, player)
    rule = logic.can_earn_skill_level(skill, level).simplify()
    MultiWorldRules.set_rule(location, rule)


def set_entrance_rules(logic, multiworld, player, world_options: StardewValleyOptions):
    for floor in range(5, 120 + 5, 5):
        MultiWorldRules.set_rule(multiworld.get_entrance(dig_to_mines_floor(floor), player),
                                 logic.can_mine_to_floor(floor).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_tide_pools, player),
                             logic.received("Beach Bridge") | (magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_quarry, player),
                             logic.received("Bridge Repair") | (magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_secret_woods, player),
                             logic.has_tool(Tool.axe, "Iron") | (magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.forest_to_sewer, player),
                             logic.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.town_to_sewer, player),
                             logic.has_rusty_key().simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.take_bus_to_desert, player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_skull_cavern, player),
                             logic.received(Wallet.skull_key).simplify())
    for floor in range(25, 200 + 25, 25):
        MultiWorldRules.set_rule(multiworld.get_entrance(dig_to_skull_floor(floor), player),
                                 logic.can_mine_to_skull_cavern_floor(floor).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.talk_to_mines_dwarf, player),
                             logic.can_speak_dwarf() & logic.has_tool(Tool.pickaxe, ToolMaterial.iron))

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.use_desert_obelisk, player),
                             logic.received(Transportation.desert_obelisk).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.use_island_obelisk, player),
                             logic.received(Transportation.island_obelisk).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.use_farm_obelisk, player),
                             logic.received(Transportation.farm_obelisk).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.buy_from_traveling_merchant, player),
                             logic.has_traveling_merchant())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_greenhouse, player),
                             logic.received("Greenhouse"))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.mountain_to_adventurer_guild, player),
                             logic.received("Adventurer's Guild"))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.mountain_to_railroad, player),
                             logic.has_lived_months(2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_witch_warp_cave, player),
                             logic.received(Wallet.dark_talisman) | (magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_witch_hut, player),
                             (logic.has(ArtisanGood.void_mayonnaise) | magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_mutant_bug_lair, player),
                             ((logic.has_rusty_key() & logic.can_reach_region(Region.railroad) &
                               logic.can_meet(NPC.krobus) | magic.can_blink(logic)).simplify()))

    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_harvey_room, player),
                             logic.has_relationship(NPC.harvey, 2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.mountain_to_maru_room, player),
                             logic.has_relationship(NPC.maru, 2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_sebastian_room, player),
                             (logic.has_relationship(NPC.sebastian, 2) | magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.forest_to_leah_cottage, player),
                             logic.has_relationship(NPC.leah, 2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_elliott_house, player),
                             logic.has_relationship(NPC.elliott, 2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_sunroom, player),
                             logic.has_relationship(NPC.caroline, 2))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.enter_wizard_basement, player),
                             logic.has_relationship(NPC.wizard, 4))
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.mountain_to_leo_treehouse, player),
                             logic.received("Treehouse"))
    if ModNames.alec in world_options.mods:
        MultiWorldRules.set_rule(multiworld.get_entrance(AlecEntrance.petshop_to_bedroom, player),
                                 (logic.has_relationship(ModNPC.alec, 2) | magic.can_blink(logic)).simplify())


def set_ginger_island_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    set_island_entrances_rules(logic, multiworld, player)
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    set_boat_repair_rules(logic, multiworld, player)
    set_island_parrot_rules(logic, multiworld, player)
    MultiWorldRules.add_rule(multiworld.get_location("Open Professor Snail Cave", player),
                             logic.has(Craftable.cherry_bomb).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Complete Island Field Office", player),
                             logic.can_complete_field_office().simplify())


def set_boat_repair_rules(logic: StardewLogic, multiworld, player):
    MultiWorldRules.add_rule(multiworld.get_location("Repair Boat Hull", player),
                             logic.has(Material.hardwood).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Repair Boat Anchor", player),
                             logic.has(MetalBar.iridium).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Repair Ticket Machine", player),
                             logic.has(ArtisanGood.battery_pack).simplify())


def set_island_entrances_rules(logic: StardewLogic, multiworld, player):
    boat_repaired = logic.received(Transportation.boat_repair).simplify()
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.fish_shop_to_boat_tunnel, player),
                             boat_repaired)
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.boat_to_ginger_island, player),
                             boat_repaired)
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_south_to_west, player),
                             logic.received("Island West Turtle").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_south_to_north, player),
                             logic.received("Island North Turtle").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_west_to_islandfarmhouse, player),
                             logic.received("Island Farmhouse").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_west_to_gourmand_cave, player),
                             logic.received("Island Farmhouse").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_north_to_dig_site, player),
                             logic.received("Dig Site Bridge").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.dig_site_to_professor_snail_cave, player),
                             logic.received("Open Professor Snail Cave").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.talk_to_island_trader, player),
                             logic.received("Island Trader").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_south_to_southeast, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.use_island_resort, player),
                             logic.received("Island Resort").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_west_to_qi_walnut_room, player),
                             logic.received("Qi Walnut Room").simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.island_north_to_volcano, player),
                             (logic.can_water(0) | logic.received("Volcano Bridge") |
                              magic.can_blink(logic)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.volcano_to_secret_beach, player),
                             logic.can_water(2).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.climb_to_volcano_5, player),
                             (logic.can_mine_perfectly() & logic.can_water(1)).simplify())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.talk_to_volcano_dwarf, player),
                             logic.can_speak_dwarf())
    MultiWorldRules.set_rule(multiworld.get_entrance(Entrance.climb_to_volcano_10, player),
                             (logic.can_mine_perfectly() & logic.can_water(1) & logic.received("Volcano Exit Shortcut")).simplify())
    parrots = [Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_jungle_to_volcano,
               Entrance.parrot_express_dig_site_to_volcano, Entrance.parrot_express_docks_to_dig_site,
               Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_volcano_to_dig_site,
               Entrance.parrot_express_docks_to_jungle, Entrance.parrot_express_dig_site_to_jungle,
               Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_jungle_to_docks,
               Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_volcano_to_docks]
    for parrot in parrots:
        MultiWorldRules.set_rule(multiworld.get_entrance(parrot, player), logic.received(Transportation.parrot_express).simplify())


def set_island_parrot_rules(logic: StardewLogic, multiworld, player):
    has_walnut = logic.has_walnut(1).simplify()
    has_5_walnut = logic.has_walnut(5).simplify()
    has_10_walnut = logic.has_walnut(10).simplify()
    has_20_walnut = logic.has_walnut(20).simplify()
    MultiWorldRules.add_rule(multiworld.get_location("Leo's Parrot", player),
                             has_walnut)
    MultiWorldRules.add_rule(multiworld.get_location("Island West Turtle", player),
                             has_10_walnut & logic.received("Island North Turtle"))
    MultiWorldRules.add_rule(multiworld.get_location("Island Farmhouse", player),
                             has_20_walnut)
    MultiWorldRules.add_rule(multiworld.get_location("Island Mailbox", player),
                             has_5_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multiworld.get_location(Transportation.farm_obelisk, player),
                             has_20_walnut & logic.received("Island Mailbox"))
    MultiWorldRules.add_rule(multiworld.get_location("Dig Site Bridge", player),
                             has_10_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multiworld.get_location("Island Trader", player),
                             has_10_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multiworld.get_location("Volcano Bridge", player),
                             has_5_walnut & logic.received("Island West Turtle") &
                             logic.can_reach_region(Region.volcano_floor_10))
    MultiWorldRules.add_rule(multiworld.get_location("Volcano Exit Shortcut", player),
                             has_5_walnut & logic.received("Island West Turtle"))
    MultiWorldRules.add_rule(multiworld.get_location("Island Resort", player),
                             has_20_walnut & logic.received("Island Farmhouse"))
    MultiWorldRules.add_rule(multiworld.get_location(Transportation.parrot_express, player),
                             has_10_walnut)


def set_cropsanity_rules(all_location_names: List[str], logic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.cropsanity == Cropsanity.option_disabled:
        return

    harvest_prefix = "Harvest "
    harvest_prefix_length = len(harvest_prefix)
    for harvest_location in locations_by_tag[LocationTags.CROPSANITY]:
        if harvest_location.name in all_location_names and (harvest_location.mod_name is None or harvest_location.mod_name in world_options.mods):
            crop_name = harvest_location.name[harvest_prefix_length:]
            MultiWorldRules.set_rule(multiworld.get_location(harvest_location.name, player),
                                     logic.has(crop_name).simplify())


def set_story_quests_rules(all_location_names: List[str], logic, multiworld, player, world_options: StardewValleyOptions):
    for quest in locations_by_tag[LocationTags.QUEST]:
        if quest.name in all_location_names and (quest.mod_name is None or quest.mod_name in world_options.mods):
            MultiWorldRules.set_rule(multiworld.get_location(quest.name, player),
                                     logic.quest_rules[quest.name].simplify())


def set_special_order_rules(all_location_names: List[str], logic: StardewLogic, multiworld, player,
                            world_options: StardewValleyOptions):
    if world_options.special_order_locations == SpecialOrderLocations.option_disabled:
        return
    board_rule = logic.received("Special Order Board") & logic.has_lived_months(4)
    for board_order in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
        if board_order.name in all_location_names:
            order_rule = board_rule & logic.special_order_rules[board_order.name]
            MultiWorldRules.set_rule(multiworld.get_location(board_order.name, player), order_rule.simplify())

    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    if world_options.special_order_locations == SpecialOrderLocations.option_board_only:
        return
    qi_rule = logic.can_reach_region(Region.qi_walnut_room) & logic.has_lived_months(8)
    for qi_order in locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
        if qi_order.name in all_location_names:
            order_rule = qi_rule & logic.special_order_rules[qi_order.name]
            MultiWorldRules.set_rule(multiworld.get_location(qi_order.name, player), order_rule.simplify())


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    help_wanted_number = world_options.help_wanted_locations
    for i in range(0, help_wanted_number):
        set_number = i // 7
        month_rule = logic.has_lived_months(set_number).simplify()
        quest_number = set_number + 1
        quest_number_in_set = i % 7
        if quest_number_in_set < 4:
            quest_number = set_number * 4 + quest_number_in_set + 1
            set_help_wanted_delivery_rule(multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(logic, multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(logic, multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(multiworld, player, month_rule, quest_number)


def set_help_wanted_delivery_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), month_rule)


def set_help_wanted_gathering_rule(multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), month_rule)


def set_help_wanted_fishing_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    fishing_rule = month_rule & logic.can_fish()
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), fishing_rule.simplify())


def set_help_wanted_slay_monsters_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    slay_rule = month_rule & logic.can_do_combat_at_level("Basic")
    MultiWorldRules.set_rule(multiworld.get_location(location_name, player), slay_rule.simplify())


def set_fishsanity_rules(all_location_names: List[str], logic: StardewLogic, multiworld: MultiWorld, player: int):
    fish_prefix = "Fishsanity: "
    for fish_location in locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            MultiWorldRules.set_rule(multiworld.get_location(fish_location.name, player),
                                     logic.has(fish_name).simplify())


def set_museumsanity_rules(all_location_names: List[str], logic: StardewLogic, multiworld: MultiWorld, player: int,
                           world_options: StardewValleyOptions):
    museum_prefix = "Museumsanity: "
    if world_options.museumsanity == Museumsanity.option_milestones:
        for museum_milestone in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, multiworld, museum_milestone, museum_prefix, player)
    elif world_options.museumsanity != Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, multiworld, museum_prefix, player)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, multiworld, museum_prefix, player):
    all_donations = sorted(locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 5 // number_donations
            rule = logic.can_donate_museum_item(all_museum_items_by_name[donation_name]) & logic.received("Traveling Merchant Metal Detector",
                                                                                                          required_detectors)
            MultiWorldRules.set_rule(multiworld.get_location(museum_location.name, player),
                                     rule.simplify())
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, multiworld: MultiWorld, museum_milestone, museum_prefix: str,
                              player: int):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    metal_detector = "Traveling Merchant Metal Detector"
    rule = None
    if milestone_name.endswith(donations_suffix):
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items, logic.can_donate_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_museum_minerals, logic.can_donate_museum_minerals)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_museum_artifacts, logic.can_donate_museum_artifacts)
    elif milestone_name == "Dwarf Scrolls":
        rule = And([logic.can_donate_museum_item(item) for item in dwarf_scrolls]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Front":
        rule = And([logic.can_donate_museum_item(item) for item in skeleton_front]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Middle":
        rule = And([logic.can_donate_museum_item(item) for item in skeleton_middle]) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Back":
        rule = And([logic.can_donate_museum_item(item) for item in skeleton_back]) & logic.received(metal_detector, 4)
    elif milestone_name == "Ancient Seed":
        rule = logic.can_donate_museum_item(Artifact.ancient_seed) & logic.received(metal_detector, 4)
    if rule is None:
        return
    MultiWorldRules.set_rule(multiworld.get_location(museum_milestone.name, player), rule.simplify())


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = "Traveling Merchant Metal Detector"
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 5 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if world_options.backpack_progression != BackpackProgression.option_vanilla:
        MultiWorldRules.set_rule(multiworld.get_location("Large Pack", player),
                                 logic.can_spend_money(2000).simplify())
        MultiWorldRules.set_rule(multiworld.get_location("Deluxe Pack", player),
                                 (logic.can_spend_money(10000) & logic.received("Progressive Backpack")).simplify())
        if ModNames.big_backpack in world_options.mods:
            MultiWorldRules.set_rule(multiworld.get_location("Premium Pack", player),
                                     (logic.can_spend_money(150000) &
                                      logic.received("Progressive Backpack", 2)).simplify())


def set_festival_rules(all_location_names: List[str], logic: StardewLogic, multiworld, player):
    festival_locations = []
    festival_locations.extend(locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            MultiWorldRules.set_rule(multiworld.get_location(festival.name, player),
                                     logic.festival_rules[festival.name].simplify())


def set_traveling_merchant_rules(logic: StardewLogic, multiworld: MultiWorld, player: int):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        for i in range(1, 4):
            location_name = f"Traveling Merchant {day} Item {i}"
            MultiWorldRules.set_rule(multiworld.get_location(location_name, player),
                                     logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.play_junimo_kart, player),
                             logic.received(Wallet.skull_key).simplify())
    if world_options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
        return

    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.play_junimo_kart, player),
                             logic.has("Junimo Kart Small Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.reach_junimo_kart_2, player),
                             logic.has("Junimo Kart Medium Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.reach_junimo_kart_3, player),
                             logic.has("Junimo Kart Big Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Junimo Kart: Sunset Speedway (Victory)", player),
                             logic.has("Junimo Kart Max Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.play_journey_of_the_prairie_king, player),
                             logic.has("JotPK Small Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.reach_jotpk_world_2, player),
                             logic.has("JotPK Medium Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_entrance(Entrance.reach_jotpk_world_3, player),
                             logic.has("JotPK Big Buff").simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Journey of the Prairie King Victory", player),
                             logic.has("JotPK Max Buff").simplify())


def set_friendsanity_rules(all_location_names: List[str], logic: StardewLogic, multiworld: MultiWorld, player: int):
    friend_prefix = "Friendsanity: "
    friend_suffix = " <3"
    for friend_location in locations_by_tag[LocationTags.FRIENDSANITY]:
        if friend_location.name not in all_location_names:
            continue
        friend_location_without_prefix = friend_location.name[len(friend_prefix):]
        friend_location_trimmed = friend_location_without_prefix[:friend_location_without_prefix.index(friend_suffix)]
        split_index = friend_location_trimmed.rindex(" ")
        friend_name = friend_location_trimmed[:split_index]
        num_hearts = int(friend_location_trimmed[split_index + 1:])
        MultiWorldRules.set_rule(multiworld.get_location(friend_location.name, player),
                                 logic.can_earn_relationship(friend_name, num_hearts).simplify())


def set_deepwoods_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.deepwoods in world_options.mods:
        MultiWorldRules.add_rule(multiworld.get_location("Breaking Up Deep Woods Gingerbread House", player),
                                 logic.has_tool(Tool.axe, "Gold") & deepwoods.can_reach_woods_depth(logic, 50).simplify())
        MultiWorldRules.add_rule(multiworld.get_location("Chop Down a Deep Woods Iridium Tree", player),
                                 logic.has_tool(Tool.axe, "Iridium").simplify())
        MultiWorldRules.set_rule(multiworld.get_entrance(DeepWoodsEntrance.use_woods_obelisk, player),
                                 logic.received("Woods Obelisk").simplify())
        for depth in range(10, 100 + 10, 10):
            MultiWorldRules.set_rule(multiworld.get_entrance(move_to_woods_depth(depth), player),
                                     deepwoods.can_chop_to_depth(logic, depth).simplify())


def set_magic_spell_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if ModNames.magic not in world_options.mods:
        return

    MultiWorldRules.set_rule(multiworld.get_entrance(MagicEntrance.store_to_altar, player),
                             (logic.has_relationship(NPC.wizard, 3) &
                              logic.can_reach_region(Region.wizard_tower)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Clear Debris", player),
                             ((logic.has_tool("Axe", "Basic") | logic.has_tool("Pickaxe", "Basic"))
                              & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Till", player),
                             (logic.has_tool("Hoe", "Basic") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Water", player),
                             (logic.has_tool("Watering Can", "Basic") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Toil School Locations", player),
                             (logic.has_tool("Watering Can", "Basic") & logic.has_tool("Hoe", "Basic")
                              & (logic.has_tool("Axe", "Basic") | logic.has_tool("Pickaxe", "Basic"))
                              & magic.can_use_altar(logic)).simplify())
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Evac", player),
                             (logic.can_mine_perfectly() & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Haste", player),
                             (logic.has("Coffee") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Heal", player),
                             (logic.has("Life Elixir") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Life School Locations", player),
                             (logic.has("Coffee") & logic.has("Life Elixir")
                              & logic.can_mine_perfectly() & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Descend", player),
                             (logic.can_reach_region(Region.mines) & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Fireball", player),
                             (logic.has("Fire Quartz") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Frostbite", player),
                             (logic.can_mine_to_floor(70) & logic.can_fish(85) & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Elemental School Locations", player),
                             (logic.can_reach_region(Region.mines) & logic.has("Fire Quartz")
                              & logic.can_reach_region(Region.mines_floor_70) & logic.can_fish(85) &
                              magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Lantern", player),
                             magic.can_use_altar(logic).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Tendrils", player),
                             (logic.can_reach_region(Region.farm) & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Shockwave", player),
                             (logic.has("Earth Crystal") & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Nature School Locations", player),
                             (logic.has("Earth Crystal") & logic.can_reach_region("Farm") &
                              magic.can_use_altar(logic)).simplify()),
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Meteor", player),
                             (logic.can_reach_region(Region.farm) & logic.has_lived_months(12)
                              & magic.can_use_altar(logic)).simplify()),
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Lucksteal", player),
                             (logic.can_reach_region(Region.witch_hut) & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze: Bloodmana", player),
                             (logic.can_reach_region(Region.mines_floor_100) & magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze All Eldritch School Locations", player),
                             (logic.can_reach_region(Region.witch_hut) &
                              logic.can_reach_region(Region.mines_floor_100) &
                              logic.can_reach_region(Region.farm) & logic.has_lived_months(12) &
                              magic.can_use_altar(logic)).simplify())
    MultiWorldRules.add_rule(multiworld.get_location("Analyze Every Magic School Location", player),
                             (logic.has_tool("Watering Can", "Basic") & logic.has_tool("Hoe", "Basic")
                              & (logic.has_tool("Axe", "Basic") | logic.has_tool("Pickaxe", "Basic")) &
                              logic.has("Coffee") & logic.has("Life Elixir")
                              & logic.can_mine_perfectly() & logic.has("Earth Crystal") &
                              logic.can_reach_region(Region.mines) &
                              logic.has("Fire Quartz") & logic.can_fish(85) &
                              logic.can_reach_region(Region.witch_hut) &
                              logic.can_reach_region(Region.mines_floor_100) &
                              logic.can_reach_region(Region.farm) & logic.has_lived_months(12) &
                              magic.can_use_altar(logic)).simplify())
