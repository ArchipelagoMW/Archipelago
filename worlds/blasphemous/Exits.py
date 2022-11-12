from typing import List, Dict


region_exit_table: Dict[str, List[str]] = {
    "menu"     : ["New Game"],

    "albero"   : ["To The Holy Line",
                  "To Desecrated Cistern",
                  "To Wasteland of the Buried Churches",
                  "To Dungeons"],

    "attots"   : ["To Mother of Mothers"],

    "ar"       : ["To Mother of Mothers",
                  "To Wall of the Holy Prohibitions",
                  "To Deambulatory of His Holiness"],

    "bottc"    : ["To Wasteland of the Buried Churches",
                  "To Ferrous Tree"],

    "botss"    : ["To The Holy Line",
                  "To Mountains of the Endless Dusk"],

    "coolotcv" : ["To Graveyard of the Peaks",
                  "To Wall of the Holy Prohibitions"],

    "dohh"     : ["To Archcathedral Rooftops"],

    "dc"       : ["To Albero",
                  "To Mercy Dreams",
                  "To Mountains of the Endless Dusk",
                  "To Echoes of Salt",
                  "To Grievance Ascends"],

    "eos"      : ["To Jondo",
                  "To Mountains of the Endless Dusk",
                  "To Desecrated Cistern",
                  "To The Resting Place of the Sister",
                  "To Mourning and Havoc"],

    "ft"       : ["To Bridge of the Three Cavalries",
                  "To Hall of the Dawning",
                  "To Patio of the Silent Steps"],

    "gotp"     : ["To Where Olive Trees Wither",
                  "To Convent of Our Lady of the Charred Visage"],

    "ga"       : ["To Jondo",
                  "To Desecrated Cistern"],

    "hotd"     : ["To Ferrous Tree"],

    "jondo"    : ["To Mountains of the Endless Dusk",
                  "To Grievance Ascends"],

    "kottw"    : ["To Mother of Mothers"],

    "lotnw"    : ["To Mother of Mothers",
                  "To The Sleeping Canvases"],

    "md"       : ["To Wasteland of the Buried Churches",
                  "To Desecrated Cistern",
                  "To The Sleeping Canvases"],

    "mom"      : ["To Patio of the Silent Steps",
                  "To Archcathedral Rooftops",
                  "To Knot of the Three Words",
                  "To Library of the Negated Words",
                  "To All the Tears of the Sea"],

    "moted"    : ["To Brotherhood of the Silent Sorrow",
                  "To Jondo",
                  "To Desecrated Cistern"],

    "mah"      : ["To Echoes of Salt",
                  "To Mother of Mothers"],

    "potss"    : ["To Ferrous Tree",
                  "To Mother of Mothers",
                  "To Wall of the Holy Prohibitions"],

    "petrous"  : ["To The Holy Line"],

    "thl"      : ["To Brotherhood of the Silent Sorrow",
                  "To Petrous",
                  "To Albero"],

    "trpots"   : ["To Echoes of Salt"],

    "tsc"      : ["To Library of the Negated Words",
                  "To Mercy Dreams"],

    "wothp"    : ["To Archcathedral Rooftops",
                  "To Convent of Our Lady of the Charred Visage"],

    "wotbc"    : ["To Albero",
                  "To Where Olive Trees Wither",
                  "To Mercy Dreams"],

    "wotw"     : ["To Wasteland of the Buried Churches",
                  "To Graveyard of the Peaks"]
}

exit_lookup_table: Dict[str, str] = {
    "New Game": "botss",
    "To Albero": "albero",
    "To All the Tears of the Sea": "attots",
    "To Archcathedral Rooftops": "ar",
    "To Bridge of the Three Cavalries": "bottc",
    "To Brotherhood of the Silent Sorrow": "botss",
    "To Convent of Our Lady of the Charred Visage": "coolotcv",
    "To Deambulatory of His Holiness": "dohh",
    "To Desecrated Cistern": "dc",
    "To Echoes of Salt": "eos",
    "To Ferrous Tree": "ft",
    "To Graveyard of the Peaks": "gotp",
    "To Grievance Ascends": "ga",
    "To Hall of the Dawning": "hotd",
    "To Jondo": "jondo",
    "To Knot of the Three Words": "kottw",
    "To Library of the Negated Words": "lotnw",
    "To Mercy Dreams": "md",
    "To Mother of Mothers": "mom",
    "To Mountains of the Endless Dusk": "moted",
    "To Mourning and Havoc": "mah",
    "To Patio of the Silent Steps": "potss",
    "To Petrous": "petrous",
    "To The Holy Line": "thl",
    "To The Resting Place of the Sister": "trpots",
    "To The Sleeping Canvases": "tsc",
    "To Wall of the Holy Prohibitions": "wothp",
    "To Wasteland of the Buried Churches": "wotbc",
    "To Where Olive Trees Wither": "wotw",
    "To Dungeons": "dungeon"
}