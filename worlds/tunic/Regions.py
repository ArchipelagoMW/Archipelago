from typing import Dict, Set

tunic_regions: Dict[str, Set[str]] = {
    "Menu": {"Overworld"},
    "Overworld": {"Menu", "Overworld Holy Cross", "East Forest", "Dark Tomb", "Bottom of the Well", "West Garden",
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry", "Swamp", "Spirit Arena"},
    "Overworld Holy Cross": set(),
    "East Forest": {"Eastern Vault Fortress"},
    "Dark Tomb": {"West Garden"},
    "Bottom of the Well": {"Dark Tomb"},
    "West Garden": {"Overworld", "Dark Tomb"},
    "Ruined Atoll": {"Frog's Domain", "Library"},
    "Frog's Domain": set(),
    "Library": {"Ruined Atoll"},
    "Eastern Vault Fortress": {"Beneath the Vault"},
    "Beneath the Vault": {"Eastern Vault Fortress"},
    "Quarry": {"Lower Quarry"},
    "Lower Quarry": {"Rooted Ziggurat"},
    "Rooted Ziggurat": set(),
    "Swamp": {"Cathedral"},
    "Cathedral": set(),
    "Spirit Arena": set()
}
