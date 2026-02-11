from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "2nd Floor": ItemData(2000, always_progression, "Remote2ndFloor", ("RULayer2", ), 2),
    "Blueprints": ItemData(2001, always_useful, "RemoteBlueprints", ("RUBlueprints", ), 2),
    "3rd Platform Floor": ItemData(2003, always_useful, "Remote3rdPlatformFloor", ("RUIslandLayer3", ), 2),
    # Entirely for display purposes
    # "Infinite Goals": ItemData(000, always_progression, "RemoteInfiniteGoals", ("RUInfiniteGoals", ), 2),
    "3rd Floor": ItemData(2004, always_useful, "Remote3rdFloor", ("RULayer3", ), 2),
    "Train Delivery": ItemData(2005, always_useful, "RemoteTrainDelivery", ("RUTrainHubDelivery", ), 2),
}

starting: dict[str, ItemData] = {
    "Space Platforms": ItemData(2100, always_progression, "RemoteSpacePlatforms", ("RUIslandPlacement", ), 2),
    "2nd Platform Floor": ItemData(2101, always_progression, "Remote2ndPlatformFloor", ("RUIslandLayer2", ), 2),
    "Wires (Category)": ItemData(2102, always_useful, "RemoteWiresCategory", ("RUWires", ), 2),
    "Trains": ItemData(2103, always_useful, "RemoteTrains", ("RUTrains", ), 2),
    "Fluids": ItemData(2104, always_progression, "RemoteFluids", ("RUFluids", ), 2),
    "Upgrades": ItemData(2105, always_progression, "RemoteUpgrades", ("RUSideUpgrades", ), 2),
}

special: dict[str, ItemData] = {
    "Operator Levels": ItemData(2200, always_progression, "RemoteOperatorLevels", ("RUPlayerLevel", ), 2),
}
