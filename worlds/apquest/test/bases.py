from test.bases import WorldTestBase

from ..world import APQuestWorld

# Tests are a big topic.
# The testing API and the core code in general empower you to test all kinds of complicated custom behavior.
# However, for APQuest, we'll stick to some of the more basic tests.


# Most of your testing will probably be done using the generic WorldTestBase.
# WorldTestBase is a class that performs a set of generic tests on your world using a given set of options.
# It also enables you to write custom tests with a slew of generic helper functions.
# The first thing you'll want to do is subclass it. You'll want to override "game" And "world" like this.
class APQuestTestBase(WorldTestBase):
    game = "APQuest"
    world: APQuestWorld


# The actual tests you write should be in files whose names start with "test_".
# Ideally, you should group similar tests together in one file, where each file has some overarching significance.

# The best order to read these tests in is:
# 1. test_easy_mode.py
# 2. test_hard_mode.py
# 3. test_extra_starting_chest.py
# 4. test_hammer.py
