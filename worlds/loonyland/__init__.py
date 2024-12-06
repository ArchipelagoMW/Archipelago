from typing import Dict

from BaseClasses import Tutorial
from ..AutoWorld import WebWorld, World

class LoonylandWeb(WebWorld):
    options_page = False
    theme = 'partyTime'

    setup_en = Tutorial(
        tutorial_name='Setup Guide',
        description='A guide to playing Loonyland',
        language='English',
        file_name='setup_en.md',
        link='setup/en',
        authors=['AutomaticFrenzy']
    )
    
    tutorials = [setup_en]

class LoonylandWorld(World):
    """
    Loonyland Halloween Hill
    """
    game = "Loonyland"
    web = LoonylandWeb()

    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}


