import math
import typing
from typing import Dict

from BaseClasses import Region, Entrance, MultiWorld, Item, ItemClassification
from Options import OptionError
from . import Levels, Items, Weapons, Story, Locations, Options, Names, Utils as ShadowUtils
from .Names import STAGE_THE_LAST_WAY
from .Options import LevelProgression
from .Story import PathInfo



def stage_id_to_region(level_id: int, region_id = 0) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "REGION_" + level_name + "_" + str(region_id)
    return region_name

def stage_id_to_story_region(level_id: int, region_id = 0) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "STORY_REGION_" + level_name + "_" + str(region_id)
    return region_name

def character_name_to_region(name):
    return "REGION_" + name

def weapon_name_to_region(name):
    return "REGION_" + name

def region_name_for_character(stage_name, name):
    return name + "_in_" + stage_name

def region_name_for_weapon(stage_name, name):
    return name + "_in_" + stage_name


def handle_single_boss(world, boss_name):
    final_bosses_full = [boss.boss for boss in Story.DefaultStoryMode if boss.end_stage_id is None and
                         Levels.LEVEL_ID_TO_LEVEL[boss.boss] not in world.options.excluded_stages]
    final_bosses = final_bosses_full.copy()


    egg_dealers = []
    options = list(set([ b for b in final_bosses if b in Levels.BOSS_GROUPING[boss_name]]))
    for option in options:
        if option in world.available_story_levels:
            egg_dealers.append(option)

    if len(egg_dealers) > 1:
        raise OptionError(f"Story handling for {boss_name} has not worked")
    elif len(egg_dealers) == 1:
        for dealer in [ e for e in egg_dealers if e not in world.available_story_levels]:
            world.options.excluded_stages = Options.ExcludedStages(list(world.options.excluded_stages) + [Levels.LEVEL_ID_TO_LEVEL(dealer)])
    else:
        if len(options) > 0:
            choice = world.random.choice(options)
            for option in [ o for o in options if o != choice ]:
                world.options.excluded_stages = Options.ExcludedStages(list(world.options.excluded_stages) + [Levels.LEVEL_ID_TO_LEVEL[option]])


def DetermineFirstStages(world):
    first_stages_selections = []
    within_selections = []

    starting_stage_count = world.options.starting_stages.value

    remaining_first_stages = [x for x in world.available_levels if x not in Levels.BOSS_STAGES and
                              x not in Levels.LAST_STORY_STAGES]

    item_info = Items.GetItemLookupDict()
    name_map = {v.name: v for k, v in item_info.items()}

    plando_items = ShadowUtils.GetPlandoItems(world)

    if (world.options.level_progression != Options.LevelProgression.option_story and
            len(plando_items) > 0):
        item_details = [name_map[i].stageId for i in plando_items if name_map[i].type == 'level_object']
        banned_by_plando = [l for l in remaining_first_stages if l in item_details]

        if len(banned_by_plando) > 0:
            remaining_first_stages = [s for s in remaining_first_stages if s not in banned_by_plando]

    if world.options.level_progression == Options.LevelProgression.option_both and \
            world.options.story_and_select_start_together:
        # print("Check together")
        first_choice = [s.end_stage_id for s in world.shuffled_story_mode if s.start_stage_id is None][0]
        if first_choice not in remaining_first_stages:
            raise OptionError("Invalid first stage based on other settings")
        first_stages_selections.append([first_choice])
        within_selections.append(first_choice)
        remaining_first_stages = [l for l in remaining_first_stages if l not in within_selections]

    if world.options.plando_starting_stages:
        rev_level_map = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
        plando_starting_stages = [rev_level_map[x] for x in world.options.plando_starting_stages]
        plando_first_stages = [l for l in plando_starting_stages if
                               l not in within_selections and l in remaining_first_stages]
        # print("plando firsts left", plando_starting_stages, within_selections, plando_first_stages)
        first_stages_selections.append(plando_first_stages)
        within_selections.extend(plando_first_stages)
        remaining_first_stages = [l for l in remaining_first_stages if l not in within_selections]

    if world.options.starting_level_method == Options.StartingLevelMethod.option_clear_stage:
        clearable = Locations.GetStagesWithNoRequirements(world)
        clearable_stages = [l for l in clearable if l not in within_selections and l in remaining_first_stages]
        first_stages_selections.append(clearable_stages)
        within_selections.extend(clearable_stages)
        remaining_first_stages = [l for l in remaining_first_stages if l not in within_selections]

    if len(remaining_first_stages) > 0 and starting_stage_count > len(within_selections):
        first_stages_selections.append(remaining_first_stages)
        within_selections.extend(remaining_first_stages)

    possible_first_regions = [ r for r in within_selections if r not in Levels.LAST_STORY_STAGES and r not in Levels.BOSS_STAGES ]

    if world.options.level_progression != Options.LevelProgression.option_story:


        #print("Select picking", starting_stage_count, possible_first_regions, first_stages_selections)

        if starting_stage_count > len(possible_first_regions) and \
            len(first_stages_selections) > 0:

            while len(first_stages_selections) > 0 and len(possible_first_regions) < starting_stage_count:
                first_choices = first_stages_selections.pop(0)
                backup_picks = starting_stage_count - len(possible_first_regions)
                #print("backups", len(first_choices), len(possible_first_regions), backup_picks)

                if backup_picks >= len(first_choices):
                    possible_first_regions.extend(first_choices)
                else:
                    possible_first_regions.extend(world.random.sample(
                        first_choices, backup_picks))

        if starting_stage_count > len(possible_first_regions):
            starting_stage_count = len(possible_first_regions)

        first_stages = world.random.sample(possible_first_regions, starting_stage_count)
        world.first_regions = first_stages

    if world.options.level_progression != Options.LevelProgression.option_select:
        stage_ids = [ start.end_stage_id for start in world.shuffled_story_mode if start.start_stage_id is None ]
        world.first_regions.extend(stage_ids)
        pass

