# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionGroup, PerGameCommonOptions, Toggle


class IncludeDebut(DefaultOnToggle):
    """Include her Debut Album (Taylor Swift) in the shuffling."""
    display_name = "Include Debut"


class IncludeFearless(Toggle):
    """Include the album Fearless in the shuffling."""
    display_name = "Include Fearless"


class IncludeFearlessTV(Toggle):
    """Include the album Fearless (Taylor's Version) in the shuffling."""
    display_name = "Include Fearless (Taylor's Version)"


class IncludeSpeakNow(Toggle):
    """Include the album Speak Now in the shuffling."""
    display_name = "Include Speak Now"


class IncludeSpeakNowTV(Toggle):
    """Include the album Speak Now (Taylor's Version) in the shuffling."""
    display_name = "Include Speak Now (Taylor's Version)"


class IncludeRed(Toggle):
    """Include the album Red in the shuffling."""
    display_name = "Include Red"


class IncludeRedTV(Toggle):
    """Include the album Red (Taylor's Version) in the shuffling."""
    display_name = "Include Red (Taylor's Version)"


class Include1989(Toggle):
    """Include the album 1989 in the shuffling."""
    display_name = "Include 1989"


class Include1989TV(Toggle):
    """Include the album 1989 (Taylor's Version) in the shuffling."""
    display_name = "Include 1989 (Taylor's Version)"


class IncludeReputation(Toggle):
    """Include the album Reputation in the shuffling."""
    display_name = "Include Reputation"


class IncludeLover(Toggle):
    """Include the album Lover in the shuffling."""
    display_name = "Include Lover"


class IncludeFolklore(Toggle):
    """Include the album Folklore in the shuffling."""
    display_name = "Include Folklore"


class IncludeEvermore(Toggle):
    """Include the album Evermore in the shuffling."""
    display_name = "Include Evermore"


class IncludeMidnights(Toggle):
    """Include the album Midnights in the shuffling."""
    display_name = "Include Midnights"


class IncludeTTPD(Toggle):
    """Include the album The Tortured Poets Department in the shuffling."""
    display_name = "Include The Tortured Poets Department"


class IncludeTLOAS(Toggle):
    """Include the album The Life of a Showgirl in the shuffling."""
    display_name = "Include The Life of a Showgirl"


class IncludeVaultTracks(Toggle):
    """Include the (from the vault) tracks in the shuffling."""
    display_name = "Include Vault Tracks"


class IncludeReRecordings(Toggle):
    """Include the rerecorded albums (Taylor's Version) in the shuffling."""
    display_name = "Include Re-recordings"


class IncludeDeluxe(Toggle):
    """Include deluxe edition songs in the shuffling."""
    display_name = "Include Deluxe Songs"

class IncludeExtra(Toggle):
    """Include extra songs (songs that were never released on CD, or not part of the normal "deluxe" album) in the shuffling."""
    display_name = "Include Extra Songs"


@dataclass
class TaylorSwiftOptions(PerGameCommonOptions):
    include_debut: IncludeDebut
    include_fearless: IncludeFearless
    include_fearless_tv: IncludeFearlessTV
    include_speak_now: IncludeSpeakNow
    include_speak_now_tv: IncludeSpeakNowTV
    include_red: IncludeRed
    include_red_tv: IncludeRedTV
    include_1989: Include1989
    include_1989_tv: Include1989TV
    include_reputation: IncludeReputation
    include_lover: IncludeLover
    include_folklore: IncludeFolklore
    include_evermore: IncludeEvermore
    include_midnights: IncludeMidnights
    include_ttpd: IncludeTTPD
    include_tloas: IncludeTLOAS
    include_vault_tracks: IncludeVaultTracks
    include_re_recordings: IncludeReRecordings
    include_deluxe: IncludeDeluxe
    include_extra: IncludeExtra


option_groups = [
    OptionGroup("Album Options", [
        IncludeDebut,
        IncludeFearless,
        IncludeFearlessTV,
        IncludeSpeakNow,
        IncludeSpeakNowTV,
        IncludeRed,
        IncludeRedTV,
        Include1989,
        Include1989TV,
        IncludeReputation,
        IncludeLover,
        IncludeFolklore,
        IncludeEvermore,
        IncludeMidnights,
        IncludeTTPD,
        IncludeTLOAS,
    ]),
    OptionGroup("Song Options", [
        IncludeVaultTracks,
        IncludeReRecordings,
        IncludeDeluxe,
        IncludeExtra
    ]),
]
