import orjson
import unittest
from NetUtils import encode, decode


class TestSerialize(unittest.TestCase):
    def test_unbounded_int(self) -> None:
        big_number = 2**200
        round_tripped_big_number = decode(encode(orjson.Fragment(str(big_number).encode())))
        self.assertEqual(big_number, round_tripped_big_number)
        self.assertEqual(type(big_number), type(round_tripped_big_number))
