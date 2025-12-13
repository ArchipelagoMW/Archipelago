from ..Options import BossHuntLength, JinjoFamilyRescueLength, MinigameHuntLength, VictoryCondition
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from ..Names import locationName

# Tests and make sure that if the correct Victory Condition is set, enough Mumbo Tokens are placed
# and the game is beatable.


class TokenTest(BanjoTooieTestBase):
    mumbo_token_location_group = set()

    def test_mumbo_tokens(self, amt: int | None = None) -> None:
        if amt is None:
            amt = len(self.mumbo_token_location_group)

        # Randomized tokens for Token Hunt
        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1

        # Locked locations for every other Mumbo token vic con
        for location in self.mumbo_token_location_group:
            item = self.world.get_location(location).item
            if item is not None:
                if "Mumbo Token" == item.name:
                    mumbo_tokens += 1
        assert amt == mumbo_tokens


class TestVictoryHAG1(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_hag1,
    }
    mumbo_token_location_group = set()

    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)


class TestVictoryHAG1Intended(TestVictoryHAG1, IntendedLogic):
    options = {
        **TestVictoryHAG1.options,
        **IntendedLogic.options
    }


class TestVictoryHAG1EasyTricks(TestVictoryHAG1, EasyTricksLogic):
    options = {
        **TestVictoryHAG1.options,
        **EasyTricksLogic.options
    }


class TestVictoryHAG1HardTricks(TestVictoryHAG1, HardTricksLogic):
    options = {
        **TestVictoryHAG1.options,
        **HardTricksLogic.options
    }


class TestVictoryHAG1Glitches(TestVictoryHAG1, GlitchesLogic):
    options = {
        **TestVictoryHAG1.options,
        **GlitchesLogic.options
    }


class TestVictoryMinigames(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_minigame_hunt
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNGAME2,
        locationName.MUMBOTKNGAME3,
        locationName.MUMBOTKNGAME4,
        locationName.MUMBOTKNGAME5,
        locationName.MUMBOTKNGAME6,
        locationName.MUMBOTKNGAME7,
        locationName.MUMBOTKNGAME8,
        locationName.MUMBOTKNGAME9,
        locationName.MUMBOTKNGAME10,
        locationName.MUMBOTKNGAME11,
        locationName.MUMBOTKNGAME12,
        locationName.MUMBOTKNGAME13,
        locationName.MUMBOTKNGAME14,
        locationName.MUMBOTKNGAME15
    }


class TestVictoryMinigamesShort(TestVictoryMinigames):
    options = {
        **TestVictoryMinigames.options,
        "minigame_hunt_length": MinigameHuntLength.range_start
    }


class TestVictoryMinigamesLong(TestVictoryMinigames):
    options = {
        **TestVictoryMinigames.options,
        "minigame_hunt_length": MinigameHuntLength.range_end
    }


class TestVictoryMinigamesIntended(TestVictoryMinigames, IntendedLogic):
    options = {
        **TestVictoryMinigames.options,
        **IntendedLogic.options
    }


class TestVictoryMinigamesEasyTricks(TestVictoryMinigames, EasyTricksLogic):
    options = {
        **TestVictoryMinigames.options,
        **EasyTricksLogic.options
    }


class TestVictoryMinigamesHardTricks(TestVictoryMinigames, HardTricksLogic):
    options = {
        **TestVictoryMinigames.options,
        **HardTricksLogic.options
    }


class TestVictoryMinigamesGlitches(TestVictoryMinigames, GlitchesLogic):
    options = {
        **TestVictoryMinigames.options,
        **GlitchesLogic.options
    }


class TestVictoryMinigamesShortIntended(TestVictoryMinigamesShort, IntendedLogic):
    options = {
        **TestVictoryMinigamesShort.options,
        **IntendedLogic.options
    }


class TestVictoryMinigamesShortEasyTricks(TestVictoryMinigamesShort, EasyTricksLogic):
    options = {
        **TestVictoryMinigamesShort.options,
        **EasyTricksLogic.options
    }