def DetermineGates(world):
    gate_mode = world.options.select_gates
    select_gates_count = world.options.select_gates_count + 1

    if gate_mode == Options.SelectGates.option_off:
        return {}

    stages_to_assign = [ l for l in Levels.ALL_STAGES if l in world.available_select_stages ]

    #print("WFIRST", world.first_regions)
    #fake_gates = {0: world.first_regions, 1: [Levels.BOSS_BLACK_BULL_LH, Levels.BOSS_EGG_BREAKER_MM, Levels.STAGE_BLACK_COMET], 2: [Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_MAD_MATRIX]}
    #return fake_gates

    world.random.shuffle(stages_to_assign)

    gates = {0: world.first_regions}
    weights = []

    for i in range(1, select_gates_count):
        gates[i] = []
        percentage = i / select_gates_count * 100
        weight = 50
        if gate_mode == Options.SelectGates.option_early:
            weight = int((100 - percentage) * weight)
        elif gate_mode == Options.SelectGates.option_late:
            weight = int(percentage * weight)

        weights.append(weight)

    valid_gates = [ l for l in gates.keys() if l != 0 ]

    for stage in stages_to_assign:
        empty_gates = [ g[0] for g in gates.items() if len(g[1]) == 0 ]
        if len(empty_gates) > 0:
            randomised_gate = world.random.choice(empty_gates)
        else:
            randomised_gate = world.random.choices(valid_gates, k=1, weights=weights)[0]
        gates[randomised_gate].append(stage)

    return gates


