# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .Options import option_groups

class TaylorSwiftWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Taylor Swift Discography for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["bennydreamly"]
    )]

    option_groups = option_groups