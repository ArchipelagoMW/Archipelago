from .Macros import BASE_MACROS

from .requirements.Skyloft import SKYLOFT_REQUIREMENTS
from .requirements.Sky import SKY_REQUIREMENTS
from .requirements.Faron import FARON_REQUIREMENTS
from .requirements.Eldin import ELDIN_REQUIREMENTS
from .requirements.Lanayru import LANAYRU_REQUIREMENTS

from .requirements.Skyview import SKYVIEW_REQUIREMENTS
from .requirements.Earth_Temple import EARTH_TEMPLE_REQUIREMENTS
from .requirements.Lanayru_Mining_Facility import LANAYRU_MINING_FACILITY_REQUIREMENTS
from .requirements.Ancient_Cistern import ANCIENT_CISTERN_REQUIREMENTS
from .requirements.Sandship import SANDSHIP_REQUIREMENTS
from .requirements.Fire_Sanctuary import FIRE_SANCTUARY_REQUIREMENTS
from .requirements.Sky_Keep import SKY_KEEP_REQUIREMENTS

ALL_REQUIREMENTS = (
    SKYLOFT_REQUIREMENTS
    | SKY_REQUIREMENTS
    | FARON_REQUIREMENTS
    | ELDIN_REQUIREMENTS
    | LANAYRU_REQUIREMENTS
    | SKYVIEW_REQUIREMENTS
    | EARTH_TEMPLE_REQUIREMENTS
    | LANAYRU_MINING_FACILITY_REQUIREMENTS
    | ANCIENT_CISTERN_REQUIREMENTS
    | SANDSHIP_REQUIREMENTS
    | FIRE_SANCTUARY_REQUIREMENTS
    | SKY_KEEP_REQUIREMENTS
)

regional_macros = {}
for reg, data in ALL_REQUIREMENTS.items():
    if "macros" in data:
        regional_macros.update({name: f"can_reach_region {reg} & ({req})" for name, req in data["macros"].items()})

MACROS = (
    BASE_MACROS
    | regional_macros
)
