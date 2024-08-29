from worlds.ff4fe import FF4FEOptions


def create_flags_from_options(options: FF4FEOptions):
    flags = (f"{build_objective_flags(options)} "
             f"Kmain/summon/moon/unsafe "
             f"{build_pass_flags(options)}"
             f"{build_characters_flags(options)}"
             f"Twild/junk "
             f"Swild "
             f"Bstandard/alt:gauntlet/whichburn "
             f"Etoggle/keep:doors,behemoths "
             f"Gdupe/mp/warp/life/sylph/backrow "
             f"-spoon")
    return flags

def build_objective_flags(options: FF4FEOptions):
    objective_flags = "Onone"
    if options.DarkMatterHunt.current_key == "true":
        objective_flags = f"Omode:dkmatter"
    return objective_flags

def build_key_items_flags(options: FF4FEOptions):
    pass

def build_pass_flags(options: FF4FEOptions):
    pass_flags = ""
    pass_key_flags = ""
    pass_shop_flags = ""
    if options.PassEnabled.current_key == "true":
        pass_key_flags = f"key"
    if options.PassInShops.current_key == "true":
        pass_shop_flags = f"shop"
    if pass_key_flags != "" and pass_shop_flags != "":
        pass_flags = f"P{pass_key_flags}/{pass_shop_flags}"
    elif pass_key_flags == "" and pass_shop_flags == "":
        pass_flags = " "
    else:
        pass_flags = (f"P{pass_key_flags}{pass_shop_flags}")
    return pass_flags

def build_characters_flags(options: FF4FEOptions):
    hero_challenge_flags = ""
    if options.HeroChallenge.current_key != "none":
        hero_challenge_flags = f"hero/start:{options.HeroChallenge.current_key.lower()}/"
    free_character_flags = ""
    if options.NoFreeCharacters.current_key == "true":
        free_character_flags += "nofree/"
    if options.NoEarnedCharacters.current_key == "true":
        free_character_flags += "noearned/"
    flags = f"Crelaxed/{hero_challenge_flags}{free_character_flags}j:spells,abilities"
    return flags

def build_treasures_flags(options: FF4FEOptions):
    pass

def build_shops_flags(options: FF4FEOptions):
    pass

def build_bosses_flags(options: FF4FEOptions):
    pass

def build_encounters_flags(options: FF4FEOptions):
    pass

def build_glitches_flags(options: FF4FEOptions):
    pass

def build_other_flags(options: FF4FEOptions):
    pass