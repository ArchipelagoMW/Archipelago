from typing import Dict, List

"""
This file is for handling SC2 data read via the bot
"""

normalized_unit_types: Dict[str, str] = {
    # Thor morphs
    "AP_ThorAP": "AP_Thor",
    "AP_MercThorAP": "AP_MercThor",
    "AP_ThorMengskSieged": "AP_ThorMengsk",
    "AP_ThorMengskAP": "AP_ThorMengsk",
    # Siege Tank morphs
    "AP_SiegeTankSiegedTransportable": "AP_SiegeTank",
    "AP_SiegeTankMengskSiegedTransportable": "AP_SiegeTankMengsk",
    "AP_SiegeBreakerSiegedTransportable": "AP_SiegeBreaker",
    "AP_InfestedSiegeBreakerSiegedTransportable": "AP_InfestedSiegeBreaker",
    "AP_StukovInfestedSiegeTank": "AP_StukovInfestedSiegeTankUprooted",
    # Cargo size upgrades
    "AP_FirebatOptimizedLogistics": "AP_Firebat",
    "AP_DevilDogOptimizedLogistics": "AP_DevilDog",
    "AP_GhostResourceEfficiency": "AP_Ghost",
    "AP_GhostMengskResourceEfficiency": "AP_GhostMengsk",
    "AP_SpectreResourceEfficiency": "AP_Spectre",
    "AP_UltraliskResourceEfficiency": "AP_Ultralisk",
    "AP_MercUltraliskResourceEfficiency": "AP_MercUltralisk",
    "AP_ReaperResourceEfficiency": "AP_Reaper",
    "AP_MercReaperResourceEfficiency": "AP_MercReaper",
}

worker_units: List[str] = [
    "AP_SCV",
    "AP_MULE", # Mules can't currently build (or be traded due to timed life), this is future proofing just in case
    "AP_Drone",
    "AP_SISCV", # Infested SCV
    "AP_Probe",
    "AP_ElderProbe",
]
