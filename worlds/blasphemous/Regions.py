from typing import List, Dict, Set


area_table: Dict[str, str] = {
    "menu"    : "Menu",
    "albero"  : "Albero",
    "attots"  : "All the Tears of the Sea",
    "ar"      : "Archcathedral Rooftops",
    "bottc"   : "Bridge of the Three Cavalries",
    "botss"   : "Brotherhood of the Silent Sorrow",
    "coolotcv": "Convent of Our Lady of the Charred Visage",
    "dohh"    : "Deambulatory of His Holiness",
    "dc"      : "Desecrated Cistern",
    "eos"     : "Echoes of Salt",
    "ft"      : "Ferrous Tree",
    "gotp"    : "Graveyard of the Peaks",
    "ga"      : "Grievance Ascends",
    "hotd"    : "Hall of the Dawning",
    "jondo"   : "Jondo",
    "kottw"   : "Knot of the Three Words",
    "lotnw"   : "Library of the Negated Words",
    "md"      : "Mercy Dreams",
    "mom"     : "Mother of Mothers",
    "moted"   : "Mountains of the Endless Dusk",
    "mah"     : "Mourning and Havoc",
    "potss"   : "Patio of the Silent Steps",
    "petrous" : "Petrous",
    "thl"     : "The Holy Line",
    "trpots"  : "The Resting Place of the Sister",
    "tsc"     : "The Sleeping Canvases",
    "wothp"   : "Wall of the Holy Prohibitions",
    "wotbc"   : "Wasteland of the Buried Churches",
    "wotw"    : "Where Olive Trees Wither",
    "dungeon" : "Dungeons"
}


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


