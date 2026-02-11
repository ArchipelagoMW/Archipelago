from . import TwilightPrincessWorldTestBase


# Dumb testing to make sure the testing works on my machine
# Also tests the basic generation
class TestTests(TwilightPrincessWorldTestBase):
    def test_tests(self) -> None:
        self.assertTrue(True)
        self.assertFalse(False)
        with self.assertRaises(AssertionError):
            self.assertTrue(False)
