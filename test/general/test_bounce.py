import unittest
from unittest.mock import MagicMock

from MultiServer import BounceTarget


def create_mock_client(team: int, game: str, tags: set[str], slot: int):
    client = MagicMock()
    client.team = team
    client.tags = tags
    client.slot = slot

    ctx = MagicMock()
    ctx.games = {slot: game}

    client.ctx = lambda: ctx

    return client


TEAM_1_SLOT_1 = create_mock_client(1, "TestGame", set(), 1)
TEAM_1_SLOT_2 = create_mock_client(1, "TestGame", {"DeathLink", "TrapLink"}, 2)
TEAM_1_SLOT_3 = create_mock_client(1, "TestGame 2", {"DeathLink"}, 3)
TEAM_2_SLOT_1 = create_mock_client(2, "TestGame", set(), 1)
TEAM_2_SLOT_2 = create_mock_client(2, "TestGame", {"DeathLink", "TrapLink"}, 2)
TEAM_2_SLOT_3 = create_mock_client(2, "TestGame 2", {"DeathLink"}, 3)

ALL_CLIENTS = [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_1, TEAM_2_SLOT_2, TEAM_2_SLOT_3]


class TestBounceTargetLegacy(unittest.TestCase):
    """
    Test various BounceTarget configurations against six mock clients with different teams, games, tags and slots.

    Uses the "legacy" operator, which is defined as: "team and (game or tags or slot)".
    """

    def test_legacy_bounce_target_default(self):
        bounce_target = BounceTarget(None, None, None, None)

        assert list(bounce_target.match_clients_legacy(ALL_CLIENTS)) == []

    def test_legacy_bounce_team_only(self):
        bounce_target = BounceTarget({1}, None, None, None)

        assert list(bounce_target.match_clients_legacy(ALL_CLIENTS)) == []

    def test_legacy_tags_condition_only(self):
        bounce_target = BounceTarget(None, None, {"DeathLink"}, None)

        self.assertEqual(
            list(bounce_target.match_clients_legacy(ALL_CLIENTS)),
            [TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_2, TEAM_2_SLOT_3],
        )

    def test_legacy_slot_condition_only(self):
        bounce_target = BounceTarget(None, None, None, {2})

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_1_SLOT_2, TEAM_2_SLOT_2])

    def test_legacy_empty_conditions(self):
        bounce_target = BounceTarget(set(), set(), set(), set())

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [])

    def test_legacy_empty_conditions_except_slot(self):
        bounce_target = BounceTarget(set(), set(), set(), {3})

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [])

    def test_legacy_empty_conditions_except_tags_and_team(self):
        bounce_target = BounceTarget({1}, set(), {"DeathLink"}, set())

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_1_SLOT_2, TEAM_1_SLOT_3])

    def test_legacy_all(self):
        bounce_target = BounceTarget({2}, {"TestGame 2"}, {"DeathLink"}, {1})

        self.assertEqual(
            list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_2_SLOT_1, TEAM_2_SLOT_2, TEAM_2_SLOT_3]
        )

    def test_legacy_multiple_games(self):
        bounce_target = BounceTarget({1}, {"TestGame", "TestGame 2"}, None, None)

        self.assertEqual(
            list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3]
        )

    def test_legacy_multiple_tags(self):
        bounce_target = BounceTarget({2}, None, {"DeathLink", "TrapLink"}, None)

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_2_SLOT_2, TEAM_2_SLOT_3])

    def test_legacy_multiple_slots(self):
        bounce_target = BounceTarget(None, None, None, {1, 2})

        self.assertEqual(
            list(bounce_target.match_clients_legacy(ALL_CLIENTS)),
            [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_2_SLOT_1, TEAM_2_SLOT_2],
        )

    def test_legacy_multiple_teams(self):
        bounce_target = BounceTarget({1, 2}, None, None, {1})

        self.assertEqual(list(bounce_target.match_clients_legacy(ALL_CLIENTS)), [TEAM_1_SLOT_1, TEAM_2_SLOT_1])


