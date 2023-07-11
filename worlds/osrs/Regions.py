import typing

from BaseClasses import CollectionState
from .Locations import LocationNames
from .Items import ItemNames


class RegionNames:
    Lumbridge = "Lumbridge"
    Lumbridge_Swamp = "Lumbridge Swamp"
    Lumbridge_Farms = "Lumbridge Farms"
    HAM_Hideout = "HAM Hideout"
    Draynor_Village = "Draynor Village"
    Draynor_Manor = "Draynor Manor"
    Wizards_Tower = "Wizard's Tower"
    Al_Kharid = "Al Kharid"
    Citharede_Abbey = "Citharede Abbey"
    South_Of_Varrock = "South of Varrock"
    Central_Varrock = "Central Varrock"
    Varrock_Palace = "Varrock Palace"
    East_Of_Varrock = "East of Varrock"
    West_Varrock = "West Varrock"
    Edgeville = "Edgeville"
    Barbarian_Village = "Barbarian Village"
    Monastery = "Monastery"
    Ice_Mountain = "Ice Mountain"
    Dwarven_Mines = "Dwarven Mines"
    Falador = "Falador"
    Falador_Farm = "Falador Farm"
    Crafting_Guild = "Crafting Guild"
    Rimmington = "Rimmington"
    Port_Sarim = "Port Sarim"
    Mudskipper_Point = "Mudskipper Point"
    Karamja = "Karamja"
    Corsair_Cove = "Corsair Cove"
    Wilderness = "The Wilderness"
    Crandor = "Crandor"
    # Resource Regions
    Egg = "Egg"
    Sheep = "Sheep"
    Milk = "Milk"
    Wheat = "Wheat"
    Windmill = "Windmill"
    Spinning_Wheel = "Spinning Wheel"
    Imp = "Imp"
    Bronze_Ores = "Tin and Copper"
    Clay_Rock = "Clay Rocks"
    Coal_Rock = "Coal Rocks"
    Iron_Rock = "Iron Rocks"
    Silver_Rock = "Silver Rocks"
    Gold_Rock = "Gold Rocks"
    Furnace = "Furnace"
    Anvil = "Anvil"


class RegionInfo(typing.NamedTuple):
    name: str
    locations: typing.List[str]
    exits: typing.Dict[str, str]
    conditionGenerator: typing.Callable[[int], typing.Dict[str, typing.Callable[[CollectionState], bool]]]


