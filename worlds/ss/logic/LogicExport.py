### This script is not ran by the AP World
### This is a helper script to export the python requirements into json format
### If you edit requirements, change the python file under the /requirements/ folder
### Then run this file to automatically export requirements into json format
### These JSON files will be under /requirements_json/


from requirements.Skyloft import SKYLOFT_REQUIREMENTS
from requirements.Sky import SKY_REQUIREMENTS
from requirements.Faron import FARON_REQUIREMENTS
from requirements.Eldin import ELDIN_REQUIREMENTS
from requirements.Lanayru import LANAYRU_REQUIREMENTS

from requirements.Skyview import SKYVIEW_REQUIREMENTS
from requirements.Earth_Temple import EARTH_TEMPLE_REQUIREMENTS
from requirements.Lanayru_Mining_Facility import LANAYRU_MINING_FACILITY_REQUIREMENTS
from requirements.Ancient_Cistern import ANCIENT_CISTERN_REQUIREMENTS
from requirements.Sandship import SANDSHIP_REQUIREMENTS
from requirements.Fire_Sanctuary import FIRE_SANCTUARY_REQUIREMENTS
from requirements.Sky_Keep import SKY_KEEP_REQUIREMENTS

from Macros import BASE_MACROS

import json

with open("./requirements_json/Skyloft.json", "w") as f:
    json.dump(SKYLOFT_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Sky.json", "w") as f:
    json.dump(SKY_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Faron.json", "w") as f:
    json.dump(FARON_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Eldin.json", "w") as f:
    json.dump(ELDIN_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Lanayru.json", "w") as f:
    json.dump(LANAYRU_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Skyview.json", "w") as f:
    json.dump(SKYVIEW_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Earth_Temple.json", "w") as f:
    json.dump(EARTH_TEMPLE_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Lanayru_Mining_Facility.json", "w") as f:
    json.dump(LANAYRU_MINING_FACILITY_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Ancient_Cistern.json", "w") as f:
    json.dump(ANCIENT_CISTERN_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Sandship.json", "w") as f:
    json.dump(SANDSHIP_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Fire_Sanctuary.json", "w") as f:
    json.dump(FIRE_SANCTUARY_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Sky_Keep.json", "w") as f:
    json.dump(SKY_KEEP_REQUIREMENTS, f, indent=2)

with open("./requirements_json/Base_Macros.json", "w") as f:
    json.dump(BASE_MACROS, f, indent=2)
