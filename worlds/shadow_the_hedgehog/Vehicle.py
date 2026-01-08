from dataclasses import dataclass
from . import Items, Names


@dataclass
class VehicleInfo:
    game_id: int
    name: str
    available_stages: []

    def __init__(self, id, name, stages):
        self.game_id = id
        self.name = Names.GetNameForVehicle(name)
        self.available_stages = stages

VEHICLE_INFO = \
[
    VehicleInfo(0x1, "Standard Car", []),
    VehicleInfo(0x2, "Convertible", []),
    VehicleInfo(0x3, "Armored Car", []),
    VehicleInfo(0x4, "Gun Motorcycle", []),
    VehicleInfo(0x5, "Gun Jumper", []),
    VehicleInfo(0x6, "Gun Cannon", []),
    VehicleInfo(0x7, "Air Saucer", []),
    VehicleInfo(0x8, "Black Hawk", []),
    VehicleInfo(0x9, "Black Volt", []),
    VehicleInfo(0xA, "Gun Turret", []),
    VehicleInfo(0xB, "Black Turret", []),
    VehicleInfo(0xC, "Gun Lift", [])

]

def GetRuleByVehicleRequirement(player, req):
    #, stage, regions):
    #if regions is not None:
    #    for i in range(0, len(regions)):
    #        if max(regions) > i:
    #            regions.append(i)
    #else:
    #    p_regions = [ l.regionIndex for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == stage]
    #    if len(p_regions) == 0:
    #        regions = []
    #    else:
    #        regions = p_regions

    matches = [ v for v in VEHICLE_INFO if Names.GetNameForVehicle(req) == v.name ]

    if len(matches) == 0:
        print("Something wrong here with", req, [ v.name for v in VEHICLE_INFO])

    return lambda state, match=matches: state.has_any([m.name for m in match],player)