room_table: Set[str] = {
    "D01Z01S01", # THL
    "D01Z01S02", # THL
    "D01Z01S03", # THL
    "D01Z01S07", # THL
    "D01Z02S01", # Albero
    "D01Z02S02", # Albero
    "D01Z02S03", # Albero
    "D01Z02S04", # Albero
    "D01Z02S05", # Albero
    "D01Z02S06", # Albero
    "D01Z02S07", # Albero
    "D01BZ04S01", # Albero Church
    "D01BZ06S01", # Ossuary
    "D01BZ08S01", # Ossuary - isidora's room?
    "D01Z03S01", # WotBC
    "D01Z03S02", # WotBC
    "D01Z03S03", # WotBC
    "D01Z03S04", # WotBC
    "D01Z03S05", # WotBC
    "D01Z03S06", # WotBC
    "D01Z03S07", # WotBC
    "D01Z04S01", # MD
    "D01Z04S02", # MD
    "D01Z04S03", # MD
    "D01Z04S05", # MD
    "D01Z04S06", # MD
    "D01Z04S07", # MD
    "D01Z04S08", # MD
    "D01Z04S09", # MD
    "D01Z04S10", # MD
    "D01Z04S11", # MD
    "D01Z04S12", # MD
    "D01Z04S13", # MD
    "D01Z04S14", # MD
    "D01Z04S15", # MD
    "D01Z04S16", # MD
    "D01Z04S17", # MD
    "D01Z04S18", # MD
    "D01Z04S19", # MD
    "D01BZ02S01", # MD - shop
    "D01Z05S01", # DC
    "D01Z05S02", # DC
    "D01Z05S03", # DC
    "D01Z05S04", # DC
    "D01Z05S05", # DC
    "D01Z05S06", # DC
    "D01Z05S07", # DC
    "D01Z05S08", # DC
    "D01Z05S09", # DC
    "D01Z05S10", # DC
    "D01Z05S11", # DC
    "D01Z05S12", # DC
    "D01Z05S13", # DC
    "D01Z05S14", # DC
    "D01Z05S15", # DC
    "D01Z05S16", # DC
    "D01Z05S17", # DC
    "D01Z05S18", # DC
    "D01Z05S19", # DC
    "D01Z05S20", # DC
    "D01Z05S21", # DC
    "D01Z05S22", # DC
    "D01Z05S23", # DC
    "D01Z05S24", # DC
    "D01Z05S25", # DC
    "D01Z05S26", # DC
    "D01Z05S27", # DC
    "D01BZ05S01", # DC - shroud of dreamt sins room?
    "D01Z06S01", # Petrous
    "D01BZ07S01", # Petrous - Jibrael
    "D02Z01S01", # WOTW
    "D02Z01S02", # WOTW
    "D02Z01S03", # WOTW
    "D02Z01S04", # WOTW
    "D02Z01S05", # WOTW
    "D02Z01S06", # WOTW
    "D02Z01S08", # WOTW
    "D02Z01S09", # WOTW
    "D02Z02S01", # GOTP
    "D02Z02S02", # GOTP
    "D02Z02S03", # GOTP
    "D02Z02S04", # GOTP
    "D02Z02S05", # GOTP
    "D02Z02S06", # GOTP
    "D02Z02S07", # GOTP
    "D02Z02S08", # GOTP
    "D02Z02S09", # GOTP
    "D02Z02S10", # GOTP
    "D02Z02S11", # GOTP
    "D02Z02S12", # GOTP
    "D02Z02S13", # GOTP
    "D02Z02S14", # GOTP
    "D02BZ02S01", # GOTP - shop
    "D02Z03S01", # COOLOTCV
    "D02Z03S02", # COOLOTCV
    "D02Z03S03", # COOLOTCV
    "D02Z03S05", # COOLOTCV
    "D02Z03S06", # COOLOTCV
    "D02Z03S07", # COOLOTCV
    "D02Z03S08", # COOLOTCV
    "D02Z03S09", # COOLOTCV
    "D02Z03S10", # COOLOTCV
    "D02Z03S11", # COOLOTCV
    "D02Z03S12", # COOLOTCV
    "D02Z03S13", # COOLOTCV
    "D02Z03S14", # COOLOTCV
    "D02Z03S15", # COOLOTCV
    "D02Z03S16", # COOLOTCV
    "D02Z03S17", # COOLOTCV
    "D02Z03S18", # COOLOTCV
    "D02Z03S19", # COOLOTCV
    "D02Z03S20", # COOLOTCV
    "D02Z03S21", # COOLOTCV
    "D02Z03S22", # COOLOTCV
    "D02Z03S23", # COOLOTCV
    "D02Z03S24", # COOLOTCV
    "D03Z01S01", # MOTED
    "D03Z01S02", # MOTED
    "D03Z01S03", # MOTED
    "D03Z01S04", # MOTED
    "D03Z01S05", # MOTED
    "D03Z01S06", # MOTED
    "D03Z02S01", # Jondo
    "D03Z02S02", # Jondo
    "D03Z02S03", # Jondo
    "D03Z02S04", # Jondo
    "D03Z02S05", # Jondo
    "D03Z02S06", # Jondo
    "D03Z02S07", # Jondo
    "D03Z02S08", # Jondo
    "D03Z02S09", # Jondo
    "D03Z02S10", # Jondo
    "D03Z02S11", # Jondo
    "D03Z02S12", # Jondo
    "D03Z02S13", # Jondo
    "D03Z02S14", # Jondo
    "D03Z02S15", # Jondo
    "D03Z03S01", # GA
    "D03Z03S02", # GA
    "D03Z03S03", # GA
    "D03Z03S04", # GA
    "D03Z03S05", # GA
    "D03Z03S06", # GA
    "D03Z03S07", # GA
    "D03Z03S08", # GA
    "D03Z03S09", # GA
    "D03Z03S10", # GA
    "D03Z03S11", # GA
    "D03Z03S12", # GA
    "D03Z03S13", # GA
    "D03Z03S14", # GA
    "D03Z03S15", # GA
    "D03Z03S16", # GA
    "D03Z03S17", # GA
    "D03Z03S18", # GA
    "D03Z03S19", # GA
    "D04Z01S01", # POTSS
    "D04Z01S02", # POTSS
    "D04Z01S03", # POTSS
    "D04Z01S04", # POTSS
    "D04Z01S05", # POTSS
    "D04Z01S06", # POTSS
    "D04Z02S01", # MOM
    "D04Z02S02", # MOM
    "D04Z02S03", # MOM
    "D04Z02S04", # MOM
    "D04Z02S05", # MOM
    "D04Z02S06", # MOM
    "D04Z02S07", # MOM
    "D04Z02S08", # MOM
    "D04Z02S09", # MOM
    "D04Z02S10", # MOM
    "D04Z02S11", # MOM
    "D04Z02S12", # MOM
    "D04Z02S13", # MOM
    "D04Z02S14", # MOM
    "D04Z02S15", # MOM
    "D04Z02S16", # MOM
    "D04Z02S17", # MOM
    "D04Z02S19", # MOM
    "D04Z02S20", # MOM
    "D04Z02S21", # MOM
    "D04Z02S22", # MOM
    "D04Z02S23", # MOM
    "D04Z02S24", # MOM
    "D04Z02S25", # MOM
    "D04BZ02S01", # MOM - Redento
    "D04Z03S01", # KOTTW
    "D04Z03S02", # KOTTW
    "D04Z04S01", # ATTOTS
    "D04Z04S02", # ATTOTS
    "D05Z01S01", # LOTNW
    "D05Z01S02", # LOTNW
    "D05Z01S03", # LOTNW
    "D05Z01S04", # LOTNW
    "D05Z01S05", # LOTNW
    "D05Z01S06", # LOTNW
    "D05Z01S07", # LOTNW
    "D05Z01S08", # LOTNW
    "D05Z01S09", # LOTNW
    "D05Z01S10", # LOTNW
    "D05Z01S11", # LOTNW
    "D05Z01S12", # LOTNW
    "D05Z01S13", # LOTNW
    "D05Z01S14", # LOTNW
    "D05Z01S15", # LOTNW
    "D05Z01S16", # LOTNW
    "D05Z01S17", # LOTNW
    "D05Z01S18", # LOTNW
    "D05Z01S19", # LOTNW
    "D05Z01S20", # LOTNW
    "D05Z01S21", # LOTNW
    "D05Z01S22", # LOTNW
    "D05Z01S23", # LOTNW
    "D05Z01S24", # LOTNW
    "D05BZ01S01", # LOTNW - secret entrance to KOTTW?
    "D05Z02S01", # TSC
    "D05Z02S02", # TSC
    "D05Z02S03", # TSC
    "D05Z02S04", # TSC
    "D05Z02S05", # TSC
    "D05Z02S06", # TSC
    "D05Z02S07", # TSC
    "D05Z02S08", # TSC
    "D05Z02S09", # TSC
    "D05Z02S10", # TSC
    "D05Z02S11", # TSC
    "D05Z02S12", # TSC
    "D05Z02S13", # TSC
    "D05Z02S14", # TSC
    "D05Z02S15", # TSC
    "D05BZ02S01", # TSC - shop
    "D06Z01S01", # AR
    "D06Z01S02", # AR
    "D06Z01S03", # AR
    "D06Z01S04", # AR
    "D06Z01S05", # AR
    "D06Z01S06", # AR
    "D06Z01S07", # AR
    "D06Z01S08", # AR
    "D06Z01S09", # AR
    "D06Z01S10", # AR
    "D06Z01S11", # AR
    "D06Z01S12", # AR
    "D06Z01S13", # AR
    "D06Z01S14", # AR
    "D06Z01S15", # AR
    "D06Z01S16", # AR
    "D06Z01S17", # AR
    "D06Z01S18", # AR
    "D06Z01S19", # AR
    "D06Z01S20", # AR
    "D06Z01S21", # AR
    "D06Z01S22", # AR
    "D06Z01S23", # AR
    "D06Z01S24", # AR
    "D06Z01S25", # AR
    "D06Z01S26", # AR
    "D07Z01S01", # DOHH?
    "D07Z01S02", # DOHH?
    "D07Z01S03", # DOHH?
    "D08Z01S01", # BOTTC
    "D08Z01S02", # BOTTC
    "D08Z02S01", # FT
    "D08Z02S02", # FT
    "D08Z02S03", # FT
    "D08Z03S01", # HOTD
    "D08Z03S02", # HOTD
    "D08Z03S03", # HOTD
    "D09Z01S01", # WOTHP
    "D09Z01S02", # WOTHP
    "D09Z01S03", # WOTHP
    "D09Z01S04", # WOTHP
    "D09Z01S05", # WOTHP
    "D09Z01S06", # WOTHP
    "D09Z01S07", # WOTHP
    "D09Z01S08", # WOTHP
    "D09Z01S09", # WOTHP
    "D09Z01S10", # WOTHP
    "D09Z01S11", # WOTHP
    "D09Z01S12", # WOTHP
    "D09Z01S13", # WOTHP
    "D09BZ01S01", # WOTHP - all cells
    "D17Z01S01", # BOTSS
    "D17Z01S02", # BOTSS
    "D17Z01S03", # BOTSS
    "D17Z01S04", # BOTSS
    "D17Z01S05", # BOTSS
    "D17Z01S06", # BOTSS
    "D17Z01S07", # BOTSS
    "D17Z01S08", # BOTSS
    "D17Z01S09", # BOTSS
    "D17Z01S10", # BOTSS
    "D17Z01S11", # BOTSS
    "D17Z01S12", # BOTSS
    "D17Z01S13", # BOTSS
    "D17Z01S14", # BOTSS
    "D17Z01S15", # BOTSS
    "D17BZ01S01", # BOTSS - chamber of the eldest brother
    "D17BZ01S01", # BOTSS - platforming challenge
    "D20Z01S01", # EOS
    "D20Z01S02", # EOS
    "D20Z01S03", # EOS
    "D20Z01S04", # EOS
    "D20Z01S05", # EOS
    "D20Z01S06", # EOS
    "D20Z01S07", # EOS
    "D20Z01S08", # EOS
    "D20Z01S09", # EOS
    "D20Z01S10", # EOS
    "D20Z01S11", # EOS
    "D20Z01S12", # EOS
    "D20Z01S13", # EOS
    "D20Z01S14", # EOS
    "D20Z02S01", # MAH
    "D20Z02S02", # MAH
    "D20Z02S03", # MAH
    "D20Z02S04", # MAH
    "D20Z02S05", # MAH
    "D20Z02S06", # MAH
    "D20Z02S07", # MAH
    "D20Z02S08", # MAH
    "D20Z02S09", # MAH
    "D20Z02S10", # MAH
    "D20Z02S11", # MAH
    "D20Z02S12", # MAH
    "D20Z03S01", # TRPOTS
}