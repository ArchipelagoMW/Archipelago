from typing import Dict, Set

tunic_regions: Dict[str, Set[str]] = {
    "Menu": {"Overworld"},
    "Overworld": {"Overworld Holy Cross", "East Forest", "Dark Tomb", "Beneath the Well", "West Garden",
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry Back", "Quarry", "Swamp",
                  "Spirit Arena"},
    "Overworld Holy Cross": set(),
    "East Forest": {"Eastern Vault Fortress"},
    "Dark Tomb": {"West Garden"},
    "Beneath the Well": {"Dark Tomb"},
    "West Garden": {"Overworld", "Dark Tomb"},
    "Ruined Atoll": {"Frog's Domain", "Library"},
    "Frog's Domain": set(),
    "Library": set(),
    "Eastern Vault Fortress": {"Beneath the Vault"},
    "Beneath the Vault": {"Eastern Vault Fortress"},
    "Quarry Back": {"Quarry"},
    "Quarry": {"Lower Quarry", "Rooted Ziggurat"},
    "Lower Quarry": {"Rooted Ziggurat"},
    "Rooted Ziggurat": set(),
    "Swamp": {"Cathedral"},
    "Cathedral": set(),
    "Spirit Arena": set()
}
