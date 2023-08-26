import typing
from BaseClasses import Location, Region
from .Names import LocationName

if typing.TYPE_CHECKING:
    from .Room import Room


class KDL3Location(Location):
    game: str = "Kirby's Dream Land 3"
    room: typing.Optional["Room"] = None

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent: typing.Union[Region, None]):
        super().__init__(player, name, address, parent)
        self.event = not address


stage_locations = {
    0x770001: LocationName.grass_land_1,
    0x770002: LocationName.grass_land_2,
    0x770003: LocationName.grass_land_3,
    0x770004: LocationName.grass_land_4,
    0x770005: LocationName.grass_land_5,
    0x770006: LocationName.grass_land_6,
    0x770007: LocationName.ripple_field_1,
    0x770008: LocationName.ripple_field_2,
    0x770009: LocationName.ripple_field_3,
    0x77000A: LocationName.ripple_field_4,
    0x77000B: LocationName.ripple_field_5,
    0x77000C: LocationName.ripple_field_6,
    0x77000D: LocationName.sand_canyon_1,
    0x77000E: LocationName.sand_canyon_2,
    0x77000F: LocationName.sand_canyon_3,
    0x770010: LocationName.sand_canyon_4,
    0x770011: LocationName.sand_canyon_5,
    0x770012: LocationName.sand_canyon_6,
    0x770013: LocationName.cloudy_park_1,
    0x770014: LocationName.cloudy_park_2,
    0x770015: LocationName.cloudy_park_3,
    0x770016: LocationName.cloudy_park_4,
    0x770017: LocationName.cloudy_park_5,
    0x770018: LocationName.cloudy_park_6,
    0x770019: LocationName.iceberg_1,
    0x77001A: LocationName.iceberg_2,
    0x77001B: LocationName.iceberg_3,
    0x77001C: LocationName.iceberg_4,
    0x77001D: LocationName.iceberg_5,
    0x77001E: LocationName.iceberg_6,
}

heart_star_locations = {
    0x770101: LocationName.grass_land_tulip,
    0x770102: LocationName.grass_land_muchi,
    0x770103: LocationName.grass_land_pitcherman,
    0x770104: LocationName.grass_land_chao,
    0x770105: LocationName.grass_land_mine,
    0x770106: LocationName.grass_land_pierre,
    0x770107: LocationName.ripple_field_kamuribana,
    0x770108: LocationName.ripple_field_bakasa,
    0x770109: LocationName.ripple_field_elieel,
    0x77010A: LocationName.ripple_field_toad,
    0x77010B: LocationName.ripple_field_mama_pitch,
    0x77010C: LocationName.ripple_field_hb002,
    0x77010D: LocationName.sand_canyon_mushrooms,
    0x77010E: LocationName.sand_canyon_auntie,
    0x77010F: LocationName.sand_canyon_caramello,
    0x770110: LocationName.sand_canyon_hikari,
    0x770111: LocationName.sand_canyon_nyupun,
    0x770112: LocationName.sand_canyon_rob,
    0x770113: LocationName.cloudy_park_hibanamodoki,
    0x770114: LocationName.cloudy_park_piyokeko,
    0x770115: LocationName.cloudy_park_mrball,
    0x770116: LocationName.cloudy_park_mikarin,
    0x770117: LocationName.cloudy_park_pick,
    0x770118: LocationName.cloudy_park_hb007,
    0x770119: LocationName.iceberg_kogoesou,
    0x77011A: LocationName.iceberg_samus,
    0x77011B: LocationName.iceberg_kawasaki,
    0x77011C: LocationName.iceberg_name,
    0x77011D: LocationName.iceberg_shiro,
    0x77011E: LocationName.iceberg_angel,
}

boss_locations = {
    0x770200: LocationName.grass_land_whispy,
    0x770201: LocationName.ripple_field_acro,
    0x770202: LocationName.sand_canyon_poncon,
    0x770203: LocationName.cloudy_park_ado,
    0x770204: LocationName.iceberg_dedede,
}

consumable_locations = {
    0x770300: LocationName.grass_land_1_u1,
    0x770301: LocationName.grass_land_1_m1,
    0x770302: LocationName.grass_land_2_u1,
    0x770303: LocationName.grass_land_3_u1,
    0x770304: LocationName.grass_land_3_m1,
    0x770305: LocationName.grass_land_4_m1,
    0x770306: LocationName.grass_land_4_u1,
    0x770307: LocationName.grass_land_4_m2,
    0x770308: LocationName.grass_land_4_m3,
    0x770309: LocationName.grass_land_6_u1,
    0x77030A: LocationName.grass_land_6_u2,
    0x77030B: LocationName.ripple_field_2_u1,
    0x77030C: LocationName.ripple_field_2_m1,
    0x77030D: LocationName.ripple_field_3_m1,
    0x77030E: LocationName.ripple_field_3_u1,
    0x77030F: LocationName.ripple_field_4_m2,
    0x770310: LocationName.ripple_field_4_u1,
    0x770311: LocationName.ripple_field_4_m1,
    0x770312: LocationName.ripple_field_5_u1,
    0x770313: LocationName.ripple_field_5_m2,
    0x770314: LocationName.ripple_field_5_m1,
    0x770315: LocationName.sand_canyon_1_u1,
    0x770316: LocationName.sand_canyon_2_u1,
    0x770317: LocationName.sand_canyon_2_m1,
    0x770318: LocationName.sand_canyon_4_m1,
    0x770319: LocationName.sand_canyon_4_u1,
    0x77031A: LocationName.sand_canyon_4_m2,
    0x77031B: LocationName.sand_canyon_5_u1,
    0x77031C: LocationName.sand_canyon_5_u3,
    0x77031D: LocationName.sand_canyon_5_m1,
    0x77031E: LocationName.sand_canyon_5_u4,
    0x77031F: LocationName.sand_canyon_5_u2,
    0x770320: LocationName.cloudy_park_1_m1,
    0x770321: LocationName.cloudy_park_1_u1,
    0x770322: LocationName.cloudy_park_4_u1,
    0x770323: LocationName.cloudy_park_4_m1,
    0x770324: LocationName.cloudy_park_5_m1,
    0x770325: LocationName.cloudy_park_6_u1,
    0x770326: LocationName.iceberg_3_m1,
    0x770327: LocationName.iceberg_5_u1,
    0x770328: LocationName.iceberg_5_u2,
    0x770329: LocationName.iceberg_5_u3,
    0x77032A: LocationName.iceberg_6_m1,
    0x77032B: LocationName.iceberg_6_u1,
}

level_consumables = {
    1: [0, 1],
    2: [2],
    3: [3, 4],
    4: [5, 6, 7, 8],
    6: [9, 10],
    8: [11, 12],
    9: [13, 14],
    10: [15, 16, 17],
    11: [18, 19, 20],
    13: [21],
    14: [22, 23],
    16: [24, 25, 26],
    17: [27, 28, 29, 30, 31],
    19: [32, 33],
    22: [34, 35],
    23: [36],
    24: [37],
    27: [38],
    29: [39, 40, 41],
    30: [42, 43],
}

location_table = {
    **stage_locations,
    **heart_star_locations,
    **boss_locations,
    **consumable_locations,
}
