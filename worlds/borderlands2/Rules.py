from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Borderlands2World
from math import sqrt
from worlds.generic.Rules import set_rule, add_rule

from .Regions import region_data_table
from .Locations import Borderlands2Location, location_data_table
from .Items import Borderlands2Item
from .archi_defs import gear_data_table, quest_data_table
from BaseClasses import ItemClassification, Region


def try_add_rule(place, rule, combine="and"):
    if place is None:
        return
    try:
        add_rule(place, rule, combine)
    except:
        print(f"failed setting rule at {place}")


def calc_jump_height(max_height_setting, num_slices, checks_amt): # needs to reflect the calculation done in sdkmod
    height_bonus = max_height_setting * 300
    max_height = 630 + height_bonus
    if num_slices == 0:
        return max_height
    frac = checks_amt / num_slices
    frac = sqrt(frac)
    return max(220, min(max_height, max_height * frac))

# TODO: try adding @cache to this
def amt_jump_checks_needed(world, jump_z_req):
    if world.options.jump_checks.value == 0:
        return 0
    if jump_z_req < 220:
        return 0
    if jump_z_req > 630:
        print(f"jump_z_req seems high: {jump_z_req}")
        return world.options.jump_checks.value
    checks_amt = 0
    height = 220
    while height < jump_z_req:
        checks_amt += 1
        height = calc_jump_height(world.options.max_jump_height.value, world.options.jump_checks.value, checks_amt)
    return checks_amt