def early_region_checks(world):

    # needto iterate in story order, not default order
    available_story_stages = []
    available_select_stages = []

    # TODO: Recall why story sorted order is used rather than randomly
    story_sorted_stages = Story.StoryToOrder(world.shuffled_story_mode)

    last_way_required = not world.options.include_last_way_shuffle or world.options.level_progression == Options.LevelProgression.option_select

    if last_way_required:
        story_sorted_stages.append(Levels.STAGE_THE_LAST_WAY)
        story_sorted_stages.append(Levels.BOSS_DEVIL_DOOM)

    #if (world.options.story_shuffle and world.options.story_boss_count == 0 and world.options.select_bosses and
    #        world.options.level_progression != Options.LevelProgression.option_story):
    #    mid_boss_stages = [ s for s in Levels.ALL_STAGES if s in Levels.BOSS_STAGES and s not in Levels.FINAL_BOSSES
    #                        and Levels.LEVEL_ID_TO_LEVEL[s] not in world.options.excluded_stages
    #                        and (Story.GetVanillaBossStage(s) is None or s in Levels.FINAL_BOSSES
    #                             or Levels.LEVEL_ID_TO_LEVEL[
    #                                 Story.GetVanillaBossStage(s)] not in world.options.excluded_stages)
    #                        ]
    #    story_sorted_stages.extend(mid_boss_stages)
    #    available_select_stages.extend(mid_boss_stages)


    for level in story_sorted_stages:
        if Levels.LEVEL_ID_TO_LEVEL[level] in world.options.excluded_stages and \
            (level != Levels.STAGE_THE_LAST_WAY or not last_way_required):
            continue

        if world.options.level_progression != Options.LevelProgression.option_select:
            story_routes_to_stage = [ s for s in world.shuffled_story_mode if
                                      s.end_stage_id == level
                                      and
                                      ((s.start_stage_id is None) or
                                      ( Levels.GetLevelCompletionNames(s.start_stage_id,
                                      s.alignment_id)[1] not in
                                      world.options.exclude_locations
                                        and s.start_stage_id in available_story_stages
                                        ) and
                                       Levels.LEVEL_ID_TO_LEVEL[s.start_stage_id] not in world.options.excluded_stages)

                                      ]
            if len(story_routes_to_stage) > 0:
                available_story_stages.append(level)
                world.available_levels.append(level)
                for story_route in story_routes_to_stage:
                    if story_route.boss is not None and story_route.boss not in available_story_stages\
                            and story_route.start_stage_id in world.available_levels:
                        world.available_levels.append(story_route.boss)
                        available_story_stages.append(story_route.boss)
                        break

            stage_as_boss = [ s.boss for s in world.shuffled_story_mode if s.boss == level and
                              s.start_stage_id in world.available_levels and level not in available_story_stages
                              and s.start_stage_id in available_story_stages]
            if len(stage_as_boss) > 0:
                available_story_stages.extend(list(set(stage_as_boss)))
                world.available_levels.append(level)

        if (world.options.level_progression != Options.LevelProgression.option_story \
                and ( level not in Levels.BOSS_STAGES or world.options.select_bosses )
                #and level not in Levels.FINAL_BOSSES
                #and level != Levels.BOSS_DEVIL_DOOM
                #and level not in Levels.LAST_STORY_STAGES # Until resolved
                and (Story.GetVanillaBossStage(level) is None or level in Levels.FINAL_BOSSES
                     or Levels.LEVEL_ID_TO_LEVEL[Story.GetVanillaBossStage(level)] not in world.options.excluded_stages)
                #and not last_way_required
                and level not in world.available_levels):
            world.available_levels.append(level)

        if level == Levels.STAGE_THE_LAST_WAY and last_way_required:
            world.available_levels.append(level)

        if level == Levels.BOSS_DEVIL_DOOM and last_way_required:
            world.available_levels.append(level)



    world.available_story_levels = available_story_stages

    if world.options.level_progression == Options.LevelProgression.option_story and not world.options.story_shuffle:
        not_excluded_stages = [ x for x in Levels.ALL_STAGES if x not in Levels.BOSS_STAGES and x not in Levels.LAST_STORY_STAGES and
                                Names.LEVEL_ID_TO_LEVEL[x] not in world.options.excluded_stages]
        available_story_stages_no_bosses = [ x for x in world.available_story_levels if x not in Levels.BOSS_STAGES]
        if len(not_excluded_stages) != len(available_story_stages_no_bosses):
            raise OptionError("Invalid stage accessibility for Story w/o Shuffle")

    if world.options.level_progression == Options.LevelProgression.option_both:
        story_inaccessible_stages = [ s for s in world.available_levels if s not in world.available_story_levels
                                      and s not in [Levels.LAST_STORY_STAGES] ]
        available_select_stages.extend(story_inaccessible_stages)

    total_select_stages = math.ceil(len(world.available_levels) * world.options.select_percentage / 100)
    while len(available_select_stages) < total_select_stages:
        available_stages = [ l for l in world.available_levels if l not in available_select_stages
                             and l not in [Levels.BOSS_DEVIL_DOOM]
                             and (Story.GetVanillaBossStage(l) is None or l in Levels.FINAL_BOSSES
                                                               or Levels.LEVEL_ID_TO_LEVEL[
                                                                   Story.GetVanillaBossStage(l)] not in world.options.excluded_stages )]
        if len(available_stages) == 0:
            break
        new_item = world.random.choice(available_stages)
        available_select_stages.append(new_item)

    if world.options.level_progression != Options.LevelProgression.option_story:
        world.available_select_stages = available_select_stages

    for char_name in Levels.CharacterToLevel.keys():
        levels_in = Levels.CharacterToLevel[char_name]
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        world.available_characters.append(char_name)

    for weapon in Weapons.WEAPON_INFO:
        levels_in = weapon.available_stages
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]

        if len(levels_left) == 0:
            continue

        #handle LW Only levels, but still add to the item pool!
        levels_left_lw = levels_left
        if world.options.exclude_go_mode_items and not world.options.include_last_way_shuffle:
            levels_left_lw = [ l for l in levels_left if l != STAGE_THE_LAST_WAY]

        if len(levels_left_lw) == 0:
            world.go_mode_weapons_only.append(weapon.name)

        world.available_weapons.append(weapon.name)

