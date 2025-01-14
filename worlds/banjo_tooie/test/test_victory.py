from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

#Tests and make sure that if the correct Victory Condition is set, enough Mumbo Tokens are placed
# and the game is beatable.
class TokenTest(BanjoTooieTestBase):
    mumbo_token_location_group = {}

    def test_mumbo_tokens(self, amt = None) -> None:
        if amt == None:
            amt = len(self.mumbo_token_location_group)

        mumbo_tokens = 0
        for item in self.world.multiworld.itempool:
            if "Mumbo Token" == item.name:
                mumbo_tokens += 1

        for location in self.mumbo_token_location_group:
            try:
                if "Mumbo Token" == self.world.multiworld.get_location(location, self.player).item.name:
                    mumbo_tokens += 1
            except:
                mumbo_tokens += 0
        assert amt == mumbo_tokens

class TestVictoryHAG1Easy(TokenTest):
    options = {
        'victory_condition': 0,
        'logic_type': 0
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }
    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)

class TestVictoryHAG1Normal(TokenTest):
    options = {
        'victory_condition': 0,
        'logic_type': 1
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }
    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)

class TestVictoryHAG1Advance(TokenTest):
    options = {
        'victory_condition': 0,
        'logic_type': 2
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }
    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)

class TestVictoryHAG1Glitch(TokenTest):
    options = {
        'victory_condition': 0,
        'logic_type': 3
    }
    mumbo_token_location_group = {
        locationName.MUMBOTKNGAME1,
        locationName.MUMBOTKNBOSS1,
        locationName.MUMBOTKNJINJO1
    }
    def test_mumbo_tokens(self) -> None:
        super().test_mumbo_tokens(0)

class TestVictoryMiniGamesEasy(TokenTest):
    options = {
        'victory_condition': 1,
        'logic_type': 0
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

class TestVictoryMiniGamesNormal(TokenTest):
    options = {
        'victory_condition': 1,
        'logic_type': 1
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

class TestVictoryMiniGamesAdvance(TokenTest):
    options = {
        'victory_condition': 1,
        'logic_type': 2
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

class TestVictoryMiniGamesGlitch(TokenTest):
    options = {
        'victory_condition': 1,
        'logic_type': 3
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

class TestVictoryBossesEasy(TokenTest):
    options = {
        'victory_condition': 2,
        'logic_type': 0
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

class TestVictoryBossesNormal(TokenTest):
    options = {
        'victory_condition': 2,
        'logic_type': 1
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

class TestVictoryBossesAdvance(TokenTest):
    options = {
        'victory_condition': 2,
        'logic_type': 2
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

class TestVictoryBossesGlitch(TokenTest):
    options = {
        'victory_condition': 2,
        'logic_type': 3
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

class TestVictoryJinjoEasy(TokenTest):
    options = {
        'victory_condition': 3,
        'logic_type': 0
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

class TestVictoryJinjoNormal(TokenTest):
    options = {
        'victory_condition': 3,
        'logic_type': 1
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

class TestVictoryJinjoAdvance(TokenTest):
    options = {
        'victory_condition': 3,
        'logic_type': 2
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

class TestVictoryJinjoGlitch(TokenTest):
    options = {
        'victory_condition': 3,
        'logic_type': 3
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

class TestVictoryWonderWingEasy(TokenTest):
    options = {
        'victory_condition': 4,
        'logic_type': 0
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

class TestVictoryWonderWingNormal(TokenTest):
    options = {
        'victory_condition': 4,
        'logic_type': 1
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

class TestVictoryWonderWingAdvance(TokenTest):
    options = {
        'victory_condition': 4,
        'logic_type': 2
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

class TestVictoryWonderWingGlitch(TokenTest):
    options = {
        'victory_condition': 4,
        'logic_type': 3
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
