import typing

from BaseClasses import Location
from .Names import LocationNames


class OSRSLocation(Location):
    game: str = "Old School Runescape"


class LocationData(typing.NamedTuple):
    id: int
    name: str
    qp: int = 0


Quest_Locations = [
    LocationData(0x070000, LocationNames.Q_Cooks_Assistant),
    LocationData(0x070001, LocationNames.Q_Demon_Slayer),
    LocationData(0x070002, LocationNames.Q_Restless_Ghost),
    LocationData(0x070003, LocationNames.Q_Romeo_Juliet),
    LocationData(0x070004, LocationNames.Q_Sheep_Shearer),
    LocationData(0x070005, LocationNames.Q_Shield_of_Arrav),
    LocationData(0x070006, LocationNames.Q_Ernest_the_Chicken),
    LocationData(0x070007, LocationNames.Q_Vampyre_Slayer),
    LocationData(0x070008, LocationNames.Q_Imp_Catcher),
    LocationData(0x070009, LocationNames.Q_Prince_Ali_Rescue),
    LocationData(0x07000A, LocationNames.Q_Dorics_Quest),
    LocationData(0x07000B, LocationNames.Q_Black_Knights_Fortress),
    LocationData(0x07000C, LocationNames.Q_Witchs_Potion),
    LocationData(0x07000D, LocationNames.Q_Knights_Sword),
    LocationData(0x07000E, LocationNames.Q_Goblin_Diplomacy),
    LocationData(0x07000F, LocationNames.Q_Pirates_Treasure),
    LocationData(0x070010, LocationNames.Q_Rune_Mysteries),
    LocationData(0x070011, LocationNames.Q_Misthalin_Mystery),
    LocationData(0x070012, LocationNames.Q_Corsair_Curse),
    LocationData(0x070013, LocationNames.Q_X_Marks_the_Spot),
    LocationData(0x070014, LocationNames.Q_Below_Ice_Mountain),
]

Skill_Locations = [
    LocationData(0x070015, LocationNames.Guppy),
    LocationData(0x070016, LocationNames.Cavefish),
    LocationData(0x070017, LocationNames.Tetra),
    LocationData(0x070018, LocationNames.Barronite_Deposit),
    LocationData(0x070019, LocationNames.Oak_Log),
    LocationData(0x07001A, LocationNames.Willow_Log),
    LocationData(0x07001B, LocationNames.Catch_Lobster),
    LocationData(0x07001C, LocationNames.Mine_Silver),
    LocationData(0x07001D, LocationNames.Mine_Coal),
    LocationData(0x07001E, LocationNames.Mine_Gold),
    LocationData(0x07001F, LocationNames.Smelt_Silver),
    LocationData(0x070020, LocationNames.Smelt_Steel),
    LocationData(0x070021, LocationNames.Smelt_Gold),
    LocationData(0x070022, LocationNames.Cut_Sapphire),
    LocationData(0x070023, LocationNames.Cut_Emerald),
    LocationData(0x070024, LocationNames.Cut_Ruby),
    LocationData(0x070025, LocationNames.Bake_Apple_Pie),
    LocationData(0x070026, LocationNames.Bake_Cake),
    LocationData(0x070027, LocationNames.Bake_Meat_Pizza)
]

Misc_Locations = [
    LocationData(0x070028, LocationNames.K_Lesser_Demon),
    LocationData(0x070029, LocationNames.K_Ogress_Shaman),
    LocationData(0x07002A, LocationNames.Total_XP_5000),
    LocationData(0x07002B, LocationNames.Total_XP_10000),
    LocationData(0x07002C, LocationNames.Total_XP_25000),
    LocationData(0x07002D, LocationNames.Total_XP_50000),
    LocationData(0x07002E, LocationNames.Total_XP_100000),
    LocationData(0x07002F, LocationNames.Total_Level_50),
    LocationData(0x070030, LocationNames.Total_Level_100),
    LocationData(0x070031, LocationNames.Total_Level_150),
    LocationData(0x070032, LocationNames.Total_Level_200),
    LocationData(0x070033, LocationNames.Combat_Level_5),
    LocationData(0x070034, LocationNames.Combat_Level_15),
    LocationData(0x070035, LocationNames.Combat_Level_25)
]

Quest_Point_Locations = [
    LocationData(0x070040, LocationNames.QP_Cooks_Assistant),
    LocationData(0x070041, LocationNames.QP_Demon_Slayer),
    LocationData(0x070042, LocationNames.QP_Restless_Ghost),
    LocationData(0x070043, LocationNames.QP_Romeo_Juliet),
    LocationData(0x070044, LocationNames.QP_Sheep_Shearer),
    LocationData(0x070045, LocationNames.QP_Shield_of_Arrav),
    LocationData(0x070046, LocationNames.QP_Ernest_the_Chicken),
    LocationData(0x070047, LocationNames.QP_Vampyre_Slayer),
    LocationData(0x070048, LocationNames.QP_Imp_Catcher),
    LocationData(0x070049, LocationNames.QP_Prince_Ali_Rescue),
    LocationData(0x07004A, LocationNames.QP_Dorics_Quest),
    LocationData(0x07004B, LocationNames.QP_Black_Knights_Fortress),
    LocationData(0x07004C, LocationNames.QP_Witchs_Potion),
    LocationData(0x07004D, LocationNames.QP_Knights_Sword),
    LocationData(0x07004E, LocationNames.QP_Goblin_Diplomacy),
    LocationData(0x07004F, LocationNames.QP_Pirates_Treasure),
    LocationData(0x070050, LocationNames.QP_Rune_Mysteries),
    LocationData(0x070051, LocationNames.QP_Misthalin_Mystery),
    LocationData(0x070052, LocationNames.QP_Corsair_Curse),
    LocationData(0x070053, LocationNames.QP_X_Marks_the_Spot),
    LocationData(0x070054, LocationNames.QP_Below_Ice_Mountain),
]
all_locations: typing.List[LocationData] = Quest_Locations + Skill_Locations + Misc_Locations
location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}
location_data_table: typing.Dict[str, LocationData] = {locData.name: locData for locData in all_locations}
