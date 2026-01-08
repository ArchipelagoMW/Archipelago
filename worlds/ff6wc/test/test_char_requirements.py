from . import FF6WCTestBase


class TestStartWithTwoCharsDefineThree(FF6WCTestBase):
    """
    While testing to make sure Kefka's Tower requires at least 3 characters,
    I found a bug where it behaves differently if I define the StartingCharacter3 option
    (even though the StartingCharacterCount is 2)
    """
    options = {
        "CharacterCount": 0,
        "EsperCount": 0,
        "DragonCount": 0,
        "BossCount": 0,
        "StartingCharacterCount": 2,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
        "StartingCharacter3": "Cyan",
    }

    def test_start_with_2(self):
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Umaro"))
        self.assertBeatable(True)


class TestStartWithTwoChars(FF6WCTestBase):
    options = {
        "CharacterCount": 0,
        "EsperCount": 0,
        "DragonCount": 0,
        "BossCount": 0,
        "StartingCharacterCount": 2,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
    }

    def test_start_with_2(self):
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Umaro"))
        self.assertBeatable(True)


class TestStartWithOneCharDefineThree(FF6WCTestBase):
    options = {
        "CharacterCount": 0,
        "EsperCount": 0,
        "DragonCount": 0,
        "BossCount": 0,
        "StartingCharacterCount": 1,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
        "StartingCharacter3": "Cyan",
    }

    def test_start_with_1(self):
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Umaro"))
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Gogo"))
        self.assertBeatable(True)


class TestStartWithOneChar(FF6WCTestBase):
    options = {
        "CharacterCount": 0,
        "EsperCount": 0,
        "DragonCount": 0,
        "BossCount": 0,
        "StartingCharacterCount": 1,
        "StartingCharacter1": "Terra",
    }

    def test_start_with_1(self):
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Umaro"))
        self.assertBeatable(False)
        self.collect(self.get_item_by_name("Gogo"))
        self.assertBeatable(True)


class TestStartWithThreeChars(FF6WCTestBase):
    options = {
        "CharacterCount": 0,
        "EsperCount": 0,
        "DragonCount": 0,
        "BossCount": 0,
        "StartingCharacterCount": 3,
        "StartingCharacter1": "Terra",
        "StartingCharacter2": "Locke",
        "StartingCharacter3": "Cyan",
    }

    def test_start_with_3(self):
        self.assertBeatable(True)