def create_regions(world) -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    stages = Levels.ALL_STAGES

    stage_regions = []
    region_to_stage_id = {}

    last_way_standard = (world.options.level_progression == Options.LevelProgression.option_select
                         or not world.options.include_last_way_shuffle or not world.options.story_shuffle == Options.StoryShuffle.option_chaos)

    first_regions = []
    for level_id in stages:
        if level_id not in world.available_levels:
            continue

        base_region_name = stage_id_to_region(level_id, 0)
        new_region = Region(base_region_name, world.player, world.multiworld)
        regions[base_region_name] = new_region
        stage_regions.append(new_region)
        region_to_stage_id[new_region] = level_id

        if level_id in world.first_regions:
            first_regions.append(new_region)

        for additional_region in [ r for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.stageId == level_id]:

            if additional_region.hardLogicOnly and \
                world.options.logic_level != Options.LogicLevel.option_hard:
                continue

            new_region_name = stage_id_to_region(level_id, additional_region.regionIndex)
            new_additional_region = Region(new_region_name, world.player, world.multiworld)
            regions[new_region_name] = new_additional_region

        if world.options.level_progression != LevelProgression.option_select:
            if level_id == Levels.STAGE_THE_LAST_WAY and last_way_standard:
                continue

            story_region_name = stage_id_to_story_region(level_id)
            new_story_region = Region(story_region_name, world.player, world.multiworld)
            regions[story_region_name] = new_story_region

            connect(world.player, "stage-access:"+Levels.LEVEL_ID_TO_LEVEL[level_id],
                    new_story_region, new_region)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)

    for region in first_regions:
        regions["Menu"].connect(regions[region.name], "Start Game "+region.name)

    if world.options.level_progression != LevelProgression.option_story:
        for region in stage_regions:
            #if region not in first_regions:
            stage_id = region_to_stage_id[region]

            connect_name = "menu-to-stage-"+str(stage_id)
            stage_item_name = Items.GetStageUnlockItem(stage_id)
            boss_item_name = None
            boss_stage_requirement = None

            if stage_id in Levels.LAST_STORY_STAGES:
                continue
            if stage_id in Levels.BOSS_STAGES:
                if stage_id not in Levels.LAST_STORY_STAGES and stage_id not in Levels.FINAL_BOSSES:
                    boss_stage_requirement = Story.GetVanillaBossStage(stage_id)
                    if boss_stage_requirement is not None:
                        boss_item_name = Items.GetStageUnlockItem(boss_stage_requirement)

            connect_rule = None
            if boss_item_name is None:
                connect_rule = lambda state, si=stage_item_name: state.has(si, world.player)
            elif boss_stage_requirement is not None and world.options.level_progression == LevelProgression.option_both:

                # check if available via story
                # check if available via select

                possible_via_select = True
                possible_via_story = True

                vanilla_boss_stage = Story.GetVanillaBossStage(stage_id)

                if vanilla_boss_stage is not None and vanilla_boss_stage not in world.available_levels:
                    possible_via_select = False

                if len([ s for s in world.shuffled_story_mode if s == stage_id ]) == 0:
                    possible_via_story = False

                if possible_via_story and possible_via_select:
                    connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name, b_stage=boss_stage_requirement: (
                            state.has(si, world.player) and
                            (state.has(b_name, world.player)
                             or
                             state.can_reach_region(stage_id_to_story_region(b_stage),world.player))
                             )
                elif possible_via_select:
                    connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name: (
                            state.has(si, world.player) and
                            state.has(b_name, world.player)
                    )
                    # Nothing to do, this is select logic
                    pass
                elif possible_via_story:
                    # Don't add route to stage via select!
                    pass

            else:
                connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name: (
                        state.has(si, world.player) and state.has(b_name, world.player)
                )

            if connect_rule is not None:
                connect(world.player, connect_name,
                        regions["Menu"], region, connect_rule)

    for char_name in Levels.CharacterToLevel.keys():
        levels_in = Levels.CharacterToLevel[char_name]
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        region_name = character_name_to_region(char_name)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.available_characters.append(char_name)

    for weapon in Weapons.WEAPON_INFO:
        if weapon.name not in world.available_weapons:
            continue

        region_name = weapon_name_to_region(weapon.name)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.available_weapons.append(weapon.name)

    #regions["FinalStory"] = Region("FinalStory", world.player, world.multiworld)
    #connect(world.player, "final-story-unlock", regions["Menu"],
    #        regions["FinalStory"])

    #regions["DevilDoom"] = Region("DevilDoom", world.player, world.multiworld)

    ##if last_way_standard:
   #     last_way_region = regions[stage_id_to_region(Levels.STAGE_THE_LAST_WAY)]
   #     connect(world.player, 'LastStoryToLastWay', regions["Menu"], last_way_region)



        #connect(world.player, "final-story-unlock-tlw", regions["FinalStory"],
        #        last_way_region)



    return regions

