"""Regression tests for KirbyAM connect_names token registration (Issue #373)."""

from __future__ import annotations

import base64
from unittest.mock import Mock

from .. import KirbyAmWorld


def test_modify_multidata_registers_auth_token_with_team_slot_tuple() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.auth = bytes(range(16))
    world.player = 1
    world.multiworld = Mock()
    world.multiworld.get_player_name.return_value = "KirbyAM Test"

    multidata = {
        "connect_names": {
            "KirbyAM Test": (0, 1),
        }
    }

    KirbyAmWorld.modify_multidata(world, multidata)

    auth_key = base64.b64encode(world.auth).decode("ascii")
    assert multidata["connect_names"][auth_key] == (0, 1)
    assert isinstance(multidata["connect_names"][auth_key], tuple)
    assert len(multidata["connect_names"][auth_key]) == 2
