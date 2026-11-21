# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

from .Items import ALBUM_OPTION_TO_NAME

if TYPE_CHECKING:
    from . import TaylorSwiftWorld


ALBUM_REGIONS: dict[str, str] = {
    "Taylor Swift":                "include_debut",
    "Fearless":                    "include_fearless",
    "Fearless (Taylor's Version)": "include_fearless_tv",
    "Speak Now":                   "include_speak_now",
    "Speak Now (Taylor's Version)": "include_speak_now_tv",
    "Red":                         "include_red",
    "Red (Taylor's Version)":      "include_red_tv",
    "1989":                        "include_1989",
    "1989 (Taylor's Version)":     "include_1989_tv",
    "Reputation":                  "include_reputation",
    "Lover":                       "include_lover",
    "Folklore":                    "include_folklore",
    "Evermore":                    "include_evermore",
    "Midnights":                   "include_midnights",
    "The Tortured Poets Department": "include_ttpd",
    "The Life of a Showgirl":      "include_tloas",
}


def create_and_connect_regions(world: TaylorSwiftWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for region_name, option_name in ALBUM_REGIONS.items():
        if getattr(world.options, option_name).value:
            album_region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(album_region)
            menu.connect(album_region, rule=Has(ALBUM_OPTION_TO_NAME[option_name]))