def connect_by_story_mode(multiworld: MultiWorld, world, player: int, order: typing.List[PathInfo]):

    for path in order:
        if path.start_stage_id is None:
            start_region = world.get_region("Menu")
            end_region_name = stage_id_to_story_region(path.end_stage_id)
            end_region = world.get_region(end_region_name)

            secret_rule = None
            #if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
            #    warp_item = Items.GetStageWarpItem(path.end_stage_id)
            #    secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)

            connect(world.player, "Base Story Entrance_" + str(order.index(path)) + str(path.start_stage_id) + "/" +
                    str(path.end_stage_id), start_region, end_region, rule=secret_rule)
            continue

        # Boss handling before here, because we need to hande bosses

        boss_region = None
        boss_rule = None
        boss_base_region = None

        if path.start_stage_id not in world.available_story_levels:
            continue

        if path.end_stage_id is not None and path.end_stage_id not in world.available_story_levels \
                and (path.boss is None or path.boss not in world.available_story_levels):
            continue

        start_base_region_name = stage_id_to_story_region(path.start_stage_id)
        start_region = world.get_region(start_base_region_name)

        invalid_boss = False
        if path.boss is not None:
            if path.boss in world.available_story_levels: # and path.end_stage_id is not None:
                boss_base_region_name = stage_id_to_region(path.boss)
                boss_base_region = world.get_region(boss_base_region_name)

                boss_region_name = stage_id_to_story_region(path.boss)
                boss_region = world.get_region(boss_region_name)

                if path.end_stage_id is not None and path.end_stage_id in world.available_story_levels:

                    boss_item = [ b for b in Locations.BossClearLocations if b.stageId == path.boss][0]
                    boss_id, boss_name = Locations.GetBossLocationName(boss_item.name, boss_item.stageId)

                    view_name = Names.GetBossClearEventName(path.boss, path.start_stage_id, path.alignment_id)

                    event_location = multiworld.get_location(view_name, player)
                    event_location.access_rule = (lambda state, n=boss_name, br=start_base_region_name: (
                        state.can_reach_location(n, player) and
                        state.can_reach_region(br, player)))

                    item_name = f"Story Access Through {Names.LEVEL_ID_TO_LEVEL[path.boss]}"

                    event_location.place_locked_item(Item(item_name,
                                                          ItemClassification.progression_skip_balancing, None, player))

                    boss_rule = lambda state, bn=item_name: state.has(bn, player)
            else:
                invalid_boss = True

        if path.end_stage_id is None:
            if boss_region is not None:
                boss_completion_location_id, boss_completion_location_name = Levels.GetLevelCompletionNames(path.start_stage_id,
                                                                                           path.alignment_id)

                view_name = Names.GetMissionClearEventName(path.start_stage_id, path.alignment_id)

                event_location = multiworld.get_location(view_name, player)
                event_location.access_rule = lambda state, n=boss_completion_location_name, rn=start_base_region_name: (
                    state.can_reach_location(n, player) and
                    state.can_reach_region(rn, player))

                item_name = (f"Story Access {Names.LEVEL_ID_TO_LEVEL[path.start_stage_id]} "
                             f"{Names.ALIGNMENT_TO_STRING[path.alignment_id]} > "
                            f"{Names.LEVEL_ID_TO_LEVEL[path.boss]}")

                event_location.place_locked_item(Item(item_name,
                                                      ItemClassification.progression_skip_balancing, None, player))

                bf_rule = lambda state, bn=item_name: state.has(bn, player)

                #bf_rule = lambda state, bn=boss_completion_location_name: state.can_reach_location(bn, player)

                if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
                    warp_item = Items.GetStageWarpItem(path.boss)
                    secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
                    bf_rule = lambda state, br=bf_rule, sr=secret_rule: br(state) and sr(state)

                boss_end_entrance = connect(world.player, "Boss Entrance_A_" + str(path.start_stage_id) + "/" +
                   str(path.alignment_id), start_region, boss_region,
                                        rule=bf_rule)

                multiworld.register_indirect_condition(start_region, boss_end_entrance)
                base_region_name = stage_id_to_region(path.start_stage_id)
                base_story_region_name = stage_id_to_story_region(path.start_stage_id)
                base_region = world.get_region(base_region_name)
                base_story_region = world.get_region(base_story_region_name)
                multiworld.register_indirect_condition(base_region, boss_end_entrance)
                multiworld.register_indirect_condition(base_story_region, boss_end_entrance)

                extra_level_regions = [l for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == path.start_stage_id]

                for region in extra_level_regions:
                    if region.hardLogicOnly and \
                            world.options.logic_level != Options.LogicLevel.option_hard:
                        continue
                    level_region_name = stage_id_to_region(region.stageId, region.regionIndex)
                    region_to_add = world.get_region(level_region_name)
                    if boss_end_entrance is not None:
                        multiworld.register_indirect_condition(region_to_add, boss_end_entrance)

            continue

        # If mission clear location is in excluded locations, ban this route
        completion_location_id, completion_location_name = Levels.GetLevelCompletionNames(path.start_stage_id,
                                                                                   path.alignment_id)

        if completion_location_name in world.options.exclude_locations and \
            path.start_stage_id != path.end_stage_id:
            print("Unable to take story path due to excluded location:", path.start_stage_id, path.alignment_id)
            continue

        if invalid_boss:
            continue

        extra_level_regions = [ l for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == path.start_stage_id ]

        view_name = Names.GetMissionClearEventName(path.start_stage_id, path.alignment_id)

        event_location = multiworld.get_location(view_name, player)
        event_location.access_rule = (lambda state, n=completion_location_name, er=start_base_region_name:
            state.can_reach_location(n, player) and
            state.can_reach_region(er, player))

        item_name = (f"Story Access {Names.LEVEL_ID_TO_LEVEL[path.start_stage_id]} "
                                              f"{Names.ALIGNMENT_TO_STRING[path.alignment_id]} > "
                                              f"{Names.LEVEL_ID_TO_LEVEL[path.end_stage_id]}"
                                              "" if path.boss is None else " via " + Names.LEVEL_ID_TO_LEVEL[path.boss])

        event_location.place_locked_item(Item(item_name,
                                              ItemClassification.progression_skip_balancing, None, player))

        base_rule = lambda state,n=item_name: state.has(n, player)
        boss_base_rule = base_rule
        if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
            warp_item = Items.GetStageWarpItem(path.end_stage_id)
            secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
            base_rule = lambda state, br=base_rule, sr=secret_rule: br(state) and sr(state)

        boss_entrance = None
        if boss_region is not None:

            if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
                warp_item = Items.GetStageWarpItem(path.boss)
                secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
                boss_base_rule = lambda state, br=boss_base_rule, sr=secret_rule: br(state) and sr(state)

            boss_entrance = connect(world.player, "Boss Entrance_B_"+str(order.index(path)) + str(path.start_stage_id) + "/",
                    start_region, boss_region, rule=boss_base_rule)
            multiworld.register_indirect_condition(start_region, boss_entrance)
            base_region_name = stage_id_to_region(path.start_stage_id)
            base_region = world.get_region(base_region_name)
            multiworld.register_indirect_condition(base_region, boss_entrance)

        if path.end_stage_id is not None and path.end_stage_id not in world.available_story_levels:
            continue

        end_region_name = stage_id_to_story_region(path.end_stage_id)
        end_region = world.get_region(end_region_name)

        if boss_rule is not None:
            modified_rule = lambda state, r_rule=base_rule, b_rule=boss_rule: (r_rule(state) and b_rule(state))
        else:
            modified_rule = base_rule

        new_entrance = connect(world.player, "Story Entrance_"+str(path.start_stage_id) + "/" +
                    str(path.end_stage_id)+"/"+str(path.alignment_id), start_region, end_region, rule=modified_rule)

        for region in extra_level_regions:
            if region.hardLogicOnly and \
                    world.options.logic_level != Options.LogicLevel.option_hard:
                continue
            level_region_name = stage_id_to_region(region.stageId, region.regionIndex)
            region_to_add = world.get_region(level_region_name)
            multiworld.register_indirect_condition(region_to_add, new_entrance)
            if boss_entrance is not None:
                multiworld.register_indirect_condition(region_to_add, boss_entrance)
                multiworld.register_indirect_condition(boss_base_region, new_entrance)


