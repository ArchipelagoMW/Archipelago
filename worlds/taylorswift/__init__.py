# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World
from Utils import visualize_regions
from .Items import TaylorSwiftItem, ITEM_NAME_TO_ID, create_all_items, create_item_with_correct_classification, get_random_filler_item_name
from .Locations import LOCATION_NAME_TO_ID, create_all_locations
from .Regions import create_and_connect_regions
from .Rules import set_all_rules, set_completion_condition
from .Options import TaylorSwiftOptions
from .Web import TaylorSwiftWeb
from .UT import UTMixin

class TaylorSwiftWorld(World, UTMixin):
    """Taylor Swift's discography as an archipelago integration where you get checks by listening to music"""

    game = "Taylor Swift Discography"
    web = TaylorSwiftWeb()

    base_id = 1989

    options_dataclass = TaylorSwiftOptions
    options: TaylorSwiftOptions

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def generate_early(self) -> None:
        # this is specific to UT, doesn't apply in normal generation
        self.get_options_from_slot_data(self)

    def create_regions(self) -> None:
        create_and_connect_regions(self)
        create_all_locations(self)
        # visualize_regions(
        #     self.get_region("Menu"),
        #     "taylorswift.puml",
        #     show_entrance_names=True,
        #     show_entrance_rules=True,
        # )

    def set_rules(self) -> None:
        set_all_rules(self)
        set_completion_condition(self)

    def create_item(self, name: str) -> TaylorSwiftItem:
        return create_item_with_correct_classification(self, name)

    def create_items(self) -> None:
        create_all_items(self)

    def get_filler_item_name(self) -> str:
        return get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "include_debut": self.options.include_debut.value,
            "include_fearless": self.options.include_fearless.value,
            "include_fearless_tv": self.options.include_fearless_tv.value,
            "include_speak_now": self.options.include_speak_now.value,
            "include_speak_now_tv": self.options.include_speak_now_tv.value,
            "include_red": self.options.include_red.value,
            "include_red_tv": self.options.include_red_tv.value,
            "include_1989": self.options.include_1989.value,
            "include_1989_tv": self.options.include_1989_tv.value,
            "include_reputation": self.options.include_reputation.value,
            "include_lover": self.options.include_lover.value,
            "include_folklore": self.options.include_folklore.value,
            "include_evermore": self.options.include_evermore.value,
            "include_midnights": self.options.include_midnights.value,
            "include_ttpd": self.options.include_ttpd.value,
            "include_tloas": self.options.include_tloas.value,
            "include_vault_tracks": self.options.include_vault_tracks.value,
            "include_re_recordings": self.options.include_re_recordings.value,
            "include_deluxe": self.options.include_deluxe.value,
            "include_extra": self.options.include_extra.value,
        }
