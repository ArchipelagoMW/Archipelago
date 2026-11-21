# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import TaylorSwiftWorld

class UTMixin:

    ut_can_gen_without_yaml = True
    passthrough: dict[str, Any]

    # for UT, not called in standard generation
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # returns slot data to be used in UT regen
        return slot_data

    def get_options_from_slot_data(self, world: TaylorSwiftWorld):

        if hasattr(world.multiworld, "re_gen_passthrough"):
            if "Taylor Swift Discography" in world.multiworld.re_gen_passthrough:
                self.passthrough = world.multiworld.re_gen_passthrough["Taylor Swift Discography"]

                for key, value in self.passthrough.items():
                    if hasattr(world.options, key):
                        opt = getattr(world.options, key)
                        opt.value = opt.from_any(value).value