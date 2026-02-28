# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/event_checks.py
#
# Copyright (C) 2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Mapping
from .locations import LocationCheck, VarCheck, FlagCheck, OnceCheck

event_checks: Mapping[str, LocationCheck] = {
    "fen_badge": FlagCheck(id=0x9C),
    "met_oak_pal_park": FlagCheck(id=0x242, invert=True),
    "lake_verity_defeat_mars": FlagCheck(id=0xBA),
    "lake_explosion": FlagCheck(id=0xB9C),
    "forest_badge": FlagCheck(id=0x74),
    "cobble_badge": FlagCheck(id=0x9D),
    "galactic_hq_defeat_cyrus": FlagCheck(id=0x235),
    "lake_valor_defeat_saturn": FlagCheck(id=0x13E),
    "lake_acuity_meet_jupiter": FlagCheck(id=0x1B9),
    "icicle_badge": FlagCheck(id=0x9E),
    "eterna_defeat_team_galactic": FlagCheck(id=0x1FD),
    "relic_badge": FlagCheck(id=0x7D),
    "coal_badge": FlagCheck(id=0x75),
    "beacon_badge": FlagCheck(id=0xB6),
    "mine_badge": FlagCheck(id=0x92),
    "beat_cynthia": FlagCheck(id=0x964),
    "distortion_world": FlagCheck(id=0x28F),
    "valley_windworks_defeat_team_galactic": FlagCheck(id=0x1A5),
}
