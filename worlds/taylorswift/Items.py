# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from BaseClasses import Item, ItemClassification

from typing import TypedDict

class TaylorSwiftItem(Item):
    game: str = "Taylor Swift Discography"

class ItemDict(TypedDict):
    classification: ItemClassification
    name: str

ITEM_NAME_TO_ID = {
    "Taylor Swift": 1989,
    "Fearless": 1990,
    "Speak Now": 1991,
    "Red": 1992,
    "1989 (Album)": 1993,
    "Reputation": 1994,
    "Lover": 1995,
    "Folklore": 1996,
    "Evermore": 1997,
    "Fearless (Taylor's Version)": 1998,
    "Red (Taylor's Version)": 1999,
    "Midnights": 2000,
    "Speak Now (Taylor's Version)": 2001,
    "1989 (Taylor's Version)": 2002,
    "The Tortured Poets Department": 2003,
    "The Life of a Showgirl": 2004,
    "Vault Tracks": 2005,
    "Re-recordings": 2006,
    "Easter Egg": 2007,
    "Behind the Lyrics": 2008,
    "Secret Message": 2009,
    "Studio Session": 2010,
    "Friendship Bracelet": 2011,
    "Audio Reversal": 2012
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Taylor Swift": ItemClassification.progression,
    "Fearless": ItemClassification.progression,
    "Speak Now": ItemClassification.progression,
    "Red": ItemClassification.progression,
    "1989 (Album)": ItemClassification.progression,
    "Reputation": ItemClassification.progression,
    "Lover": ItemClassification.progression,
    "Folklore": ItemClassification.progression,
    "Evermore": ItemClassification.progression,
    "Fearless (Taylor's Version)": ItemClassification.progression,
    "Red (Taylor's Version)": ItemClassification.progression,
    "Midnights": ItemClassification.progression,
    "Speak Now (Taylor's Version)": ItemClassification.progression,
    "1989 (Taylor's Version)": ItemClassification.progression,
    "The Tortured Poets Department": ItemClassification.progression,
    "The Life of a Showgirl": ItemClassification.progression,
    "Vault Tracks": ItemClassification.progression,
    "Re-recordings": ItemClassification.progression,
    "Easter Egg": ItemClassification.filler,
    "Behind the Lyrics": ItemClassification.filler,
    "Secret Message": ItemClassification.filler,
    "Studio Session": ItemClassification.filler,
    "Friendship Bracelet": ItemClassification.filler,
    "Audio Reversal": ItemClassification.trap
}

ALBUM_OPTIONS = {
    "Taylor Swift":           "include_debut",
    "Fearless":               "include_fearless",
    "Fearless (Taylor's Version)": "include_fearless_tv",
    "Speak Now":              "include_speak_now",
    "Speak Now (Taylor's Version)": "include_speak_now_tv",
    "Red":                    "include_red",
    "Red (Taylor's Version)": "include_red_tv",
    "1989 (Album)":                   "include_1989",
    "1989 (Taylor's Version)": "include_1989_tv",
    "Reputation":             "include_reputation",
    "Lover":                  "include_lover",
    "Folklore":               "include_folklore",
    "Evermore":               "include_evermore",
    "Midnights":              "include_midnights",
    "The Tortured Poets Department": "include_ttpd",
    "The Life of a Showgirl": "include_tloas",
}

ALBUM_OPTION_TO_NAME = {
    option: name for name, option in ALBUM_OPTIONS.items()
}

FILLER_NAMES = [
    "Easter Egg",
    "Behind the Lyrics",
    "Secret Message",
    "Studio Session",
    "Friendship Bracelet",
]

TRAP_NAMES = [
    "Audio Reversal"
]


def create_item_with_correct_classification(world, name: str) -> TaylorSwiftItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return TaylorSwiftItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def get_random_filler_item_name(world) -> str:
    return world.random.choice(FILLER_NAMES)


def create_all_items(world) -> None:
    itempool: list[Item] = []

    for album_name, option_name in ALBUM_OPTIONS.items():
        if getattr(world.options, option_name).value:
            itempool.append(world.create_item(album_name))

    if world.options.include_vault_tracks.value:
        itempool.append(world.create_item("Vault Tracks"))

    if world.options.include_re_recordings.value:
        itempool.append(world.create_item("Re-recordings"))

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_filler = number_of_unfilled_locations - len(itempool)
    number_of_traps = int(needed_filler * 0.1)
    needed_filler -= number_of_traps
    for i in range(number_of_traps):
        itempool.append(world.create_item(world.random.choice(TRAP_NAMES)))
    itempool += [world.create_filler() for _ in range(needed_filler)]

    world.multiworld.itempool += itempool