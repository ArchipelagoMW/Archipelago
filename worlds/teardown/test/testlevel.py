from .bases import TeardownTestBase


# When writing a test, you'll first need to subclass unittest.TestCase.
# In our case, we'll subclass the APQuestTestBase we defined in bases.py.
class BasicTestLogic(TeardownTestBase):
    # Our test base is a subclass of WorldTestBase.
    # WorldTestBase takes a dict of options and sets up a multiworld for you with a single world of your game.
    # The world will have the options you specified.
    options = {
        "Mission Amount": 40,
        "Randomize Starting Tools": False,
        "Randomize Starting Level": False,
        #"Valuable Sanity": False,

        # Options you don't specify will use their default values.
        # It is good practice to specify every option that has an impact on your test, even when it's the default value.
        # As such, we'll spell out that hard_mode is meant to be False.
    }
