import unittest

from ..resource_state_vars import dict_to_rs, rs_leq


class TestLT(unittest.TestCase):

    def test_one(self):
        state1 = dict_to_rs({"OVERCHARMED": 1})
        state2 = dict_to_rs({"OVERCHARMED": 2})
        outcome = True

        assert outcome == rs_leq(state1, state2)

    def test_two(self):
        state1 = dict_to_rs({"OVERCHARMED": 1})
        state2 = dict_to_rs({"OVERCHARMED": 1, "USEDSHADE": 1})
        outcome = True

        assert outcome == rs_leq(state1, state2)

    def test_three(self):
        state1 = dict_to_rs({"OVERCHARMED": 2})
        state2 = dict_to_rs({"OVERCHARMED": 1, "USEDSHADE": 1})
        outcome = False

        assert outcome == rs_leq(state1, state2)

    # this case is irrelevant if we move to effectively le instead
    # def test_four(self):
    #     state1 = {"OVERCHARMED": 2}
    #     state2 = {"OVERCHARMED": 2}
    #     outcome = False

    #     assert outcome == lt(state1, state2)
