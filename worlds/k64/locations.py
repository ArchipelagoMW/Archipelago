import typing
from BaseClasses import Location
from .names import LocationName


class K64Location(Location):
    game: str = "Kirby 64 - The Crystal Shards"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


stage_locations = {
    0x640001: LocationName.pop_star_1,
    0x640002: LocationName.pop_star_2,
    0x640003: LocationName.pop_star_3,
    0x640004: LocationName.rock_star_1,
    0x640005: LocationName.rock_star_2,
    0x640006: LocationName.rock_star_3,
    0x640007: LocationName.rock_star_4,
    0x640008: LocationName.aqua_star_1,
    0x640009: LocationName.aqua_star_2,
    0x64000A: LocationName.aqua_star_3,
    0x64000B: LocationName.aqua_star_4,
    0x64000C: LocationName.neo_star_1,
    0x64000D: LocationName.neo_star_2,
    0x64000E: LocationName.neo_star_3,
    0x64000F: LocationName.neo_star_4,
    0x640010: LocationName.shiver_star_1,
    0x640011: LocationName.shiver_star_2,
    0x640012: LocationName.shiver_star_3,
    0x640013: LocationName.shiver_star_4,
    0x640014: LocationName.ripple_star_1,
    0x640015: LocationName.ripple_star_2,
    0x640016: LocationName.ripple_star_3,
}

crystal_shard_locations = {
    0x640101: LocationName.pop_star_1_s1,
    0x640102: LocationName.pop_star_1_s2,
    0x640103: LocationName.pop_star_1_s3,
    0x640104: LocationName.pop_star_2_s1,
    0x640105: LocationName.pop_star_2_s2,
    0x640106: LocationName.pop_star_2_s3,
    0x640107: LocationName.pop_star_3_s1,
    0x640108: LocationName.pop_star_3_s2,
    0x640109: LocationName.pop_star_3_s3,
    0x64010A: LocationName.rock_star_1_s1,
    0x64010B: LocationName.rock_star_1_s2,
    0x64010C: LocationName.rock_star_1_s3,
    0x64010D: LocationName.rock_star_2_s1,
    0x64010E: LocationName.rock_star_2_s2,
    0x64010F: LocationName.rock_star_2_s3,
    0x640110: LocationName.rock_star_3_s1,
    0x640111: LocationName.rock_star_3_s2,
    0x640112: LocationName.rock_star_3_s3,
    0x640113: LocationName.rock_star_4_s1,
    0x640114: LocationName.rock_star_4_s2,
    0x640115: LocationName.rock_star_4_s3,
    0x640116: LocationName.aqua_star_1_s1,
    0x640117: LocationName.aqua_star_1_s2,
    0x640118: LocationName.aqua_star_1_s3,
    0x640119: LocationName.aqua_star_2_s1,
    0x64011A: LocationName.aqua_star_2_s2,
    0x64011B: LocationName.aqua_star_2_s3,
    0x64011C: LocationName.aqua_star_3_s1,
    0x64011D: LocationName.aqua_star_3_s2,
    0x64011E: LocationName.aqua_star_3_s3,
    0x64011F: LocationName.aqua_star_4_s1,
    0x640120: LocationName.aqua_star_4_s2,
    0x640121: LocationName.aqua_star_4_s3,
    0x640122: LocationName.neo_star_1_s1,
    0x640123: LocationName.neo_star_1_s2,
    0x640124: LocationName.neo_star_1_s3,
    0x640125: LocationName.neo_star_2_s1,
    0x640126: LocationName.neo_star_2_s2,
    0x640127: LocationName.neo_star_2_s3,
    0x640128: LocationName.neo_star_3_s1,
    0x640129: LocationName.neo_star_3_s2,
    0x64012A: LocationName.neo_star_3_s3,
    0x64012B: LocationName.neo_star_4_s1,
    0x64012C: LocationName.neo_star_4_s2,
    0x64012D: LocationName.neo_star_4_s3,
    0x64012E: LocationName.shiver_star_1_s1,
    0x64012F: LocationName.shiver_star_1_s2,
    0x640130: LocationName.shiver_star_1_s3,
    0x640131: LocationName.shiver_star_2_s1,
    0x640132: LocationName.shiver_star_2_s2,
    0x640133: LocationName.shiver_star_2_s3,
    0x640134: LocationName.shiver_star_3_s1,
    0x640135: LocationName.shiver_star_3_s2,
    0x640136: LocationName.shiver_star_3_s3,
    0x640137: LocationName.shiver_star_4_s1,
    0x640138: LocationName.shiver_star_4_s2,
    0x640139: LocationName.shiver_star_4_s3,
    0x64013A: LocationName.ripple_star_1_s1,
    0x64013B: LocationName.ripple_star_1_s2,
    0x64013C: LocationName.ripple_star_1_s3,
    0x64013D: LocationName.ripple_star_2_s1,
    0x64013E: LocationName.ripple_star_2_s2,
    0x64013F: LocationName.ripple_star_2_s3,
    0x640140: LocationName.ripple_star_3_s1,
    0x640141: LocationName.ripple_star_3_s2,
    0x640142: LocationName.ripple_star_3_s3,
}

boss_locations = {
    0x640200: LocationName.pop_star_boss,
    0x640201: LocationName.rock_star_boss,
    0x640202: LocationName.aqua_star_boss,
    0x640203: LocationName.neo_star_boss,
    0x640204: LocationName.shiver_star_boss,
    0x640205: LocationName.ripple_star_boss,
}

location_table = {
    **stage_locations,
    **crystal_shard_locations,
    **boss_locations,
}
