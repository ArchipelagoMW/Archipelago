from BaseClasses import Location, MultiWorld
METROID_PRIME_LOCATION_BASE = 5031100


class MetroidPrimeLocation(Location):
    game: str = "Metroid Prime"


chozo_location_table = {
    'Chozo Ruins: Main Plaza - Half-Pipe': 5031100,
    'Chozo Ruins: Main Plaza - Grapple Ledge': 5031101,
    'Chozo Ruins: Main Plaza - Tree': 5031102,
    'Chozo Ruins: Main Plaza - Locked Door': 5031103,
    'Chozo Ruins: Ruined Fountain': 5031104,
    'Chozo Ruins: Ruined Shrine - Plated Beetle': 5031105,
    'Chozo Ruins: Ruined Shrine - Half-Pipe': 5031106,
    'Chozo Ruins: Ruined Shrine - Lower Tunnel': 5031107,
    'Chozo Ruins: Vault': 5031108,
    'Chozo Ruins: Training Chamber': 5031109,
    'Chozo Ruins: Ruined Nursery': 5031110,
    'Chozo Ruins: Training Chamber Access': 5031111,
    'Chozo Ruins: Magma Pool': 5031112,
    'Chozo Ruins: Tower of Light': 5031113,
    'Chozo Ruins: Tower Chamber': 5031114,
    'Chozo Ruins: Ruined Gallery - Missile Wall': 5031115,
    'Chozo Ruins: Ruined Gallery - Tunnel': 5031116,
    'Chozo Ruins: Transport Access North': 5031117,
    'Chozo Ruins: Gathering Hall': 5031118,
    'Chozo Ruins: Hive Totem': 5031119,
    'Chozo Ruins: Sunchamber - Flaaghra': 5031120,
    'Chozo Ruins: Sunchamber - Ghosts': 5031121,
    'Chozo Ruins: Watery Hall Access': 5031122,
    'Chozo Ruins: Watery Hall - Scan Puzzle': 5031123,
    'Chozo Ruins: Watery Hall - Underwater': 5031124,
    'Chozo Ruins: Dynamo - Lower': 5031125,
    'Chozo Ruins: Dynamo - Spider Track': 5031126,
    'Chozo Ruins: Burn Dome - Missile': 5031127,
    'Chozo Ruins: Burn Dome - Incinerator Drone': 5031128,
    'Chozo Ruins: Furnace - Spider Tracks': 5031129,
    'Chozo Ruins: Furnace - Inside Furnace': 5031130,
    'Chozo Ruins: Hall of the Elders': 5031131,
    'Chozo Ruins: Crossway': 5031132,
    'Chozo Ruins: Elder Chamber': 5031133,
    'Chozo Ruins: Antechamber': 5031134
}

phen_location_table = {
    'Phendrana Drifts: Phendrana Shorelines - Behind Ice': 5031135,
    'Phendrana Drifts: Phendrana Shorelines - Spider Track': 5031136,
    'Phendrana Drifts: Chozo Ice Temple': 5031137,
    'Phendrana Drifts: Ice Ruins West': 5031138,
    'Phendrana Drifts: Ice Ruins East - Behind Ice': 5031139,
    'Phendrana Drifts: Ice Ruins East - Spider Track': 5031140,
    'Phendrana Drifts: Chapel of the Elders': 5031141,
    'Phendrana Drifts: Ruined Courtyard': 5031142,
    'Phendrana Drifts: Phendrana Canyon': 5031143,
    'Phendrana Drifts: Quarantine Cave': 5031144,
    'Phendrana Drifts: Research Lab Hydra': 5031145,
    'Phendrana Drifts: Quarantine Monitor': 5031146,
    'Phendrana Drifts: Observatory': 5031147,
    'Phendrana Drifts: Transport Access': 5031148,
    'Phendrana Drifts: Control Tower': 5031149,
    'Phendrana Drifts: Research Core': 5031150,
    'Phendrana Drifts: Frost Cave': 5031151,
    'Phendrana Drifts: Research Lab Aether - Tank': 5031152,
    'Phendrana Drifts: Research Lab Aether - Morph Track': 5031153,
    'Phendrana Drifts: Gravity Chamber - Underwater': 5031154,
    'Phendrana Drifts: Gravity Chamber - Grapple Ledge': 5031155,
    'Phendrana Drifts: Storage Cave': 5031156,
    'Phendrana Drifts: Security Cave': 5031157
}

tallon_location_table = {
    'Tallon Overworld: Landing Site': 5031158,
    'Tallon Overworld: Alcove': 5031159,
    'Tallon Overworld: Frigate Crash Site': 5031160,
    'Tallon Overworld: Overgrown Cavern': 5031161,
    'Tallon Overworld: Root Cave': 5031162,
    'Tallon Overworld: Artifact Temple': 5031163,
    'Tallon Overworld: Transport Tunnel B': 5031164,
    'Tallon Overworld: Arbor Chamber': 5031165,
    'Tallon Overworld: Cargo Freight Lift to Deck Gamma': 5031166,
    'Tallon Overworld: Biohazard Containment': 5031167,
    'Tallon Overworld: Hydro Access Tunnel': 5031168,
    'Tallon Overworld: Great Tree Chamber': 5031169,
    'Tallon Overworld: Life Grove Tunnel': 5031170,
    'Tallon Overworld: Life Grove - Start': 5031171,
    'Tallon Overworld: Life Grove - Underwater Spinner': 5031172
}

mines_location_table = {
    'Phazon Mines: Main Quarry': 5031173,
    'Phazon Mines: Security Access A': 5031174,
    'Phazon Mines: Storage Depot B': 5031175,
    'Phazon Mines: Storage Depot A': 5031176,
    'Phazon Mines: Elite Research - Phazon Elite': 5031177,
    'Phazon Mines: Elite Research - Laser': 5031178,
    'Phazon Mines: Elite Control Access': 5031179,
    'Phazon Mines: Ventilation Shaft': 5031180,
    'Phazon Mines: Phazon Processing Center': 5031181,
    'Phazon Mines: Processing Center Access': 5031182,
    'Phazon Mines: Elite Quarters': 5031183,
    'Phazon Mines: Central Dynamo': 5031184,
    'Phazon Mines: Metroid Quarantine B': 5031185,
    'Phazon Mines: Metroid Quarantine A': 5031186,
    'Phazon Mines: Fungal Hall B': 5031187,
    'Phazon Mines: Phazon Mining Tunnel': 5031188,
    'Phazon Mines: Fungal Hall Access': 5031189
}

magmoor_location_table = {
    'Magmoor Caverns: Lava Lake': 5031190,
    'Magmoor Caverns: Triclops Pit': 5031191,
    'Magmoor Caverns: Storage Cavern': 5031192,
    'Magmoor Caverns: Transport Tunnel A': 5031193,
    'Magmoor Caverns: Warrior Shrine': 5031194,
    'Magmoor Caverns: Shore Tunnel': 5031195,
    'Magmoor Caverns: Fiery Shores - Morph Track': 5031196,
    'Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel': 5031197,
    'Magmoor Caverns: Plasma Processing': 5031198,
    'Magmoor Caverns: Magmoor Workstation': 5031199
}

every_location: dict[str, int] = {
    **chozo_location_table,
    **phen_location_table,
    **tallon_location_table,
    **mines_location_table,
    **magmoor_location_table
}