def get_level_region_name(level):
    if level == 0:
        return "Level 0"
    if level > 30:
        return "Level 31+"
    start = ((level - 1) // 5) * 5 + 1
    end = start + 4
    return f"Level {start}-{end}"

def set_world_rules(world: Borderlands2World):

    # items must be classified as progression to use in rules here

    #add_rule(world.multiworld.get
    # add_rule(world.multiworld.get_entrance("SouthernShelf to ThreeHornsDivide", world.player),
    #     lambda state: state.has("Common Pistol", world.player))
    # add_rule(world.multiworld.get_location("Enemy: Knuckle Dragger", world.player),
    #     lambda state: state.has("Melee", world.player))

    # need melee to break vines to Hector
    try_add_rule(world.try_get_entrance("Mt.ScarabResearchCenter to FFSBossFight"),
             lambda state: state.has("Melee", world.player))

    try_add_rule(world.try_get_entrance("CandlerakksCrag to Terminus"),
            lambda state: state.has("Crouch", world.player))
    # If you die to the dragon, you need to crouch under the gate
    try_add_rule(world.try_get_entrance("HatredsShadow to LairOfInfiniteAgony"),
             lambda state: state.has("Crouch", world.player))

    # FFS Butt Stalion requires the amulet
    try_add_rule(world.try_get_location("Challenge Backburner: Fandir Fiction"),
            lambda state: state.has("Unique Relic", world.player))
    try_add_rule(world.try_get_location("Rainbow Shotgun"),
            lambda state: state.has("Unique Relic", world.player))
    try_add_rule(world.try_get_location("Rainbow Shotgun"),
            lambda state: state.has("Rainbow Shotgun", world.player), "or")


    try_add_rule(world.try_get_location("Challenge Sanctuary: Jackpot!"),
            lambda state: state.has("Progressive Money Cap", world.player))

    # rules from location_data_table
    for location_name, location_data in location_data_table.items():
        loc = world.try_get_location(location_name)
        if not loc:
            continue

        # jump requirement
        if world.options.jump_checks.value > 0:
            if location_data.jump_z_req > 0:
                checks_amt = amt_jump_checks_needed(world, location_data.jump_z_req)
                # print(f"jump_z_req {location_data.jump_z_req} checks: {checks_amt}")
                try_add_rule(loc, lambda state, checks_amt=checks_amt: state.has("Progressive Jump", world.player, checks_amt))

        # other required regions
        for reg in location_data.other_req_regions:
            try_add_rule(loc, lambda state, region=reg: state.can_reach_region(region, world.player))

        # other required items
        for item in location_data.req_items:
            try_add_rule(loc, lambda state, item=item: state.has(item, world.player))

        # required item group
        for group in location_data.req_groups:
            try_add_rule(loc, lambda state, group=group: state.has_group(group, world.player))

        # level requirement
        if location_data.level > 0:
            level_reg_name = get_level_region_name(location_data.level)
            try_add_rule(loc, lambda state, lr=level_reg_name: state.can_reach_region(lr, world.player))


    # TODO: I think this could be set up as events instead of regions, had other issues when trying it the first time
    # level entrances can_reach rules
    level_entrance_rules = {
        "Level 1-5 to Level 6-10": ["SouthernShelf", "SouthernShelfBay"],
        "Level 6-10 to Level 11-15": ["ThreeHornsDivide", "ThreeHornsValley", "FrostburnCanyon", "SouthpawSteam&Power", "FriendshipGulag"],
        "Level 11-15 to Level 16-20": ["Dust", "BloodshotStronghold", "BloodshotRamparts", "Fridge", "HighlandsOutwash",
                                       "FinksSlaughterhouse", "SanctuaryHole", "TundraExpress", "EndOfTheLine",
                                       "MarcusMercenaryShop", "GluttonyGulch", "RotgutDistillery", "WamBamIsland", "HallowedHollow",
                                       "BadassCrater", "Oasis",
                                      ],
        "Level 16-20 to Level 21-25": ["Highlands", "CausticCaverns", "WildlifeExploitationPreserve", "NaturalSelectionAnnex", "Opportunity", "ThousandCuts",
                                       "PyroPetesBar", "Forge", "MagnysLighthouse", "LeviathansLair",
                                      ],
        "Level 21-25 to Level 26-30": ["Lynchwood", "Bunker", "EridiumBlight", "SawtoothCauldron"],
        "Level 26-30 to Level 31+": ["VaultOfTheWarrior"],
    }

    for entrance_name, regions in level_entrance_rules.items():
        entrance = world.try_get_entrance(entrance_name)
        if entrance:
            try_add_rule(entrance,
                lambda state, regs=regions: any(state.can_reach_region(reg, world.player) for reg in regs)
            )
            for region_name in regions:
                # Register indirect condition - required when using regions inside entrance rule
                region = world.try_get_region(region_name)
                if region:
                    world.multiworld.register_indirect_condition(region, entrance)

    # require basic combat to surpass level 0
    if world.options.gear_rarity_item_pool.value > 0:
        try_add_rule(world.try_get_entrance("Level 0 to Level 1-5"),
            lambda state: state.has_any(["Melee", "Common Pistol"], world.player))

        try_add_rule(world.try_get_entrance("Level 6-10 to Level 11-15"),
            lambda state: state.has_all(["Melee", "Common Pistol", "Common Shield", "Common Shotgun", "Uncommon Pistol"], world.player))


    # map region connection rules
    if world.options.entrance_locks.value == 1:
        for name, region_data in region_data_table.items():
            region = world.multiworld.get_region(name, world.player)
            for c_region_name in region_data.connecting_regions:
                c_region_data = region_data_table[c_region_name]
                ent_name = f"{region.name} to {c_region_name}"
                t_item = c_region_data.travel_item_name
                entrance = world.try_get_entrance(ent_name)
                if t_item:
                    try_add_rule(entrance, lambda state, travel_item=t_item: state.has(travel_item, world.player))

                # rules for story required regions
                for story_req_reg_name in c_region_data.story_req_regions:
                    # print(f"{ent_name} - {story_req_reg_name}")
                    try_add_rule(entrance, lambda state, reg=story_req_reg_name: state.can_reach_region(reg, world.player))
                    # Register indirect condition - required when using regions inside entrance rule
                    req_region = world.try_get_region(story_req_reg_name)
                    if req_region:
                        world.multiworld.register_indirect_condition(req_region, entrance)

                    # # event based, also not working
                    # region = world.try_get_region(story_req_reg_name)
                    # # print(f"{story_req_reg_name} - {c_region_name}")
                    # # event_loc = world.try_get_location(f"Story Location - {story_req_reg_name}")
                    # # if not event_loc:
                    # #     event_loc = Borderlands2Location(world.player, f"Story Location - {story_req_reg_name}", None, region)
                    # #     event_loc.place_locked_item(Borderlands2Item(f"Story Reached {story_req_reg_name}", ItemClassification.progression, None, world.player))
                    # print(f"Story Reached {story_req_reg_name}")
                    # try_add_rule(entrance, lambda state, reg=story_req_reg_name: state.has(f"Story Reached {reg}", world.player))


    # misc. region rules

    try_add_rule(world.try_get_location("Challenge Money: For the Hoard!"), # requires 10,000
        lambda state: state.has("Progressive Money Cap", world.player, 2))

    if world.options.gear_rarity_item_pool.value > 0:
        try_add_rule(world.try_get_entrance("WindshearWaste to SouthernShelf"),
            lambda state: state.has_any(["Melee", "Common Pistol"], world.player))

    # expect player to have access to Backburner before starting FFS
    try_add_rule(world.try_get_entrance("Menu to FFSIntroSanctuary"),
        lambda state: state.has("Travel: The Backburner", world.player))

    # need to shoot the bridge halfway through CandlerakksCrag
    try_add_rule(world.try_get_entrance("HuntersGrotto to CandlerakksCrag"),
        lambda state: state.has("Common Pistol", world.player))

    # Terminus requires crouching through a tunnel. technically there are vending machines before the tunnel, but not gonna worry about it.
    try_add_rule(world.try_get_entrance("CandlerakksCrag to Terminus"),
        lambda state: state.has("Crouch", world.player))

    # force player to be able to re-reach sanctuary before being able to make it disappear TODO: maybe put this behind a setting in the future
    try_add_rule(world.try_get_entrance("TundraExpress to EndOfTheLine"),
        lambda state: state.has_all(["Travel: The Fridge", "Travel: Highlands Outwash", "Travel: Highlands"], world.player))
    # TODO: maybe need to do similar for Control Core Angel through end of game

    if world.options.jump_checks.value > 0:
        try_add_rule(world.try_get_entrance("BadassCrater to TorgueArena"),
            lambda state: state.has("Progressive Jump", world.player, amt_jump_checks_needed(world, 490))) # jumping out of "kicked out" area, final cookie vending machine, barrier into Badassasaurus fight
        try_add_rule(world.try_get_entrance("HerosPass to VaultOfTheWarrior"),
            lambda state: state.has("Progressive Jump", world.player, amt_jump_checks_needed(world, 629))) # TODO: not sure why / what amount?
        try_add_rule(world.try_get_entrance("Menu to Oasis"),
            lambda state: state.has("Progressive Jump", world.player, amt_jump_checks_needed(world, 629))) # TODO: not sure why / what amount?
        try_add_rule(world.try_get_entrance("Menu to GluttonyGulch"),
            lambda state: state.has("Progressive Jump", world.player, amt_jump_checks_needed(world, 350))) # Torgue Stage


    # gear reward grants gear location (alternative requirement, use combine="or")
    # TODO: I think this only works for the Progression items (not quest rewards)
    gear_to_rewards = {}
    for quest_name, data in quest_data_table.items():
        if not data.associated_gear:
            continue
        if data.associated_gear not in gear_to_rewards:
            gear_to_rewards[data.associated_gear] = []
        gear_to_rewards[data.associated_gear].append("Reward: " + quest_name)

    for gear_name in gear_data_table:
        # same item grants location
        if world.options.receive_gear.value != 0:
            try_add_rule(world.try_get_location(gear_name), lambda state, gear_item=gear_name: state.has(gear_item, world.player), combine="or")
        # associated reward grants location
        rewards = gear_to_rewards.get(gear_name, [])
        for reward in rewards:
            try_add_rule(world.try_get_location(gear_name), lambda state, r=reward: state.has(r, world.player), combine="or")

    # alternative override for levels
    try_add_rule(world.try_get_entrance("Level 1-5 to Level 6-10"), lambda state: state.has("Override Level 15", world.player), combine="or")
    try_add_rule(world.try_get_entrance("Level 6-10 to Level 11-15"), lambda state: state.has("Override Level 15", world.player), combine="or")

    try_add_rule(world.try_get_entrance("Level 1-5 to Level 6-10"), lambda state: state.has("Override Level 30", world.player), combine="or")
    try_add_rule(world.try_get_entrance("Level 6-10 to Level 11-15"), lambda state: state.has("Override Level 30", world.player), combine="or")
    try_add_rule(world.try_get_entrance("Level 11-15 to Level 16-20"), lambda state: state.has("Override Level 30", world.player), combine="or")
    try_add_rule(world.try_get_entrance("Level 16-20 to Level 21-25"), lambda state: state.has("Override Level 30", world.player), combine="or")
    try_add_rule(world.try_get_entrance("Level 21-25 to Level 26-30"), lambda state: state.has("Override Level 30", world.player), combine="or")

