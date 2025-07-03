from .bases import CrystalProjectTestBase

class TestStuffingTheMostItemsIntoBeginnerRegions(CrystalProjectTestBase):
    options = {
        "goal": 2, #clamshells
        "clamshellGoalQuantity": 99,
        "extraClamshellsInPool": 99,
        "includedRegions": 0, #beginner
        "jobRando": 2, #full
        "startingJobQuantity": 1,
        "killBossesMode": 0,
        "shopsanity": 0,
        "regionsanity": 1,
        "progressiveLevelSize": 3,
        "maxLevel": 99,
        "keyMode": 2, #vanilla
        "startWithTreasureFinder": 0,
        "startWithMaps": 1,
        "includeSummonAbilities": 1,
        "includeScholarAbilities": 1
    }
    #Todo: turn off start with maps in the future once we get enough item massaging for that to not break unit tests
    run_default_tests = True