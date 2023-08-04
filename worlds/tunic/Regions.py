from typing import Dict, Set

tunic_regions: Dict[str, Set[str]] = {
    "Menu": {"Overworld"},
    "Overworld": {"Menu", "Overworld Holy Cross", "East Forest", "Dark Tomb", "Bottom of the Well", "West Garden",
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry", "Swamp", "Spirit Arena"},
    "Overworld Holy Cross": {"Overworld"},
    "East Forest": {"Overworld", "Eastern Vault Fortress"},
    "Dark Tomb": {"Overworld", "West Garden"},
    "Bottom of the Well": {"Overworld", "Dark Tomb"},
    "West Garden": {"Overworld", "Dark Tomb"},
    "Ruined Atoll": {"Overworld", "Frog's Domain", "Library"},
    "Frog's Domain": {"Ruined Atoll"},
    "Library": {"Ruined Atoll"},
    "Eastern Vault Fortress": {"Overworld", "Beneath the Vault"},
    "Beneath the Vault": {"Overworld", "Eastern Vault Fortress"},
    "Quarry": {"Overworld", "Lower Quarry"},
    "Lower Quarry": {"Quarry", "Rooted Ziggurat"},
    "Rooted Ziggurat": {"Lower Quarry"},
    "Swamp": {"Overworld", "Cathedral"},
    "Cathedral": {"Swamp"},
    "Spirit Arena": {"Overworld"}
}