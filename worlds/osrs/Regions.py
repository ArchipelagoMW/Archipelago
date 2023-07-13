import typing

from BaseClasses import CollectionState
from .Locations import LocationNames
from .Items import ItemNames
from .Names import RegionNames


class RegionInfo(typing.NamedTuple):
    name: str
    access_rule: typing.Callable[[int], typing.Callable[[CollectionState], bool]]
    connects_to: typing.List[str]
    resources: typing.List[str]
    locations: typing.List[str]
    extra_conditions: typing.Optional[
        typing.Callable[[int], typing.Dict[str, typing.Callable[[CollectionState], bool]]]] = lambda _: {}

    def build_exits_dict(self) -> typing.Dict[str, str]:
        exits_dict = {}
        for region in self.connects_to:
            exits_dict[region] = f"{self.name}->{region}"
        for resource in self.resources:
            exits_dict[resource] = f"{self.name}->{resource}"
        return exits_dict

    def build_extra_condition(self, player, region):
        condition_dict = self.extra_conditions(player)
        if region in condition_dict:
            return condition_dict[region]
        else:
            return lambda _: True


all_regions = [
    RegionInfo("Menu",
               lambda _: lambda _: True,
               [],
               [],
               [
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
                   LocationNames.Total_Level_150,
                   LocationNames.Total_Level_200,
                   LocationNames.Combat_Level_5,
                   LocationNames.Combat_Level_15,
                   LocationNames.Combat_Level_25,
               ],
               ),

    RegionInfo(RegionNames.Lumbridge,
               lambda player: lambda state: state.has(ItemNames.Lumbridge, player),
               [
                   RegionNames.Lumbridge_Swamp,
                   RegionNames.Lumbridge_Farms,
                   RegionNames.HAM_Hideout,
                   RegionNames.Al_Kharid,
                   # Canoe
                   RegionNames.South_Of_Varrock,
                   RegionNames.Barbarian_Village,
                   RegionNames.Edgeville
               ],
               [
                   RegionNames.Spinning_Wheel,
                   RegionNames.Imp,
                   RegionNames.Oak_Tree,
                   RegionNames.Willow_Tree,
                   RegionNames.Fly_Fish
               ],
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
               ),
    RegionInfo(RegionNames.Lumbridge_Swamp,
               lambda player: lambda state: state.has(ItemNames.Lumbridge_Swamp, player),
               [
                   RegionNames.Lumbridge,
                   RegionNames.HAM_Hideout
               ],
               [
                   RegionNames.Bronze_Ores,
                   RegionNames.Coal_Rock,
                   RegionNames.Shrimp
               ],
               [
                   LocationNames.Q_Misthalin_Mystery,
                   LocationNames.QP_Misthalin_Mystery,
               ],
               ),
    RegionInfo(RegionNames.Lumbridge_Farms,
               lambda player: lambda state: state.has(ItemNames.Lumbridge_Farms, player),
               [
                   RegionNames.Lumbridge,
                   RegionNames.HAM_Hideout,
                   RegionNames.Draynor_Village,
                   RegionNames.South_Of_Varrock
               ],
               [
                   RegionNames.Egg,
                   RegionNames.Sheep,
                   RegionNames.Milk,
                   RegionNames.Wheat,
                   RegionNames.Windmill,
                   RegionNames.Imp,
                   RegionNames.Willow_Tree
               ],
               [
                   LocationNames.Q_Sheep_Shearer,
                   LocationNames.QP_Sheep_Shearer
               ],
               ),
    RegionInfo(RegionNames.HAM_Hideout,
               lambda player: lambda state: state.has(ItemNames.HAM_Hideout, player),
               [
                   RegionNames.Lumbridge,
                   RegionNames.Lumbridge_Swamp,
                   RegionNames.Lumbridge_Farms,
                   RegionNames.Draynor_Village
               ],
               [],
               [],
               ),
    RegionInfo(RegionNames.Draynor_Village,
               lambda player: lambda state: state.has(ItemNames.Draynor_Village, player),
               [
                   RegionNames.Lumbridge_Farms,
                   RegionNames.HAM_Hideout,
                   RegionNames.Wizards_Tower,
                   RegionNames.Draynor_Manor,
                   RegionNames.Falador_Farm
               ],
               [
                   RegionNames.Wheat,
                   RegionNames.Imp,
                   RegionNames.Anvil,
                   RegionNames.Oak_Tree,
                   RegionNames.Willow_Tree,
                   RegionNames.Shrimp
               ],
               [
                   LocationNames.Q_Vampyre_Slayer,
                   LocationNames.QP_Vampyre_Slayer,
               ],
               ),
    RegionInfo(RegionNames.Draynor_Manor,
               lambda player: lambda state: state.has(ItemNames.Draynor_Manor, player),
               [
                   RegionNames.Draynor_Village,
                   RegionNames.Barbarian_Village,
               ],
               [],
               [
                   LocationNames.Q_Ernest_the_Chicken,
                   LocationNames.QP_Ernest_the_Chicken
               ],
               ),
    RegionInfo(RegionNames.Wizards_Tower,
               lambda player: lambda state: state.has(ItemNames.Wizards_Tower, player),
               [
                   RegionNames.Draynor_Village
               ],
               [],
               [
                   LocationNames.Q_Imp_Catcher,
                   LocationNames.QP_Imp_Catcher
               ],
               ),
    RegionInfo(RegionNames.Al_Kharid,
               lambda player: lambda state: state.has(ItemNames.Al_Kharid, player),
               [
                   RegionNames.Lumbridge,
                   RegionNames.South_Of_Varrock,
                   RegionNames.Citharede_Abbey
               ],
               [
                   RegionNames.Imp,
                   RegionNames.Bronze_Ores,
                   RegionNames.Coal_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Silver_Rock,
                   RegionNames.Gold_Rock,
                   RegionNames.Furnace,
                   RegionNames.Shrimp
               ],
               [
                   LocationNames.Q_Prince_Ali_Rescue,
                   LocationNames.QP_Prince_Ali_Rescue
               ],
               ),
    RegionInfo(RegionNames.Citharede_Abbey,
               lambda player: lambda state: state.has(ItemNames.Citharede_Abbey, player),
               [
                   RegionNames.Al_Kharid
               ],
               [
                   RegionNames.Coal_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Anvil
               ],
               [],
               ),
    RegionInfo(RegionNames.South_Of_Varrock,
               lambda player: lambda state: state.has(ItemNames.South_Of_Varrock, player),
               [
                   RegionNames.Al_Kharid,
                   RegionNames.Central_Varrock,
                   RegionNames.East_Of_Varrock,
                   RegionNames.West_Varrock,
                   # Canoe
                   RegionNames.Lumbridge,
                   RegionNames.Barbarian_Village,
                   RegionNames.Edgeville
               ],
               [
                   RegionNames.Sheep,
                   RegionNames.Wheat,
                   RegionNames.Bronze_Ores,
                   RegionNames.Clay_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Silver_Rock,
                   RegionNames.Willow_Tree
               ],
               [],
               ),
    RegionInfo(RegionNames.Central_Varrock,
               lambda player: lambda state: state.has(ItemNames.Central_Varrock, player),
               [
                   RegionNames.South_Of_Varrock,
                   RegionNames.East_Of_Varrock,
                   RegionNames.West_Varrock,
                   RegionNames.Varrock_Palace
               ],
               [
                   RegionNames.Imp,
                   RegionNames.Anvil,
                   RegionNames.Oak_Tree
               ],
               [
                   LocationNames.Q_Demon_Slayer,
                   LocationNames.Q_Romeo_Juliet,
                   LocationNames.QP_Demon_Slayer,
                   LocationNames.QP_Romeo_Juliet
               ],
               ),
    RegionInfo(RegionNames.Varrock_Palace,
               lambda player: lambda state: state.has(ItemNames.Varrock_Palace, player),
               [
                   RegionNames.East_Of_Varrock,
                   RegionNames.Wilderness,
               ],
               [
                   RegionNames.Oak_Tree
               ],
               [
                   LocationNames.Q_Shield_of_Arrav,
                   LocationNames.QP_Shield_of_Arrav,
               ],
               ),
    RegionInfo(RegionNames.East_Of_Varrock,
               lambda player: lambda state: state.has(ItemNames.East_Of_Varrock, player),
               [
                   RegionNames.Central_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.South_Of_Varrock,
                   RegionNames.Wilderness
               ],
               [],
               [],
               ),
    RegionInfo(RegionNames.West_Varrock,
               lambda player: lambda state: state.has(ItemNames.West_Varrock, player),
               [
                   RegionNames.Central_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.Edgeville,
                   RegionNames.Barbarian_Village,
                   RegionNames.Wilderness,
                   RegionNames.South_Of_Varrock
               ],
               [
                   RegionNames.Wheat,
                   RegionNames.Windmill,
                   RegionNames.Anvil
               ],
               [
                   LocationNames.Bake_Apple_Pie
               ],
               lambda player: ({
                   RegionNames.Windmill:
                       lambda state: state.can_reach(RegionNames.Imp, None, player),
               })
               ),
    RegionInfo(RegionNames.Edgeville,
               lambda player: lambda state: state.has(ItemNames.Edgeville, player),
               [
                   RegionNames.Wilderness,
                   RegionNames.West_Varrock,
                   RegionNames.Monastery,
                   RegionNames.Barbarian_Village
               ],
               [
                   RegionNames.Imp,
                   RegionNames.Bronze_Ores,
                   RegionNames.Coal_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Furnace,
                   RegionNames.Willow_Tree
               ],
               [],
               ),
    RegionInfo(RegionNames.Barbarian_Village,
               lambda player: lambda state: state.has(ItemNames.Barbarian_Village, player),
               [
                   RegionNames.Edgeville,
                   RegionNames.West_Varrock,
                   RegionNames.Draynor_Manor,
                   RegionNames.Dwarven_Mines,
                   # Canoe
                   RegionNames.South_Of_Varrock,
                   RegionNames.Lumbridge
               ],
               [
                   RegionNames.Spinning_Wheel,
                   RegionNames.Coal_Rock,
                   RegionNames.Anvil,
                   RegionNames.Fly_Fish
               ],
               [],
               ),
    RegionInfo(RegionNames.Monastery,
               lambda player: lambda state: state.has(ItemNames.Monastery, player),
               [RegionNames.Edgeville,
                RegionNames.Dwarven_Mines,
                RegionNames.Ice_Mountain,
                RegionNames.Wilderness],
               [
                   RegionNames.Sheep
               ],
               [],

               ),
    RegionInfo(RegionNames.Ice_Mountain,
               lambda player: lambda state: state.has(ItemNames.Ice_Mountain, player),
               [
                   RegionNames.Wilderness,
                   RegionNames.Monastery,
                   RegionNames.Dwarven_Mines
               ],
               [],
               [
                   LocationNames.Q_Goblin_Diplomacy,
                   LocationNames.Guppy,
                   LocationNames.Cavefish,
                   LocationNames.Tetra,
                   LocationNames.Barronite_Deposit,
                   LocationNames.QP_Goblin_Diplomacy
               ],
               ),
    RegionInfo(RegionNames.Dwarven_Mines,
               lambda player: lambda state: state.has(ItemNames.Dwarven_Mines, player),
               [
                   RegionNames.Barbarian_Village,
                   RegionNames.Monastery,
                   RegionNames.Ice_Mountain,
                   RegionNames.Falador,
               ],
               [
                   RegionNames.Wheat,
                   RegionNames.Bronze_Ores,
                   RegionNames.Clay_Rock,
                   RegionNames.Coal_Rock,
                   RegionNames.Clay_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Gold_Rock,
                   RegionNames.Anvil
               ],
               [
                   LocationNames.Q_Below_Ice_Mountain,
                   LocationNames.Q_Dorics_Quest,
                   LocationNames.QP_Below_Ice_Mountain,
                   LocationNames.QP_Dorics_Quest,
               ],
               lambda player: ({
                   RegionNames.Bronze_Ores:
                       lambda state: state.can_reach(RegionNames.Monastery, None, player) or state.can_reach(
                           RegionNames.Ice_Mountain, None, player),
                   RegionNames.Clay_Rock:
                       lambda state: state.can_reach(RegionNames.Monastery, None, player) or state.can_reach(
                           RegionNames.Ice_Mountain, None, player),
                   RegionNames.Coal_Rock:
                       lambda state: state.can_reach(RegionNames.Monastery, None, player) or state.can_reach(
                           RegionNames.Ice_Mountain, None, player),
                   RegionNames.Iron_Rock:
                       lambda state: state.can_reach(RegionNames.Monastery, None, player) or state.can_reach(
                           RegionNames.Ice_Mountain, None, player),
                   RegionNames.Gold_Rock:
                       lambda state: state.can_reach(RegionNames.Monastery, None, player) or state.can_reach(
                           RegionNames.Ice_Mountain, None, player),
                   RegionNames.Anvil:
                       lambda state: state.has(ItemNames.QP_Dorics_Quest, None, player)
               })
               ),
    RegionInfo(RegionNames.Falador,
               lambda player: lambda state: state.has(ItemNames.Falador, player),
               [
                   RegionNames.Dwarven_Mines,
                   RegionNames.Falador_Farm
               ],
               [
                   RegionNames.Spinning_Wheel,
                   RegionNames.Imp,
                   RegionNames.Coal_Rock,
                   RegionNames.Furnace,
                   RegionNames.Oak_Tree
               ],
               [
                   LocationNames.Q_Knights_Sword,
                   LocationNames.Q_Black_Knights_Fortress,
                   LocationNames.QP_Knights_Sword,
                   LocationNames.QP_Black_Knights_Fortress,
               ],
               ),
    RegionInfo(RegionNames.Falador_Farm,
               lambda player: lambda state: state.has(ItemNames.Falador_Farm, player),
               [
                   RegionNames.Crafting_Guild,
                   RegionNames.Draynor_Village,
                   RegionNames.Rimmington,
                   RegionNames.Port_Sarim
               ],
               [
                   RegionNames.Egg,
                   RegionNames.Milk,
                   RegionNames.Imp,
                   RegionNames.Oak_Tree
               ],
               [
                   LocationNames.Q_Corsair_Curse,
                   LocationNames.QP_Corsair_Curse
               ],
               ),
    RegionInfo(RegionNames.Crafting_Guild,
               lambda player: lambda state: state.has(ItemNames.Crafting_Guild, player),
               [
                   RegionNames.Falador_Farm,
                   RegionNames.Rimmington
               ],
               [
                   RegionNames.Sheep,
                   RegionNames.Milk,
                   RegionNames.Spinning_Wheel,
                   RegionNames.Clay_Rock,
                   RegionNames.Silver_Rock,
                   RegionNames.Gold_Rock,
                   RegionNames.Willow_Tree
               ],
               [],
               lambda player: ({
                   # Crafting guild requires apron from varrock clothes store
                   RegionNames.Milk:
                       lambda state: state.can_reach(RegionNames.Central_Varrock, None, player),
                   RegionNames.Spinning_Wheel:
                       lambda state: state.can_reach(RegionNames.Central_Varrock, None, player),
                   RegionNames.Clay_Rock:
                       lambda state: state.can_reach(RegionNames.Central_Varrock, None, player),
                   RegionNames.Silver_Rock:
                       lambda state: state.can_reach(RegionNames.Central_Varrock, None, player),
                   RegionNames.Gold_Rock:
                       lambda state: state.can_reach(RegionNames.Central_Varrock, None, player)
               })
               ),
    RegionInfo(RegionNames.Rimmington,
               lambda player: lambda state: state.has(ItemNames.Rimmington, player),
               [
                   RegionNames.Crafting_Guild,
                   RegionNames.Falador_Farm,
                   RegionNames.Port_Sarim,
                   RegionNames.Mudskipper_Point,
                   RegionNames.Corsair_Cove
               ],
               [
                   RegionNames.Wheat,
                   RegionNames.Imp,
                   RegionNames.Bronze_Ores,
                   RegionNames.Clay_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Gold_Rock,
                   RegionNames.Willow_Tree,
                   RegionNames.Shrimp
               ],
               [
                   LocationNames.Q_Witchs_Potion,
                   LocationNames.QP_Witchs_Potion
               ]
               ),
    RegionInfo(RegionNames.Port_Sarim,
               lambda player: lambda state: state.has(ItemNames.Port_Sarim, player),
               [
                   RegionNames.Falador_Farm,
                   RegionNames.Rimmington,
                   RegionNames.Mudskipper_Point,
                   RegionNames.Crandor
               ],
               [
                   RegionNames.Oak_Tree,
                   RegionNames.Willow_Tree
               ],
               [
                   LocationNames.Q_Pirates_Treasure,
                   LocationNames.QP_Pirates_Treasure
               ],
               lambda player: ({
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
                                      state.can_reach(RegionNames.Draynor_Village, None, player)),
               }),
               ),
    RegionInfo(RegionNames.Mudskipper_Point,
               lambda player: lambda state: state.has(ItemNames.Mudskipper_Point, player),
               [
                   RegionNames.Port_Sarim,
                   RegionNames.Rimmington,
                   RegionNames.Karamja
               ],
               [
                   RegionNames.Anvil
               ],
               [],
               lambda player: ({
                   RegionNames.Karamja:
                       lambda state: state.has(ItemNames.Karamja, player) and
                                     state.can_reach(RegionNames.Port_Sarim, None, player)
               })
               ),
    RegionInfo(RegionNames.Karamja,
               lambda player: lambda state: state.has(ItemNames.Karamja, player),
               [
                   RegionNames.Mudskipper_Point
               ],
               [
                   RegionNames.Imp,
                   RegionNames.Gold_Rock,
                   RegionNames.Shrimp,
                   RegionNames.Lobster
               ],
               [],
               ),
    RegionInfo(RegionNames.Corsair_Cove,
               lambda player: lambda state: state.has(ItemNames.Corsair_Cove, player),
               [
                   RegionNames.Rimmington
               ],
               [
                   RegionNames.Anvil,
                   RegionNames.Shrimp
               ],
               [
                   LocationNames.K_Ogress_Shaman,
               ],
               ),
    RegionInfo(RegionNames.Wilderness,
               lambda player: lambda state: state.has(ItemNames.Wilderness, player),
               [
                   RegionNames.Ice_Mountain,
                   RegionNames.Monastery,
                   RegionNames.Edgeville,
                   RegionNames.West_Varrock,
                   RegionNames.Varrock_Palace,
                   RegionNames.East_Of_Varrock
               ],
               [
                   RegionNames.Coal_Rock,
                   RegionNames.Iron_Rock,
                   RegionNames.Furnace,
                   RegionNames.Anvil,
                   RegionNames.Shrimp,
                   RegionNames.Lobster
               ],
               [],
               lambda player: ({
                   # Can't walk through walls
                   RegionNames.Varrock_Palace:
                       lambda state: state.has(ItemNames.Varrock_Palace, player) and
                                     state.can_reach(RegionNames.East_Of_Varrock, None, player) or state.can_reach(
                           RegionNames.West_Varrock, None, player)
               })
               ),
    RegionInfo(RegionNames.Crandor,
               lambda player: lambda state: state.has(ItemNames.Crandor, player),
               [
                   RegionNames.Karamja,
                   RegionNames.Port_Sarim
               ],
               [
                   RegionNames.Coal_Rock,
                   RegionNames.Gold_Rock
               ],
               [
                   LocationNames.Q_Dragon_Slayer
               ],
               ),

    RegionInfo(RegionNames.Egg, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Sheep, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Milk, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Wheat, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Windmill, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Spinning_Wheel, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Imp, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Bronze_Ores, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Clay_Rock, lambda _: lambda _: True, [], [], []),

    RegionInfo(RegionNames.Coal_Rock,
               lambda _: lambda _: True,
               [], [], [LocationNames.Mine_Coal]),
    RegionInfo(RegionNames.Iron_Rock, lambda _: lambda _: True,
               [], [], [LocationNames.Smelt_Steel]),
    RegionInfo(RegionNames.Silver_Rock,
               lambda _: lambda _: True,
               [], [], [LocationNames.Mine_Silver, LocationNames.Smelt_Silver]),
    RegionInfo(RegionNames.Gold_Rock,
               lambda _: lambda _: True,
               [], [], [LocationNames.Mine_Gold, LocationNames.Smelt_Gold]),
    RegionInfo(RegionNames.Furnace,
               lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Anvil,
               lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Oak_Tree,
               lambda _: lambda _: True,
               [], [], [LocationNames.Oak_Log]),
    RegionInfo(RegionNames.Willow_Tree,
               lambda _: lambda _: True,
               [], [], [LocationNames.Willow_Log]),
    RegionInfo(RegionNames.Shrimp, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Fly_Fish, lambda _: lambda _: True, [], [], []),
    RegionInfo(RegionNames.Lobster,
               lambda _: lambda _: True,
               [], [], [LocationNames.Catch_Lobster]),
]

regions_by_name: typing.Dict[str, RegionInfo] = {region.name: region for region in all_regions}
