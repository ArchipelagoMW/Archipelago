import logging
from .Rules import adventure_trophies, classic_trophies, allstar_trophies

def setup_gamevars(world) -> None:
    world.all_trophies.remove("Birdo (Trophy)")
    world.all_trophies.remove("Kraid (Trophy)")
    world.all_trophies.remove("UFO (Trophy)")
    world.all_trophies.remove("Falcon Flyer (Trophy)")
    world.all_trophies.remove("Sudowoodo (Trophy)")  # These are always in the pool and need to not be rolled randomly
    character_selection = ["Dr. Mario", "Mario", "Luigi", "Bowser", "Peach",
                            "Yoshi", "Donkey Kong", "Captain Falcon", "Ganondorf", "Falco",
                            "Fox", "Ness", "Ice Climbers", "Kirby", "Samus",
                            "Zelda", "Link", "Young Link", "Pichu", "Pikachu",
                            "Jigglypuff", "Mewtwo", "Mr. Game & Watch", "Marth", "Roy"]

    world.starting_character = character_selection[world.options.starting_character]
    world.multiworld.push_precollected(world.create_item(world.starting_character))

    if world.options.lottery_pool_mode == 1:
        for i in range(4):
            world.multiworld.itempool.append(world.create_item("Progressive Lottery Pool"))
            world.extra_item_count += 1
    elif world.options.lottery_pool_mode == 2:
        world.multiworld.itempool.append(world.create_item("Lottery Pool Upgrade (Adventure/Classic Clear)")),
        world.multiworld.itempool.append(world.create_item("Lottery Pool Upgrade (Secret Characters)")),
        world.multiworld.itempool.append(world.create_item("Lottery Pool Upgrade (200 Vs. Matches)")),
        world.multiworld.itempool.append(world.create_item("Lottery Pool Upgrade (250 Trophies)")),
        world.extra_item_count += 4

    world.total_trophy_count = world.options.trophies_required + world.options.extra_trophies
    if world.total_trophy_count > 293:
        logging.warning(f"""Warning: {world.multiworld.get_player_name(world.player)}'s generated Trophy Count is too high.
                Required: {world.options.trophies_required} | Extra: {world.options.extra_trophies}. This will be automatically capped.""")
        world.total_trophy_count = 293
        world.options.extra_trophies.value = 293 - world.options.trophies_required

    world.total_trophy_count = max(0, world.total_trophy_count - 5) #Don't create extras for the trophies that always exist
    for i in range(world.total_trophy_count):
        if not world.all_trophies:
            break
        else:
            trophy = world.random.choice(world.all_trophies)
            world.all_trophies.remove(trophy)
            world.picked_trophies.add(trophy)

    if world.options.lottery_pool_mode:
        world.required_item_count += 4

    if world.options.target_checks:
        world.location_count += 25

    if world.options.ten_man_checks:
        world.location_count += 25

    if world.options.event_checks:
        world.location_count += 45

    if world.options.enable_rare_pokemon_checks:
        world.location_count += 2

    if world.options.diskun_trophy_check:
        world.location_count += 1

    if world.options.mewtwo_unlock_check:
        world.location_count += 1

    if world.options.vs_count_checks:
        world.location_count += 7

    if world.options.hard_modes_clear:
        world.location_count += 3

    if world.options.enable_annoying_multiman_checks:
        world.location_count += 2

    if world.options.long_targettest_checks:
        world.location_count += 3

    if world.options.bonus_checks:
        world.location_count += 224
        
        if world.options.enable_rare_pokemon_checks:
            world.location_count += 2 #Pokemon bonuses

        if world.options.enable_hard_bonuses:
            world.location_count += 13

        if world.options.enable_extreme_bonuses:
            world.location_count += 7
        
        if world.options.hard_modes_clear:
            world.location_count += 1




def place_static_items(world):
    world.get_location("Trophy Room - Admire Collection").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_giga_bowser:
        world.get_location("Goal: Giga Bowser Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_crazy_hand:
        world.get_location("Goal: Crazy Hand Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_event_51:
        world.get_location("Goal: Event 51").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_all_events:
        world.get_location("Goal: All Events Clear").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_all_targets:
        world.get_location("Goal: All Targets Clear").place_locked_item(world.create_item("Sense of Accomplishment"))

def calculate_trophy_based_locations(world):
    if adventure_trophies.issubset(world.picked_trophies):
        world.all_adventure_trophies = True
    else:
        world.all_adventure_trophies = False

    if classic_trophies.issubset(world.picked_trophies):
        world.all_classic_trophies = True
    else:
        world.all_classic_trophies = False

    if allstar_trophies.issubset(world.picked_trophies):
        world.all_allstar_trophies = True
    else:
        world.all_allstar_trophies = False

    if len(world.picked_trophies) >= 250 or world.options.lottery_pool_mode:
        world.use_250_trophy_pool = True
    else:
        world.use_250_trophy_pool = False