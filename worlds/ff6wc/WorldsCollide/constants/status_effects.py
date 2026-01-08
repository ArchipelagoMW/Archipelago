class A:
    id_name = {
        0   : "Dark",
        1   : "Zombie",
        2   : "Poison",
        3   : "Magitek",
        4   : "Clear",
        5   : "Imp",
        6   : "Petrify",
        7   : "Death",
    }
    name_id = {v: k for k, v in id_name.items()}

class B:
    id_name = {
        0   : "Condemned",
        1   : "Near Fatal",
        2   : "Image",
        3   : "Mute",
        4   : "Berserk",
        5   : "Muddle",
        6   : "Seizure",
        7   : "Sleep",
    }
    name_id = {v: k for k, v in id_name.items()}

class C:
    id_name = {
        0   : "Dance", # float
        1   : "Regen",
        2   : "Slow",
        3   : "Haste",
        4   : "Stop",
        5   : "Shell",
        6   : "Safe",
        7   : "Reflect",
    }
    name_id = {v: k for k, v in id_name.items()}

class D:
    id_name = {
        0   : "Rage",
        1   : "Freeze",
        2   : "Life 3",
        3   : "Morph",
        4   : "Chant",
        5   : "Hide",
        6   : "Dog Block",
        7   : "Float",
    }
    name_id = {v: k for k, v in id_name.items()}

class PhantasmOvercast:
    id_name = {
        1   : "Overcast",
        6   : "Phantasm",
    }
    name_id = {v: k for k, v in id_name.items()}
