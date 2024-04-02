from BaseClasses import Location, MultiWorld
METROID_PRIME_LOCATION_BASE = 5031100


class MetroidPrimeLocation(Location):
    game: str = "Metroid Prime"


chozo_location_table = {
    'CR Main Plaza - Half-Pipe': 5031100,
    'CR Main Plaza - Grapple Ledge': 5031101,
    'CR Main Plaza - Tree': 5031102,
    'CR Main Plaza - Locked Door': 5031103,
    'CR Ruined Fountain': 5031104,
    'CR Ruined Shrine - Plated Beetle': 5031105,
    'CR Ruined Shrine - Half-Pipe': 5031106,
    'CR Ruined Shrine - Lower Tunnel': 5031107,
    'CR Vault': 5031108,
    'CR Training Chamber': 5031109,
    'CR Ruined Nursery': 5031110,
    'CR Training Chamber Access': 5031111,
    'CR Magma Pool': 5031112,
    'CR Tower of Light': 5031113,
    'CR Tower Chamber': 5031114,
    'CR Ruined Gallery - Missile Wall': 5031115,
    'CR Ruined Gallery - Tunnel': 5031116,
    'CR Transport Access North': 5031117,
    'CR Gathering Hall': 5031118,
    'CR Hive Totem': 5031119,
    'CR Sunchamber - Flaaghra': 5031120,
    'CR Sunchamber - Ghosts': 5031121,
    'CR Watery Hall Access': 5031122,
    'CR Watery Hall - Scan Puzzle': 5031123,
    'CR Watery Hall - Underwater': 5031124,
    'CR Dynamo - Lower': 5031125,
    'CR Dynamo - Spider Track': 5031126,
    'CR Burn Dome - Missile': 5031127,
    'CR Burn Dome - Incinerator Drone': 5031128,
    'CR Furnace - Spider Tracks': 5031129,
    'CR Furnace - Inside Furnace': 5031130,
    'CR Hall of the Elders': 5031131,
    'CR Crossway': 5031132,
    'CR Elder Chamber': 5031133,
    'CR Antechamber': 5031134
}

phen_location_table = {
    'PD Phendrana Shorelines - Behind Ice': 5031135,
    'PD Phendrana Shorelines - Spider Track': 5031136,
    'PD Chozo Ice Temple': 5031137,
    'PD Ice Ruins West': 5031138,
    'PD Ice Ruins East - Behind Ice': 5031139,
    'PD Ice Ruins East - Spider Track': 5031140,
    'PD Chapel of the Elders': 5031141,
    'PD Ruined Courtyard': 5031142,
    'PD Phendrana Canyon': 5031143,
    'PD Quarantine Cave': 5031144,
    'PD Research Lab Hydra': 5031145,
    'PD Quarantine Monitor': 5031146,
    'PD Observatory': 5031147,
    'PD Transport Access': 5031148,
    'PD Control Tower': 5031149,
    'PD Research Core': 5031150,
    'PD Frost Cave': 5031151,
    'PD Research Lab Aether - Tank': 5031152,
    'PD Research Lab Aether - Morph Track': 5031153,
    'PD Gravity Chamber - Underwater': 5031154,
    'PD Gravity Chamber - Grapple Ledge': 5031155,
    'PD Storage Cave': 5031156,
    'PD Security Cave': 5031157
}

tallon_location_table = {
    'TO Landing Site': 5031158,
    'TO Alcove': 5031159,
    'TO Frigate Crash Site': 5031160,
    'TO Overgrown Cavern': 5031161,
    'TO Root Cave': 5031162,
    'TO Artifact Temple': 5031163,
    'TO Transport Tunnel B': 5031164,
    'TO Arbor Chamber': 5031165,
    'TO Cargo Freight Lift to Deck Gamma': 5031166,
    'TO Biohazard Containment': 5031167,
    'TO Hydro Access Tunnel': 5031168,
    'TO Great Tree Chamber': 5031169,
    'TO Life Grove Tunnel': 5031170,
    'TO Life Grove - Start': 5031171,
    'TO Life Grove - Underwater Spinner': 5031172
}

mines_location_table = {
    'PM Main Quarry': 5031173,
    'PM Security Access A': 5031174,
    'PM Storage Depot B': 5031175,
    'PM Storage Depot A': 5031176,
    'PM Elite Research - Phazon Elite': 5031177,
    'PM Elite Research - Laser': 5031178,
    'PM Elite Control Access': 5031179,
    'PM Ventilation Shaft': 5031180,
    'PM Phazon Processing Center': 5031181,
    'PM Processing Center Access': 5031182,
    'PM Elite Quarters': 5031183,
    'PM Central Dynamo': 5031184,
    'PM Metroid Quarantine B': 5031185,
    'PM Metroid Quarantine A': 5031186,
    'PM Fungal Hall B': 5031187,
    'PM Phazon Mining Tunnel': 5031188,
    'PM Fungal Hall Access': 5031189
}

magmoor_location_table = {
    'MC Lava Lake': 5031190,
    'MC Triclops Pit': 5031191,
    'MC Storage Cavern': 5031192,
    'MC Transport Tunnel A': 5031193,
    'MC Warrior Shrine': 5031194,
    'MC Shore Tunnel': 5031195,
    'MC Fiery Shores - Morph Track': 5031196,
    'MC Fiery Shores - Warrior Shrine Tunnel': 5031197,
    'MC Plasma Processing': 5031198,
    'MC Magmoor Workstation': 5031199
}

every_location: dict[str, int] = {
    **chozo_location_table,
    **phen_location_table,
    **tallon_location_table,
    **mines_location_table,
    **magmoor_location_table
}
