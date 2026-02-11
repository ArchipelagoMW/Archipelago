from test.bases import WorldTestBase

class FatesanityTest(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    fatesanity = True

class FishsanityTest(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    fishsanity = 1

class BigFishsanityTest(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    fishsanity = 3


class ShortTest(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    include_dungeons = False
    duty_difficulty = "Normal"
    max_party_size = "Light Party"

class FreeTrial(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    level_cap = 70
    goal = "defeat shinryu"

class ArrFish(WorldTestBase):
    game = "Manual_FFXIV_Silasary"

    fishsanity = 1
    level_cap = 50
    duty_difficulty = "no_duties"