class TestBounceTargetOr(unittest.TestCase):
    """
    Test various BounceTarget configurations against six mock clients with different teams, games, tags and slots.

    Uses the "or" operator, which is defined as: "any(team, game, tags, slot)".

    A missing condition (None) or an empty set is treated as always False.
    """

    def test_or_bounce_target_default(self):
        bounce_target = BounceTarget(None, None, None, None)

        assert list(bounce_target.match_clients_or(ALL_CLIENTS)) == []

    def test_or_bounce_team_only(self):
        bounce_target = BounceTarget({1}, None, None, None)

        assert list(bounce_target.match_clients_or(ALL_CLIENTS)) == [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3]

    def test_or_tags_condition_only(self):
        bounce_target = BounceTarget(None, None, {"DeathLink"}, None)

        self.assertEqual(
            list(bounce_target.match_clients_or(ALL_CLIENTS)),
            [TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_2, TEAM_2_SLOT_3],
        )

    def test_or_slot_condition_only(self):
        bounce_target = BounceTarget(None, None, None, {2})

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), [TEAM_1_SLOT_2, TEAM_2_SLOT_2])

    def test_or_empty_conditions(self):
        bounce_target = BounceTarget(set(), set(), set(), set())

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), [])

    def test_or_empty_conditions_except_slot(self):
        bounce_target = BounceTarget(set(), set(), set(), {3})

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), [TEAM_1_SLOT_3, TEAM_2_SLOT_3])

    def test_or_empty_conditions_except_tags_and_team(self):
        bounce_target = BounceTarget({1}, set(), {"DeathLink"}, set())

        self.assertEqual(
            list(bounce_target.match_clients_or(ALL_CLIENTS)),
            [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_2, TEAM_2_SLOT_3],
        )

    def test_or_all(self):
        bounce_target = BounceTarget({2}, {"TestGame 2"}, {"DeathLink"}, {1})

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), ALL_CLIENTS)

    def test_or_multiple_games(self):
        bounce_target = BounceTarget({1}, {"TestGame", "TestGame 2"}, None, None)

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), ALL_CLIENTS)

    def test_or_multiple_tags(self):
        bounce_target = BounceTarget({2}, None, {"DeathLink", "TrapLink"}, None)

        self.assertEqual(
            list(bounce_target.match_clients_or(ALL_CLIENTS)),
            [TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_1, TEAM_2_SLOT_2, TEAM_2_SLOT_3],
        )

    def test_or_multiple_slots(self):
        bounce_target = BounceTarget(None, None, None, {1, 2})

        self.assertEqual(
            list(bounce_target.match_clients_or(ALL_CLIENTS)),
            [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_2_SLOT_1, TEAM_2_SLOT_2],
        )

    def test_or_multiple_teams(self):
        bounce_target = BounceTarget({1, 2}, None, None, {1})

        self.assertEqual(list(bounce_target.match_clients_or(ALL_CLIENTS)), ALL_CLIENTS)


class TestBounceTargetAnd(unittest.TestCase):
    """
    Test various BounceTarget configurations against six mock clients with different teams, games, tags and slots.

    Uses the "and" operator, which is defined as: "all(team, game, tags, slot)".

    A missing condition (None) is interpreted as always True, where an empty set is treated as always False.
    This means that for an "and"-type bounce packet, a single empty set means the whole condition selects no clients.
    """

    def test_and_bounce_target_default(self):
        bounce_target = BounceTarget(None, None, None, None)

        assert list(bounce_target.match_clients_and(ALL_CLIENTS)) == ALL_CLIENTS

    def test_and_bounce_team_only(self):
        bounce_target = BounceTarget({1}, None, None, None)

        assert list(bounce_target.match_clients_and(ALL_CLIENTS)) == [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3]

    def test_and_tags_condition_only(self):
        bounce_target = BounceTarget(None, None, {"DeathLink"}, None)

        self.assertEqual(
            list(bounce_target.match_clients_and(ALL_CLIENTS)),
            [TEAM_1_SLOT_2, TEAM_1_SLOT_3, TEAM_2_SLOT_2, TEAM_2_SLOT_3],
        )

    def test_and_slot_condition_only(self):
        bounce_target = BounceTarget(None, None, None, {2})

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_1_SLOT_2, TEAM_2_SLOT_2])

    def test_and_empty_conditions(self):
        bounce_target = BounceTarget(set(), set(), set(), set())

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [])

    def test_and_empty_conditions_except_slot(self):
        bounce_target = BounceTarget(set(), set(), set(), {3})

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [])

    def test_and_empty_conditions_except_tags_and_team(self):
        bounce_target = BounceTarget({1}, None, {"DeathLink"}, None)

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_1_SLOT_2, TEAM_1_SLOT_3])

    def test_and_all(self):
        bounce_target = BounceTarget({2}, {"TestGame 2"}, {"DeathLink"}, {3})

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_2_SLOT_3])

    def test_and_multiple_games(self):
        bounce_target = BounceTarget({1}, {"TestGame", "TestGame 2"}, None, None)

        self.assertEqual(
            list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_1_SLOT_3]
        )

    def test_and_multiple_tags(self):
        bounce_target = BounceTarget({2}, None, {"DeathLink", "TrapLink"}, None)

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_2_SLOT_2, TEAM_2_SLOT_3])

    def test_and_multiple_slots(self):
        bounce_target = BounceTarget(None, None, None, {1, 2})

        self.assertEqual(
            list(bounce_target.match_clients_and(ALL_CLIENTS)),
            [TEAM_1_SLOT_1, TEAM_1_SLOT_2, TEAM_2_SLOT_1, TEAM_2_SLOT_2],
        )

    def test_and_multiple_teams(self):
        bounce_target = BounceTarget({1, 2}, None, None, {1})

        self.assertEqual(list(bounce_target.match_clients_and(ALL_CLIENTS)), [TEAM_1_SLOT_1, TEAM_2_SLOT_1])