all_regions = [
    RegionInfo("Menu",
               [
                   LocationNames.Oak_Log,
                   LocationNames.Willow_Log,
                   LocationNames.Catch_Lobster,
                   LocationNames.Cut_Sapphire,
                   LocationNames.Cut_Emerald,
                   LocationNames.Cut_Ruby,
                   LocationNames.K_Lesser_Demon,
                   LocationNames.Bake_Cake,
                   LocationNames.Bake_Meat_Pizza,
                   LocationNames.Total_XP_5000,
                   LocationNames.Total_XP_10000,
                   LocationNames.Total_XP_25000,
                   LocationNames.Total_XP_50000,
                   LocationNames.Total_XP_100000,
                   LocationNames.Total_Level_50,
                   LocationNames.Total_Level_100,
                   LocationNames.Total_Level_200,
                   LocationNames.Combat_Level_5,
                   LocationNames.Combat_Level_15,
                   LocationNames.Combat_Level_25,
               ],
               {},
               lambda player: {}
               ),
    RegionInfo(RegionNames.Lumbridge,
               [
                   LocationNames.Q_Cooks_Assistant,
                   LocationNames.Q_Rune_Mysteries,
                   LocationNames.Q_Restless_Ghost,
                   LocationNames.Q_X_Marks_the_Spot,
                   LocationNames.QP_Cooks_Assistant,
                   LocationNames.QP_Rune_Mysteries,
                   LocationNames.QP_Restless_Ghost,
                   LocationNames.QP_X_Marks_the_Spot
               ],
               {
                   f"{RegionNames.Lumbridge}->{RegionNames.Lumbridge_Swamp}": RegionNames.Lumbridge_Swamp,
                   f"{RegionNames.Lumbridge}->{RegionNames.Lumbridge_Farms}": RegionNames.Lumbridge_Farms,
                   f"{RegionNames.Lumbridge}->{RegionNames.HAM_Hideout}": RegionNames.HAM_Hideout,
                   f"{RegionNames.Lumbridge}->{RegionNames.Al_Kharid}": RegionNames.Al_Kharid,
                   f"{RegionNames.Lumbridge}->{RegionNames.Spinning_Wheel}": RegionNames.Spinning_Wheel,
                   f"{RegionNames.Lumbridge}->{RegionNames.Imp}": RegionNames.Imp,
               },
               lambda player: ({
                   RegionNames.Lumbridge_Swamp:
                       lambda state: (state.has(ItemNames.Lumbridge_Swamp, player)),
                   RegionNames.Lumbridge_Farms:
                       lambda state: (state.has(ItemNames.Lumbridge_Farms, player)),
                   RegionNames.HAM_Hideout:
                       lambda state: (state.has(ItemNames.HAM_Hideout, player)),
                   RegionNames.Al_Kharid:
                       lambda state: (state.has(ItemNames.Al_Kharid, player)),
                   RegionNames.Spinning_Wheel:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Lumbridge_Swamp,
               [
                   LocationNames.Q_Misthalin_Mystery,
                   LocationNames.QP_Misthalin_Mystery,
               ],
               {
                   f"{RegionNames.Lumbridge_Swamp}->{RegionNames.Lumbridge}": RegionNames.Lumbridge,
                   f"{RegionNames.Lumbridge_Swamp}->{RegionNames.HAM_Hideout}": RegionNames.HAM_Hideout,
                   f"{RegionNames.Lumbridge_Swamp}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.Lumbridge_Swamp}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
               },
               lambda player: ({
                   RegionNames.Lumbridge:
                       lambda state: (state.has(ItemNames.Lumbridge, player)),
                   RegionNames.HAM_Hideout:
                       lambda state: (state.has(ItemNames.HAM_Hideout, player)),
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True
               })
               ),
    RegionInfo(RegionNames.Lumbridge_Farms,
               [
                   LocationNames.Q_Sheep_Shearer,
                   LocationNames.QP_Sheep_Shearer
               ],
               {
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Lumbridge}": RegionNames.Lumbridge,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.HAM_Hideout}": RegionNames.HAM_Hideout,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Draynor_Village}": RegionNames.Draynor_Village,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.South_Of_Varrock}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Egg}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Sheep}": RegionNames.Sheep,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Milk}": RegionNames.Milk,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Windmill}": RegionNames.Windmill,
                   f"{RegionNames.Lumbridge_Farms}->{RegionNames.Imp}": RegionNames.Imp,
               },
               lambda player: ({
                   RegionNames.Lumbridge:
                       lambda state: (state.has(ItemNames.Lumbridge, player)),
                   RegionNames.HAM_Hideout:
                       lambda state: (state.has(ItemNames.HAM_Hideout, player)),
                   RegionNames.Draynor_Village:
                       lambda state: (state.has(ItemNames.Draynor_Village, player)),
                   RegionNames.South_Of_Varrock:
                       lambda state: (state.has(ItemNames.South_Of_Varrock, player)),
                   RegionNames.Egg:
                       lambda state: True,
                   RegionNames.Sheep:
                       lambda state: True,
                   RegionNames.Milk:
                       lambda state: True,
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Windmill:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.HAM_Hideout,
               [],
               {
                   f"{RegionNames.HAM_Hideout}->{RegionNames.Lumbridge}": RegionNames.Lumbridge,
                   f"{RegionNames.HAM_Hideout}->{RegionNames.Lumbridge_Swamp}": RegionNames.Lumbridge_Swamp,
                   f"{RegionNames.HAM_Hideout}->{RegionNames.Lumbridge_Farms}": RegionNames.Lumbridge_Farms,
                   f"{RegionNames.HAM_Hideout}->{RegionNames.Draynor_Village}": RegionNames.Draynor_Village,
               },
               lambda player: ({
                   RegionNames.Lumbridge:
                       lambda state: (state.has(ItemNames.Lumbridge, player)),
                   RegionNames.Lumbridge_Swamp:
                       lambda state: (state.has(ItemNames.Lumbridge_Swamp, player)),
                   RegionNames.Lumbridge_Farms:
                       lambda state: (state.has(ItemNames.Lumbridge_Farms, player)),
                   RegionNames.Draynor_Village:
                       lambda state: (state.has(ItemNames.Draynor_Village, player)),
               })
               ),
    RegionInfo(RegionNames.Draynor_Village,
               [
                   LocationNames.Q_Vampyre_Slayer,
                   LocationNames.QP_Vampyre_Slayer,
               ],
               {
                   f"{RegionNames.Draynor_Village}->{RegionNames.Lumbridge_Farms}": RegionNames.Lumbridge_Farms,
                   f"{RegionNames.Draynor_Village}->{RegionNames.HAM_Hideout}": RegionNames.HAM_Hideout,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Wizards_Tower}": RegionNames.Wizards_Tower,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Draynor_Manor}": RegionNames.Draynor_Manor,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Falador_Farm}": RegionNames.Falador_Farm,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Draynor_Village}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Lumbridge_Farms:
                       lambda state: (state.has(ItemNames.Lumbridge_Farms, player)),
                   RegionNames.HAM_Hideout:
                       lambda state: (state.has(ItemNames.HAM_Hideout, player)),
                   RegionNames.Wizards_Tower:
                       lambda state: (state.has(ItemNames.Wizards_Tower, player)),
                   RegionNames.Draynor_Manor:
                       lambda state: (state.has(ItemNames.Draynor_Manor, player)),
                   RegionNames.Falador_Farm:
                       lambda state: (state.has(ItemNames.Falador_Farm, player)),
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Draynor_Manor,
               [
                   LocationNames.Q_Ernest_the_Chicken,
                   LocationNames.QP_Ernest_the_Chicken
               ],
               {
                   f"{RegionNames.Draynor_Manor}->{RegionNames.Draynor_Village}": RegionNames.Draynor_Village,
                   f"{RegionNames.Draynor_Manor}->{RegionNames.Barbarian_Village}": RegionNames.Barbarian_Village,
               },
               lambda player: ({
                   RegionNames.Draynor_Village:
                       lambda state: (state.has(ItemNames.Draynor_Village, player)),
                   RegionNames.Barbarian_Village:
                       lambda state: (state.has(ItemNames.Barbarian_Village, player)),
               })
               ),
    RegionInfo(RegionNames.Wizards_Tower,
               [
                   LocationNames.Q_Imp_Catcher,
                   LocationNames.QP_Imp_Catcher
               ],
               {
                   f"{RegionNames.Wizards_Tower}->{RegionNames.Draynor_Village}": RegionNames.Draynor_Village,
               },
               lambda player: ({
                   RegionNames.Draynor_Village:
                       lambda state: (state.has(ItemNames.Draynor_Village, player)),
               })
               ),
    RegionInfo(RegionNames.Al_Kharid,
               [
                   LocationNames.Q_Prince_Ali_Rescue,
                   LocationNames.QP_Prince_Ali_Rescue
               ],
               {
                   f"{RegionNames.Al_Kharid}->{RegionNames.Lumbridge}": RegionNames.Lumbridge,
                   f"{RegionNames.Al_Kharid}->{RegionNames.South_Of_Varrock}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Citharede_Abbey}": RegionNames.Citharede_Abbey,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Silver_Rock}": RegionNames.Silver_Rock,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
                   f"{RegionNames.Al_Kharid}->{RegionNames.Furnace}": RegionNames.Furnace,
               },
               lambda player: ({
                   RegionNames.Lumbridge:
                       lambda state: (state.has(ItemNames.Lumbridge, player)),
                   RegionNames.South_Of_Varrock:
                       lambda state: (state.has(ItemNames.South_Of_Varrock, player)),
                   RegionNames.Citharede_Abbey:
                       lambda state: (state.has(ItemNames.Citharede_Abbey, player)),
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Silver_Rock:
                       lambda state: True,
                   RegionNames.Gold_Rock:
                       lambda state: True,
                   RegionNames.Furnace:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Citharede_Abbey,
               [],
               {
                   f"{RegionNames.Citharede_Abbey}->{RegionNames.Al_Kharid}": RegionNames.Al_Kharid,
                   f"{RegionNames.Citharede_Abbey}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Citharede_Abbey}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Citharede_Abbey}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Al_Kharid:
                       lambda state: (state.has(ItemNames.Al_Kharid, player)),
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Anvil:
                       lambda state: True
               })
               ),
    RegionInfo(RegionNames.South_Of_Varrock,
               [],
               {
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Al_Kharid}": RegionNames.Al_Kharid,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Central_Varrock}": RegionNames.Central_Varrock,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.East_Of_Varrock}": RegionNames.East_Of_Varrock,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.West_Varrock}": RegionNames.West_Varrock,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Sheep}": RegionNames.Sheep,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Clay_Rock}": RegionNames.Clay_Rock,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.South_Of_Varrock}->{RegionNames.Silver_Rock}": RegionNames.Silver_Rock,
               },
               lambda player: ({
                   RegionNames.Al_Kharid:
                       lambda state: (state.has(ItemNames.Al_Kharid, player)),
                   RegionNames.Central_Varrock:
                       lambda state: (state.has(ItemNames.Central_Varrock, player)),
                   RegionNames.East_Of_Varrock:
                       lambda state: (state.has(ItemNames.East_Of_Varrock, player)),
                   RegionNames.West_Varrock:
                       lambda state: (state.has(ItemNames.West_Varrock, player)),
                   RegionNames.Sheep:
                       lambda state: True,
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Clay_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Silver_Rock:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Central_Varrock,
               [
                   LocationNames.Q_Demon_Slayer,
                   LocationNames.Q_Romeo_Juliet,
                   LocationNames.QP_Demon_Slayer,
                   LocationNames.QP_Romeo_Juliet
               ],
               {
                   f"{RegionNames.Central_Varrock}->{RegionNames.South_Of_Varrock}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.Central_Varrock}->{RegionNames.East_Of_Varrock}": RegionNames.East_Of_Varrock,
                   f"{RegionNames.Central_Varrock}->{RegionNames.West_Varrock}": RegionNames.West_Varrock,
                   f"{RegionNames.Central_Varrock}->{RegionNames.Varrock_Palace}": RegionNames.Varrock_Palace,
                   f"{RegionNames.Central_Varrock}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Central_Varrock}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.South_Of_Varrock:
                       lambda state: (state.has(ItemNames.South_Of_Varrock, player)),
                   RegionNames.East_Of_Varrock:
                       lambda state: (state.has(ItemNames.East_Of_Varrock, player)),
                   RegionNames.West_Varrock:
                       lambda state: (state.has(ItemNames.West_Varrock, player)),
                   RegionNames.Varrock_Palace:
                       lambda state: (state.has(ItemNames.Varrock_Palace, player)),
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Varrock_Palace,
               [
                   LocationNames.Q_Shield_of_Arrav,
                   LocationNames.QP_Shield_of_Arrav,
               ],
               {
                   f"{RegionNames.Varrock_Palace}->{RegionNames.East_Of_Varrock}": RegionNames.East_Of_Varrock,
                   f"{RegionNames.Varrock_Palace}->{RegionNames.Wilderness}": RegionNames.Wilderness,
               },
               lambda player: ({
                   RegionNames.East_Of_Varrock:
                       lambda state: (state.has(ItemNames.East_Of_Varrock, player)),
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
               })
               ),
    RegionInfo(RegionNames.East_Of_Varrock,
               [],
               {
                   f"{RegionNames.East_Of_Varrock}->{RegionNames.Central_Varrock}": RegionNames.Central_Varrock,
                   f"{RegionNames.East_Of_Varrock}->{RegionNames.Varrock_Palace}": RegionNames.Varrock_Palace,
                   f"{RegionNames.East_Of_Varrock}->{RegionNames.South_Of_Varrock}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.East_Of_Varrock}->{RegionNames.Wilderness}": RegionNames.Wilderness,
               },
               lambda player: ({
                   RegionNames.Central_Varrock:
                       lambda state: (state.has(ItemNames.Central_Varrock, player)),
                   RegionNames.Varrock_Palace:
                       lambda state: (state.has(ItemNames.Varrock_Palace, player)),
                   RegionNames.South_Of_Varrock:
                       lambda state: (state.has(ItemNames.South_Of_Varrock, player)),
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
               })
               ),
    RegionInfo(RegionNames.West_Varrock,
               [
                   LocationNames.Bake_Apple_Pie
               ],
               {
                   f"{RegionNames.West_Varrock}->{RegionNames.Central_Varrock}": RegionNames.Central_Varrock,
                   f"{RegionNames.West_Varrock}->{RegionNames.Varrock_Palace}": RegionNames.Varrock_Palace,
                   f"{RegionNames.West_Varrock}->{RegionNames.Edgeville}": RegionNames.Edgeville,
                   f"{RegionNames.West_Varrock}->{RegionNames.Barbarian_Village}": RegionNames.Barbarian_Village,
                   f"{RegionNames.West_Varrock}->{RegionNames.Wilderness}": RegionNames.Wilderness,
                   f"{RegionNames.West_Varrock}->{RegionNames.South_Of_Varrock}": RegionNames.South_Of_Varrock,
                   f"{RegionNames.West_Varrock}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.West_Varrock}->{RegionNames.Windmill}": RegionNames.Windmill,
                   f"{RegionNames.West_Varrock}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Central_Varrock:
                       lambda state: (state.has(ItemNames.Central_Varrock, player)),
                   RegionNames.Varrock_Palace:
                       lambda state: (state.has(ItemNames.Varrock_Palace, player)),
                   RegionNames.Edgeville:
                       lambda state: (state.has(ItemNames.Edgeville, player)),
                   RegionNames.Barbarian_Village:
                       lambda state: (state.has(ItemNames.Barbarian_Village, player)),
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
                   RegionNames.South_Of_Varrock:
                       lambda state: (state.has(ItemNames.South_Of_Varrock, player)),
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Windmill:
                       lambda state: state.can_reach(RegionNames.East_Of_Varrock, None, player) or state.can_reach(
                           RegionNames.Imp, None, player),
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Edgeville,
               [
               ],
               {
                   f"{RegionNames.Edgeville}->{RegionNames.Wilderness}": RegionNames.Wilderness,
                   f"{RegionNames.Edgeville}->{RegionNames.West_Varrock}": RegionNames.West_Varrock,
                   f"{RegionNames.Edgeville}->{RegionNames.Monastery}": RegionNames.Monastery,
                   f"{RegionNames.Edgeville}->{RegionNames.Barbarian_Village}": RegionNames.Barbarian_Village,
                   f"{RegionNames.Edgeville}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Edgeville}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.Edgeville}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Edgeville}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Edgeville}->{RegionNames.Furnace}": RegionNames.Furnace,
               },
               lambda player: ({
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
                   RegionNames.West_Varrock:
                       lambda state: (state.has(ItemNames.West_Varrock, player)),
                   RegionNames.Monastery:
                       lambda state: (state.has(ItemNames.Monastery, player)),
                   RegionNames.Barbarian_Village:
                       lambda state: (state.has(ItemNames.Barbarian_Village, player)),
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Furnace:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Barbarian_Village,
               [
               ],
               {
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Edgeville}": RegionNames.Edgeville,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.West_Varrock}": RegionNames.West_Varrock,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Draynor_Manor}": RegionNames.Draynor_Manor,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Dwarven_Mines}": RegionNames.Dwarven_Mines,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Spinning_Wheel}": RegionNames.Spinning_Wheel,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Barbarian_Village}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Edgeville:
                       lambda state: (state.has(ItemNames.Edgeville, player)),
                   RegionNames.West_Varrock:
                       lambda state: (state.has(ItemNames.West_Varrock, player)),
                   RegionNames.Draynor_Manor:
                       lambda state: (state.has(ItemNames.Draynor_Manor, player)),
                   RegionNames.Dwarven_Mines:
                       lambda state: (state.has(ItemNames.Dwarven_Mines, player)),
                   RegionNames.Spinning_Wheel:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Monastery,
               [
               ],
               {
                   f"{RegionNames.Monastery}->{RegionNames.Edgeville}": RegionNames.Edgeville,
                   f"{RegionNames.Monastery}->{RegionNames.Dwarven_Mines}": RegionNames.Dwarven_Mines,
                   f"{RegionNames.Monastery}->{RegionNames.Ice_Mountain}": RegionNames.Ice_Mountain,
                   f"{RegionNames.Monastery}->{RegionNames.Wilderness}": RegionNames.Wilderness,
                   f"{RegionNames.Monastery}->{RegionNames.Sheep}": RegionNames.Sheep,
               },
               lambda player: ({
                   RegionNames.Edgeville:
                       lambda state: (state.has(ItemNames.Edgeville, player)),
                   RegionNames.Dwarven_Mines:
                       lambda state: (state.has(ItemNames.Dwarven_Mines, player)),
                   RegionNames.Ice_Mountain:
                       lambda state: (state.has(ItemNames.Ice_Mountain, player)),
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
                   RegionNames.Sheep:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Ice_Mountain,
               [
                   LocationNames.Q_Goblin_Diplomacy,
                   LocationNames.Guppy,
                   LocationNames.Cavefish,
                   LocationNames.Tetra,
                   LocationNames.Barronite_Deposit,
                   LocationNames.QP_Goblin_Diplomacy
               ],
               {
                   f"{RegionNames.Ice_Mountain}->{RegionNames.Wilderness}": RegionNames.Wilderness,
                   f"{RegionNames.Ice_Mountain}->{RegionNames.Monastery}": RegionNames.Monastery,
                   f"{RegionNames.Ice_Mountain}->{RegionNames.Dwarven_Mines}": RegionNames.Dwarven_Mines,
               },
               lambda player: ({
                   RegionNames.Wilderness:
                       lambda state: (state.has(ItemNames.Wilderness, player)),
                   RegionNames.Monastery:
                       lambda state: (state.has(ItemNames.Monastery, player)),
                   RegionNames.Dwarven_Mines:
                       lambda state: (state.has(ItemNames.Dwarven_Mines, player)),
               })
               ),
    RegionInfo(RegionNames.Dwarven_Mines,
               [
                   LocationNames.Q_Below_Ice_Mountain,
                   LocationNames.Q_Dorics_Quest,
                   LocationNames.QP_Below_Ice_Mountain,
                   LocationNames.QP_Dorics_Quest,
               ],
               {
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Barbarian_Village}": RegionNames.Barbarian_Village,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Monastery}": RegionNames.Monastery,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Ice_Mountain}": RegionNames.Ice_Mountain,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Falador}": RegionNames.Falador,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Clay_Rock}": RegionNames.Clay_Rock,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Dwarven_Mines}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
               },
               lambda player: ({
                   RegionNames.Barbarian_Village:
                       lambda state: (state.has(ItemNames.Barbarian_Village, player)),
                   RegionNames.Monastery:
                       lambda state: (state.has(ItemNames.Monastery, player)),
                   RegionNames.Ice_Mountain:
                       lambda state: (state.has(ItemNames.Ice_Mountain, player)),
                   RegionNames.Falador:
                       lambda state: (state.has(ItemNames.Falador, player)),
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Clay_Rock:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Gold_Rock:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Falador,
               [
                   LocationNames.Q_Knights_Sword,
                   LocationNames.Q_Black_Knights_Fortress,
                   LocationNames.QP_Knights_Sword,
                   LocationNames.QP_Black_Knights_Fortress,
               ],
               {
                   f"{RegionNames.Falador}->{RegionNames.Dwarven_Mines}": RegionNames.Dwarven_Mines,
                   f"{RegionNames.Falador}->{RegionNames.Falador_Farm}": RegionNames.Falador_Farm,
                   f"{RegionNames.Falador}->{RegionNames.Spinning_Wheel}": RegionNames.Spinning_Wheel,
                   f"{RegionNames.Falador}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Falador}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Falador}->{RegionNames.Furnace}": RegionNames.Furnace,
               },
               lambda player: ({
                   RegionNames.Dwarven_Mines:
                       lambda state: (state.has(ItemNames.Dwarven_Mines, player)),
                   RegionNames.Falador_Farm:
                       lambda state: (state.has(ItemNames.Falador_Farm, player)),
                   RegionNames.Spinning_Wheel:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Furnace:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Falador_Farm,
               [
                   LocationNames.Q_Corsair_Curse,
                   LocationNames.QP_Corsair_Curse
               ],
               {
                   f"{RegionNames.Falador_Farm}->{RegionNames.Crafting_Guild}": RegionNames.Crafting_Guild,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Draynor_Village}": RegionNames.Draynor_Village,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Rimmington}": RegionNames.Rimmington,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Port_Sarim}": RegionNames.Port_Sarim,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Egg}": RegionNames.Egg,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Milk}": RegionNames.Milk,
                   f"{RegionNames.Falador_Farm}->{RegionNames.Imp}": RegionNames.Imp,
               },
               lambda player: ({
                   RegionNames.Crafting_Guild:
                       lambda state: (state.has(ItemNames.Crafting_Guild, player)),
                   RegionNames.Draynor_Village:
                       lambda state: (state.has(ItemNames.Draynor_Village, player)),
                   RegionNames.Rimmington:
                       lambda state: (state.has(ItemNames.Rimmington, player)),
                   RegionNames.Port_Sarim:
                       lambda state: (state.has(ItemNames.Port_Sarim, player)),
                   RegionNames.Egg:
                       lambda state: True,
                   RegionNames.Milk:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Crafting_Guild,
               [],
               {
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Falador_Farm}": RegionNames.Falador_Farm,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Rimmington}": RegionNames.Rimmington,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Sheep}": RegionNames.Sheep,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Milk}": RegionNames.Milk,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Spinning_Wheel}": RegionNames.Spinning_Wheel,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Clay_Rock}": RegionNames.Clay_Rock,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Silver_Rock}": RegionNames.Silver_Rock,
                   f"{RegionNames.Crafting_Guild}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
               },
               lambda player: ({
                   RegionNames.Falador_Farm:
                       lambda state: (state.has(ItemNames.Falador_Farm, player)),
                   RegionNames.Rimmington:
                       lambda state: (state.has(ItemNames.Rimmington, player)),
                   RegionNames.Sheep:
                       lambda state: True,
                   RegionNames.Milk:
                       lambda state: state.can_reach(RegionNames.West_Varrock, None, player) or state.can_reach(
                           RegionNames.Central_Varrock, None, player),
                   RegionNames.Spinning_Wheel:
                       lambda state: state.can_reach(RegionNames.West_Varrock, None, player) or state.can_reach(
                           RegionNames.Central_Varrock, None, player),
                   RegionNames.Clay_Rock:
                       lambda state: state.can_reach(RegionNames.West_Varrock, None, player) or state.can_reach(
                           RegionNames.Central_Varrock, None, player),
                   RegionNames.Silver_Rock:
                       lambda state: state.can_reach(RegionNames.West_Varrock, None, player) or state.can_reach(
                           RegionNames.Central_Varrock, None, player),
                   RegionNames.Gold_Rock:
                       lambda state: state.can_reach(RegionNames.West_Varrock, None, player) or state.can_reach(
                           RegionNames.Central_Varrock, None, player),
               })
               ),
    RegionInfo(RegionNames.Rimmington,
               [
                   LocationNames.Q_Witchs_Potion,
                   LocationNames.QP_Witchs_Potion
               ],
               {
                   f"{RegionNames.Rimmington}->{RegionNames.Crafting_Guild}": RegionNames.Crafting_Guild,
                   f"{RegionNames.Rimmington}->{RegionNames.Falador_Farm}": RegionNames.Falador_Farm,
                   f"{RegionNames.Rimmington}->{RegionNames.Port_Sarim}": RegionNames.Port_Sarim,
                   f"{RegionNames.Rimmington}->{RegionNames.Mudskipper_Point}": RegionNames.Mudskipper_Point,
                   f"{RegionNames.Rimmington}->{RegionNames.Corsair_Cove}": RegionNames.Corsair_Cove,
                   f"{RegionNames.Rimmington}->{RegionNames.Wheat}": RegionNames.Wheat,
                   f"{RegionNames.Rimmington}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Rimmington}->{RegionNames.Bronze_Ores}": RegionNames.Bronze_Ores,
                   f"{RegionNames.Rimmington}->{RegionNames.Clay_Rock}": RegionNames.Clay_Rock,
                   f"{RegionNames.Rimmington}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Rimmington}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
               },
               lambda player: ({
                   RegionNames.Crafting_Guild:
                       lambda state: (state.has(ItemNames.Crafting_Guild, player)),
                   RegionNames.Falador_Farm:
                       lambda state: (state.has(ItemNames.Falador_Farm, player)),
                   RegionNames.Port_Sarim:
                       lambda state: (state.has(ItemNames.Port_Sarim, player)),
                   RegionNames.Mudskipper_Point:
                       lambda state: (state.has(ItemNames.Mudskipper_Point, player)),
                   RegionNames.Corsair_Cove:
                       lambda state: (state.has(ItemNames.Corsair_Cove, player)),
                   RegionNames.Wheat:
                       lambda state: True,
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Bronze_Ores:
                       lambda state: True,
                   RegionNames.Clay_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Gold_Rock:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Port_Sarim,
               [
                   LocationNames.Q_Pirates_Treasure,
                   LocationNames.QP_Pirates_Treasure
               ],
               {
                   f"{RegionNames.Port_Sarim}->{RegionNames.Falador_Farm}": RegionNames.Falador_Farm,
                   f"{RegionNames.Port_Sarim}->{RegionNames.Rimmington}": RegionNames.Rimmington,
                   f"{RegionNames.Port_Sarim}->{RegionNames.Mudskipper_Point}": RegionNames.Mudskipper_Point,
                   f"{RegionNames.Port_Sarim}->{RegionNames.Crandor}": RegionNames.Crandor,
               },
               lambda player: ({
                   RegionNames.Falador_Farm:
                       lambda state: (state.has(ItemNames.Falador_Farm, player)),
                   RegionNames.Rimmington:
                       lambda state: (state.has(ItemNames.Rimmington, player)),
                   RegionNames.Mudskipper_Point:
                       lambda state: (state.has(ItemNames.Mudskipper_Point, player)),
                   RegionNames.Crandor:
                       lambda state: (state.has(ItemNames.Crandor, player) and
                                      state.can_reach(RegionNames.South_Of_Varrock, None, player) and
                                      state.can_reach(RegionNames.Edgeville, None, player) and
                                      state.can_reach(RegionNames.Lumbridge, None, player) and
                                      state.can_reach(RegionNames.Rimmington, None, player) and
                                      state.can_reach(RegionNames.Monastery, None, player) and
                                      (state.can_reach(RegionNames.Dwarven_Mines, None,
                                                       player) or state.can_reach(
                                          RegionNames.Falador, None, player)) and
                                      state.can_reach(RegionNames.Port_Sarim, None, player) and
                                      state.can_reach(RegionNames.Draynor_Village, None, player))

               }),
               ),
    RegionInfo(RegionNames.Mudskipper_Point,
               [],
               {
                   f"{RegionNames.Mudskipper_Point}->{RegionNames.Port_Sarim}": RegionNames.Port_Sarim,
                   f"{RegionNames.Mudskipper_Point}->{RegionNames.Rimmington}": RegionNames.Rimmington,
                   f"{RegionNames.Mudskipper_Point}->{RegionNames.Karamja}": RegionNames.Karamja,
                   f"{RegionNames.Mudskipper_Point}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Port_Sarim:
                       lambda state: (state.has(ItemNames.Port_Sarim, player)),
                   RegionNames.Rimmington:
                       lambda state: (state.has(ItemNames.Rimmington, player)),
                   RegionNames.Karamja:
                       lambda state: (state.has(ItemNames.Karamja, player) and state.can_reach(RegionNames.Port_Sarim,
                                                                                               None, player)),
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Karamja,
               [],
               {
                   f"{RegionNames.Karamja}->{RegionNames.Mudskipper_Point}": RegionNames.Mudskipper_Point,
                   f"{RegionNames.Karamja}->{RegionNames.Imp}": RegionNames.Imp,
                   f"{RegionNames.Karamja}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
               },
               lambda player: ({
                   RegionNames.Mudskipper_Point:
                       lambda state: (state.has(ItemNames.Mudskipper_Point, player)),
                   RegionNames.Imp:
                       lambda state: True,
                   RegionNames.Gold_Rock:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Corsair_Cove,
               [
                   LocationNames.K_Ogress_Shaman,
               ],
               {
                   f"{RegionNames.Corsair_Cove}->{RegionNames.Port_Sarim}": RegionNames.Port_Sarim,
                   f"{RegionNames.Corsair_Cove}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Port_Sarim:
                       lambda state: (state.has(ItemNames.Port_Sarim, player)),
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Wilderness,
               [],
               {
                   f"{RegionNames.Wilderness}->{RegionNames.Ice_Mountain}": RegionNames.Ice_Mountain,
                   f"{RegionNames.Wilderness}->{RegionNames.Monastery}": RegionNames.Monastery,
                   f"{RegionNames.Wilderness}->{RegionNames.Edgeville}": RegionNames.Edgeville,
                   f"{RegionNames.Wilderness}->{RegionNames.West_Varrock}": RegionNames.West_Varrock,
                   f"{RegionNames.Wilderness}->{RegionNames.Varrock_Palace}": RegionNames.Varrock_Palace,
                   f"{RegionNames.Wilderness}->{RegionNames.East_Of_Varrock}": RegionNames.East_Of_Varrock,
                   f"{RegionNames.Wilderness}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Wilderness}->{RegionNames.Iron_Rock}": RegionNames.Iron_Rock,
                   f"{RegionNames.Wilderness}->{RegionNames.Furnace}": RegionNames.Furnace,
                   f"{RegionNames.Wilderness}->{RegionNames.Anvil}": RegionNames.Anvil,
               },
               lambda player: ({
                   RegionNames.Ice_Mountain:
                       lambda state: (state.has(ItemNames.Ice_Mountain, player)),
                   RegionNames.Monastery:
                       lambda state: (state.has(ItemNames.Monastery, player)),
                   RegionNames.Edgeville:
                       lambda state: (state.has(ItemNames.Edgeville, player)),
                   RegionNames.West_Varrock:
                       lambda state: (state.has(ItemNames.West_Varrock, player)),
                   RegionNames.Varrock_Palace:
                       lambda state: (state.has(ItemNames.Varrock_Palace, player)),
                   RegionNames.East_Of_Varrock:
                       lambda state: (state.has(ItemNames.East_Of_Varrock, player)),
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Iron_Rock:
                       lambda state: True,
                   RegionNames.Furnace:
                       lambda state: True,
                   RegionNames.Anvil:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Crandor,
               [
                   LocationNames.Q_Dragon_Slayer
               ],
               {
                   f"{RegionNames.Crandor}->{RegionNames.Karamja}": RegionNames.Karamja,
                   f"{RegionNames.Crandor}->{RegionNames.Port_Sarim}": RegionNames.Port_Sarim,
                   f"{RegionNames.Crandor}->{RegionNames.Coal_Rock}": RegionNames.Coal_Rock,
                   f"{RegionNames.Crandor}->{RegionNames.Gold_Rock}": RegionNames.Gold_Rock,
               },
               lambda player: ({
                   RegionNames.Karamja:
                       lambda state: (state.has(ItemNames.Karamja, player)),
                   RegionNames.Coal_Rock:
                       lambda state: True,
                   RegionNames.Gold_Rock:
                       lambda state: True,
               })
               ),
    RegionInfo(RegionNames.Egg, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Sheep, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Milk, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Wheat, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Windmill, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Spinning_Wheel, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Imp, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Bronze_Ores, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Clay_Rock, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Coal_Rock, [
        LocationNames.Mine_Coal
    ], {}, lambda player: {}),
    RegionInfo(RegionNames.Iron_Rock, [
        LocationNames.Smelt_Steel
    ], {}, lambda player: {}),
    RegionInfo(RegionNames.Silver_Rock,
               [
                   LocationNames.Mine_Silver,
                   LocationNames.Smelt_Silver
               ], {}, lambda player: {}),
    RegionInfo(RegionNames.Gold_Rock, [
        LocationNames.Mine_Gold,
        LocationNames.Smelt_Gold
    ], {}, lambda player: {}),
    RegionInfo(RegionNames.Furnace, [], {}, lambda player: {}),
    RegionInfo(RegionNames.Anvil, [], {}, lambda player: {})
]
