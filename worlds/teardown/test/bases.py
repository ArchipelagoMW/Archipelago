from test.bases import WorldTestBase

from ..world import TeardownWorld


# Most of your testing will probably be done using the generic WorldTestBase.
# WorldTestBase is a class that performs a set of generic tests on your world using a given set of options.
# It also enables you to write custom tests with a slew of generic helper functions.
# The first thing you'll want to do is subclass it. You'll want to override "game" And "world" like this.
class APQuestTestBase(WorldTestBase):
    game = "Teardown"
    world: TeardownWorld


# The actual tests you write should be in files whose names start with "test_".
# Ideally, you should group similar tests together in one file, where each file has some overarching significance.

# The best order to read these tests in is:
# 1. test_easy_mode.py
# 2. test_hard_mode.py
# 3. test_extra_starting_chest.py
# 4. test_hammer.py
