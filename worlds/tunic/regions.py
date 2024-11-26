from typing import Dict, Set

tunic_regions: Dict[str, Set[str]] = {
    "Menu": {"Overworld"},
    "Overworld": {"Overworld Holy Cross", "East Forest", "Dark Tomb", "Beneath the Well", "West Garden",
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry Back", "Quarry", "Swamp",
                  "Spirit Arena"},
    "Overworld Holy Cross": set(),
    "East Forest": set(),
    "Dark Tomb": {"West Garden"},
    "Beneath the Well": set(),
    "West Garden": set(),
    "Ruined Atoll": {"Frog's Domain", "Library"},
    "Frog's Domain": set(),
    "Library": set(),
    "Eastern Vault Fortress": {"Beneath the Vault"},
    "Beneath the Vault": {"Eastern Vault Fortress"},
    "Quarry Back": {"Quarry"},
    "Quarry": {"Monastery", "Lower Quarry"},
    "Monastery": set(),
    "Lower Quarry": {"Rooted Ziggurat"},
    "Rooted Ziggurat": set(),
    "Swamp": {"Cathedral"},
    "Cathedral": set(),
    "Spirit Arena": set()
}
