CHARACTER_COUNT = 14   # 14 playable characters
TERRA, LOCKE, CYAN, SHADOW, EDGAR, SABIN, CELES, STRAGO, RELM, SETZER, MOG, GAU, GOGO, UMARO = range(CHARACTER_COUNT)
SOLDIER, IMP, GENERAL_LEO, BANON_DUNCAN, ESPER_TERRA, MERCHANT, GHOST, KEFKA = range(CHARACTER_COUNT, 22)

id_character = {
    0   : "TERRA",
    1   : "LOCKE",
    2   : "CYAN",
    3   : "SHADOW",
    4   : "EDGAR",
    5   : "SABIN",
    6   : "CELES",
    7   : "STRAGO",
    8   : "RELM",
    9   : "SETZER",
    10  : "MOG",
    11  : "GAU",
    12  : "GOGO",
    13  : "UMARO",
}
character_id = {v: k for k, v in id_character.items()}

id_name = id_character.copy()
id_name.update({
    14  : "Soldier",
    15  : "Imp",
    16  : "General Leo",
    17  : "Banon/Duncan",
    18  : "Esper Terra",
    19  : "Merchant",
    20  : "Ghost",
    21  : "Kefka",
})
name_id = {v: k for k, v in id_name.items()}

sorted_character_names = sorted(list(character_id))
