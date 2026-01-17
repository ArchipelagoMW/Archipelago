from .bases import CrystalProjectTestBase

class TestStuffingTheMostItemsIntoBeginnerRegions(CrystalProjectTestBase):
    options = {
        "goal": 2, #clamshells
        "clamshell_goal_quantity": 99,
        "extra_clamshells_in_pool": 99,
        "included_regions": 0, #beginner
        "job_rando": 2, #full
        "starting_job_quantity": 1,
        "kill_bosses_mode": 0,
        "shopsanity": 0,
        "regionsanity": 1,
        "progressive_level_size": 1,
        "max_level": 99,
        "key_mode": 2, #vanilla
        "start_with_treasure_finder": 0,
        "start_with_maps": 0,
        "include_summon_abilities": 1,
        "include_scholar_abilities": 1
    }

    run_default_tests = True