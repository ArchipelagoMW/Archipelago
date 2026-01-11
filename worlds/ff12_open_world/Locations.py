from typing import Dict, NamedTuple, Optional
from BaseClasses import Location, LocationProgressType
from .Items import FF12OW_BASE_ID


class FF12OpenWorldLocation(Location):
    game: str = "Final Fantasy 12 Open World"


class FF12OpenWorldLocationData(NamedTuple):
    region: str
    type: str
    str_id: str
    address: Optional[int] = None
    classification: LocationProgressType = LocationProgressType.DEFAULT
    secondary_index: int = 0
    difficulty: int = 0

location_data_table: Dict[str, FF12OpenWorldLocationData] = {
    "Archades - Grand Arcade Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 0,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="alc_a01",
        difficulty=7
    ),
    "Old Archades - Alley of Muted Sighs Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 3,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 4,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 5,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 6,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 7,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 8,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=7,
        difficulty=1
    ),
    "Old Archades - Alley of Muted Sighs Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 9,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a01",
        secondary_index=8,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 10,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 11,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 12,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 13,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 14,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 15,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 16,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 17,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=7,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 18,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=8,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 19,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=9,
        difficulty=1
    ),
    "Old Archades - Alley of Low Whispers Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 20,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ald_a02",
        secondary_index=10,
        difficulty=1
    ),
    "Skyferry - Air Deck Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 21,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="asp_a03",
        difficulty=1
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 22,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 23,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=1,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 24,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 25,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=3,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 26,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=4,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 27,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=5,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 28,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=6,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Effulgent Light Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 29,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a01",
        secondary_index=7,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 30,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 31,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=1,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 32,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 33,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=3,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 34,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=4,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 35,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=5,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 36,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=6,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 37,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=7,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of Distant Song Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 38,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_a02",
        secondary_index=8,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 39,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 40,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=1,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 41,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 42,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=3,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 43,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=4,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 44,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=5,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 45,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=6,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 46,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=7,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 47,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=8,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 48,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=9,
        difficulty=6
    ),
    "Necrohol of Nabudis - Cloister of the Highborn Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 49,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_b01",
        secondary_index=10,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 50,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 51,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=1,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 52,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 53,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=3,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 54,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=4,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 55,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=5,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 56,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=6,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of the Ivory Covenant Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 57,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c01",
        secondary_index=7,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 58,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 59,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        secondary_index=1,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 60,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 61,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        secondary_index=3,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 62,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        secondary_index=4,
        difficulty=6
    ),
    "Necrohol of Nabudis - Hall of Slumbering Might Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 63,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_c02",
        secondary_index=5,
        difficulty=6
    ),
    "Necrohol of Nabudis - The Crucible Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 64,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_e01",
        difficulty=7
    ),
    "Necrohol of Nabudis - Cloister of Solace Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 65,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_f01",
        difficulty=7
    ),
    "Necrohol of Nabudis - Cloister of Reason Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 66,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bds_g01",
        difficulty=7
    ),
    "Nabreus Deadlands - Greencrag Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 67,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a01",
        difficulty=5
    ),
    "Nabreus Deadlands - Greencrag Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 68,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a01",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - Vale of Lingering Sorrow Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 69,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a03",
        difficulty=5
    ),
    "Nabreus Deadlands - Vale of Lingering Sorrow Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 70,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a03",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - Vale of Lingering Sorrow Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 71,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a03",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Vale of Lingering Sorrow Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 72,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a03",
        secondary_index=3,
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 73,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 74,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 75,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 76,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        secondary_index=3,
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 77,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        secondary_index=4,
        difficulty=5
    ),
    "Nabreus Deadlands - Echoes of the Past Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 78,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_a05",
        secondary_index=5,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 79,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 80,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 81,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 82,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=3,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 83,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=4,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 84,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=5,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 85,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=6,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 86,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=7,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 87,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=8,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 88,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=9,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 89,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=10,
        difficulty=5
    ),
    "Nabreus Deadlands - The Slumbermead Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 90,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b01",
        secondary_index=11,
        difficulty=5
    ),
    "Nabreus Deadlands - The Fog Mutters Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 91,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b03",
        difficulty=5
    ),
    "Nabreus Deadlands - The Fog Mutters Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 92,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b03",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - The Fog Mutters Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 93,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b03",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 94,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 95,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 96,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 97,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=3,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 98,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=4,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 99,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=5,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 100,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=6,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 101,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=7,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 102,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=8,
        difficulty=5
    ),
    "Nabreus Deadlands - Lifeless Strand Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 103,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b05",
        secondary_index=9,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 104,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 105,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=1,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 106,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 107,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=3,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 108,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=4,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 109,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=5,
        difficulty=5
    ),
    "Nabreus Deadlands - Field of the Fallen Lord Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 110,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bog_b06",
        secondary_index=6,
        difficulty=5
    ),
    "Mt. Bur-Omisace - Temple Grounds Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 111,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="bul_a03",
        difficulty=2
    ),
    "Draklor Laboratory - 6613 East Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 112,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_c03",
        difficulty=4
    ),
    "Draklor Laboratory - 6613 East Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 113,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_c03",
        secondary_index=1,
        difficulty=4
    ),
    "Draklor Laboratory - 6613 East Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 114,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_c03",
        secondary_index=2,
        difficulty=4
    ),
    "Draklor Laboratory - 7002 East Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 115,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_c15",
        difficulty=4
    ),
    "Draklor Laboratory - 7002 East Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 116,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_c15",
        secondary_index=1,
        difficulty=4
    ),
    "Draklor Laboratory - 6711 West Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 117,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_d02",
        difficulty=4
    ),
    "Draklor Laboratory - 6711 West Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 118,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_d02",
        secondary_index=1,
        difficulty=4
    ),
    "Draklor Laboratory - 6711 West Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 119,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_d02",
        secondary_index=2,
        difficulty=4
    ),
    "Draklor Laboratory - 6801 West Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 120,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_e15",
        difficulty=4
    ),
    "Draklor Laboratory - 6801 West Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 121,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_e15",
        secondary_index=1,
        difficulty=4
    ),
    "Draklor Laboratory - 6801 West Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 122,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_e15",
        secondary_index=2,
        difficulty=4
    ),
    "Draklor Laboratory - 6801 West Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 123,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dor_e15",
        secondary_index=3,
        difficulty=4
    ),
    "Dalmasca Estersand - The Stepping Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 124,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 125,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 126,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 127,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 128,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 129,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 130,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 131,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 132,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Estersand - The Stepping Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 133,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a01",
        secondary_index=9,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 134,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 135,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 136,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 137,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 138,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 139,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 140,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 141,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Estersand - Yardang Labyrinth Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 142,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a02",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 143,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 144,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 145,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 146,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 147,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 148,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 149,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 150,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 151,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 152,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=9,
        difficulty=1
    ),
    "Dalmasca Estersand - Sand-swept Naze Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 153,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a03",
        secondary_index=10,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 154,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 155,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 156,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 157,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 158,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 159,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 160,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 161,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 162,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Estersand - Banks of the Nebra Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 163,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a04",
        secondary_index=9,
        difficulty=1
    ),
    "Dalmasca Estersand - Outpost Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 164,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a07",
        difficulty=1
    ),
    "Dalmasca Estersand - Outpost Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 165,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a07",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Outpost Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 166,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a07",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Outpost Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 167,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_a07",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Estersand - The Yoma Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 168,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 169,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=1,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 170,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=2,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 171,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=3,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 172,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=4,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 173,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=5,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 174,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=6,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 175,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=7,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 176,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=8,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 177,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=9,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 178,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=10,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 179,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=11,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 180,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=12,
        difficulty=2
    ),
    "Dalmasca Estersand - The Yoma Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 181,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c01",
        secondary_index=13,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 182,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 183,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=1,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 184,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=2,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 185,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=3,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 186,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=4,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 187,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=5,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 188,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=6,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 189,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=7,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 190,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=8,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 191,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=9,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 192,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=10,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 193,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=11,
        difficulty=2
    ),
    "Dalmasca Estersand - Broken Sands Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 194,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="dst_c02",
        secondary_index=12,
        difficulty=2
    ),
    "Ogir-Yensa Sandsea - Platform 1 - East Tanks Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 195,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a01",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - East Tanks Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 196,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - East Tanks Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 197,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - East Tanks Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 198,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 199,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 200,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 201,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 202,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 203,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 204,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 205,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 206,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=7,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 207,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=8,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - Refinery Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 208,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a02",
        secondary_index=9,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 209,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 210,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 211,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 212,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 213,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 214,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 215,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 216,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=7,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 217,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=8,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - East Junction Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 218,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a03",
        secondary_index=9,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 219,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 220,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 221,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 222,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 223,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 224,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 225,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=6,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Primary Tank Complex Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 226,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a04",
        secondary_index=7,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 227,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 228,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 229,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 230,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 231,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 232,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 233,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=6,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 234,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=7,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Central Junction Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 235,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a05",
        secondary_index=8,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 236,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 237,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 238,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 239,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 240,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 1 - South Tanks Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 241,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a06",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 242,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 243,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=1,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 244,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=2,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 245,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=3,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 246,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=4,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 247,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=5,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 248,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=6,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 249,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=7,
        difficulty=1
    ),
    "Ogir-Yensa Sandsea - Platform 2 - Refinery Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 250,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ene_a07",
        secondary_index=8,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 251,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 252,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 253,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 254,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 255,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 256,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - The Urutan-Yensa Sea Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 257,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 258,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 259,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        secondary_index=1,
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 260,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        secondary_index=2,
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 261,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        secondary_index=3,
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 262,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        secondary_index=4,
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Withering Shores Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 263,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a02",
        secondary_index=5,
        difficulty=5
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 264,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 265,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 266,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 267,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 268,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 269,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 270,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 271,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=7,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Augur Hill Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 272,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a03",
        secondary_index=8,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 273,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 274,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 275,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 276,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=3,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 277,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=4,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 278,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=5,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 279,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=6,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 280,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=7,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Yellow Sands Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 281,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_a04",
        secondary_index=8,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 282,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 283,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 284,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 285,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=3,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 286,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=4,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 287,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=5,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 288,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=6,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 289,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=7,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Demesne of the Sandqueen Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 290,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b01",
        secondary_index=8,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Trail of Fading Warmth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 291,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b02",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 292,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 293,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 294,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 295,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=3,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 296,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=4,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 297,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=5,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 298,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=6,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 299,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=7,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 300,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=8,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 301,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=9,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Simoon Bluff Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 302,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="enw_b03",
        secondary_index=10,
        difficulty=1
    ),
    "Phon Coast - The Reseta Strand Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 303,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 304,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 305,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 306,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 307,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 308,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 309,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 310,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 311,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - The Reseta Strand Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 312,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a01",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 313,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 314,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 315,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 316,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 317,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 318,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 319,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 320,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 321,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - Pora-Pora Sands Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 322,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a02",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 323,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 324,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 325,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 326,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 327,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 328,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 329,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 330,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 331,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - The Mauleia Strand Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 332,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a03",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 333,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 334,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 335,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 336,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 337,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 338,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 339,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 340,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - Cape Uahuk Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 341,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a04",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 342,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 343,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 344,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 345,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 346,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 347,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 348,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - Cape Tialan Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 349,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a05",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 350,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 351,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 352,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 353,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 354,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 355,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 356,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 357,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 358,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 359,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 360,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=10,
        difficulty=2
    ),
    "Phon Coast - The Hakawea Shore Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 361,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_a07",
        secondary_index=11,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 362,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 363,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 364,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 365,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 366,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 367,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 368,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 369,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 370,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 371,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - Caima Hills Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 372,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c01",
        secondary_index=10,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 373,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 374,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 375,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 376,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 377,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 378,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 379,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 380,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 381,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 382,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=9,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 383,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=10,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 384,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=11,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 385,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=12,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 386,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=13,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 387,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=14,
        difficulty=2
    ),
    "Phon Coast - The Vaddu Strand Treasure 16": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 388,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c02",
        secondary_index=15,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 389,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 390,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=1,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 391,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=2,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 392,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=3,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 393,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=4,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 394,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=5,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 395,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=6,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 396,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=7,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 397,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=8,
        difficulty=2
    ),
    "Phon Coast - Limatra Hills Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 398,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="fon_c03",
        secondary_index=9,
        difficulty=2
    ),
    "Salikawood - The Omen-Spur Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 399,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a01",
        difficulty=2
    ),
    "Salikawood - The Omen-Spur Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 400,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a01",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 401,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 402,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 403,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=2,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 404,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=3,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 405,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=4,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 406,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=5,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 407,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=6,
        difficulty=2
    ),
    "Salikawood - Trunkwall Road Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 408,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a02",
        secondary_index=7,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 409,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 410,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 411,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=2,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 412,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=3,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 413,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=4,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 414,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=5,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 415,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=6,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 416,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=7,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 417,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=8,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 418,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=9,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 419,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=10,
        difficulty=2
    ),
    "Salikawood - Diverging Way Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 420,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a03",
        secondary_index=11,
        difficulty=2
    ),
    "Salikawood - Sun-dappled Path Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 421,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a04",
        difficulty=2
    ),
    "Salikawood - Sun-dappled Path Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 422,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a04",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Sun-dappled Path Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 423,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a04",
        secondary_index=2,
        difficulty=2
    ),
    "Salikawood - Sun-dappled Path Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 424,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a04",
        secondary_index=3,
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 425,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 426,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 427,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        secondary_index=2,
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 428,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        secondary_index=3,
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 429,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        secondary_index=4,
        difficulty=2
    ),
    "Salikawood - Garden of Decay Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 430,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_a05",
        secondary_index=5,
        difficulty=2
    ),
    "Salikawood - Quietened Trace Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 431,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b01",
        difficulty=2
    ),
    "Salikawood - Quietened Trace Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 432,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b01",
        secondary_index=1,
        difficulty=2
    ),
    "Salikawood - Quietened Trace Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 433,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b01",
        secondary_index=2,
        difficulty=2
    ),
    "Salikawood - Quietened Trace Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 434,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b01",
        secondary_index=3,
        difficulty=2
    ),
    "Salikawood - Grand Bower Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 435,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b02",
        difficulty=5
    ),
    "Salikawood - Grand Bower Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 436,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b02",
        secondary_index=1,
        difficulty=5
    ),
    "Salikawood - Grand Bower Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 437,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b02",
        secondary_index=2,
        difficulty=5
    ),
    "Salikawood - Grand Bower Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 438,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_b02",
        secondary_index=3,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 439,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 440,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=1,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 441,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=2,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 442,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=3,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 443,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=4,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 444,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=5,
        difficulty=5
    ),
    "Salikawood - Corridor of Ages Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 445,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c01",
        secondary_index=6,
        difficulty=5
    ),
    "Salikawood - Piebald Path Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 446,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c02",
        difficulty=5
    ),
    "Salikawood - Piebald Path Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 447,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c02",
        secondary_index=1,
        difficulty=5
    ),
    "Salikawood - Piebald Path Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 448,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="frs_c02",
        secondary_index=2,
        difficulty=5
    ),
    "Giruvegan - The Trimahla Water-Steps Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 449,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b01",
        difficulty=4
    ),
    "Giruvegan - The Trimahla Water-Steps Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 450,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b01",
        secondary_index=1,
        difficulty=4
    ),
    "Giruvegan - The Trimahla Water-Steps Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 451,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b01",
        secondary_index=2,
        difficulty=4
    ),
    "Giruvegan - The Trimahla Water-Steps Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 452,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b01",
        secondary_index=3,
        difficulty=4
    ),
    "Giruvegan - The Trimahla Water-Steps Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 453,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b01",
        secondary_index=4,
        difficulty=4
    ),
    "Giruvegan - The Aadha Water-Steps Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 454,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b02",
        difficulty=4
    ),
    "Giruvegan - The Aadha Water-Steps Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 455,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b02",
        secondary_index=1,
        difficulty=4
    ),
    "Giruvegan - The Aadha Water-Steps Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 456,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_b02",
        secondary_index=2,
        difficulty=4
    ),
    "Giruvegan - The Haamilkah Water-Steps Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 457,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_c01",
        difficulty=4
    ),
    "Giruvegan - Gate of Fire Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 458,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_c02",
        difficulty=4
    ),
    "Giruvegan - Gate of Fire Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 459,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_c02",
        secondary_index=1,
        difficulty=4
    ),
    "Giruvegan - Gate of Fire Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 460,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_c02",
        secondary_index=2,
        difficulty=4
    ),
    "Giruvegan - Gate of Wind Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 461,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_d01",
        difficulty=4
    ),
    "Giruvegan - Gate of Wind Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 462,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_d01",
        secondary_index=1,
        difficulty=4
    ),
    "Giruvegan - Kabonii Jilaam Pratii'vaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 463,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_e02",
        difficulty=4
    ),
    "Giruvegan - Kabnoii Jilaam Avaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 464,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_e03",
        difficulty=4
    ),
    "Giruvegan - Bhrum Pis Avaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 465,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_f03",
        difficulty=4
    ),
    "Giruvegan - Bhrum Pis Pratii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 466,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_f04",
        difficulty=4
    ),
    "Giruvegan - Trahk Pis Praa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 467,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_g02",
        difficulty=4
    ),
    "Giruvegan - Trahk Jilaam Praa'dii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 468,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_g05",
        difficulty=4
    ),
    "Giruvegan - Crystal Peak Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 469,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_h01",
        difficulty=8
    ),
    "Giruvegan - Crystal Peak Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 470,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_h01",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Dhebon Jilaam Avaapratii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 471,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_i08",
        difficulty=8
    ),
    "Giruvegan - Dhebon Jilaam Avaapratii Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 472,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_i08",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Praa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 473,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j03",
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Praa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 474,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j03",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Praa'vaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 475,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j05",
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Praa'vaa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 476,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j05",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Pratii'vaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 477,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j06",
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Pratii'vaa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 478,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j06",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Udiipratii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 479,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j08",
        difficulty=8
    ),
    "Giruvegan - Sirhru Phullam Udiipratii Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 480,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j08",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Jilaam Praa'vaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 481,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j13",
        difficulty=8
    ),
    "Giruvegan - Sirhru Jilaam Praa'vaa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 482,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j13",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Sirhru Jilaam Pratii'vaa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 483,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j14",
        difficulty=8
    ),
    "Giruvegan - Sirhru Jilaam Pratii'vaa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 484,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_j14",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Pratii'dii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 485,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k06",
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Pratii'dii Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 486,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k06",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Udiipraa Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 487,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k09",
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Udiipraa Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 488,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k09",
        secondary_index=1,
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Pratii Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 489,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k12",
        difficulty=8
    ),
    "Giruvegan - Uldobi Phullam Pratii Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 490,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gil_k12",
        secondary_index=1,
        difficulty=8
    ),
    "Jahara - The Elderknoll Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 491,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="glf_a03",
        difficulty=1
    ),
    "Jahara - The Elderknoll Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 492,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="glf_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Golmore Jungle - Paths of Chained Light Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 493,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a01",
        difficulty=2
    ),
    "Golmore Jungle - Paths of Chained Light Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 494,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a01",
        secondary_index=1,
        difficulty=2
    ),
    "Golmore Jungle - Paths of Chained Light Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 495,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a01",
        secondary_index=2,
        difficulty=2
    ),
    "Golmore Jungle - Paths of Chained Light Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 496,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a01",
        secondary_index=3,
        difficulty=2
    ),
    "Golmore Jungle - The Needlebrake Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 497,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a02",
        difficulty=2
    ),
    "Golmore Jungle - The Needlebrake Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 498,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a02",
        secondary_index=1,
        difficulty=2
    ),
    "Golmore Jungle - The Needlebrake Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 499,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a02",
        secondary_index=2,
        difficulty=2
    ),
    "Golmore Jungle - The Needlebrake Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 500,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a02",
        secondary_index=3,
        difficulty=2
    ),
    "Golmore Jungle - The Needlebrake Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 501,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a02",
        secondary_index=4,
        difficulty=2
    ),
    "Golmore Jungle - The Parting Glade Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 502,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_a04",
        difficulty=2
    ),
    "Golmore Jungle - The Rustling Chapel Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 503,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_b01",
        difficulty=2
    ),
    "Golmore Jungle - The Rustling Chapel Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 504,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_b01",
        secondary_index=1,
        difficulty=2
    ),
    "Golmore Jungle - The Rustling Chapel Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 505,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_b01",
        secondary_index=2,
        difficulty=2
    ),
    "Golmore Jungle - The Rustling Chapel Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 506,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_b01",
        secondary_index=3,
        difficulty=2
    ),
    "Golmore Jungle - Dell of the Dreamer Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 507,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_c01",
        difficulty=2
    ),
    "Golmore Jungle - The Branchway Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 508,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d01",
        difficulty=2
    ),
    "Golmore Jungle - The Branchway Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 509,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d01",
        secondary_index=1,
        difficulty=2
    ),
    "Golmore Jungle - The Branchway Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 510,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d01",
        secondary_index=2,
        difficulty=2
    ),
    "Golmore Jungle - The Greenswathe Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 511,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d02",
        difficulty=2
    ),
    "Golmore Jungle - The Greenswathe Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 512,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d02",
        secondary_index=1,
        difficulty=2
    ),
    "Golmore Jungle - The Greenswathe Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 513,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="gol_d02",
        secondary_index=2,
        difficulty=2
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 514,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 515,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 516,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 517,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=3,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 518,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=4,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 519,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=5,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 520,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=6,
        difficulty=5
    ),
    "Garamsythe Waterway - North Spur Sluiceway Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 521,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a03",
        secondary_index=7,
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 522,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 523,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 524,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 525,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        secondary_index=3,
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 526,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        secondary_index=4,
        difficulty=5
    ),
    "Garamsythe Waterway - Northern Sluiceway Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 527,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a05",
        secondary_index=5,
        difficulty=5
    ),
    "Garamsythe Waterway - East Waterway Control Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 528,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a06",
        difficulty=5
    ),
    "Garamsythe Waterway - East Waterway Control Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 529,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a06",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - East Waterway Control Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 530,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a06",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - East Waterway Control Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 531,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_a06",
        secondary_index=3,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 532,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 533,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 534,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 535,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        secondary_index=3,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 536,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        secondary_index=4,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 11 Channel (water is drained) Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 537,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e02",
        secondary_index=5,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 10 Channel (water is drained) Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 538,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e07",
        difficulty=5
    ),
    "Garamsythe Waterway - No. 10 Channel (water is drained) Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 539,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e07",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 10 Channel (water is drained) Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 540,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e07",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 10 Channel (water is drained) Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 541,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e07",
        secondary_index=3,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 10 Channel (water is drained) Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 542,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e07",
        secondary_index=4,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 3 Cloaca Spur (water is drained) Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 543,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e09",
        difficulty=5
    ),
    "Garamsythe Waterway - No. 3 Cloaca Spur (water is drained) Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 544,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e09",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 3 Cloaca Spur (water is drained) Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 545,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e09",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 4 Cloaca Spur (water is drained) Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 546,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e12",
        difficulty=5
    ),
    "Garamsythe Waterway - No. 4 Cloaca Spur (water is drained) Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 547,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e12",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - No. 4 Cloaca Spur (water is drained) Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 548,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="grm_e12",
        secondary_index=2,
        difficulty=5
    ),
    "Henne Mines - Phase 1 Dig Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 549,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 550,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=1,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 551,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=2,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 552,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=3,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 553,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=4,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 554,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=5,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 555,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=6,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 556,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=7,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 557,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=8,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 558,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=9,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 559,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=10,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 560,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=11,
        difficulty=2
    ),
    "Henne Mines - Phase 1 Dig Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 561,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a04",
        secondary_index=12,
        difficulty=2
    ),
    "Henne Mines - Crossover A Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 562,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a05",
        difficulty=2
    ),
    "Henne Mines - Crossover A Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 563,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a05",
        secondary_index=1,
        difficulty=2
    ),
    "Henne Mines - Crossover A Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 564,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a05",
        secondary_index=2,
        difficulty=2
    ),
    "Henne Mines - Crossover A Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 565,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_a05",
        secondary_index=3,
        difficulty=2
    ),
    "Henne Mines - Phase 2 Dig Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 566,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 567,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=1,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 568,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=2,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 569,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=3,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 570,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=4,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 571,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=5,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 572,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=6,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 573,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=7,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 574,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=8,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 575,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=9,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 576,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=10,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 577,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=11,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 578,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=12,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 579,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=13,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Dig Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 580,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c01",
        secondary_index=14,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 581,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 582,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=1,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 583,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=2,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 584,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=3,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 585,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=4,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 586,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=5,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 587,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=6,
        difficulty=8
    ),
    "Henne Mines - Crossover C Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 588,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c02",
        secondary_index=7,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 589,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 590,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        secondary_index=1,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 591,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        secondary_index=2,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 592,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        secondary_index=3,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 593,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        secondary_index=4,
        difficulty=8
    ),
    "Henne Mines - Phase 2 Shaft Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 594,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_c04",
        secondary_index=5,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 595,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 596,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=1,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 597,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=2,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 598,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=3,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 599,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=4,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 600,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=5,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 601,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=6,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 602,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=7,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 603,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=8,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 604,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=9,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 605,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=10,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 606,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=11,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 607,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=12,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 608,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=13,
        difficulty=8
    ),
    "Henne Mines - Special Charter Shaft Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 609,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="hne_d01",
        secondary_index=14,
        difficulty=8
    ),
    "Lhusu Mines - Shaft Entry Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 610,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        difficulty=1
    ),
    "Lhusu Mines - Shaft Entry Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 611,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Lhusu Mines - Shaft Entry Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 612,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Lhusu Mines - Shaft Entry Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 613,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Lhusu Mines - Shaft Entry Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 614,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Lhusu Mines - Shaft Entry Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 615,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Lhusu Mines - Oltam Span Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 616,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a02",
        difficulty=1
    ),
    "Lhusu Mines - Oltam Span Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 617,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Lhusu Mines - Oltam Span Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 618,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Lhusu Mines - Transitway 1 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 619,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a03",
        difficulty=1
    ),
    "Lhusu Mines - Transitway 1 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 620,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Lhusu Mines - Transitway 1 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 621,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Lhusu Mines - Shunia Twinspan Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 622,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b01",
        difficulty=1
    ),
    "Lhusu Mines - Shunia Twinspan Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 623,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b01",
        secondary_index=1,
        difficulty=1
    ),
    "Lhusu Mines - Shunia Twinspan Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 624,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b01",
        secondary_index=2,
        difficulty=1
    ),
    "Lhusu Mines - Site 3 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 625,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 626,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=1,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 627,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=2,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 628,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=3,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 629,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=4,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 630,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=5,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 631,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=6,
        difficulty=5
    ),
    "Lhusu Mines - Site 3 Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 632,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_b03",
        secondary_index=7,
        difficulty=5
    ),
    "Lhusu Mines - Site 9 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 633,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 634,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=1,
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 635,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=2,
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 636,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=3,
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 637,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=4,
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 638,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=5,
        difficulty=6
    ),
    "Lhusu Mines - Site 9 Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 639,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d01",
        secondary_index=6,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 640,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 641,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=1,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 642,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=2,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 643,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=3,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 644,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=4,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 645,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=5,
        difficulty=6
    ),
    "Lhusu Mines - Site 11 Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 646,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_d03",
        secondary_index=6,
        difficulty=6
    ),
    "Lhusu Mines - Site 7 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 647,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_e01",
        difficulty=6
    ),
    "Lhusu Mines - Lasche Span Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 648,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f01",
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 649,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 650,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=1,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 651,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=2,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 652,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=3,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 653,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=4,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 654,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=5,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 655,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=6,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 656,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=7,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 657,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=8,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 658,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=9,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 659,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=10,
        difficulty=6
    ),
    "Lhusu Mines - Site 5 Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 660,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f02",
        secondary_index=11,
        difficulty=6
    ),
    "Lhusu Mines - Site 6 South Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 661,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f03",
        difficulty=6
    ),
    "Lhusu Mines - Site 6 South Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 662,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f03",
        secondary_index=1,
        difficulty=6
    ),
    "Lhusu Mines - Site 6 South Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 663,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f03",
        secondary_index=2,
        difficulty=6
    ),
    "Lhusu Mines - Site 6 South Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 664,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f03",
        secondary_index=3,
        difficulty=6
    ),
    "Lhusu Mines - Site 6 South Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 665,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f03",
        secondary_index=4,
        difficulty=6
    ),
    "Lhusu Mines - Site 6 North Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 666,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f04",
        difficulty=6
    ),
    "Lhusu Mines - Site 6 North Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 667,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f04",
        secondary_index=1,
        difficulty=6
    ),
    "Lhusu Mines - Staging Area Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 668,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="lus_f05",
        difficulty=6
    ),
    "Feywood - Walk of Flitting Rifts Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 669,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 670,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 671,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 672,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 673,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 674,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 675,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 676,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 677,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 678,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=9,
        difficulty=3
    ),
    "Feywood - Walk of Flitting Rifts Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 679,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a01",
        secondary_index=10,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 680,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 681,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 682,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 683,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 684,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 685,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 686,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 687,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 688,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - Walk of Stolen Truths Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 689,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a02",
        secondary_index=9,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 690,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 691,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 692,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 693,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 694,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 695,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 696,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 697,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 698,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 699,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=9,
        difficulty=3
    ),
    "Feywood - Walk of Dancing Shadow Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 700,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a03",
        secondary_index=10,
        difficulty=3
    ),
    "Feywood - Antiquity's End Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 701,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_a04",
        difficulty=3
    ),
    "Feywood - Redolent Glade Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 702,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_b01",
        difficulty=3
    ),
    "Feywood - Redolent Glade Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 703,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_b01",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 704,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 705,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 706,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 707,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 708,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 709,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 710,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 711,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - White Magick's Embrace Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 712,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c01",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 713,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 714,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 715,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 716,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 717,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 718,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 719,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 720,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 721,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 722,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=9,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 723,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=10,
        difficulty=3
    ),
    "Feywood - Ice Field of Clearsight Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 724,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c02",
        secondary_index=11,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 725,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 726,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=1,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 727,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=2,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 728,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=3,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 729,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=4,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 730,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=5,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 731,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=6,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 732,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=7,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 733,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=8,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 734,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=9,
        difficulty=3
    ),
    "Feywood - The Edge of Reason Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 735,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mfr_c03",
        secondary_index=10,
        difficulty=3
    ),
    "Barheim Passage - The Lightworks Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 736,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a01",
        difficulty=3
    ),
    "Barheim Passage - The Lightworks Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 737,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a01",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - The Lightworks Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 738,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a01",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 739,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 740,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 741,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 742,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=3,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 743,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=4,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 744,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=5,
        difficulty=3
    ),
    "Barheim Passage - Great Eastern Passage Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 745,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a02",
        secondary_index=6,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 36 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 746,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a03",
        difficulty=3
    ),
    "Barheim Passage - Op Sector 36 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 747,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a03",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 36 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 748,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a03",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Special Op Sector 3 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 749,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a04",
        difficulty=3
    ),
    "Barheim Passage - Special Op Sector 3 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 750,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a04",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Special Op Sector 3 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 751,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a04",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 37 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 752,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a05",
        difficulty=3
    ),
    "Barheim Passage - Op Sector 37 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 753,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a05",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 37 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 754,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a05",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 37 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 755,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a05",
        secondary_index=3,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 37 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 756,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a05",
        secondary_index=4,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 29 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 757,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a06",
        difficulty=3
    ),
    "Barheim Passage - Op Sector 29 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 758,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a06",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Op Sector 29 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 759,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_a06",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Great Central Passage Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 760,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b01",
        difficulty=3
    ),
    "Barheim Passage - Great Central Passage Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 761,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b01",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - Great Central Passage Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 762,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b01",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Great Central Passage Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 763,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b01",
        secondary_index=3,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 764,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 765,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=1,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 766,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 767,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=3,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 768,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=4,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 769,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=5,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 770,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=6,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 771,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=7,
        difficulty=3
    ),
    "Barheim Passage - The Zeviah Subterrane Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 772,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_b02",
        secondary_index=8,
        difficulty=3
    ),
    "Barheim Passage - Terminus No. 7 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 773,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_d01",
        difficulty=5
    ),
    "Barheim Passage - Terminus No. 7 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 774,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_d01",
        secondary_index=1,
        difficulty=5
    ),
    "Barheim Passage - East-West Bypass Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 775,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e01",
        difficulty=5
    ),
    "Barheim Passage - East-West Bypass Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 776,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e01",
        secondary_index=1,
        difficulty=5
    ),
    "Barheim Passage - East-West Bypass Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 777,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e01",
        secondary_index=2,
        difficulty=5
    ),
    "Barheim Passage - East-West Bypass Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 778,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e01",
        secondary_index=3,
        difficulty=5
    ),
    "Barheim Passage - East-West Bypass Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 779,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e01",
        secondary_index=4,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 780,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 781,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=1,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 782,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=2,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 783,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=3,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 784,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=4,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 785,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=5,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 786,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=6,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 787,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=7,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 788,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=8,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 789,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=9,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 790,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=10,
        difficulty=5
    ),
    "Barheim Passage - The Zeviah Span Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 791,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e02",
        secondary_index=11,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 792,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 793,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=1,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 794,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=2,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 795,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=3,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 796,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=4,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 797,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=5,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 798,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=6,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 799,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=7,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 800,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=8,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 801,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=9,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 802,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=10,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 803,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=11,
        difficulty=5
    ),
    "Barheim Passage - West Annex Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 804,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e03",
        secondary_index=12,
        difficulty=5
    ),
    "Barheim Passage - Terminus No. 7 Adjunct Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 805,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e04",
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 806,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 807,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=1,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 808,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=2,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 809,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=3,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 810,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=4,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 811,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=5,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 812,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=6,
        difficulty=5
    ),
    "Barheim Passage - Special Op Sector 5 Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 813,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mic_e05",
        secondary_index=7,
        difficulty=5
    ),
    "Mosphoran Highwaste - Southern Skirts Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 814,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a01",
        difficulty=2
    ),
    "Mosphoran Highwaste - Southern Skirts Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 815,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a01",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Southern Skirts Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 816,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a01",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Southern Skirts Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 817,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a01",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Southern Skirts Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 818,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a01",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 819,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 820,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 821,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 822,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 823,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 824,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=5,
        difficulty=2
    ),
    "Mosphoran Highwaste - Summit Path Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 825,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_a02",
        secondary_index=6,
        difficulty=2
    ),
    "Mosphoran Highwaste - Rays of Ashen Light Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 826,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b01",
        difficulty=2
    ),
    "Mosphoran Highwaste - Rays of Ashen Light Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 827,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b01",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Rays of Ashen Light Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 828,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b01",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Rays of Ashen Light Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 829,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b01",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Rays of Ashen Light Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 830,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b01",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Empyrean Way Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 831,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b02",
        difficulty=2
    ),
    "Mosphoran Highwaste - Empyrean Way Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 832,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b02",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Empyrean Way Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 833,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b02",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Empyrean Way Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 834,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b02",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Empyrean Way Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 835,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b02",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Skyreach Ridge Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 836,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b03",
        difficulty=2
    ),
    "Mosphoran Highwaste - Skyreach Ridge Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 837,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b03",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Skyreach Ridge Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 838,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b03",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Skyreach Ridge Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 839,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b03",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Trail of Sky-flung Stone Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 840,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b04",
        difficulty=2
    ),
    "Mosphoran Highwaste - Trail of Sky-flung Stone Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 841,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b04",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Trail of Sky-flung Stone Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 842,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b04",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Trail of Sky-flung Stone Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 843,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b04",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Trail of Sky-flung Stone Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 844,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b04",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 845,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 846,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 847,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 848,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=3,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 849,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=4,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 850,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=5,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 851,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=6,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 852,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=7,
        difficulty=2
    ),
    "Mosphoran Highwaste - Northern Skirts Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 853,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b05",
        secondary_index=8,
        difficulty=2
    ),
    "Mosphoran Highwaste - Halny Crossing Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 854,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b06",
        difficulty=2
    ),
    "Mosphoran Highwaste - Halny Crossing Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 855,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_b06",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Babbling Vale Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 856,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_d01",
        difficulty=2
    ),
    "Mosphoran Highwaste - Babbling Vale Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 857,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_d01",
        secondary_index=1,
        difficulty=2
    ),
    "Mosphoran Highwaste - Babbling Vale Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 858,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_d01",
        secondary_index=2,
        difficulty=2
    ),
    "Mosphoran Highwaste - Babbling Vale Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 859,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mnt_d01",
        secondary_index=3,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Sky Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 860,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_a01",
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Sky Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 861,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_a01",
        secondary_index=1,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Sky Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 862,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_a01",
        secondary_index=2,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Mind Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 863,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_a02",
        difficulty=2
    ),
    "Stilshrine of Miriam - Cold Distance Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 864,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b02",
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Prescience Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 865,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b03",
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 866,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 867,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=1,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 868,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=2,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 869,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=3,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 870,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=4,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 871,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=5,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 872,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=6,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 873,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=7,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 874,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=8,
        difficulty=2
    ),
    "Stilshrine of Miriam - Walk of Reason Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 875,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_b04",
        secondary_index=9,
        difficulty=2
    ),
    "Stilshrine of Miriam - Ward of Steel Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 876,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_c01",
        difficulty=2
    ),
    "Stilshrine of Miriam - Ward of Velitation Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 877,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_d01",
        difficulty=2
    ),
    "Stilshrine of Miriam - Ward of Velitation Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 878,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_d01",
        secondary_index=1,
        difficulty=2
    ),
    "Stilshrine of Miriam - Ward of Velitation Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 879,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_d01",
        secondary_index=2,
        difficulty=2
    ),
    "Stilshrine of Miriam - Hall of Worth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 880,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_e01",
        difficulty=2
    ),
    "Stilshrine of Miriam - Hall of Worth Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 881,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="mrm_e01",
        secondary_index=1,
        difficulty=2
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 882,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 883,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 884,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 885,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 886,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 887,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 888,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 889,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=7,
        difficulty=1
    ),
    "Ozmone Plain - Field of Fallen Wings Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 890,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a01",
        secondary_index=8,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 891,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 892,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 893,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 894,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 895,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 896,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 897,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Ozmone Plain - The Switcback Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 898,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a02",
        secondary_index=7,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 899,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 900,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 901,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 902,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 903,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 904,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 905,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 906,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=7,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 907,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=8,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 908,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=9,
        difficulty=1
    ),
    "Ozmone Plain - Haulo Green Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 909,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_a03",
        secondary_index=10,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 910,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 911,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 912,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 913,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=3,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 914,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=4,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 915,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=5,
        difficulty=1
    ),
    "Ozmone Plain - Dagan Flats Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 916,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b01",
        secondary_index=6,
        difficulty=1
    ),
    "Ozmone Plain - Field of Light Winds Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 917,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b02",
        difficulty=1
    ),
    "Ozmone Plain - Field of Light Winds Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 918,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b02",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - The Greensnake Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 919,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b03",
        difficulty=1
    ),
    "Ozmone Plain - The Greensnake Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 920,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b03",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - The Greensnake Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 921,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_b03",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 922,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 923,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=1,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 924,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=2,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 925,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=3,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 926,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=4,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 927,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=5,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 928,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=6,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 929,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=7,
        difficulty=1
    ),
    "Ozmone Plain - The Shred Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 930,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ozm_c01",
        secondary_index=8,
        difficulty=1
    ),
    "Paramina Rift - Head of the Silverflow Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 931,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 932,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 933,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 934,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 935,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 936,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=5,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 937,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=6,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 938,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=7,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 939,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=8,
        difficulty=2
    ),
    "Paramina Rift - Head of the Silverflow Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 940,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a02",
        secondary_index=9,
        difficulty=2
    ),
    "Paramina Rift - Freezing Gorge Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 941,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a03",
        difficulty=2
    ),
    "Paramina Rift - Freezing Gorge Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 942,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a03",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Freezing Gorge Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 943,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a03",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Freezing Gorge Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 944,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a03",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Freezing Gorge Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 945,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_a03",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 946,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 947,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 948,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 949,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 950,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 951,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=5,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 952,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=6,
        difficulty=2
    ),
    "Paramina Rift - Frozen Brook Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 953,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b01",
        secondary_index=7,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 954,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 955,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 956,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 957,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 958,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 959,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=5,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 960,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=6,
        difficulty=2
    ),
    "Paramina Rift - Icebound Flow Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 961,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b02",
        secondary_index=7,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 962,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 963,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 964,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 965,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 966,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 967,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=5,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 968,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=6,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 969,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=7,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 970,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=8,
        difficulty=2
    ),
    "Paramina Rift - Karydine Glacier Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 971,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_b03",
        secondary_index=9,
        difficulty=2
    ),
    "Paramina Rift - Path of the Firstfall Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 972,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c01",
        difficulty=2
    ),
    "Paramina Rift - Spine of the Icewyrm Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 973,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c02",
        difficulty=2
    ),
    "Paramina Rift - Spine of the Icewyrm Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 974,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c02",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Spine of the Icewyrm Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 975,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c02",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 976,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 977,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=1,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 978,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=2,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 979,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=3,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 980,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=4,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 981,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=5,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 982,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=6,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 983,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=7,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 984,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=8,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 985,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=9,
        difficulty=2
    ),
    "Paramina Rift - Silverflow's End Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 986,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pbc_c03",
        secondary_index=10,
        difficulty=2
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 987,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 988,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 989,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 990,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 991,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 992,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 993,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 994,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 995,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 996,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Uazcuff Hills Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 997,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a01",
        secondary_index=10,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 998,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 999,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1000,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1001,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1002,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1003,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1004,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1005,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1006,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1007,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1008,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=10,
        difficulty=3
    ),
    "Tchita Uplands - Sundered Earth Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1009,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a02",
        secondary_index=11,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1010,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1011,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1012,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1013,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1014,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1015,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1016,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1017,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1018,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - The Highlands Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1019,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a03",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1020,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1021,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1022,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1023,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1024,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1025,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1026,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1027,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Fields of Eternity Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1028,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_a04",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1029,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1030,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1031,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1032,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1033,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1034,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1035,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1036,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1037,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - The Skytrail Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1038,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b01",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1039,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1040,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1041,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1042,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1043,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1044,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1045,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1046,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1047,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - Realm of the Elder Dream Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1048,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b02",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1049,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1050,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1051,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1052,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1053,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1054,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1055,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1056,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1057,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - The Lost Way Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1058,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b03",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1059,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1060,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1061,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1062,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1063,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1064,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1065,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Garden of Life's Circle Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1066,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b04",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1067,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1068,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1069,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1070,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=3,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1071,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=4,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1072,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=5,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1073,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=6,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1074,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=7,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1075,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=8,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1076,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=9,
        difficulty=3
    ),
    "Tchita Uplands - Oliphzak Rise Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1077,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="pla_b05",
        secondary_index=10,
        difficulty=3
    ),
    "Pharos of Ridorana - The Wellspring Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1078,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_a01",
        difficulty=5
    ),
    "Pharos of Ridorana - The Wellspring Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1079,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_a01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1080,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1081,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1082,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1083,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1084,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1085,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Labyrinth Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1086,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_b01",
        secondary_index=6,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1087,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1088,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1089,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1090,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1091,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1092,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 1st Flight Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1093,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d01",
        secondary_index=6,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 2nd Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1094,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d02",
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 2nd Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1095,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d02",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 2nd Flight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1096,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d02",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 2nd Flight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1097,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_d02",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1098,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1099,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1100,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1101,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1102,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 3rd Flight Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1103,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 4th Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1104,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e02",
        difficulty=5
    ),
    "Pharos of Ridorana - Wellspring Ravel - 4th Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1105,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_e02",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Horizon's Cusp Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1106,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_f02",
        difficulty=5
    ),
    "Pharos of Ridorana - Horizon's Cusp Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1107,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_f02",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Horizon's Cusp Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1108,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_f02",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Horizon's Cusp Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1109,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_f02",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana Subterra - Penumbra - North Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1110,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g02",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - North Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1111,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g02",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - North Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1112,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g02",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - North Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1113,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g02",
        secondary_index=3,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - North Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1114,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g02",
        secondary_index=4,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - South Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1115,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g03",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - South Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1116,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g03",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Penumbra - South Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1117,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_g03",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - North Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1118,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h02",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - North Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1119,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h02",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - North Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1120,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h02",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - North Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1121,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h02",
        secondary_index=3,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1122,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1123,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1124,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1125,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        secondary_index=3,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1126,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        secondary_index=4,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Umbra - South Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1127,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_h03",
        secondary_index=5,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1128,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1129,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1130,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1131,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=3,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1132,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=4,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1133,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=5,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1134,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=6,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1135,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=7,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - North Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1136,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i02",
        secondary_index=8,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1137,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1138,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1139,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1140,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=3,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1141,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=4,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1142,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=5,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1143,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=6,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1144,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=7,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Abyssal - South Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1145,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_i03",
        secondary_index=8,
        difficulty=7
    ),
    "Pharos of Ridorana - The Bounds of Truth Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1146,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_j02",
        difficulty=5
    ),
    "Pharos of Ridorana - The Bounds of Truth Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1147,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_j02",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - The Bounds of Truth Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1148,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_j02",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - The Bounds of Truth Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1149,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_j02",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1150,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1151,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1152,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1153,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1154,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1155,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1156,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=6,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1157,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=7,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Banishment Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1158,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_k01",
        secondary_index=8,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1159,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1160,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1161,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1162,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1163,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1164,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Suffering Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1165,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_l01",
        secondary_index=6,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1166,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1167,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1168,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1169,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1170,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1171,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1172,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=6,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1173,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=7,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1174,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=8,
        difficulty=5
    ),
    "Pharos of Ridorana - Station of Ascension Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1175,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_m01",
        secondary_index=9,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 1st Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1176,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n01",
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 1st Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1177,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 1st Flight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1178,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 1st Flight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1179,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n01",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 1st Flight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1180,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n01",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1181,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1182,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1183,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1184,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        secondary_index=3,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1185,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        secondary_index=4,
        difficulty=5
    ),
    "Pharos of Ridorana - Spire Ravel - 2nd Flight Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1186,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_n02",
        secondary_index=5,
        difficulty=5
    ),
    "Pharos of Ridorana - Empyrean Ravel Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1187,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_q01",
        difficulty=5
    ),
    "Pharos of Ridorana - Empyrean Ravel Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1188,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_q01",
        secondary_index=1,
        difficulty=5
    ),
    "Pharos of Ridorana - Empyrean Ravel Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1189,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_q01",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Empyrean Ravel Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1190,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rbl_q01",
        secondary_index=3,
        difficulty=5
    ),
    "Dreadnought Leviathan - Port Section Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1191,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b01",
        difficulty=1
    ),
    "Dreadnought Leviathan - Port Section Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1192,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b01",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Port Section Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1193,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b01",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Port Section Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1194,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b01",
        secondary_index=3,
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1195,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1196,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1197,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1198,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        secondary_index=3,
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1199,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        secondary_index=4,
        difficulty=1
    ),
    "Dreadnought Leviathan - Large Freight Stores Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1200,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b02",
        secondary_index=5,
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1201,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1202,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1203,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1204,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        secondary_index=3,
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1205,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        secondary_index=4,
        difficulty=1
    ),
    "Dreadnought Leviathan - Starboard Section Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1206,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b03",
        secondary_index=5,
        difficulty=1
    ),
    "Dreadnought Leviathan - Sub-control Room Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1207,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b04",
        difficulty=1
    ),
    "Dreadnought Leviathan - Sub-control Room Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1208,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b04",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Sub-control Room Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1209,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b04",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Sub-control Room Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1210,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rsn_b04",
        secondary_index=3,
        difficulty=1
    ),
    "Sochen Cave Palace - Falls of Time Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1211,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1212,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1213,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1214,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1215,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=4,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1216,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=5,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1217,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=6,
        difficulty=3
    ),
    "Sochen Cave Palace - Falls of Time Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1218,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a01",
        secondary_index=7,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1219,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1220,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1221,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1222,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1223,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=4,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1224,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=5,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1225,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=6,
        difficulty=3
    ),
    "Sochen Cave Palace - Mirror of the Soul Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1226,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a02",
        secondary_index=7,
        difficulty=3
    ),
    "Sochen Cave Palace - The Acolyte's Burden Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1227,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a03",
        difficulty=3
    ),
    "Sochen Cave Palace - The Acolyte's Burden Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1228,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a03",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1229,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1230,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1231,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1232,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1233,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=4,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1234,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=5,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1235,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=6,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1236,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=7,
        difficulty=3
    ),
    "Sochen Cave Palace - Doubt Abandoned Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1237,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_a04",
        secondary_index=8,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1238,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1239,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1240,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1241,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1242,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=4,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1243,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=5,
        difficulty=3
    ),
    "Sochen Cave Palace - Destiny's March Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1244,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b01",
        secondary_index=6,
        difficulty=3
    ),
    "Sochen Cave Palace - Temptation Eluded Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1245,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b02",
        difficulty=3
    ),
    "Sochen Cave Palace - Temptation Eluded Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1246,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b02",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Temptation Eluded Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1247,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b02",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Temptation Eluded Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1248,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_b02",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Shadowlight Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1249,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_c01",
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Shadowlight Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1250,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_c01",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Shadowlight Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1251,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_c01",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Shadowlight Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1252,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_c01",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Shadowlight Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1253,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_c01",
        secondary_index=4,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Lambent Darkness Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1254,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_d01",
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Lambent Darkness Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1255,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_d01",
        secondary_index=1,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Lambent Darkness Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1256,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_d01",
        secondary_index=2,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of Lambent Darkness Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1257,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_d01",
        secondary_index=3,
        difficulty=3
    ),
    "Sochen Cave Palace - Hall of the Wroth God Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1258,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_e01",
        difficulty=8
    ),
    "Sochen Cave Palace - Hall of the Wroth God Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1259,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_e01",
        secondary_index=1,
        difficulty=8
    ),
    "Sochen Cave Palace - Hall of the Wroth God Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1260,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_e01",
        secondary_index=2,
        difficulty=8
    ),
    "Sochen Cave Palace - Hall of the Wroth God Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1261,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rui_e01",
        secondary_index=3,
        difficulty=8
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1262,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1263,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=1,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1264,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=2,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1265,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=3,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1266,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=4,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1267,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=5,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1268,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=6,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1269,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=7,
        difficulty=4
    ),
    "Ridorana Cataract - Echoes from Time's Garden Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1270,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_a03",
        secondary_index=8,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1271,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1272,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=1,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1273,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=2,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1274,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=3,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1275,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=4,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1276,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=5,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1277,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=6,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1278,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=7,
        difficulty=4
    ),
    "Ridorana Cataract - City of Other Days Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1279,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b01",
        secondary_index=8,
        difficulty=4
    ),
    "Ridorana Cataract - Path of Hidden Blessing Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1280,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_b02",
        difficulty=4
    ),
    "Pharos of Ridorana - They Who Thirst Not Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1281,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_c01",
        difficulty=4
    ),
    "Pharos of Ridorana - They Who Thirst Not Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1282,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_c01",
        secondary_index=1,
        difficulty=4
    ),
    "Pharos of Ridorana - They Who Thirst Not Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1283,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_c01",
        secondary_index=2,
        difficulty=4
    ),
    "Pharos of Ridorana - They Who Thirst Not Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1284,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_c01",
        secondary_index=3,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1285,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1286,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=1,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1287,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=2,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1288,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=3,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1289,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=4,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1290,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=5,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1291,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=6,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1292,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=7,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1293,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=8,
        difficulty=4
    ),
    "Ridorana Cataract - Colosseum Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1294,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwf_d01",
        secondary_index=9,
        difficulty=4
    ),
    "Tomb of Raithwall - Royal Passage Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1295,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c01",
        difficulty=1
    ),
    "Tomb of Raithwall - Royal Passage Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1296,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c01",
        secondary_index=1,
        difficulty=1
    ),
    "Tomb of Raithwall - Royal Passage Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1297,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c01",
        secondary_index=2,
        difficulty=1
    ),
    "Tomb of Raithwall - Royal Passage Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1298,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c01",
        secondary_index=3,
        difficulty=1
    ),
    "Tomb of Raithwall - Royal Passage Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1299,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c01",
        secondary_index=4,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1300,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1301,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=1,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1302,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=2,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1303,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=3,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1304,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=4,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1305,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=5,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1306,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=6,
        difficulty=1
    ),
    "Tomb of Raithwall - Southfall Passage Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1307,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c02",
        secondary_index=7,
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1308,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1309,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        secondary_index=1,
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1310,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        secondary_index=2,
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1311,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        secondary_index=3,
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1312,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        secondary_index=4,
        difficulty=1
    ),
    "Tomb of Raithwall - Northfall Passage Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1313,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_c03",
        secondary_index=5,
        difficulty=1
    ),
    "Tomb of Raithwall - Cloister of Flame Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1314,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_d01",
        difficulty=1
    ),
    "Tomb of Raithwall - Cloister of Flame Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1315,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_d01",
        secondary_index=1,
        difficulty=1
    ),
    "Tomb of Raithwall - Cloister of Flame Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1316,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_d01",
        secondary_index=2,
        difficulty=1
    ),
    "Tomb of Raithwall - Cloister of Flame Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1317,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="rwg_d01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1318,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1319,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1320,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1321,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1322,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1323,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Dry - Throne Road Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1324,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1325,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1326,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1327,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1328,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1329,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1330,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Dry - Warrior's Wash Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1331,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1332,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1333,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1334,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1335,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1336,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1337,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas North Bank Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1338,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1339,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1340,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1341,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1342,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1343,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1344,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Dry - Toam Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1345,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_a04",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1346,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1347,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1348,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1349,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1350,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1351,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1352,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1353,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=7,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1354,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=8,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1355,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=9,
        difficulty=1
    ),
    "Giza Plains Dry - Starfall Field Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1356,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c01",
        secondary_index=10,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1357,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1358,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1359,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1360,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1361,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Dry - Gizas South Bank Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1362,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_c03",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Throne Road Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1363,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d01",
        difficulty=1
    ),
    "Giza Plains Rains - Throne Road Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1364,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d01",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Throne Road Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1365,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d01",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Throne Road Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1366,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1367,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1368,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1369,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1370,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1371,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Warrior's Wash Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1372,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d02",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas North Bank Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1373,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d03",
        difficulty=1
    ),
    "Giza Plains Rains - Gizas North Bank Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1374,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d03",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas North Bank Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1375,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d03",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas North Bank Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1376,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d03",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas North Bank Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1377,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d03",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1378,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1379,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1380,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1381,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1382,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Toam Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1383,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_d04",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Nomad Village Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1384,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_e01",
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1385,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1386,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1387,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1388,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1389,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1390,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Starfall Field Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1391,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f01",
        secondary_index=6,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1392,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1393,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1394,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1395,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1396,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Gizas South Bank Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1397,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_f03",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1398,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1399,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1400,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=2,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1401,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=3,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1402,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=4,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1403,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=5,
        difficulty=1
    ),
    "Giza Plains Rains - Tracks of the Beast Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1404,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="sav_g01",
        secondary_index=6,
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1405,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1406,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1407,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1408,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1409,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Lowtown - North Sprawl Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1410,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Lowtown - South Sprawl Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1411,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a02",
        difficulty=1
    ),
    "Lowtown - South Sprawl Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1412,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Lowtown - South Sprawl Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1413,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Lowtown - South Sprawl Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1414,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Lowtown - South Sprawl Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1415,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="slm_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1416,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1417,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1418,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1419,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1420,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1421,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1422,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1423,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1424,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1425,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1426,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1427,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1428,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1429,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=13,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1430,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=14,
        difficulty=5
    ),
    "Cerobi Steppe - Old Elanise Road Treasure 16": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1431,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a01",
        secondary_index=15,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1432,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1433,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1434,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1435,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1436,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1437,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1438,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1439,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1440,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1441,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1442,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1443,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1444,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - Crossfield Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1445,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a02",
        secondary_index=13,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1446,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1447,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1448,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1449,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1450,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1451,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1452,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1453,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1454,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1455,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1456,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1457,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1458,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - The Terraced Bank Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1459,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_a03",
        secondary_index=13,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1460,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1461,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1462,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1463,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1464,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1465,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1466,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1467,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1468,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1469,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1470,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1471,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - North Liavell Hills Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1472,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b01",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1473,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1474,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1475,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1476,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1477,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1478,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1479,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1480,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1481,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1482,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1483,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1484,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1485,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1486,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=13,
        difficulty=5
    ),
    "Cerobi Steppe - South Liavell Hills Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1487,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b02",
        secondary_index=14,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1488,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1489,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1490,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1491,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1492,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1493,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1494,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1495,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1496,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1497,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1498,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1499,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1500,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1501,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=13,
        difficulty=5
    ),
    "Cerobi Steppe - Feddik River Treasure 15": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1502,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b03",
        secondary_index=14,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1503,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1504,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1505,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1506,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=3,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1507,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=4,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1508,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=5,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1509,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=6,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1510,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=7,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1511,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=8,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1512,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=9,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1513,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=10,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 12": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1514,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=11,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 13": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1515,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=12,
        difficulty=5
    ),
    "Cerobi Steppe - The Northsward Treasure 14": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1516,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="srb_b04",
        secondary_index=13,
        difficulty=5
    ),
    "Balfonheim - Sea Breeze Lane Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1517,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a01",
        difficulty=1
    ),
    "Balfonheim - Sea Breeze Lane Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1518,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Balfonheim - Sea Breeze Lane Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1519,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Balfonheim - Port Villa West Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1520,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a13",
        difficulty=1
    ),
    "Balfonheim - The Whitecap Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1521,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a14",
        difficulty=1
    ),
    "Balfonheim - Port Villa East Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1522,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="var_a15",
        difficulty=1
    ),
    "Eruyt Village - Fane of the Path Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1523,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="vic_a01",
        difficulty=1
    ),
    "Eruyt Village - The Spiritwood Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1524,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="vic_a02",
        difficulty=1
    ),
    "Eruyt Village - The Spiritwood Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1525,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="vic_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1526,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1527,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1528,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1529,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1530,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1531,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1532,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Westersand - Galtea Downs Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1533,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a01",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1534,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1535,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1536,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1537,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1538,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1539,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1540,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1541,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Westersand - Corridor of Sand Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1542,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a02",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1543,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1544,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1545,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1546,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1547,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1548,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1549,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1550,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1551,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 10": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1552,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=9,
        difficulty=1
    ),
    "Dalmasca Westersand - Shimmering Horizons Treasure 11": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1553,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a03",
        secondary_index=10,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1554,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1555,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1556,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1557,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1558,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1559,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1560,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1561,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Westersand - The Midfault Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1562,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a04",
        secondary_index=8,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1563,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1564,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1565,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1566,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=3,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1567,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=4,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1568,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=5,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1569,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=6,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1570,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=7,
        difficulty=1
    ),
    "Dalmasca Westersand - Windtrace Dunes Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1571,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="wdl_a05",
        secondary_index=8,
        difficulty=1
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1572,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1573,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1574,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1575,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1576,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1577,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=5,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1578,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=6,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 8": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1579,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=7,
        difficulty=5
    ),
    "Zertinan Caverns - Invitation to Heresy Treasure 9": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1580,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a01",
        secondary_index=8,
        difficulty=5
    ),
    "Zertinan Caverns - Sandfalls Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1581,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a02",
        difficulty=5
    ),
    "Zertinan Caverns - Sandfalls Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1582,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a02",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Sandfalls Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1583,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a02",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Sandfalls Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1584,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a02",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - Sandfalls Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1585,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a02",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - Hourglass Basin Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1586,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a03",
        difficulty=5
    ),
    "Zertinan Caverns - Hourglass Basin Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1587,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a03",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Hourglass Basin Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1588,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a03",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Hourglass Basin Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1589,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_a03",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - The Undershore Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1590,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b01",
        difficulty=5
    ),
    "Zertinan Caverns - The Undershore Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1591,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b01",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - The Undershore Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1592,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b01",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - The Undershore Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1593,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b01",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - The Undershore Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1594,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b01",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1595,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1596,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1597,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1598,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1599,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - Halls of Ardent Darkness Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1600,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_b02",
        secondary_index=5,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1601,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1602,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1603,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1604,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1605,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1606,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=5,
        difficulty=5
    ),
    "Zertinan Caverns - The Balamka Fault Treasure 7": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1607,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c01",
        secondary_index=6,
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1608,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1609,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1610,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 4": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1611,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        secondary_index=3,
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 5": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1612,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        secondary_index=4,
        difficulty=5
    ),
    "Zertinan Caverns - Drybeam Cavern Treasure 6": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1613,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c02",
        secondary_index=5,
        difficulty=5
    ),
    "Zertinan Caverns - Darkened Wharf Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1614,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c03",
        difficulty=5
    ),
    "Zertinan Caverns - Darkened Wharf Treasure 2": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1615,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c03",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Darkened Wharf Treasure 3": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1616,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c03",
        secondary_index=2,
        difficulty=5
    ),
    "Zertinan Caverns - Canopy of Clay Treasure 1": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1617,
        classification=LocationProgressType.DEFAULT,
        type="treasure",
        str_id="ztc_c04",
        difficulty=5
    ),
    "Rabanastre - Tomaj 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1618,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9000"
    ),
    "Rabanastre - Tomaj 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1619,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9000",
        secondary_index=1
    ),
    "Rabanastre - Tomaj 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1620,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9000",
        secondary_index=2
    ),
    "Rabanastre - Tomaj 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1621,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916B"
    ),
    "Rabanastre - Tomaj 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1622,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916B",
        secondary_index=1
    ),
    "Rabanastre - Tomaj 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1623,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916B",
        secondary_index=2
    ),
    "Rabanastre - Tomaj 3 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1624,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916C"
    ),
    "Rabanastre - Tomaj 3 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1625,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916C",
        secondary_index=1
    ),
    "Rabanastre - Tomaj 3 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1626,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916C",
        secondary_index=2
    ),
    "Giza Plains Dry - Masyua Shadestone Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1627,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9002"
    ),
    "Giza Plains Dry - Masyua Shadestone Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1628,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9002",
        secondary_index=1
    ),
    "Giza Plains Dry - Masyua Shadestone Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1629,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9002",
        secondary_index=2
    ),
    "Giza Plains Dry - Giza Sunstone Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1630,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9001",
        difficulty=1
    ),
    "Giza Plains Dry - Giza Sunstone Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1631,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9001",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Giza Sunstone Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1632,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9001",
        secondary_index=2,
        difficulty=1
    ),
    "Lowtown - Dalan Crescent Stone Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1633,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905E"
    ),
    "Lowtown - Dalan Crescent Stone Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1634,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905E",
        secondary_index=1
    ),
    "Lowtown - Dalan Crescent Stone Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1635,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905E",
        secondary_index=2
    ),
    "Lowtown - Dalan Sword of the Order Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1636,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905F"
    ),
    "Lowtown - Dalan Sword of the Order Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1637,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905F",
        secondary_index=1
    ),
    "Lowtown - Dalan Sword of the Order Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1638,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905F",
        secondary_index=2
    ),
    "Lowtown - Balzac Sword of the Order Turn In Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1639,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911E"
    ),
    "Lowtown - Balzac Sword of the Order Turn In Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1640,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911E",
        secondary_index=1
    ),
    "Lowtown - Balzac Sword of the Order Turn In Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1641,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911E",
        secondary_index=2
    ),
    "Dreadnought Leviathan - No. 1 Brig Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1642,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9060",
        difficulty=1
    ),
    "Dreadnought Leviathan - No. 1 Brig Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1643,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9060",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - No. 1 Brig Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1644,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9060",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Systems Access Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1645,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9061",
        difficulty=1
    ),
    "Dreadnought Leviathan - Systems Access Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1646,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9061",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Systems Access Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1647,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9061",
        secondary_index=2,
        difficulty=1
    ),
    "Dreadnought Leviathan - Manufacted Nethicite Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1648,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912C",
        difficulty=1
    ),
    "Dreadnought Leviathan - Manufacted Nethicite Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1649,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912C",
        secondary_index=1,
        difficulty=1
    ),
    "Dreadnought Leviathan - Manufacted Nethicite Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1650,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912C",
        secondary_index=2,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Eksir Berries Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1651,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912D",
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Eksir Berries Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1652,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912D",
        secondary_index=1,
        difficulty=1
    ),
    "Nam-Yensa Sandsea - Eksir Berries Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1653,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912D",
        secondary_index=2,
        difficulty=1
    ),
    "Tomb of Raithwall - Defeat Belias Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1654,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9190",
        difficulty=2
    ),
    "Tomb of Raithwall - Defeat Belias Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1655,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9190",
        secondary_index=1,
        difficulty=2
    ),
    "Tomb of Raithwall - Defeat Belias Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1656,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9190",
        secondary_index=2,
        difficulty=2
    ),
    "Tomb of Raithwall - Dawn Shard Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1657,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912E",
        difficulty=2
    ),
    "Tomb of Raithwall - Dawn Shard Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1658,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912E",
        secondary_index=1,
        difficulty=2
    ),
    "Tomb of Raithwall - Dawn Shard Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1659,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912E",
        secondary_index=2,
        difficulty=2
    ),
    "Tomb of Raithwall - Defeat Vossler Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1660,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918E",
        difficulty=2
    ),
    "Tomb of Raithwall - Defeat Vossler Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1661,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918E",
        secondary_index=1,
        difficulty=2
    ),
    "Tomb of Raithwall - Defeat Vossler Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1662,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918E",
        secondary_index=2,
        difficulty=2
    ),
    "Royal Palace - Goddess's Magicite Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1663,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912F",
        difficulty=1
    ),
    "Royal Palace - Goddess's Magicite Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1664,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912F",
        secondary_index=1,
        difficulty=1
    ),
    "Royal Palace - Goddess's Magicite Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1665,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="912F",
        secondary_index=2,
        difficulty=1
    ),
    "Barheim Passage - Burrough Tube Fuse Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1666,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9130",
        difficulty=1
    ),
    "Barheim Passage - Burrough Tube Fuse Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1667,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9130",
        secondary_index=1,
        difficulty=1
    ),
    "Barheim Passage - Burrough Tube Fuse Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1668,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9130",
        secondary_index=2,
        difficulty=1
    ),
    "Jahara - Great-chief Elder After Defeating Vossler Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1669,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911F",
        difficulty=2
    ),
    "Jahara - Great-chief Elder After Defeating Vossler Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1670,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911F",
        secondary_index=1,
        difficulty=2
    ),
    "Jahara - Great-chief Elder After Defeating Vossler Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1671,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="911F",
        secondary_index=2,
        difficulty=2
    ),
    "Eruyt Village - Lente's Tear Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1672,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9131",
        difficulty=2
    ),
    "Eruyt Village - Lente's Tear Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1673,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9131",
        secondary_index=1,
        difficulty=2
    ),
    "Eruyt Village - Lente's Tear Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1674,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9131",
        secondary_index=2,
        difficulty=2
    ),
    "Stilshrine of Miriam - Defeat Mateus Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1675,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9191",
        difficulty=2
    ),
    "Stilshrine of Miriam - Defeat Mateus Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1676,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9191",
        secondary_index=1,
        difficulty=2
    ),
    "Stilshrine of Miriam - Defeat Mateus Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1677,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9191",
        secondary_index=2,
        difficulty=2
    ),
    "Stilshrine of Miriam - Sword of Kings Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1678,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9132",
        difficulty=2
    ),
    "Stilshrine of Miriam - Sword of Kings Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1679,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9132",
        secondary_index=1,
        difficulty=2
    ),
    "Stilshrine of Miriam - Sword of Kings Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1680,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9132",
        secondary_index=2,
        difficulty=2
    ),
    "Tchita Uplands - Soul Ward Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1681,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9133",
        difficulty=3
    ),
    "Tchita Uplands - Soul Ward Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1682,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9133",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Soul Ward Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1683,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9133",
        secondary_index=2,
        difficulty=3
    ),
    "Tchita Uplands - Mandragora Reward Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1684,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9052",
        difficulty=3
    ),
    "Tchita Uplands - Mandragora Reward Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1685,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9052",
        secondary_index=1,
        difficulty=3
    ),
    "Tchita Uplands - Mandragora Reward Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1686,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9052",
        secondary_index=2,
        difficulty=3
    ),
    "Draklor Laboratory - Defeat Cid 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1687,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918D",
        difficulty=5
    ),
    "Draklor Laboratory - Defeat Cid 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1688,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918D",
        secondary_index=1,
        difficulty=5
    ),
    "Draklor Laboratory - Defeat Cid 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1689,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918D",
        secondary_index=2,
        difficulty=5
    ),
    "Archades - Pinewood Chop 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1690,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9134"
    ),
    "Archades - Pinewood Chop 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1691,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9134",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1692,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9134",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1693,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9135"
    ),
    "Archades - Pinewood Chop 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1694,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9135",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1695,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9135",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 3 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1696,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9136"
    ),
    "Archades - Pinewood Chop 3 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1697,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9136",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 3 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1698,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9136",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 4 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1699,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9137"
    ),
    "Archades - Pinewood Chop 4 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1700,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9137",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 4 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1701,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9137",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 5 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1702,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9138"
    ),
    "Archades - Pinewood Chop 5 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1703,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9138",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 5 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1704,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9138",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 6 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1705,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9139"
    ),
    "Archades - Pinewood Chop 6 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1706,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9139",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 6 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1707,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9139",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 7 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1708,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913A"
    ),
    "Archades - Pinewood Chop 7 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1709,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913A",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 7 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1710,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913A",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 8 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1711,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913B"
    ),
    "Archades - Pinewood Chop 8 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1712,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913B",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 8 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1713,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913B",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 9 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1714,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913C"
    ),
    "Archades - Pinewood Chop 9 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1715,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913C",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 9 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1716,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913C",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 10 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1717,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913D"
    ),
    "Archades - Pinewood Chop 10 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1718,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913D",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 10 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1719,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913D",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 11 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1720,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913E"
    ),
    "Archades - Pinewood Chop 11 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1721,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913E",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 11 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1722,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913E",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 12 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1723,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913F"
    ),
    "Archades - Pinewood Chop 12 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1724,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913F",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 12 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1725,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="913F",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 13 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1726,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9140"
    ),
    "Archades - Pinewood Chop 13 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1727,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9140",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 13 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1728,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9140",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 14 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1729,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9141"
    ),
    "Archades - Pinewood Chop 14 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1730,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9141",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 14 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1731,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9141",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 15 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1732,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9142"
    ),
    "Archades - Pinewood Chop 15 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1733,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9142",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 15 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1734,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9142",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 16 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1735,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9143"
    ),
    "Archades - Pinewood Chop 16 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1736,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9143",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 16 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1737,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9143",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 17 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1738,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9144"
    ),
    "Archades - Pinewood Chop 17 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1739,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9144",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 17 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1740,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9144",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 18 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1741,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9145"
    ),
    "Archades - Pinewood Chop 18 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1742,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9145",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 18 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1743,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9145",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 19 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1744,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9146"
    ),
    "Archades - Pinewood Chop 19 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1745,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9146",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 19 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1746,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9146",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 20 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1747,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9147"
    ),
    "Archades - Pinewood Chop 20 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1748,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9147",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 20 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1749,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9147",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 21 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1750,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9148"
    ),
    "Archades - Pinewood Chop 21 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1751,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9148",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 21 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1752,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9148",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 22 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1753,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9149"
    ),
    "Archades - Pinewood Chop 22 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1754,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9149",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 22 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1755,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9149",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 23 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1756,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914A"
    ),
    "Archades - Pinewood Chop 23 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1757,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914A",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 23 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1758,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914A",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 24 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1759,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914B"
    ),
    "Archades - Pinewood Chop 24 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1760,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914B",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 24 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1761,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914B",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 25 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1762,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914C"
    ),
    "Archades - Pinewood Chop 25 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1763,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914C",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 25 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1764,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914C",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 26 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1765,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914D"
    ),
    "Archades - Pinewood Chop 26 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1766,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914D",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 26 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1767,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914D",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 27 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1768,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914E"
    ),
    "Archades - Pinewood Chop 27 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1769,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914E",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 27 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1770,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914E",
        secondary_index=2
    ),
    "Archades - Pinewood Chop 28 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1771,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914F"
    ),
    "Archades - Pinewood Chop 28 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1772,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914F",
        secondary_index=1
    ),
    "Archades - Pinewood Chop 28 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1773,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="914F",
        secondary_index=2
    ),
    "Archades - Sandalwood Chop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1774,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9150",
        difficulty=2
    ),
    "Archades - Sandalwood Chop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1775,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9150",
        secondary_index=1,
        difficulty=2
    ),
    "Archades - Sandalwood Chop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1776,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9150",
        secondary_index=2,
        difficulty=2
    ),
    "Draklor Laboratory - Lab Access Card Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1777,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9151"
    ),
    "Draklor Laboratory - Lab Access Card Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1778,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9151",
        secondary_index=1
    ),
    "Draklor Laboratory - Lab Access Card Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1779,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9151",
        secondary_index=2
    ),
    "Giruvegan - Defeat Shemhazai Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1780,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9192",
        difficulty=5
    ),
    "Giruvegan - Defeat Shemhazai Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1781,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9192",
        secondary_index=1,
        difficulty=5
    ),
    "Giruvegan - Defeat Shemhazai Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1782,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9192",
        secondary_index=2,
        difficulty=5
    ),
    "Giruvegan - Treaty-Blade Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1783,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9152",
        difficulty=5
    ),
    "Giruvegan - Treaty-Blade Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1784,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9152",
        secondary_index=1,
        difficulty=5
    ),
    "Giruvegan - Treaty-Blade Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1785,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9152",
        secondary_index=2,
        difficulty=5
    ),
    "Pharos of Ridorana - Black Orb 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1786,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9153",
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1787,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9153",
        secondary_index=1,
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1788,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9153",
        secondary_index=2,
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1789,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9154",
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1790,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9154",
        secondary_index=1,
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1791,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9154",
        secondary_index=2,
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 3 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1792,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9155",
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 3 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1793,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9155",
        secondary_index=1,
        difficulty=6
    ),
    "Pharos of Ridorana - Black Orb 3 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1794,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9155",
        secondary_index=2,
        difficulty=6
    ),
    "Pharos of Ridorana - Defeat Hashmal Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1795,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9193",
        difficulty=6
    ),
    "Pharos of Ridorana - Defeat Hashmal Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1796,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9193",
        secondary_index=1,
        difficulty=6
    ),
    "Pharos of Ridorana - Defeat Hashmal Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1797,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9193",
        secondary_index=2,
        difficulty=6
    ),
    "Pharos of Ridorana - Defeat Famfrit and Cid 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1798,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918F",
        difficulty=7
    ),
    "Pharos of Ridorana - Defeat Famfrit and Cid 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1799,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918F",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana - Defeat Famfrit and Cid 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1800,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918F",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 4 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1801,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9156",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 4 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1802,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9156",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 4 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1803,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9156",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 5 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1804,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9157",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 5 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1805,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9157",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 5 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1806,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9157",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 6 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1807,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9158",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 6 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1808,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9158",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 6 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1809,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9158",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 7 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1810,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9159",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 7 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1811,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9159",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 7 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1812,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9159",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 8 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1813,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915A",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 8 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1814,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915A",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 8 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1815,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915A",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 9 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1816,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915B",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 9 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1817,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915B",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 9 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1818,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915B",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 10 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1819,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915C",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 10 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1820,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915C",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 10 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1821,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915C",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 11 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1822,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915D",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 11 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1823,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915D",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 11 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1824,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915D",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 12 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1825,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915E",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 12 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1826,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915E",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 12 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1827,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915E",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 13 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1828,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915F",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 13 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1829,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915F",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 13 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1830,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="915F",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 14 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1831,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9160",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 14 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1832,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9160",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 14 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1833,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9160",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 15 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1834,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9161",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 15 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1835,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9161",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 15 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1836,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9161",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 16 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1837,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9162",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 16 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1838,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9162",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 16 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1839,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9162",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 17 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1840,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9163",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 17 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1841,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9163",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 17 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1842,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9163",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 18 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1843,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9164",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 18 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1844,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9164",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 18 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1845,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9164",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 19 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1846,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9165",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 19 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1847,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9165",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 19 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1848,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9165",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 20 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1849,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9166",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 20 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1850,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9166",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 20 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1851,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9166",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 21 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1852,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9167",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 21 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1853,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9167",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 21 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1854,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9167",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 22 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1855,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9168",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 22 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1856,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9168",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 22 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1857,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9168",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 23 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1858,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9169",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 23 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1859,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9169",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 23 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1860,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9169",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 24 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1861,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916A",
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 24 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1862,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916A",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana Subterra - Black Orb 24 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1863,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916A",
        secondary_index=2,
        difficulty=7
    ),
    "Rabanastre - Hunt 1: Rogue Tomato Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1864,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9003",
        difficulty=1
    ),
    "Rabanastre - Hunt 1: Rogue Tomato Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1865,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9003",
        secondary_index=1,
        difficulty=1
    ),
    "Rabanastre - Hunt 1: Rogue Tomato Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1866,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9003",
        secondary_index=2,
        difficulty=1
    ),
    "Rabanastre - Hunt 2: Thextera Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1867,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9004",
        difficulty=1
    ),
    "Rabanastre - Hunt 2: Thextera Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1868,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9004",
        secondary_index=1,
        difficulty=1
    ),
    "Rabanastre - Hunt 2: Thextera Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1869,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9004",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Hunt 3: Flowering Cactoid Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1870,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9005",
        difficulty=1
    ),
    "Dalmasca Estersand - Hunt 3: Flowering Cactoid Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1871,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9005",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Hunt 3: Flowering Cactoid Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1872,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9005",
        secondary_index=2,
        difficulty=1
    ),
    "Lowtown - Hunt 4: Wraith Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1873,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9006",
        difficulty=1
    ),
    "Lowtown - Hunt 4: Wraith Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1874,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9006",
        secondary_index=1,
        difficulty=1
    ),
    "Lowtown - Hunt 4: Wraith Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1875,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9006",
        secondary_index=2,
        difficulty=1
    ),
    "Bhujerba - Hunt 5: Nidhogg Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1876,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9007",
        difficulty=1
    ),
    "Bhujerba - Hunt 5: Nidhogg Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1877,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9007",
        secondary_index=1,
        difficulty=1
    ),
    "Bhujerba - Hunt 5: Nidhogg Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1878,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9007",
        secondary_index=2,
        difficulty=1
    ),
    "Rabanastre - Hunt 6: White Mousse Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1879,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9008",
        difficulty=5
    ),
    "Rabanastre - Hunt 6: White Mousse Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1880,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9008",
        secondary_index=1,
        difficulty=5
    ),
    "Rabanastre - Hunt 6: White Mousse Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1881,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9008",
        secondary_index=2,
        difficulty=5
    ),
    "Lowtown - Hunt 7: Ring Wyrm Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1882,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9009",
        difficulty=3
    ),
    "Lowtown - Hunt 7: Ring Wyrm Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1883,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9009",
        secondary_index=1,
        difficulty=3
    ),
    "Lowtown - Hunt 7: Ring Wyrm Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1884,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9009",
        secondary_index=2,
        difficulty=3
    ),
    "Rabanastre - Hunt 8: Wyvern Lord Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1885,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900A",
        difficulty=2
    ),
    "Rabanastre - Hunt 8: Wyvern Lord Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1886,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900A",
        secondary_index=1,
        difficulty=2
    ),
    "Rabanastre - Hunt 8: Wyvern Lord Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1887,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900A",
        secondary_index=2,
        difficulty=2
    ),
    "Rabanastre - Hunt 9: Marilith Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1888,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900B",
        difficulty=5
    ),
    "Rabanastre - Hunt 9: Marilith Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1889,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900B",
        secondary_index=1,
        difficulty=5
    ),
    "Rabanastre - Hunt 9: Marilith Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1890,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900B",
        secondary_index=2,
        difficulty=5
    ),
    "Jahara - Hunt 10: Enkelados Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1891,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900C",
        difficulty=2
    ),
    "Jahara - Hunt 10: Enkelados Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1892,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900C",
        secondary_index=1,
        difficulty=2
    ),
    "Jahara - Hunt 10: Enkelados Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1893,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900C",
        secondary_index=2,
        difficulty=2
    ),
    "Giza Plains Rains - Hunt 11: Croakadile Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1894,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900D",
        difficulty=2
    ),
    "Giza Plains Rains - Hunt 11: Croakadile Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1895,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900D",
        secondary_index=1,
        difficulty=2
    ),
    "Giza Plains Rains - Hunt 11: Croakadile Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1896,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900D",
        secondary_index=2,
        difficulty=2
    ),
    "Jahara - Hunt 12: Ixtab Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1897,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900E",
        difficulty=2
    ),
    "Jahara - Hunt 12: Ixtab Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1898,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900E",
        secondary_index=1,
        difficulty=2
    ),
    "Jahara - Hunt 12: Ixtab Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1899,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900E",
        secondary_index=2,
        difficulty=2
    ),
    "Mt. Bur-Omisace - Hunt 13: Feral Retriever Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1900,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900F",
        difficulty=3
    ),
    "Mt. Bur-Omisace - Hunt 13: Feral Retriever Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1901,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900F",
        secondary_index=1,
        difficulty=3
    ),
    "Mt. Bur-Omisace - Hunt 13: Feral Retriever Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1902,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="900F",
        secondary_index=2,
        difficulty=3
    ),
    "Eruyt Village - Hunt 14: Vorpal Bunny Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1903,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9010",
        difficulty=3
    ),
    "Eruyt Village - Hunt 14: Vorpal Bunny Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1904,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9010",
        secondary_index=1,
        difficulty=3
    ),
    "Eruyt Village - Hunt 14: Vorpal Bunny Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1905,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9010",
        secondary_index=2,
        difficulty=3
    ),
    "Jahara - Hunt 15: Mindflayer Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1906,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9011",
        difficulty=4
    ),
    "Jahara - Hunt 15: Mindflayer Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1907,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9011",
        secondary_index=1,
        difficulty=4
    ),
    "Jahara - Hunt 15: Mindflayer Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1908,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9011",
        secondary_index=2,
        difficulty=4
    ),
    "Dalmasca Estersand - Hunt 16: Bloodwing Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1909,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9012",
        difficulty=5
    ),
    "Dalmasca Estersand - Hunt 16: Bloodwing Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1910,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9012",
        secondary_index=1,
        difficulty=5
    ),
    "Dalmasca Estersand - Hunt 16: Bloodwing Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1911,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9012",
        secondary_index=2,
        difficulty=5
    ),
    "Nalbina Fortress - Hunt 17: Atomos Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1912,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9013",
        difficulty=3
    ),
    "Nalbina Fortress - Hunt 17: Atomos Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1913,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9013",
        secondary_index=1,
        difficulty=3
    ),
    "Nalbina Fortress - Hunt 17: Atomos Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1914,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9013",
        secondary_index=2,
        difficulty=3
    ),
    "Nalbina Fortress - Hunt 18: Roblon Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1915,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9014",
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 18: Roblon Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1916,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9014",
        secondary_index=1,
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 18: Roblon Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1917,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9014",
        secondary_index=2,
        difficulty=6
    ),
    "Mosphoran Highwaste - Hunt 19: Braegh Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1918,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9015",
        difficulty=4
    ),
    "Mosphoran Highwaste - Hunt 19: Braegh Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1919,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9015",
        secondary_index=1,
        difficulty=4
    ),
    "Mosphoran Highwaste - Hunt 19: Braegh Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1920,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9015",
        secondary_index=2,
        difficulty=4
    ),
    "Archades - Hunt 20: Darksteel Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1921,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9016",
        difficulty=4
    ),
    "Archades - Hunt 20: Darksteel Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1922,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9016",
        secondary_index=1,
        difficulty=4
    ),
    "Archades - Hunt 20: Darksteel Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1923,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9016",
        secondary_index=2,
        difficulty=4
    ),
    "Balfonheim - Hunt 21: Vyraal Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1924,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9017",
        difficulty=5
    ),
    "Balfonheim - Hunt 21: Vyraal Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1925,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9017",
        secondary_index=1,
        difficulty=5
    ),
    "Balfonheim - Hunt 21: Vyraal Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1926,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9017",
        secondary_index=2,
        difficulty=5
    ),
    "Old Archades - Hunt 22: Lindwyrm Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1927,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9018",
        difficulty=5
    ),
    "Old Archades - Hunt 22: Lindwyrm Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1928,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9018",
        secondary_index=1,
        difficulty=5
    ),
    "Old Archades - Hunt 22: Lindwyrm Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1929,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9018",
        secondary_index=2,
        difficulty=5
    ),
    "Archades - Hunt 23: Overlord Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1930,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9019",
        difficulty=6
    ),
    "Archades - Hunt 23: Overlord Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1931,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9019",
        secondary_index=1,
        difficulty=6
    ),
    "Archades - Hunt 23: Overlord Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1932,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9019",
        secondary_index=2,
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 24: Goliath Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1933,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901A",
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 24: Goliath Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1934,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901A",
        secondary_index=1,
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 24: Goliath Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1935,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901A",
        secondary_index=2,
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 25: Deathscythe Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1936,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901B",
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 25: Deathscythe Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1937,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901B",
        secondary_index=1,
        difficulty=6
    ),
    "Nalbina Fortress - Hunt 25: Deathscythe Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1938,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901B",
        secondary_index=2,
        difficulty=6
    ),
    "Skyferry - Hunt 26: Deathgaze Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1939,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901C",
        difficulty=7
    ),
    "Skyferry - Hunt 26: Deathgaze Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1940,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901C",
        secondary_index=1,
        difficulty=7
    ),
    "Skyferry - Hunt 26: Deathgaze Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1941,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901C",
        secondary_index=2,
        difficulty=7
    ),
    "Bhujerba - Hunt 27: Diabolos Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1942,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901D",
        difficulty=7
    ),
    "Bhujerba - Hunt 27: Diabolos Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1943,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901D",
        secondary_index=1,
        difficulty=7
    ),
    "Bhujerba - Hunt 27: Diabolos Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1944,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901D",
        secondary_index=2,
        difficulty=7
    ),
    "Mt. Bur-Omisace - Hunt 28: Piscodaemon Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1945,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901E",
        difficulty=5
    ),
    "Mt. Bur-Omisace - Hunt 28: Piscodaemon Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1946,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901E",
        secondary_index=1,
        difficulty=5
    ),
    "Mt. Bur-Omisace - Hunt 28: Piscodaemon Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1947,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901E",
        secondary_index=2,
        difficulty=5
    ),
    "Eruyt Village - Hunt 29: Wild Malboro Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1948,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901F",
        difficulty=6
    ),
    "Eruyt Village - Hunt 29: Wild Malboro Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1949,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901F",
        secondary_index=1,
        difficulty=6
    ),
    "Eruyt Village - Hunt 29: Wild Malboro Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1950,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="901F",
        secondary_index=2,
        difficulty=6
    ),
    "Jahara - Hunt 30: Catoblepas Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1951,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9020",
        difficulty=6
    ),
    "Jahara - Hunt 30: Catoblepas Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1952,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9020",
        secondary_index=1,
        difficulty=6
    ),
    "Jahara - Hunt 30: Catoblepas Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1953,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9020",
        secondary_index=2,
        difficulty=6
    ),
    "Mt. Bur-Omisace - Hunt 31: Fafnir Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1954,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9021",
        difficulty=7
    ),
    "Mt. Bur-Omisace - Hunt 31: Fafnir Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1955,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9021",
        secondary_index=1,
        difficulty=7
    ),
    "Mt. Bur-Omisace - Hunt 31: Fafnir Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1956,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9021",
        secondary_index=2,
        difficulty=7
    ),
    "Balfonheim - Hunt 32: Pylraster Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1957,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9022",
        difficulty=7
    ),
    "Balfonheim - Hunt 32: Pylraster Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1958,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9022",
        secondary_index=1,
        difficulty=7
    ),
    "Balfonheim - Hunt 32: Pylraster Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1959,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9022",
        secondary_index=2,
        difficulty=7
    ),
    "Giza Plains Dry - Hunt 33: Cluckatrice Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1960,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9023",
        difficulty=1
    ),
    "Giza Plains Dry - Hunt 33: Cluckatrice Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1961,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9023",
        secondary_index=1,
        difficulty=1
    ),
    "Giza Plains Dry - Hunt 33: Cluckatrice Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1962,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9023",
        secondary_index=2,
        difficulty=1
    ),
    "Bhujerba - Hunt 34: Rocktoise Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1963,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9024",
        difficulty=1
    ),
    "Bhujerba - Hunt 34: Rocktoise Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1964,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9024",
        secondary_index=1,
        difficulty=1
    ),
    "Bhujerba - Hunt 34: Rocktoise Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1965,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9024",
        secondary_index=2,
        difficulty=1
    ),
    "Lowtown - Hunt 35: Orthros Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1966,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9025",
        difficulty=5
    ),
    "Lowtown - Hunt 35: Orthros Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1967,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9025",
        secondary_index=1,
        difficulty=5
    ),
    "Lowtown - Hunt 35: Orthros Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1968,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9025",
        secondary_index=2,
        difficulty=5
    ),
    "Giza Plains Dry - Hunt 36: Gil Snapper Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1969,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9026",
        difficulty=3
    ),
    "Giza Plains Dry - Hunt 36: Gil Snapper Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1970,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9026",
        secondary_index=1,
        difficulty=3
    ),
    "Giza Plains Dry - Hunt 36: Gil Snapper Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1971,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9026",
        secondary_index=2,
        difficulty=3
    ),
    "Mt. Bur-Omisace - Hunt 37: Trickster Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1972,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9027",
        difficulty=5
    ),
    "Mt. Bur-Omisace - Hunt 37: Trickster Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1973,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9027",
        secondary_index=1,
        difficulty=5
    ),
    "Mt. Bur-Omisace - Hunt 37: Trickster Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1974,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9027",
        secondary_index=2,
        difficulty=5
    ),
    "Bhujerba - Hunt 38: Antlion Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1975,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9028",
        difficulty=5
    ),
    "Bhujerba - Hunt 38: Antlion Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1976,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9028",
        secondary_index=1,
        difficulty=5
    ),
    "Bhujerba - Hunt 38: Antlion Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1977,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9028",
        secondary_index=2,
        difficulty=5
    ),
    "Aerodrome - Hunt 39: Carrot Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1978,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9029",
        difficulty=7
    ),
    "Aerodrome - Hunt 39: Carrot Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1979,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9029",
        secondary_index=1,
        difficulty=7
    ),
    "Aerodrome - Hunt 39: Carrot Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1980,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9029",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Hunt 40: Gilgamesh Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1981,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902A",
        difficulty=7
    ),
    "Clan Hall - Hunt 40: Gilgamesh Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1982,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902A",
        secondary_index=1,
        difficulty=7
    ),
    "Clan Hall - Hunt 40: Gilgamesh Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1983,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902A",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Hunt 41: Belito Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1984,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9122",
        difficulty=5
    ),
    "Clan Hall - Hunt 41: Belito Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1985,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9122",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Hunt 41: Belito Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1986,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9122",
        secondary_index=2,
        difficulty=5
    ),
    "Lowtown - Hunt 42: Behemoth King Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1987,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902B",
        difficulty=7
    ),
    "Lowtown - Hunt 42: Behemoth King Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1988,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902B",
        secondary_index=1,
        difficulty=7
    ),
    "Lowtown - Hunt 42: Behemoth King Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1989,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902B",
        secondary_index=2,
        difficulty=7
    ),
    "Balfonheim - Hunt 43: Ixion Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1990,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902C",
        difficulty=6
    ),
    "Balfonheim - Hunt 43: Ixion Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1991,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902C",
        secondary_index=1,
        difficulty=6
    ),
    "Balfonheim - Hunt 43: Ixion Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1992,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902C",
        secondary_index=2,
        difficulty=6
    ),
    "Clan Hall - Hunt 44: Shadowseer Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1993,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902D",
        difficulty=6
    ),
    "Clan Hall - Hunt 44: Shadowseer Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1994,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902D",
        secondary_index=1,
        difficulty=6
    ),
    "Clan Hall - Hunt 44: Shadowseer Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1995,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902D",
        secondary_index=2,
        difficulty=6
    ),
    "Clan Hall - Hunt 45: Yiazmat Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1996,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902E",
        difficulty=8
    ),
    "Clan Hall - Hunt 45: Yiazmat Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1997,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902E",
        secondary_index=1,
        difficulty=8
    ),
    "Clan Hall - Hunt 45: Yiazmat Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1998,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902E",
        secondary_index=2,
        difficulty=8
    ),
    "Clan Hall - Clan Rank: Moppet Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 1999,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902F",
        difficulty=1
    ),
    "Clan Hall - Clan Rank: Moppet Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2000,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902F",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Rank: Moppet Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2001,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="902F",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Rank: Hedge Knight Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2002,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9030",
        difficulty=2
    ),
    "Clan Hall - Clan Rank: Hedge Knight Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2003,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9030",
        secondary_index=1,
        difficulty=2
    ),
    "Clan Hall - Clan Rank: Hedge Knight Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2004,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9030",
        secondary_index=2,
        difficulty=2
    ),
    "Clan Hall - Clan Rank: Rear Guard Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2005,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9031",
        difficulty=3
    ),
    "Clan Hall - Clan Rank: Rear Guard Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2006,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9031",
        secondary_index=1,
        difficulty=3
    ),
    "Clan Hall - Clan Rank: Rear Guard Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2007,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9031",
        secondary_index=2,
        difficulty=3
    ),
    "Clan Hall - Clan Rank: Vanguard Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2008,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9032",
        difficulty=4
    ),
    "Clan Hall - Clan Rank: Vanguard Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2009,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9032",
        secondary_index=1,
        difficulty=4
    ),
    "Clan Hall - Clan Rank: Vanguard Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2010,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9032",
        secondary_index=2,
        difficulty=4
    ),
    "Clan Hall - Clan Rank: Headhunter Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2011,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9033",
        difficulty=5
    ),
    "Clan Hall - Clan Rank: Headhunter Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2012,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9033",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Rank: Headhunter Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2013,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9033",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Rank: Ward of Justice Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2014,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9034",
        difficulty=6
    ),
    "Clan Hall - Clan Rank: Ward of Justice Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2015,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9034",
        secondary_index=1,
        difficulty=6
    ),
    "Clan Hall - Clan Rank: Ward of Justice Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2016,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9034",
        secondary_index=2,
        difficulty=6
    ),
    "Clan Hall - Clan Rank: Brave Companion Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2017,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9035",
        difficulty=7
    ),
    "Clan Hall - Clan Rank: Brave Companion Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2018,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9035",
        secondary_index=1,
        difficulty=7
    ),
    "Clan Hall - Clan Rank: Brave Companion Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2019,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9035",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Clan Rank: Riskbreaker Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2020,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9036",
        difficulty=8
    ),
    "Clan Hall - Clan Rank: Riskbreaker Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2021,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9036",
        secondary_index=1,
        difficulty=8
    ),
    "Clan Hall - Clan Rank: Riskbreaker Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2022,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9036",
        secondary_index=2,
        difficulty=8
    ),
    "Clan Hall - Clan Rank: Paragon of Justice Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2023,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9037",
        difficulty=9
    ),
    "Clan Hall - Clan Rank: Paragon of Justice Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2024,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9037",
        secondary_index=1,
        difficulty=9
    ),
    "Clan Hall - Clan Rank: Paragon of Justice Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2025,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9037",
        secondary_index=2,
        difficulty=9
    ),
    "Clan Hall - Clan Rank: High Guardian Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2026,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9038",
        difficulty=10
    ),
    "Clan Hall - Clan Rank: High Guardian Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2027,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9038",
        secondary_index=1,
        difficulty=10
    ),
    "Clan Hall - Clan Rank: High Guardian Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2028,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9038",
        secondary_index=2,
        difficulty=10
    ),
    "Clan Hall - Clan Rank: Knight of the Round Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2029,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9039",
        difficulty=11
    ),
    "Clan Hall - Clan Rank: Knight of the Round Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2030,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9039",
        secondary_index=1,
        difficulty=11
    ),
    "Clan Hall - Clan Rank: Knight of the Round Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2031,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9039",
        secondary_index=2,
        difficulty=11
    ),
    "Clan Hall - Clan Rank: Order of Ambrosia Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2032,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="903A",
        difficulty=12
    ),
    "Clan Hall - Clan Rank: Order of Ambrosia Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2033,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="903A",
        secondary_index=1,
        difficulty=12
    ),
    "Clan Hall - Clan Rank: Order of Ambrosia Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2034,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="903A",
        secondary_index=2,
        difficulty=12
    ),
    "Clan Hall - Clan Boss: Flans Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2035,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903B",
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Flans Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2036,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903B",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Flans Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2037,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903B",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Firemane Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2038,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903C",
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Firemane Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2039,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903C",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Firemane Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2040,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903C",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Earth Tyrant Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2041,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903D",
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Earth Tyrant Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2042,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903D",
        secondary_index=1,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Earth Tyrant Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2043,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903D",
        secondary_index=2,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Mimic Queen Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2044,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903E",
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Mimic Queen Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2045,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903E",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Mimic Queen Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2046,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903E",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Demon Wall 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2047,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903F",
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Demon Wall 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2048,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903F",
        secondary_index=1,
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Demon Wall 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2049,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="903F",
        secondary_index=2,
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Demon Wall 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2050,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9040",
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Demon Wall 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2051,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9040",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Demon Wall 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2052,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9040",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Boss: Elder Wyrm Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2053,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9041",
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Elder Wyrm Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2054,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9041",
        secondary_index=1,
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Elder Wyrm Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2055,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9041",
        secondary_index=2,
        difficulty=3
    ),
    "Clan Hall - Clan Boss: Tiamat Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2056,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9042",
        difficulty=2
    ),
    "Clan Hall - Clan Boss: Tiamat Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2057,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9042",
        secondary_index=1,
        difficulty=2
    ),
    "Clan Hall - Clan Boss: Tiamat Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2058,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9042",
        secondary_index=2,
        difficulty=2
    ),
    "Clan Hall - Clan Boss: Vinuskar Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2059,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9043",
        difficulty=2
    ),
    "Clan Hall - Clan Boss: Vinuskar Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2060,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9043",
        secondary_index=1,
        difficulty=2
    ),
    "Clan Hall - Clan Boss: Vinuskar Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2061,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9043",
        secondary_index=2,
        difficulty=2
    ),
    "Clan Hall - Clan Boss: King Bomb Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2062,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9044",
        difficulty=5
    ),
    "Clan Hall - Clan Boss: King Bomb Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2063,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9044",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: King Bomb Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2064,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9044",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Mandragora Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2065,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9045",
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Mandragora Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2066,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9045",
        secondary_index=1,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Mandragora Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2067,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9045",
        secondary_index=2,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Ahriman Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2068,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9046",
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Ahriman Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2069,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9046",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Ahriman Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2070,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9046",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Hell Wyrm Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2071,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9047",
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Hell Wyrm Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2072,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9047",
        secondary_index=1,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Hell Wyrm Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2073,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9047",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Rafflesia Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2074,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9048",
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Rafflesia Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2075,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9048",
        secondary_index=1,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Rafflesia Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2076,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9048",
        secondary_index=2,
        difficulty=4
    ),
    "Clan Hall - Clan Boss: Daedulus Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2077,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9049",
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Daedulus Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2078,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9049",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Daedulus Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2079,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9049",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Tyrant Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2080,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904A",
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Tyrant Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2081,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904A",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Tyrant Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2082,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904A",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Hydro Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2083,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904B",
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Hydro Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2084,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904B",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Hydro Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2085,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904B",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Boss: Humbaba Mistant Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2086,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904C",
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Humbaba Mistant Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2087,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904C",
        secondary_index=1,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Humbaba Mistant Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2088,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904C",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Fury Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2089,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904D",
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Fury Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2090,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904D",
        secondary_index=1,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Fury Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2091,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904D",
        secondary_index=2,
        difficulty=7
    ),
    "Clan Hall - Clan Boss: Omega Mark XII Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2092,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905A",
        difficulty=8
    ),
    "Clan Hall - Clan Boss: Omega Mark XII Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2093,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905A",
        secondary_index=1,
        difficulty=8
    ),
    "Clan Hall - Clan Boss: Omega Mark XII Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2094,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="905A",
        secondary_index=2,
        difficulty=8
    ),
    "Clan Hall - Clan Esper: Control 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2095,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904E",
        difficulty=1
    ),
    "Clan Hall - Clan Esper: Control 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2096,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904E",
        secondary_index=1,
        difficulty=1
    ),
    "Clan Hall - Clan Esper: Control 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2097,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904E",
        secondary_index=2,
        difficulty=1
    ),
    "Clan Hall - Clan Esper: Control 4 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2098,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904F",
        difficulty=3
    ),
    "Clan Hall - Clan Esper: Control 4 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2099,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904F",
        secondary_index=1,
        difficulty=3
    ),
    "Clan Hall - Clan Esper: Control 4 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2100,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="904F",
        secondary_index=2,
        difficulty=3
    ),
    "Clan Hall - Clan Esper: Control 8 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2101,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9050",
        difficulty=5
    ),
    "Clan Hall - Clan Esper: Control 8 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2102,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9050",
        secondary_index=1,
        difficulty=5
    ),
    "Clan Hall - Clan Esper: Control 8 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2103,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9050",
        secondary_index=2,
        difficulty=5
    ),
    "Clan Hall - Clan Esper: Control 13 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2104,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9051",
        difficulty=8
    ),
    "Clan Hall - Clan Esper: Control 13 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2105,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9051",
        secondary_index=1,
        difficulty=8
    ),
    "Clan Hall - Clan Esper: Control 13 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2106,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9051",
        secondary_index=2,
        difficulty=8
    ),
    "Dalmasca Estersand - Flowering Cactoid Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2107,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916D",
        difficulty=1
    ),
    "Dalmasca Estersand - Flowering Cactoid Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2108,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916D",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Flowering Cactoid Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2109,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916D",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Patient Barheim Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2110,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916E",
        difficulty=2
    ),
    "Dalmasca Estersand - Patient Barheim Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2111,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916E",
        secondary_index=1,
        difficulty=2
    ),
    "Dalmasca Estersand - Patient Barheim Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2112,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916E",
        secondary_index=2,
        difficulty=2
    ),
    "Dalmasca Estersand - Dantro's Wife Give Cactus Flower Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2113,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9081",
        difficulty=1
    ),
    "Dalmasca Estersand - Dantro's Wife Give Cactus Flower Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2114,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9081",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Dantro's Wife Give Cactus Flower Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2115,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9081",
        secondary_index=2,
        difficulty=1
    ),
    "Dalmasca Estersand - Cactus Family Quest Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2116,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908A",
        difficulty=1
    ),
    "Dalmasca Estersand - Cactus Family Quest Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2117,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908A",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Estersand - Cactus Family Quest Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2118,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908A",
        secondary_index=2,
        difficulty=1
    ),
    "Mt. Bur-Omisace - Acolyte Stone of the Condemner Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2119,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916F",
        difficulty=3
    ),
    "Mt. Bur-Omisace - Acolyte Stone of the Condemner Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2120,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916F",
        secondary_index=1,
        difficulty=3
    ),
    "Mt. Bur-Omisace - Acolyte Stone of the Condemner Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2121,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="916F",
        secondary_index=2,
        difficulty=3
    ),
    "Dalmasca Westersand - Earth Tyrant Quest Wind Globe Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2122,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9170",
        difficulty=1
    ),
    "Dalmasca Westersand - Earth Tyrant Quest Wind Globe Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2123,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9170",
        secondary_index=1,
        difficulty=1
    ),
    "Dalmasca Westersand - Earth Tyrant Quest Wind Globe Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2124,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9170",
        secondary_index=2,
        difficulty=1
    ),
    "Rabanastre - Earth Tyrant Quest Windvane Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2125,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9171",
        difficulty=1
    ),
    "Rabanastre - Earth Tyrant Quest Windvane Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2126,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9171",
        secondary_index=1,
        difficulty=1
    ),
    "Rabanastre - Earth Tyrant Quest Windvane Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2127,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9171",
        secondary_index=2,
        difficulty=1
    ),
    "Garamsythe Waterway - White Mousse Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2128,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9172",
        difficulty=5
    ),
    "Garamsythe Waterway - White Mousse Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2129,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9172",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - White Mousse Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2130,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9172",
        secondary_index=2,
        difficulty=5
    ),
    "Rabanastre - Sorbet Sluice Gate Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2131,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9173",
        difficulty=5
    ),
    "Rabanastre - Sorbet Sluice Gate Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2132,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9173",
        secondary_index=1,
        difficulty=5
    ),
    "Rabanastre - Sorbet Sluice Gate Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2133,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9173",
        secondary_index=2,
        difficulty=5
    ),
    "Ozmone Plain - Enkelados Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2134,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9174",
        difficulty=3
    ),
    "Ozmone Plain - Enkelados Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2135,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9174",
        secondary_index=1,
        difficulty=3
    ),
    "Ozmone Plain - Enkelados Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2136,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9174",
        secondary_index=2,
        difficulty=3
    ),
    "Giza Plains Dry - Lesina Give Errmonea Leaf Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2137,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9062",
        difficulty=3
    ),
    "Giza Plains Dry - Lesina Give Errmonea Leaf Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2138,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9062",
        secondary_index=1,
        difficulty=3
    ),
    "Giza Plains Dry - Lesina Give Errmonea Leaf Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2139,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9062",
        secondary_index=2,
        difficulty=3
    ),
    "Bhujerba - Pilika Merchant's Armband Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2140,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9175",
        difficulty=1
    ),
    "Bhujerba - Pilika Merchant's Armband Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2141,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9175",
        secondary_index=1,
        difficulty=1
    ),
    "Bhujerba - Pilika Merchant's Armband Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2142,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9175",
        secondary_index=2,
        difficulty=1
    ),
    "Bhujerba - Clio's Technicks Pilika's Diary Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2143,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9176",
        difficulty=1
    ),
    "Bhujerba - Clio's Technicks Pilika's Diary Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2144,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9176",
        secondary_index=1,
        difficulty=1
    ),
    "Bhujerba - Clio's Technicks Pilika's Diary Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2145,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9176",
        secondary_index=2,
        difficulty=1
    ),
    "Bhujerba - Pilika Give Pilika's Diary Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2146,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908D",
        difficulty=1
    ),
    "Bhujerba - Pilika Give Pilika's Diary Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2147,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908D",
        secondary_index=1,
        difficulty=1
    ),
    "Bhujerba - Pilika Give Pilika's Diary Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2148,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908D",
        secondary_index=2,
        difficulty=1
    ),
    "Golmore Jungle - Vorpal Bunny Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2149,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9177",
        difficulty=3
    ),
    "Golmore Jungle - Vorpal Bunny Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2150,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9177",
        secondary_index=1,
        difficulty=3
    ),
    "Golmore Jungle - Vorpal Bunny Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2151,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9177",
        secondary_index=2,
        difficulty=3
    ),
    "Giza Plains Rains - Croakadile Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2152,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9178",
        difficulty=2
    ),
    "Giza Plains Rains - Croakadile Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2153,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9178",
        secondary_index=1,
        difficulty=2
    ),
    "Giza Plains Rains - Croakadile Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2154,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9178",
        secondary_index=2,
        difficulty=2
    ),
    "Tchita Uplands - Lindwyrm Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2155,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9179",
        difficulty=5
    ),
    "Tchita Uplands - Lindwyrm Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2156,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9179",
        secondary_index=1,
        difficulty=5
    ),
    "Tchita Uplands - Lindwyrm Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2157,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9179",
        secondary_index=2,
        difficulty=5
    ),
    "Giza Plains Rains - Nomads Silent Urn Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2158,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917A",
        difficulty=3
    ),
    "Giza Plains Rains - Nomads Silent Urn Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2159,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917A",
        secondary_index=1,
        difficulty=3
    ),
    "Giza Plains Rains - Nomads Silent Urn Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2160,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917A",
        secondary_index=2,
        difficulty=3
    ),
    "Garamsythe Waterway - Orthros Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2161,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917B",
        difficulty=5
    ),
    "Garamsythe Waterway - Orthros Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2162,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917B",
        secondary_index=1,
        difficulty=5
    ),
    "Garamsythe Waterway - Orthros Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2163,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917B",
        secondary_index=2,
        difficulty=5
    ),
    "Bhujerba - Niray Site 3 Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2164,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917D"
    ),
    "Bhujerba - Niray Site 3 Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2165,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917D",
        secondary_index=1
    ),
    "Bhujerba - Niray Site 3 Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2166,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917D",
        secondary_index=2
    ),
    "Phon Coast - Site 11 Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2167,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917E",
        difficulty=5
    ),
    "Phon Coast - Site 11 Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2168,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917E",
        secondary_index=1,
        difficulty=5
    ),
    "Phon Coast - Site 11 Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2169,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917E",
        secondary_index=2,
        difficulty=5
    ),
    "Paramina Rift - Fafnir Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2170,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917F",
        difficulty=7
    ),
    "Paramina Rift - Fafnir Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2171,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917F",
        secondary_index=1,
        difficulty=7
    ),
    "Paramina Rift - Fafnir Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2172,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917F",
        secondary_index=2,
        difficulty=7
    ),
    "Zertinan Caverns - Marilith Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2173,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9180",
        difficulty=5
    ),
    "Zertinan Caverns - Marilith Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2174,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9180",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Marilith Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2175,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9180",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - Vyraal Drop Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2176,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9181",
        difficulty=5
    ),
    "Cerobi Steppe - Vyraal Drop Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2177,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9181",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - Vyraal Drop Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2178,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9181",
        secondary_index=2,
        difficulty=5
    ),
    "Balfonheim - Viera Wayfarer Dragon Scale Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2179,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9182",
        difficulty=5
    ),
    "Balfonheim - Viera Wayfarer Dragon Scale Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2180,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9182",
        secondary_index=1,
        difficulty=5
    ),
    "Balfonheim - Viera Wayfarer Dragon Scale Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2181,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9182",
        secondary_index=2,
        difficulty=5
    ),
    "Cerobi Steppe - Wyrm Philosopher Ageworn Key Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2182,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9183",
        difficulty=5
    ),
    "Cerobi Steppe - Wyrm Philosopher Ageworn Key Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2183,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9183",
        secondary_index=1,
        difficulty=5
    ),
    "Cerobi Steppe - Wyrm Philosopher Ageworn Key Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2184,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9183",
        secondary_index=2,
        difficulty=5
    ),
    "Skyferry - Ann's Letter Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2185,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9184",
        difficulty=2
    ),
    "Skyferry - Ann's Letter Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2186,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9184",
        secondary_index=1,
        difficulty=2
    ),
    "Skyferry - Ann's Letter Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2187,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9184",
        secondary_index=2,
        difficulty=2
    ),
    "Skyferry - Ann's Sisters Quest Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2188,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906C",
        difficulty=7
    ),
    "Skyferry - Ann's Sisters Quest Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2189,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906C",
        secondary_index=1,
        difficulty=7
    ),
    "Skyferry - Ann's Sisters Quest Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2190,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906C",
        secondary_index=2,
        difficulty=7
    ),
    "Lowtown - Dusty Letter Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2191,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9185",
        difficulty=2
    ),
    "Lowtown - Dusty Letter Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2192,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9185",
        secondary_index=1,
        difficulty=2
    ),
    "Lowtown - Dusty Letter Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2193,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9185",
        secondary_index=2,
        difficulty=2
    ),
    "Lowtown - Samal Blackened Fragment Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2194,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917C",
        difficulty=5
    ),
    "Lowtown - Samal Blackened Fragment Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2195,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917C",
        secondary_index=1,
        difficulty=5
    ),
    "Lowtown - Samal Blackened Fragment Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2196,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="917C",
        secondary_index=2,
        difficulty=5
    ),
    "Garamsythe Waterway - Dull Fragment Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2197,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9186"
    ),
    "Garamsythe Waterway - Dull Fragment Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2198,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9186",
        secondary_index=1
    ),
    "Garamsythe Waterway - Dull Fragment Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2199,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9186",
        secondary_index=2
    ),
    "Rabanastre - Grimy Fragment Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2200,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9187",
        difficulty=5
    ),
    "Rabanastre - Grimy Fragment Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2201,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9187",
        secondary_index=1,
        difficulty=5
    ),
    "Rabanastre - Grimy Fragment Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2202,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9187",
        secondary_index=2,
        difficulty=5
    ),
    "Old Archades - Moonsilver Medallion Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2203,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9188",
        difficulty=5
    ),
    "Old Archades - Moonsilver Medallion Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2204,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9188",
        secondary_index=1,
        difficulty=5
    ),
    "Old Archades - Moonsilver Medallion Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2205,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9188",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Nabreus Medallion 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2206,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9189",
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2207,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9189",
        secondary_index=1,
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2208,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9189",
        secondary_index=2,
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2209,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918A",
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2210,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918A",
        secondary_index=1,
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2211,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918A",
        secondary_index=2,
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 3 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2212,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918B",
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 3 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2213,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918B",
        secondary_index=1,
        difficulty=6
    ),
    "Nabreus Deadlands - Nabreus Medallion 3 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2214,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918B",
        secondary_index=2,
        difficulty=6
    ),
    "Necrohol of Nabudis - Medallion of Might Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2215,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918C",
        difficulty=7
    ),
    "Necrohol of Nabudis - Medallion of Might Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2216,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918C",
        secondary_index=1,
        difficulty=7
    ),
    "Necrohol of Nabudis - Medallion of Might Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2217,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="918C",
        secondary_index=2,
        difficulty=7
    ),
    "Rabanastre - Viera Rendezvous Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2218,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9056",
        difficulty=1
    ),
    "Rabanastre - Viera Rendezvous Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2219,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9056",
        secondary_index=1,
        difficulty=1
    ),
    "Rabanastre - Viera Rendezvous Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2220,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9056",
        secondary_index=2,
        difficulty=1
    ),
    "Rabanastre - Ktjn Reward Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2221,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9058",
        difficulty=2
    ),
    "Rabanastre - Ktjn Reward Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2222,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9058",
        secondary_index=1,
        difficulty=2
    ),
    "Rabanastre - Ktjn Reward Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2223,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9058",
        secondary_index=2,
        difficulty=2
    ),
    "Nalbina Fortress - Jovy Reward Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2224,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906A",
        difficulty=7
    ),
    "Nalbina Fortress - Jovy Reward Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2225,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906A",
        secondary_index=1,
        difficulty=7
    ),
    "Nalbina Fortress - Jovy Reward Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2226,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906A",
        secondary_index=2,
        difficulty=7
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 1 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2227,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906E"
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 1 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2228,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906E",
        secondary_index=1
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 1 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2229,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906E",
        secondary_index=2
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 2 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2230,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906F"
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 2 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2231,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906F",
        secondary_index=1
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 2 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2232,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="906F",
        secondary_index=2
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 3 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2233,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9057"
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 3 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2234,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9057",
        secondary_index=1
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 3 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2235,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9057",
        secondary_index=2
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 4 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2236,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9070"
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 4 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2237,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9070",
        secondary_index=1
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 4 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2238,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9070",
        secondary_index=2
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 5 Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2239,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9059"
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 5 Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2240,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9059",
        secondary_index=1
    ),
    "Dalmasca Estersand - Outpost Mysterious Glint 5 Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2241,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9059",
        secondary_index=2
    ),
    "Balfonheim - Footrace Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2242,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908F"
    ),
    "Balfonheim - Footrace Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2243,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908F",
        secondary_index=1
    ),
    "Balfonheim - Footrace Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2244,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="908F",
        secondary_index=2
    ),
    "Zertinan Caverns - Defeat Adrammelech Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2245,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9194",
        difficulty=3
    ),
    "Zertinan Caverns - Defeat Adrammelech Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2246,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9194",
        secondary_index=1,
        difficulty=3
    ),
    "Zertinan Caverns - Defeat Adrammelech Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2247,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9194",
        secondary_index=2,
        difficulty=3
    ),
    "Barheim Passage - Defeat Zalera Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2248,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9195",
        difficulty=4
    ),
    "Barheim Passage - Defeat Zalera Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2249,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9195",
        secondary_index=1,
        difficulty=4
    ),
    "Barheim Passage - Defeat Zalera Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2250,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9195",
        secondary_index=2,
        difficulty=4
    ),
    "Garamsythe Waterway - Defeat Cuchulainn Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2251,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9196",
        difficulty=6
    ),
    "Garamsythe Waterway - Defeat Cuchulainn Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2252,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9196",
        secondary_index=1,
        difficulty=6
    ),
    "Garamsythe Waterway - Defeat Cuchulainn Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2253,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9196",
        secondary_index=2,
        difficulty=6
    ),
    "Stilshrine of Miriam - Defeat Zeromus Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2254,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9197",
        difficulty=5
    ),
    "Stilshrine of Miriam - Defeat Zeromus Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2255,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9197",
        secondary_index=1,
        difficulty=5
    ),
    "Stilshrine of Miriam - Defeat Zeromus Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2256,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9197",
        secondary_index=2,
        difficulty=5
    ),
    "Mosphoran Highwaste - Defeat Exodus Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2257,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9198",
        difficulty=4
    ),
    "Mosphoran Highwaste - Defeat Exodus Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2258,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9198",
        secondary_index=1,
        difficulty=4
    ),
    "Mosphoran Highwaste - Defeat Exodus Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2259,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9198",
        secondary_index=2,
        difficulty=4
    ),
    "Necrohol of Nabudis - Defeat Chaos Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2260,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9199",
        difficulty=5
    ),
    "Necrohol of Nabudis - Defeat Chaos Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2261,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9199",
        secondary_index=1,
        difficulty=5
    ),
    "Necrohol of Nabudis - Defeat Chaos Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2262,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9199",
        secondary_index=2,
        difficulty=5
    ),
    "Giruvegan - Defeat Ultima Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2263,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919A",
        difficulty=6
    ),
    "Giruvegan - Defeat Ultima Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2264,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919A",
        secondary_index=1,
        difficulty=6
    ),
    "Giruvegan - Defeat Ultima Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2265,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919A",
        secondary_index=2,
        difficulty=6
    ),
    "Henne Mines - Defeat Zodiark Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2266,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919B",
        difficulty=7
    ),
    "Henne Mines - Defeat Zodiark Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2267,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919B",
        secondary_index=1,
        difficulty=7
    ),
    "Henne Mines - Defeat Zodiark Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2268,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="919B",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Thalassinon - Shelled Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2269,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9090",
        difficulty=6
    ),
    "Phon Coast - Thalassinon - Shelled Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2270,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9090",
        secondary_index=1,
        difficulty=6
    ),
    "Phon Coast - Thalassinon - Shelled Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2271,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9090",
        secondary_index=2,
        difficulty=6
    ),
    "Garamsythe Waterway - Gavial - Fur-scaled Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2272,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9091",
        difficulty=6
    ),
    "Garamsythe Waterway - Gavial - Fur-scaled Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2273,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9091",
        secondary_index=1,
        difficulty=6
    ),
    "Garamsythe Waterway - Gavial - Fur-scaled Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2274,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9091",
        secondary_index=2,
        difficulty=6
    ),
    "Barheim Passage - Ishteen - Bony Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2275,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9092",
        difficulty=7
    ),
    "Barheim Passage - Ishteen - Bony Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2276,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9092",
        secondary_index=1,
        difficulty=7
    ),
    "Barheim Passage - Ishteen - Bony Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2277,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9092",
        secondary_index=2,
        difficulty=7
    ),
    "Dalmasca Westersand - Kaiser Wolf - Fanged Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2278,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9093",
        difficulty=5
    ),
    "Dalmasca Westersand - Kaiser Wolf - Fanged Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2279,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9093",
        secondary_index=1,
        difficulty=5
    ),
    "Dalmasca Westersand - Kaiser Wolf - Fanged Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2280,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9093",
        secondary_index=2,
        difficulty=5
    ),
    "Dalmasca Estersand - Terror Tyrant - Hide-covered Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2281,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9094",
        difficulty=7
    ),
    "Dalmasca Estersand - Terror Tyrant - Hide-covered Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2282,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9094",
        secondary_index=1,
        difficulty=7
    ),
    "Dalmasca Estersand - Terror Tyrant - Hide-covered Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2283,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9094",
        secondary_index=2,
        difficulty=7
    ),
    "Giza Plains Dry - Nazarnir - Maned Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2284,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9095",
        difficulty=7
    ),
    "Giza Plains Dry - Nazarnir - Maned Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2285,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9095",
        secondary_index=1,
        difficulty=7
    ),
    "Giza Plains Dry - Nazarnir - Maned Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2286,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9095",
        secondary_index=2,
        difficulty=7
    ),
    "Zertinan Caverns - Alteci - Fell Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2287,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9096",
        difficulty=5
    ),
    "Zertinan Caverns - Alteci - Fell Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2288,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9096",
        secondary_index=1,
        difficulty=5
    ),
    "Zertinan Caverns - Alteci - Fell Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2289,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9096",
        secondary_index=2,
        difficulty=5
    ),
    "Lhusu Mines - Disma - Accursed Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2290,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9097",
        difficulty=7
    ),
    "Lhusu Mines - Disma - Accursed Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2291,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9097",
        secondary_index=1,
        difficulty=7
    ),
    "Lhusu Mines - Disma - Accursed Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2292,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9097",
        secondary_index=2,
        difficulty=7
    ),
    "Ogir-Yensa Sandsea - Bull Chocobo - Beaked Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2293,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9098",
        difficulty=7
    ),
    "Ogir-Yensa Sandsea - Bull Chocobo - Beaked Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2294,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9098",
        secondary_index=1,
        difficulty=7
    ),
    "Ogir-Yensa Sandsea - Bull Chocobo - Beaked Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2295,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9098",
        secondary_index=2,
        difficulty=7
    ),
    "Nam-Yensa Sandsea - Victanir - Maverick Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2296,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9099",
        difficulty=7
    ),
    "Nam-Yensa Sandsea - Victanir - Maverick Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2297,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9099",
        secondary_index=1,
        difficulty=7
    ),
    "Nam-Yensa Sandsea - Victanir - Maverick Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2298,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="9099",
        secondary_index=2,
        difficulty=7
    ),
    "Tomb of Raithwall - Zombie Lord - Soulless Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2299,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909A",
        difficulty=6
    ),
    "Tomb of Raithwall - Zombie Lord - Soulless Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2300,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909A",
        secondary_index=1,
        difficulty=6
    ),
    "Tomb of Raithwall - Zombie Lord - Soulless Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2301,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909A",
        secondary_index=2,
        difficulty=6
    ),
    "Mosphoran Highwaste - Dheed - Leathern Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2302,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909B",
        difficulty=7
    ),
    "Mosphoran Highwaste - Dheed - Leathern Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2303,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909B",
        secondary_index=1,
        difficulty=7
    ),
    "Mosphoran Highwaste - Dheed - Leathern Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2304,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909B",
        secondary_index=2,
        difficulty=7
    ),
    "Salikawood - Rageclaw - Sickle Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2305,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909C",
        difficulty=5
    ),
    "Salikawood - Rageclaw - Sickle Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2306,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909C",
        secondary_index=1,
        difficulty=5
    ),
    "Salikawood - Rageclaw - Sickle Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2307,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909C",
        secondary_index=2,
        difficulty=5
    ),
    "Nabreus Deadlands - Arioch - Vengeful Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2308,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909D",
        difficulty=7
    ),
    "Nabreus Deadlands - Arioch - Vengeful Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2309,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909D",
        secondary_index=1,
        difficulty=7
    ),
    "Nabreus Deadlands - Arioch - Vengeful Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2310,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909D",
        secondary_index=2,
        difficulty=7
    ),
    "Necrohol of Nabudis - Vorres - Gravesoil Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2311,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909E",
        difficulty=7
    ),
    "Necrohol of Nabudis - Vorres - Gravesoil Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2312,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909E",
        secondary_index=1,
        difficulty=7
    ),
    "Necrohol of Nabudis - Vorres - Gravesoil Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2313,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909E",
        secondary_index=2,
        difficulty=7
    ),
    "Ozmone Plain - Killbug - Metallic Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2314,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909F",
        difficulty=6
    ),
    "Ozmone Plain - Killbug - Metallic Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2315,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909F",
        secondary_index=1,
        difficulty=6
    ),
    "Ozmone Plain - Killbug - Metallic Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2316,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="909F",
        secondary_index=2,
        difficulty=6
    ),
    "Henne Mines - Melt - Slimy Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2317,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A0",
        difficulty=7
    ),
    "Henne Mines - Melt - Slimy Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2318,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A0",
        secondary_index=1,
        difficulty=7
    ),
    "Henne Mines - Melt - Slimy Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2319,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A0",
        secondary_index=2,
        difficulty=7
    ),
    "Golmore Jungle - Biding Mantis - Scythe Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2320,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A1",
        difficulty=6
    ),
    "Golmore Jungle - Biding Mantis - Scythe Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2321,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A1",
        secondary_index=1,
        difficulty=6
    ),
    "Golmore Jungle - Biding Mantis - Scythe Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2322,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A1",
        secondary_index=2,
        difficulty=6
    ),
    "Feywood - Dreadguard - Feathered Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2323,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A2",
        difficulty=7
    ),
    "Feywood - Dreadguard - Feathered Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2324,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A2",
        secondary_index=1,
        difficulty=7
    ),
    "Feywood - Dreadguard - Feathered Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2325,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A2",
        secondary_index=2,
        difficulty=7
    ),
    "Giruvegan - Crystal Knight - Skull Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2326,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A3",
        difficulty=5
    ),
    "Giruvegan - Crystal Knight - Skull Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2327,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A3",
        secondary_index=1,
        difficulty=5
    ),
    "Giruvegan - Crystal Knight - Skull Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2328,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A3",
        secondary_index=2,
        difficulty=5
    ),
    "Paramina Rift - Ancbolder - Mind Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2329,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A4",
        difficulty=5
    ),
    "Paramina Rift - Ancbolder - Mind Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2330,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A4",
        secondary_index=1,
        difficulty=5
    ),
    "Paramina Rift - Ancbolder - Mind Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2331,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A4",
        secondary_index=2,
        difficulty=5
    ),
    "Stilshrine of Miriam - Myath - Eternal Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2332,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A5",
        difficulty=5
    ),
    "Stilshrine of Miriam - Myath - Eternal Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2333,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A5",
        secondary_index=1,
        difficulty=5
    ),
    "Stilshrine of Miriam - Myath - Eternal Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2334,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A5",
        secondary_index=2,
        difficulty=5
    ),
    "Phon Coast - Skullash - Clawed Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2335,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A6",
        difficulty=7
    ),
    "Phon Coast - Skullash - Clawed Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2336,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A6",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Skullash - Clawed Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2337,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A6",
        secondary_index=2,
        difficulty=7
    ),
    "Tchita Uplands - Kris - Odiferous Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2338,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A7",
        difficulty=7
    ),
    "Tchita Uplands - Kris - Odiferous Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2339,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A7",
        secondary_index=1,
        difficulty=7
    ),
    "Tchita Uplands - Kris - Odiferous Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2340,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A7",
        secondary_index=2,
        difficulty=7
    ),
    "Tchita Uplands - Grimalkin - Whiskered Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2341,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A8",
        difficulty=7
    ),
    "Tchita Uplands - Grimalkin - Whiskered Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2342,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A8",
        secondary_index=1,
        difficulty=7
    ),
    "Tchita Uplands - Grimalkin - Whiskered Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2343,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A8",
        secondary_index=2,
        difficulty=7
    ),
    "Sochen Cave Palace - Wendice - Frigid Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2344,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A9",
        difficulty=5
    ),
    "Sochen Cave Palace - Wendice - Frigid Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2345,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A9",
        secondary_index=1,
        difficulty=5
    ),
    "Sochen Cave Palace - Wendice - Frigid Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2346,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90A9",
        secondary_index=2,
        difficulty=5
    ),
    "Sochen Cave Palace - Anubys - Ensanguined Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2347,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AA",
        difficulty=7
    ),
    "Sochen Cave Palace - Anubys - Ensanguined Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2348,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AA",
        secondary_index=1,
        difficulty=7
    ),
    "Sochen Cave Palace - Anubys - Ensanguined Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2349,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AA",
        secondary_index=2,
        difficulty=7
    ),
    "Cerobi Steppe - Bluesang - Cruel Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2350,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AB",
        difficulty=7
    ),
    "Cerobi Steppe - Bluesang - Cruel Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2351,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AB",
        secondary_index=1,
        difficulty=7
    ),
    "Cerobi Steppe - Bluesang - Cruel Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2352,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AB",
        secondary_index=2,
        difficulty=7
    ),
    "Cerobi Steppe - Aspidochelon - Adamantine Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2353,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AC",
        difficulty=7
    ),
    "Cerobi Steppe - Aspidochelon - Adamantine Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2354,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AC",
        secondary_index=1,
        difficulty=7
    ),
    "Cerobi Steppe - Aspidochelon - Adamantine Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2355,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AC",
        secondary_index=2,
        difficulty=7
    ),
    "Ridorana Cataract - Abelisk - Reptilian Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2356,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AD",
        difficulty=7
    ),
    "Ridorana Cataract - Abelisk - Reptilian Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2357,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AD",
        secondary_index=1,
        difficulty=7
    ),
    "Ridorana Cataract - Abelisk - Reptilian Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2358,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AD",
        secondary_index=2,
        difficulty=7
    ),
    "Pharos of Ridorana - Avenger - Vile Trophy Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2359,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AE",
        difficulty=7
    ),
    "Pharos of Ridorana - Avenger - Vile Trophy Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2360,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AE",
        secondary_index=1,
        difficulty=7
    ),
    "Pharos of Ridorana - Avenger - Vile Trophy Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2361,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90AE",
        secondary_index=2,
        difficulty=7
    ),
    "Archades - Hunt Club Owner 5 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2362,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90F9",
        difficulty=6
    ),
    "Archades - Hunt Club Owner 5 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2363,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90F9",
        secondary_index=1,
        difficulty=6
    ),
    "Archades - Hunt Club Owner 5 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2364,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90F9",
        secondary_index=2,
        difficulty=6
    ),
    "Archades - Hunt Club Owner 10 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2365,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FA",
        difficulty=7
    ),
    "Archades - Hunt Club Owner 10 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2366,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FA",
        secondary_index=1,
        difficulty=7
    ),
    "Archades - Hunt Club Owner 10 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2367,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FA",
        secondary_index=2,
        difficulty=7
    ),
    "Archades - Hunt Club Owner 15 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2368,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FB",
        difficulty=7
    ),
    "Archades - Hunt Club Owner 15 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2369,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FB",
        secondary_index=1,
        difficulty=7
    ),
    "Archades - Hunt Club Owner 15 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2370,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FB",
        secondary_index=2,
        difficulty=7
    ),
    "Archades - Hunt Club Owner 20 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2371,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FC",
        difficulty=8
    ),
    "Archades - Hunt Club Owner 20 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2372,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FC",
        secondary_index=1,
        difficulty=8
    ),
    "Archades - Hunt Club Owner 20 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2373,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FC",
        secondary_index=2,
        difficulty=8
    ),
    "Archades - Hunt Club Owner 25 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2374,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FD",
        difficulty=9
    ),
    "Archades - Hunt Club Owner 25 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2375,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FD",
        secondary_index=1,
        difficulty=9
    ),
    "Archades - Hunt Club Owner 25 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2376,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FD",
        secondary_index=2,
        difficulty=9
    ),
    "Archades - Hunt Club Owner 30 Trophy Rares Defeated Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2377,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FE",
        difficulty=10
    ),
    "Archades - Hunt Club Owner 30 Trophy Rares Defeated Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2378,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FE",
        secondary_index=1,
        difficulty=10
    ),
    "Archades - Hunt Club Owner 30 Trophy Rares Defeated Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2379,
        classification=LocationProgressType.DEFAULT,
        type="reward",
        str_id="90FE",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 16 or more Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2380,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F3",
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 16 or more Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2381,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F3",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 16 or more Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2382,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F3",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 15 or less Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2383,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F4",
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 15 or less Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2384,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F4",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Atak 15 or less Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2385,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F4",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 16 or more Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2386,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F5",
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 16 or more Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2387,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F5",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 16 or more Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2388,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F5",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 15 or less Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2389,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F6",
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 15 or less Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2390,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F6",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Blok 15 or less Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2391,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F6",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 16 or more Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2392,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F7",
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 16 or more Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2393,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F7",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 16 or more Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2394,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F7",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 15 or less Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2395,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F8",
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 15 or less Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2396,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F8",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - All Trophies Stok 15 or less Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2397,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90F8",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - Atak 1, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2398,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90FF",
        difficulty=5
    ),
    "Phon Coast - Atak 1, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2399,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90FF",
        secondary_index=1,
        difficulty=5
    ),
    "Phon Coast - Atak 1, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2400,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="90FF",
        secondary_index=2,
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 1, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2401,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9100",
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 1, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2402,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9100",
        secondary_index=1,
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 1, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2403,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9100",
        secondary_index=2,
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 1 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2404,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9101",
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 1 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2405,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9101",
        secondary_index=1,
        difficulty=5
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 1 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2406,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9101",
        secondary_index=2,
        difficulty=5
    ),
    "Phon Coast - Atak 5, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2407,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9102",
        difficulty=6
    ),
    "Phon Coast - Atak 5, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2408,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9102",
        secondary_index=1,
        difficulty=6
    ),
    "Phon Coast - Atak 5, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2409,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9102",
        secondary_index=2,
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 5, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2410,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9103",
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 5, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2411,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9103",
        secondary_index=1,
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 5, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2412,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9103",
        secondary_index=2,
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 5 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2413,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9104",
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 5 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2414,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9104",
        secondary_index=1,
        difficulty=6
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 5 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2415,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9104",
        secondary_index=2,
        difficulty=6
    ),
    "Phon Coast - Atak 10, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2416,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9105",
        difficulty=7
    ),
    "Phon Coast - Atak 10, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2417,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9105",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 10, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2418,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9105",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 10, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2419,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9106",
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 10, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2420,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9106",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 10, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2421,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9106",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 10 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2422,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9107",
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 10 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2423,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9107",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 10 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2424,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9107",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 15, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2425,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9108",
        difficulty=7
    ),
    "Phon Coast - Atak 15, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2426,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9108",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 15, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2427,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9108",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 15, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2428,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9109",
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 15, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2429,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9109",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 15, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2430,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9109",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 15 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2431,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910A",
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 15 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2432,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910A",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 15 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2433,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910A",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 10, Blok 5, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2434,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910B",
        difficulty=7
    ),
    "Phon Coast - Atak 10, Blok 5, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2435,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910B",
        secondary_index=1,
        difficulty=7
    ),
    "Phon Coast - Atak 10, Blok 5, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2436,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910B",
        secondary_index=2,
        difficulty=7
    ),
    "Phon Coast - Atak 20, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2437,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910C",
        difficulty=8
    ),
    "Phon Coast - Atak 20, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2438,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910C",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 20, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2439,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910C",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 20, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2440,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910D",
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 20, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2441,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910D",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 20, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2442,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910D",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 20 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2443,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910E",
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 20 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2444,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910E",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 20 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2445,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910E",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 10, Stok 5 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2446,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910F",
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 10, Stok 5 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2447,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910F",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 10, Stok 5 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2448,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="910F",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 25, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2449,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9110",
        difficulty=9
    ),
    "Phon Coast - Atak 25, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2450,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9110",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 25, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2451,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9110",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 25, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2452,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9111",
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 25, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2453,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9111",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 25, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2454,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9111",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 25 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2455,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9112",
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 25 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2456,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9112",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 25 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2457,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9112",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 15 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2458,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9113",
        difficulty=9
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 15 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2459,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9113",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 15 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2460,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9113",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 30, Blok 0, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2461,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9114",
        difficulty=10
    ),
    "Phon Coast - Atak 30, Blok 0, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2462,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9114",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - Atak 30, Blok 0, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2463,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9114",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 30, Stok 0 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2464,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9115",
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 30, Stok 0 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2465,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9115",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 30, Stok 0 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2466,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9115",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 30 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2467,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9116",
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 30 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2468,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9116",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - Atak 0, Blok 0, Stok 30 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2469,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9116",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - Atak 10, Blok 10, Stok 10 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2470,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9117",
        difficulty=10
    ),
    "Phon Coast - Atak 10, Blok 10, Stok 10 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2471,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9117",
        secondary_index=1,
        difficulty=10
    ),
    "Phon Coast - Atak 10, Blok 10, Stok 10 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2472,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9117",
        secondary_index=2,
        difficulty=10
    ),
    "Phon Coast - Atak 25, Blok 1, Stok 1 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2473,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9118",
        difficulty=9
    ),
    "Phon Coast - Atak 25, Blok 1, Stok 1 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2474,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9118",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 25, Blok 1, Stok 1 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2475,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9118",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 25, Stok 1 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2476,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9119",
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 25, Stok 1 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2477,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9119",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 25, Stok 1 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2478,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="9119",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 1, Stok 25 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2479,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911A",
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 1, Stok 25 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2480,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911A",
        secondary_index=1,
        difficulty=9
    ),
    "Phon Coast - Atak 1, Blok 1, Stok 25 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2481,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911A",
        secondary_index=2,
        difficulty=9
    ),
    "Phon Coast - Atak 12, Blok 5, Stok 5 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2482,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911B",
        difficulty=8
    ),
    "Phon Coast - Atak 12, Blok 5, Stok 5 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2483,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911B",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 12, Blok 5, Stok 5 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2484,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911B",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 12, Stok 5 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2485,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911C",
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 12, Stok 5 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2486,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911C",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 12, Stok 5 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2487,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911C",
        secondary_index=2,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 12 Outfitters Reward (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2488,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911D",
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 12 Outfitters Reward (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2489,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911D",
        secondary_index=1,
        difficulty=8
    ),
    "Phon Coast - Atak 5, Blok 5, Stok 12 Outfitters Reward (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2490,
        classification=LocationProgressType.EXCLUDED,
        type="reward",
        str_id="911D",
        secondary_index=2,
        difficulty=8
    ),
    "Vaan's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2491,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        difficulty=3
    ),
    "Vaan's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2492,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=1,
        difficulty=3
    ),
    "Vaan's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2493,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=2,
        difficulty=3
    ),
    "Vaan's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2494,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=3,
        difficulty=3
    ),
    "Vaan's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2495,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=4,
        difficulty=3
    ),
    "Vaan's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2496,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=5,
        difficulty=3
    ),
    "Vaan's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2497,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=6,
        difficulty=3
    ),
    "Vaan's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2498,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=7,
        difficulty=3
    ),
    "Vaan's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2499,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="0",
        secondary_index=8,
        difficulty=3
    ),
    "Ashe's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2500,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        difficulty=3
    ),
    "Ashe's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2501,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=1,
        difficulty=3
    ),
    "Ashe's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2502,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=2,
        difficulty=3
    ),
    "Ashe's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2503,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=3,
        difficulty=3
    ),
    "Ashe's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2504,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=4,
        difficulty=3
    ),
    "Ashe's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2505,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=5,
        difficulty=3
    ),
    "Ashe's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2506,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=6,
        difficulty=3
    ),
    "Ashe's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2507,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=7,
        difficulty=3
    ),
    "Ashe's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2508,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="1",
        secondary_index=8,
        difficulty=3
    ),
    "Fran's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2509,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        difficulty=3
    ),
    "Fran's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2510,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=1,
        difficulty=3
    ),
    "Fran's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2511,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=2,
        difficulty=3
    ),
    "Fran's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2512,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=3,
        difficulty=3
    ),
    "Fran's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2513,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=4,
        difficulty=3
    ),
    "Fran's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2514,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=5,
        difficulty=3
    ),
    "Fran's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2515,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=6,
        difficulty=3
    ),
    "Fran's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2516,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=7,
        difficulty=3
    ),
    "Fran's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2517,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="2",
        secondary_index=8,
        difficulty=3
    ),
    "Balthier's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2518,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        difficulty=3
    ),
    "Balthier's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2519,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=1,
        difficulty=3
    ),
    "Balthier's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2520,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=2,
        difficulty=3
    ),
    "Balthier's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2521,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=3,
        difficulty=3
    ),
    "Balthier's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2522,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=4,
        difficulty=3
    ),
    "Balthier's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2523,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=5,
        difficulty=3
    ),
    "Balthier's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2524,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=6,
        difficulty=3
    ),
    "Balthier's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2525,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=7,
        difficulty=3
    ),
    "Balthier's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2526,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="3",
        secondary_index=8,
        difficulty=3
    ),
    "Basch's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2527,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        difficulty=3
    ),
    "Basch's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2528,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=1,
        difficulty=3
    ),
    "Basch's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2529,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=2,
        difficulty=3
    ),
    "Basch's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2530,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=3,
        difficulty=3
    ),
    "Basch's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2531,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=4,
        difficulty=3
    ),
    "Basch's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2532,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=5,
        difficulty=3
    ),
    "Basch's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2533,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=6,
        difficulty=3
    ),
    "Basch's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2534,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=7,
        difficulty=3
    ),
    "Basch's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2535,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="4",
        secondary_index=8,
        difficulty=3
    ),
    "Penelo's Starting Items (1)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2536,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        difficulty=3
    ),
    "Penelo's Starting Items (2)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2537,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=1,
        difficulty=3
    ),
    "Penelo's Starting Items (3)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2538,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=2,
        difficulty=3
    ),
    "Penelo's Starting Items (4)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2539,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=3,
        difficulty=3
    ),
    "Penelo's Starting Items (5)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2540,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=4,
        difficulty=3
    ),
    "Penelo's Starting Items (6)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2541,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=5,
        difficulty=3
    ),
    "Penelo's Starting Items (7)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2542,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=6,
        difficulty=3
    ),
    "Penelo's Starting Items (8)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2543,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=7,
        difficulty=3
    ),
    "Penelo's Starting Items (9)": FF12OpenWorldLocationData(
        region="Ivalice",
        address=FF12OW_BASE_ID + 2544,
        classification=LocationProgressType.DEFAULT,
        type="inventory",
        str_id="5",
        secondary_index=8,
        difficulty=3
    ),
}

location_table = {location_name: location_data.address for location_name, location_data in location_data_table.items()}