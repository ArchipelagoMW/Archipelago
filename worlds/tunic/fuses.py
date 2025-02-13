from typing import NamedTuple, Optional, Dict


class TunicLocationData(NamedTuple):
    region: str
    er_region: str
    

fuse_location_base_id = 509342400 + 10000

fuse_location_table: Dict[str, TunicLocationData] = {
    "Overworld - [Southeast] Activate Fuse": TunicLocationData("Overworld", "Overworld"),
    "Swamp - [Central] Activate Fuse": TunicLocationData("Swamp Mid", "Swamp Mid"),
    "Swamp - [Outside Cathedral] Activate Fuse": TunicLocationData("Swamp Mid", "Swamp Mid"),
    "Cathedral - Activate Fuse": TunicLocationData("Cathedral Main", "Cathedral Main"),
    "West Furnace - Activate Fuse": TunicLocationData("Furnace Fuse", "Furnace Fuse"),
    "West Garden - [South Highlands] Activate Fuse": TunicLocationData("West Garden South Checkpoint", "West Garden South Checkpoint"),
    "Ruined Atoll - [Northwest] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Ruined Atoll - [Northeast] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Ruined Atoll - [Southeast] Activate Fuse": TunicLocationData("Ruined Atoll Ladder Tops", "Ruined Atoll Ladder Tops"),
    "Ruined Atoll - [Southwest] Activate Fuse": TunicLocationData("Ruined Atoll", "Ruined Atoll"),
    "Library Lab - Activate Fuse": TunicLocationData("Library Lab", "Library Lab"),
    "Fortress Courtyard - [From Overworld] Activate Fuse": TunicLocationData("Fortress Exterior from Overworld", "Fortress Exterior from Overworld"),
    "Fortress Courtyard - [Near Cave] Activate Fuse": TunicLocationData("Fortress Exterior from Overworld", "Fortress Exterior from Overworld"),
    "Fortress Courtyard - [Upper] Activate Fuse": TunicLocationData("Fortress Courtyard Upper", "Fortress Courtyard Upper"),
    "Fortress Courtyard - [Central] Activate Fuse": TunicLocationData("Fortress Courtyard", "Fortress Courtyard"),
    "Beneath the Fortress - Activate Fuse": TunicLocationData("Beneath the Vault Back", "Beneath the Vault Back"),
    "Eastern Vault Fortress - [Candle Room] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Eastern Vault Fortress - [Left of Door] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Eastern Vault Fortress - [Right of Door] Activate Fuse": TunicLocationData("Eastern Vault Fortress", "Eastern Vault Fortress"),
    "Quarry Entryway - Activate Fuse": TunicLocationData("Quarry Connector", "Quarry Connector"),
    "Quarry - Activate Fuse": TunicLocationData("Quarry Entry", "Quarry Entry"),
    "Rooted Ziggurat Lower - [Miniboss] Activate Fuse": TunicLocationData("Rooted Ziggurat Lower Mid Checkpoint", "Rooted Ziggurat Lower Mid Checkpoint"),
    "Rooted Ziggurat Lower - [Before Boss] Activate Fuse": TunicLocationData("Rooted Ziggurat Lower Back", "Rooted Ziggurat Lower Back"),
}

fuse_location_name_to_id: dict[str, int] = {name: fuse_location_base_id + index
                                                 for index, name in enumerate(fuse_location_table)}

fuse_location_groups: dict[str, set[str]] = {}
for location_name, location_data in fuse_location_table.items():
    fuse_location_groups.setdefault(location_data.region, set()).add(location_name)