class TestVictoryMinigamesShortHardTricks(TestVictoryMinigamesShort, HardTricksLogic):
    options = {
        **TestVictoryMinigamesShort.options,
        **HardTricksLogic.options
    }


class TestVictoryMinigamesShortGlitches(TestVictoryMinigamesShort, GlitchesLogic):
    options = {
        **TestVictoryMinigamesShort.options,
        **GlitchesLogic.options
    }


class TestVictoryMinigamesLongIntended(TestVictoryMinigamesLong, IntendedLogic):
    options = {
        **TestVictoryMinigamesLong.options,
        **IntendedLogic.options
    }


class TestVictoryMinigamesLongEasyTricks(TestVictoryMinigamesLong, EasyTricksLogic):
    options = {
        **TestVictoryMinigamesLong.options,
        **EasyTricksLogic.options
    }


class TestVictoryMinigamesLongHardTricks(TestVictoryMinigamesLong, HardTricksLogic):
    options = {
        **TestVictoryMinigamesLong.options,
        **HardTricksLogic.options
    }


class TestVictoryMinigamesLongGlitches(TestVictoryMinigamesLong, GlitchesLogic):
    options = {
        **TestVictoryMinigamesLong.options,
        **GlitchesLogic.options
    }


class TestVictoryBosses(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_boss_hunt
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8
    }


class TestVictoryBossesShort(TestVictoryBosses):
    options = {
        **TestVictoryBosses.options,
        "boss_hunt_length": BossHuntLength.range_start
    }


class TestVictoryBossesLong(TestVictoryBosses):
    options = {
        **TestVictoryBosses.options,
        "boss_hunt_length": BossHuntLength.range_end
    }


class TestVictoryBossesIntended(TestVictoryBosses, IntendedLogic):
    options = {
        **TestVictoryBosses.options,
        **IntendedLogic.options
    }


