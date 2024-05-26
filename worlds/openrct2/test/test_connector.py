import unittest

class TestConn(unittest.TestCase):
    def test_conn(self) -> None:
        self.assertTrue(True, "true is true")

def run_tests():
    unittest.main(verbosity=9, warnings="error", failfast=True)

if __name__ == '__main__':
    run_tests()
