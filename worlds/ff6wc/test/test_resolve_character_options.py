from . import FF6WCTestBase

from worlds.ff6wc.Options import StartingCharacter1, StartingCharacter2, StartingCharacter3, resolve_character_options
from worlds.ff6wc import Rom

NO_FALSE_NEGATIVE = 30  # with 30 it's 1/100 chance that an incorrect implementation will pass


class TestGogoStart(FF6WCTestBase):
    """ allowing this even though some game hosts might get angry at us for it """
    options = {
        "StartingCharacterCount": 1,
        "StartingCharacter1": "Gogo",
        "StartingCharacter2": "None",
        "StartingCharacter3": "None",
        "StartingCharacter4": "None",
    }

    def test_gogo_start(self) -> None:
        characters = resolve_character_options(self.world.options, self.world.random)
        self.assertListEqual(characters, ["Gogo"])
        self.assertEqual(self.world.options.StartingCharacterCount.value, 1)
        self.assertEqual(self.world.options.StartingCharacter1.value, StartingCharacter1.option_gogo)


class TestRandomGogoUmaro(FF6WCTestBase):
    # This is just to illustrate the test:
    # options = {
    #     "StartingCharacterCount": {
    #         1: 50,
    #         2: 50,
    #     },
    #     "StartingCharacter1": "random",
    #     "StartingCharacter2": "Celes",
    # }

    def test_1_random(self) -> None:
        TestRandomGogoUmaro.options = {
            "StartingCharacterCount": 1,
            "StartingCharacter1": "random",
            "StartingCharacter2": "Celes",
        }

        gu = {"Gogo", "Umaro"}
        for _ in range(NO_FALSE_NEGATIVE):
            self.world_setup()
            characters = resolve_character_options(self.world.options, self.world.random)
            self.assertNotIn(characters[0], gu)

        TestRandomGogoUmaro.options = {}

    def test_2_first_random(self) -> None:
        """ slot 1 random doesn't allow Gogo or Umaro, even if we have a ngu """
        TestRandomGogoUmaro.options = {
            "StartingCharacterCount": 2,
            "StartingCharacter1": "random",
            "StartingCharacter2": "Celes",
        }

        gu = {"Gogo", "Umaro"}
        for _ in range(NO_FALSE_NEGATIVE):
            self.world_setup()
            characters = resolve_character_options(self.world.options, self.world.random)
            self.assertNotIn(characters[0], gu)

        TestRandomGogoUmaro.options = {}

    def test_2_second_random(self) -> None:
        """ slot 2 random might allow Umaro, but random resolution from None won't """
        TestRandomGogoUmaro.options = {
            "StartingCharacterCount": 2,
            "StartingCharacter1": "Gogo",
            "StartingCharacter2": "None",
        }

        gu = {"Gogo", "Umaro"}
        ngu = set(Rom.characters)
        for _ in range(NO_FALSE_NEGATIVE):
            self.world_setup()
            characters = resolve_character_options(self.world.options, self.world.random)
            self.assertNotIn(characters[1], gu)
            self.assertIn(characters[1], ngu)

        TestRandomGogoUmaro.options = {}

    def test_3_random(self) -> None:
        """ slot 2 none can pick Umaro """
        TestRandomGogoUmaro.options = {
            "StartingCharacterCount": 3,
            "StartingCharacter1": "Gogo",
            "StartingCharacter2": "None",
            "StartingCharacter3": "Celes",
        }
        samples = 500
        message = (
            "You should have bought a lottery ticket instead of running these tests. "
            f"The probability of this failing is about 1 in {round(1e-18/((11/12) ** samples))} quintillion."
        )

        count_gu = 0
        for _ in range(samples):
            self.world_setup()
            characters = resolve_character_options(self.world.options, self.world.random)
            count_gu += characters[1] == "Umaro"
            if count_gu > 0:
                break
        self.assertGreater(count_gu, 0, message)

        TestRandomGogoUmaro.options = {}


class TestMiddleNone(FF6WCTestBase):
    options = {
        "StartingCharacterCount": 3,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "None",
        "StartingCharacter3": "Cyan",
    }

    def test_middle_none(self) -> None:
        characters = resolve_character_options(self.world.options, self.world.random)
        self.assertEqual(len(characters), 3)
        self.assertEqual(self.world.options.StartingCharacterCount.value, 3)
        self.assertEqual(characters[0], "Terra")
        self.assertEqual(self.world.options.StartingCharacter1.value, StartingCharacter1.option_terra)
        self.assertEqual(characters[2], "Cyan")
        self.assertEqual(self.world.options.StartingCharacter3.value, StartingCharacter3.option_cyan)
        self.assertIn(characters[1], Rom.characters)
        self.assertEqual(self.world.options.StartingCharacter2.current_key.capitalize(), characters[1])
        self.assertEqual(len(characters), len(set(characters)))


class TestDuplicates(FF6WCTestBase):
    options = {
        "StartingCharacterCount": 3,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Terra",
        "StartingCharacter3": "Terra",
    }

    def test_duplicates(self) -> None:
        characters = resolve_character_options(self.world.options, self.world.random)
        self.assertEqual(len(characters), 3)
        self.assertEqual(self.world.options.StartingCharacterCount.value, 3)
        self.assertEqual(characters[0], "Terra")
        self.assertEqual(self.world.options.StartingCharacter1.value, StartingCharacter1.option_terra)
        self.assertIn(characters[1], Rom.characters)
        self.assertEqual(self.world.options.StartingCharacter2.current_key.capitalize(), characters[1])
        self.assertIn(characters[2], Rom.characters)
        self.assertEqual(self.world.options.StartingCharacter3.current_key.capitalize(), characters[2])
        self.assertEqual(len(characters), len(set(characters)))


class TestExtraGiven(FF6WCTestBase):
    options = {
        "StartingCharacterCount": 2,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
        "StartingCharacter3": "Cyan",
    }

    def test_extra_given(self) -> None:
        characters = resolve_character_options(self.world.options, self.world.random)
        self.assertEqual(len(characters), 2)
        self.assertEqual(self.world.options.StartingCharacterCount.value, 2)
        self.assertEqual(characters[0], "Terra")
        self.assertEqual(self.world.options.StartingCharacter1.value, StartingCharacter1.option_terra)
        self.assertEqual(characters[1], "Locke")
        self.assertEqual(self.world.options.StartingCharacter2.value, StartingCharacter2.option_locke)


class TestEndNone(FF6WCTestBase):
    options = {
        "StartingCharacterCount": 3,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
        "StartingCharacter3": "None",
    }

    def test_end_none(self) -> None:
        characters = resolve_character_options(self.world.options, self.world.random)
        self.assertEqual(len(characters), 3)
        self.assertEqual(self.world.options.StartingCharacterCount.value, 3)
        self.assertEqual(characters[0], "Terra")
        self.assertEqual(self.world.options.StartingCharacter1.value, StartingCharacter1.option_terra)
        self.assertEqual(characters[1], "Locke")
        self.assertEqual(self.world.options.StartingCharacter2.value, StartingCharacter2.option_locke)
        self.assertIn(characters[2], Rom.characters)
        self.assertEqual(self.world.options.StartingCharacter3.current_key.capitalize(), characters[2])
        self.assertEqual(len(characters), len(set(characters)))
