import typing
from BaseClasses import Location
from .Names import LocationName


class KDL3Location(Location):
    game: str = "Kirby's Dream Land 3"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
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

location_table = {
    **stage_locations,
    **heart_star_locations,
    **boss_locations,
}