class TestVictoryBossesEasyTricks(TestVictoryBosses, EasyTricksLogic):
    options = {
        **TestVictoryBosses.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesHardTricks(TestVictoryBosses, HardTricksLogic):
    options = {
        **TestVictoryBosses.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesGlitches(TestVictoryBosses, GlitchesLogic):
    options = {
        **TestVictoryBosses.options,
        **GlitchesLogic.options
    }


class TestVictoryBossesShortIntended(TestVictoryBossesShort, IntendedLogic):
    options = {
        **TestVictoryBossesShort.options,
        **IntendedLogic.options
    }


class TestVictoryBossesShortEasyTricks(TestVictoryBossesShort, EasyTricksLogic):
    options = {
        **TestVictoryBossesShort.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesShortHardTricks(TestVictoryBossesShort, HardTricksLogic):
    options = {
        **TestVictoryBossesShort.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesShortGlitches(TestVictoryBossesShort, GlitchesLogic):
    options = {
        **TestVictoryBossesShort.options,
        **GlitchesLogic.options
    }


class TestVictoryBossesLongIntended(TestVictoryBossesLong, IntendedLogic):
    options = {
        **TestVictoryBossesLong.options,
        **IntendedLogic.options
    }


class TestVictoryBossesLongEasyTricks(TestVictoryBossesLong, EasyTricksLogic):
    options = {
        **TestVictoryBossesLong.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesLongHardTricks(TestVictoryBossesLong, HardTricksLogic):
    options = {
        **TestVictoryBossesLong.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesLongGlitches(TestVictoryBossesLong, GlitchesLogic):
    options = {
        **TestVictoryBossesLong.options,
        **GlitchesLogic.options
    }


class TestVictoryJinjos(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "logic_type": 0
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNJINJO1,
        locationName.MUMBOTKNJINJO2,
        locationName.MUMBOTKNJINJO3,
        locationName.MUMBOTKNJINJO4,
        locationName.MUMBOTKNJINJO5,
        locationName.MUMBOTKNJINJO6,
        locationName.MUMBOTKNJINJO7,
        locationName.MUMBOTKNJINJO8,
        locationName.MUMBOTKNJINJO9,
    }


class TestVictoryJinjosShort(TestVictoryJinjos):
    options = {
        **TestVictoryJinjos.options,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_start
    }


class TestVictoryJinjosLong(TestVictoryJinjos):
    options = {
        **TestVictoryJinjos.options,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_end
    }


class TestVictoryJinjosIntended(TestVictoryJinjos, IntendedLogic):
    options = {
        **TestVictoryJinjos.options,
        **IntendedLogic.options
    }


class TestVictoryJinjosEasyTricks(TestVictoryJinjos, EasyTricksLogic):
    options = {
        **TestVictoryJinjos.options,
        **EasyTricksLogic.options
    }


class TestVictoryJinjosHardTricks(TestVictoryJinjos, HardTricksLogic):
    options = {
        **TestVictoryJinjos.options,
        **HardTricksLogic.options
    }


class TestVictoryJinjosGlitches(TestVictoryJinjos, GlitchesLogic):
    options = {
        **TestVictoryJinjos.options,
        **GlitchesLogic.options
    }


class TestVictoryJinjosShortIntended(TestVictoryJinjosShort, IntendedLogic):
    options = {
        **TestVictoryJinjosShort.options,
        **IntendedLogic.options
    }


class TestVictoryJinjosShortEasyTricks(TestVictoryJinjosShort, EasyTricksLogic):
    options = {
        **TestVictoryJinjosShort.options,
        **EasyTricksLogic.options
    }


class TestVictoryJinjosShortHardTricks(TestVictoryJinjosShort, HardTricksLogic):
    options = {
        **TestVictoryJinjosShort.options,
        **HardTricksLogic.options
    }


class TestVictoryJinjosShortGlitches(TestVictoryJinjosShort, GlitchesLogic):
    options = {
        **TestVictoryJinjosShort.options,
        **GlitchesLogic.options
    }


class TestVictoryJinjosLongIntended(TestVictoryJinjosLong, IntendedLogic):
    options = {
        **TestVictoryJinjosLong.options,
        **IntendedLogic.options
    }


class TestVictoryJinjosLongEasyTricks(TestVictoryJinjosLong, EasyTricksLogic):
    options = {
        **TestVictoryJinjosLong.options,
        **EasyTricksLogic.options
    }


class TestVictoryJinjosLongHardTricks(TestVictoryJinjosLong, HardTricksLogic):
    options = {
        **TestVictoryJinjosLong.options,
        **HardTricksLogic.options
    }


class TestVictoryJinjosLongGlitches(TestVictoryJinjosLong, GlitchesLogic):
    options = {
        **TestVictoryJinjosLong.options,
        **GlitchesLogic.options
    }


class TestVictoryWonderwing(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_wonderwing_challenge
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNGAME2,
        locationName.MUMBOTKNGAME3,
        locationName.MUMBOTKNGAME4,
        locationName.MUMBOTKNGAME5,
        locationName.MUMBOTKNGAME6,
        locationName.MUMBOTKNGAME7,
        locationName.MUMBOTKNGAME8,
        locationName.MUMBOTKNGAME9,
        locationName.MUMBOTKNGAME10,
        locationName.MUMBOTKNGAME11,
        locationName.MUMBOTKNGAME12,
        locationName.MUMBOTKNGAME13,
        locationName.MUMBOTKNGAME14,
        locationName.MUMBOTKNGAME15,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8,
        locationName.MUMBOTKNJINJO1,
        locationName.MUMBOTKNJINJO2,
        locationName.MUMBOTKNJINJO3,
        locationName.MUMBOTKNJINJO4,
        locationName.MUMBOTKNJINJO5,
        locationName.MUMBOTKNJINJO6,
        locationName.MUMBOTKNJINJO7,
        locationName.MUMBOTKNJINJO8,
        locationName.MUMBOTKNJINJO9,
    }


class TestVictoryWonderwingIntended(TestVictoryWonderwing, IntendedLogic):
    options = {
        **TestVictoryWonderwing.options,
        **IntendedLogic.options
    }


class TestVictoryWonderwingEasyTricks(TestVictoryWonderwing, EasyTricksLogic):
    options = {
        **TestVictoryWonderwing.options,
        **EasyTricksLogic.options
    }


class TestVictoryWonderwingHardTricks(TestVictoryWonderwing, HardTricksLogic):
    options = {
        **TestVictoryWonderwing.options,
        **HardTricksLogic.options
    }


class TestVictoryWonderwingGlitches(TestVictoryWonderwing, GlitchesLogic):
    options = {
        **TestVictoryWonderwing.options,
        **GlitchesLogic.options
    }


class TestVictoryBossesHAG1(TokenTest):
    options = {
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNBOSS2,
        locationName.MUMBOTKNBOSS3,
        locationName.MUMBOTKNBOSS4,
        locationName.MUMBOTKNBOSS5,
        locationName.MUMBOTKNBOSS6,
        locationName.MUMBOTKNBOSS7,
        locationName.MUMBOTKNBOSS8
    }


class TestVictoryBossesHAG1Short(TestVictoryBossesHAG1):
    options = {
        **TestVictoryBossesHAG1.options,
        "boss_hunt_length": BossHuntLength.range_start
    }


class TestVictoryBossesHAG1Long(TestVictoryBossesHAG1):
    options = {
        **TestVictoryBossesHAG1.options,
        "boss_hunt_length": BossHuntLength.range_end
    }


class TestVictoryBossesHAG1Intended(TestVictoryBossesHAG1, IntendedLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **IntendedLogic.options
    }


class TestVictoryBossesHAG1EasyTricks(TestVictoryBossesHAG1, EasyTricksLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesHAG1HardTricks(TestVictoryBossesHAG1, HardTricksLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesHAG1Glitches(TestVictoryBossesHAG1, GlitchesLogic):
    options = {
        **TestVictoryBossesHAG1.options,
        **GlitchesLogic.options
    }


class TestVictoryBossesHAG1ShortIntended(TestVictoryBossesHAG1Short, IntendedLogic):
    options = {
        **TestVictoryBossesHAG1Short.options,
        **IntendedLogic.options
    }


class TestVictoryBossesHAG1ShortEasyTricks(TestVictoryBossesHAG1Short, EasyTricksLogic):
    options = {
        **TestVictoryBossesHAG1Short.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesHAG1ShortHardTricks(TestVictoryBossesHAG1Short, HardTricksLogic):
    options = {
        **TestVictoryBossesHAG1Short.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesHAG1ShortGlitches(TestVictoryBossesHAG1Short, GlitchesLogic):
    options = {
        **TestVictoryBossesHAG1Short.options,
        **GlitchesLogic.options
    }


class TestVictoryBossesHAG1LongIntended(TestVictoryBossesHAG1Long, IntendedLogic):
    options = {
        **TestVictoryBossesHAG1Long.options,
        **IntendedLogic.options
    }


class TestVictoryBossesHAG1LongEasyTricks(TestVictoryBossesHAG1Long, EasyTricksLogic):
    options = {
        **TestVictoryBossesHAG1Long.options,
        **EasyTricksLogic.options
    }


class TestVictoryBossesHAG1LongHardTricks(TestVictoryBossesHAG1Long, HardTricksLogic):
    options = {
        **TestVictoryBossesHAG1Long.options,
        **HardTricksLogic.options
    }


class TestVictoryBossesHAG1LongGlitches(TestVictoryBossesHAG1Long, GlitchesLogic):
    options = {
        **TestVictoryBossesHAG1Long.options,
        **GlitchesLogic.options
    }
