from typing import TYPE_CHECKING

from .area_rando_types import AreaDoor
if TYPE_CHECKING:
    from .romWriter import RomWriter

spaceport_doors = {
    "StationCorridorL": AreaDoor('1a5ec', '85dc00040116000100800000', 'SpacePort', 'StationCorridorL', 6),
    "StationCorridorBR": AreaDoor('1a5bc', '85dc00050e26000200800000', 'SpacePort', 'StationCorridorBR', 6),
    "DockingPort2AccessR": AreaDoor('1a85c', '11d400052e06020000800000', 'SpacePort', 'DockingPort2AccessR', 6),
    "DockingUmbilical2L": AreaDoor('1abb0', 'c3d300000106000000800000', 'SpacePort', 'DockingUmbilical2L', 6),
    "SternR": AreaDoor('1a898', '9cd300011e160101008020a6', 'SpacePort', 'SternR', 6),
    "SternTL": AreaDoor('1a6a0', '9cd300040106000000800000', 'SpacePort', 'SternTL', 6),
    "CompartmentsR": AreaDoor('1a658', '179d00055d16050110010000', 'SpacePort', 'CompartmentsR', 6),
    "CompartmentsL": AreaDoor('1a640', '179d00040116000100800000', 'SpacePort', 'CompartmentsL', 6),
    "AftTR": AreaDoor('1a6e8', '6ac700050d06000010010000', 'SpacePort', 'AftTR', 6),
    "LoungeR": AreaDoor('19470', '6fde00051e06010000800000', 'SpacePort', 'LoungeR', 6),
    "DockingPort1AccessL": AreaDoor('1929c', '29de00040106000000800000', 'SpacePort', 'DockingPort1AccessL', 6),
    "AirLockL": AreaDoor('1a988', '01eb00000106000000800000', 'SpacePort', 'AirLockL', 6),
    "DockingUmbilical1R": AreaDoor('1a9ac', 'cbdc00013e06030000800000', 'SpacePort', 'DockingUmbilical1R', 6),
    "CrewQuartersAccessL": AreaDoor('1ab50', '41df00040106000000800000', 'SpacePort', 'CrewQuartersAccessL', 6),
    "AirLockR": AreaDoor('1a97c', '01eb00010e06000000800000', 'SpacePort', 'AirLockR', 6),
    "CrewQuartersBL": AreaDoor('1a91c', '47eb00040116000100800000', 'SpacePort', 'CrewQuartersBL', 6),
    "CrewQuartersAccessR": AreaDoor('1ab44', '41df00051e06010000800000', 'SpacePort', 'CrewQuartersAccessR', 6),
    "MainEngineeringBR": AreaDoor('19b30', '37e400053e36030300800000', 'SpacePort', 'MainEngineeringBR', 6),
    "FuelingPortAccessL": AreaDoor('1a940', '4dc000040106000000800000', 'SpacePort', 'FuelingPortAccessL', 6),
    "FuelingPortAccessR": AreaDoor('1a088', '4dc0000110100101008095a9', 'SpacePort', 'FuelingPortAccessR', 6),
    "FuelingPortL": AreaDoor('19bd8', 'f9db00000106000000800000', 'SpacePort', 'FuelingPortL', 6),

    "CargoBayBL": AreaDoor('191dc', '3fdc00040136000300800000', 'SpacePort', 'CargoBayBL', 6),
    "DockingPort4R": AreaDoor('19c8c', '14cb00050e06000000800000', 'SpacePort', 'DockingPort4R', 6),
    "CargoBayMR": AreaDoor('193c8', '3fdc00052e26020200800000', 'SpacePort', 'CargoBayMR', 6),
    "DockingPort3L": AreaDoor('19338', 'edca00040106000000800000', 'SpacePort', 'DockingPort3L', 6),

    "CargoBayTL": AreaDoor('19398', '3fdc00040116000100800000', 'SpacePort', 'CargoBayTL', 6),
    "BridgeL": AreaDoor('1959c', '818100040116000100800000', 'SpacePort', 'BridgeL', 6),
}


def shrink_spaceport(rom_writer: "RomWriter") -> None:
    rom_writer.connect_doors(spaceport_doors['StationCorridorL'], spaceport_doors['SternR'])
    rom_writer.connect_doors(spaceport_doors['SternTL'], spaceport_doors['AftTR'])
    rom_writer.connect_doors(spaceport_doors['LoungeR'], spaceport_doors['AirLockL'])
    rom_writer.connect_doors(spaceport_doors['AirLockR'], spaceport_doors['CrewQuartersBL'])
    rom_writer.connect_doors(spaceport_doors['MainEngineeringBR'], spaceport_doors['FuelingPortL'])
    rom_writer.connect_doors(spaceport_doors['CargoBayMR'], spaceport_doors['DockingPort3L'])
    rom_writer.connect_doors(spaceport_doors['CargoBayBL'], spaceport_doors['DockingPort4R'])
