"""Verify that NetUtils' enums work correctly with all supported Python versions."""

import unittest
from enum import Enum
from typing import Type

from NetUtils import ClientStatus, HintStatus, SlotType
from Utils import restricted_dumps, restricted_loads


class Base:
    class DataEnumTest(unittest.TestCase):
        type: Type[Enum]
        value: Enum

        def test_unpickle(self) -> None:
            """Tests that enums used in multidata or multisave can be pickled and unpickled."""
            pickled = pickle.dumps(self.value)
            unpickled = restricted_loads(pickled)
            self.assertEqual(unpickled, self.value)
            self.assertIsInstance(unpickled, self.type)


class HintStatusTest(Base.DataEnumTest):
    type = HintStatus
    value = HintStatus.HINT_AVOID


class ClientStatusTest(Base.DataEnumTest):
    type = ClientStatus
    value = ClientStatus.CLIENT_GOAL


class SlotTypeTest(Base.DataEnumTest):
    type = SlotType
    value = SlotType.player