def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):

    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    return connection

def IsMatch(l1, l2):
    for l in l1:
        if l in l2:
            return True
    return False

# Find starting items to provide automatically
def FindStartingItems(world, required=False):

    starting_stages = []

    if world.options.level_progression != Options.LevelProgression.option_select:
        first_story_stage = [ s.end_stage_id for s in world.shuffled_story_mode if s.start_stage_id is None][0]
        starting_stages.append(first_story_stage)

    if world.options.level_progression != Options.LevelProgression.option_story:
        starting_stages.extend(world.first_regions)

    if len(world.starting_items) == 0:
        if len(world.options.start_inventory.value.keys()) > 0:
            world.starting_items.extend(world.options.start_inventory.value.keys())

    base_regions_by_logic = Levels.GetBaseAccessibleRegions(starting_stages, world.options, world.starting_items)

    base_from_regions = [ str(s[0]) + "/" + str(s[1]) for s in base_regions_by_logic ]

    escape_options = [ r.restrictionTypes for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.stageId in starting_stages and \
                     IsMatch(base_from_regions, [ str(r.stageId)+"/"+str(fr) for fr in r.fromRegions])
                           and str(r.stageId ) + "/" + str(r.regionIndex) not in base_from_regions]

    escape_list = []
    for option in escape_options:
        for option_group in option:
            if option_group not in escape_list:
                escape_list.append(option_group)

    item_options = []
    failed_item_options = []
    for base_option in escape_options:
        if len(base_option) == 1:
            option = base_option[0]
        else:
            continue
        if option == Names.REGION_RESTRICTION_TYPES.Pulley:
            item_options.append("Pulley")
        elif option == Names.REGION_RESTRICTION_TYPES.Heal:
            item_options.append("Weapon:Heal Cannon")
        elif option == Names.REGION_RESTRICTION_TYPES.AirSaucer:
            item_options.append("Vehicle:Air Saucer")
        elif option == Names.REGION_RESTRICTION_TYPES.BlackArmsTurret:
            item_options.append("Vehicle:Black Turret")
        elif option == Names.REGION_RESTRICTION_TYPES.BlackHawk:
            item_options.append("Vehicle:Black Hawk")
        elif option == Names.REGION_RESTRICTION_TYPES.BlackVolt:
            item_options.append("Vehicle:Black Volt")
        elif option == Names.REGION_RESTRICTION_TYPES.Explosion:
            item_options.append("Bombs")
        elif option == Names.REGION_RESTRICTION_TYPES.GunTurret:
            item_options.append("Vehicle:Gun Turret")
        elif option == Names.REGION_RESTRICTION_TYPES.LightDash:
            item_options.append("Air Shoes")
        elif option == Names.REGION_RESTRICTION_TYPES.Rocket:
            item_options.append("Rocket")
        elif option == Names.REGION_RESTRICTION_TYPES.Torch:
            item_options.append("Weapon:Cryptic Torch")
        elif option == Names.REGION_RESTRICTION_TYPES.GunJumper:
            item_options.append("Vehicle:Gun Jumper")
        elif option == Names.REGION_RESTRICTION_TYPES.WarpHole:
            item_options.append("Warp Holes")
        elif option == Names.REGION_RESTRICTION_TYPES.Zipwire:
            item_options.append("Zipwire")
        elif option == Names.REGION_RESTRICTION_TYPES.Vacuum:
            item_options.append("Weapon:Vacuum Pod")
        else:
            failed_item_options.append(option)

    if len(item_options) == 0:
        if required:
            print("Unknown error with obtaining anti-lock mechanism", failed_item_options)
            raise OptionError("Invalid item options")
        return []

    item_options = list(set(item_options))
    return [world.random.choice(item_options)]




