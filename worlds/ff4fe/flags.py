from worlds.ff4fe import FF4FEOptions


def create_flags_from_options(options: FF4FEOptions):
    flags = (f"{build_objective_flags(options)} "
             f"Kmain/summon/moon/unsafe "
             f"{build_pass_flags(options)} "
             f"{build_characters_flags(options)} "
             f"Twild/junk "
             f"{build_shops_flags(options)} "
             f"Bstandard/alt:gauntlet/whichburn "
             f"Etoggle/keep:doors,behemoths "
             f"Gdupe/mp/warp/life/sylph/backrow "
             f"-spoon "
             f"{build_starter_kit_flags(options)}")
    return flags

def build_objective_flags(options: FF4FEOptions):
    objective_flags = "Omode:"
    primary_objectives = []
    if options.ForgeTheCrystal.current_key == "true":
        primary_objectives.append("classicforge")
    if options.ConquerTheGiant.current_key == "true":
        primary_objectives.append("classicgiant")
    if options.DefeatTheFiends.current_key == "true":
        primary_objectives.append("fiends")
    if options.FindTheDarkMatter.current_key == "true":
        primary_objectives.append("dkmatter")
    objective_flags += ",".join(primary_objectives)
    if objective_flags == "Omode:":
        objective_flags += "none/"
    else:
        objective_flags += "/"
    if options.AdditionalObjectives.value != 0:
        objective_flags += f"random:{options.AdditionalObjectives.value}"
    if options.ObjectiveReward.current_key == "crystal" or options.ForgeTheCrystal.current_key == "true":
        objective_flags += "/win:crystal/req:all"
    else:
        objective_flags += "/win:game/req:all"
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
    party_size_flags = f"Cparty:{options.PartySize}/"
    hero_challenge_flags = ""
    if options.HeroChallenge.current_key != "none":
        hero_challenge_flags = f"hero/start:{options.HeroChallenge.current_key.lower()}/"
    free_character_flags = ""
    if options.NoFreeCharacters.current_key == "true":
        free_character_flags += "nofree/"
    if options.NoEarnedCharacters.current_key == "true":
        free_character_flags += "noearned/"
    duplicate_character_flags = ""
    if options.AllowDuplicateCharacters.current_key == "false":
        duplicate_character_flags += "nodupes/"
    permajoin_flags = ""
    if options.CharactersPermajoin.current_key == "true":
        permajoin_flags = "permajoin/"
    permadeath_flags = ""
    if options.CharactersPermajoin.current_key == "yes":
        permadeath_flags = "permadeath/"
    if options.CharactersPermajoin.current_key == "extreme":
        permadeath_flags = "permadeader/"
    flags = (f"{party_size_flags}{hero_challenge_flags}"
             f"{free_character_flags}{duplicate_character_flags}"
             f"{permajoin_flags}{permadeath_flags}j:spells,abilities")
    return flags

def build_treasures_flags(options: FF4FEOptions):
    pass

def build_shops_flags(options: FF4FEOptions):
    shops_flags = f"Sempty"
    if options.ShopRandomization.current_key == "vanilla":
        shops_flags = f"Svanilla"
    elif options.ShopRandomization.current_key == "shuffle":
        shops_flags = f"Sshuffle"
    elif options.ShopRandomization.current_key == "standard":
        shops_flags = f"Sstandard"
    elif options.ShopRandomization.current_key == "pro":
        shops_flags = f"Spro"
    elif options.ShopRandomization.current_key == "wild":
        shops_flags = f"Swild"
    elif options.ShopRandomization.current_key == "cabins":
        shops_flags = f"Scabins"
    if options.FreeShops.current_key == "true":
        shops_flags += "/free"
    return shops_flags

def build_bosses_flags(options: FF4FEOptions):
    pass

def build_encounters_flags(options: FF4FEOptions):
    pass

def build_glitches_flags(options: FF4FEOptions):
    pass

def build_other_flags(options: FF4FEOptions):
    pass

def build_starter_kit_flags(options: FF4FEOptions):
    kit1 = process_kit_name(options.StarterKitOne.current_key)
    kit2 = process_kit_name(options.StarterKitTwo.current_key)
    kit3 = process_kit_name(options.StarterKitThree.current_key)
    if kit1 == "none":
        kit1 = ""
    else:
        kit1 = f"-kit:{kit1}"
    if kit2 == "none":
        kit2 = ""
    else:
        kit2 = f"-kit2:{kit2}"
    if kit3 == "none":
        kit3 = ""
    else:
        kit3 = f"-kit3:{kit3}"
    return f"{kit1} {kit2} {kit3}"


def process_kit_name(kit: str):
    if kit == "grab_bag":
        return "grabbag"
    elif kit == "MIAB":
        return "miab"
    elif kit == "not_deme":
        return "notdeme"
    elif kit == "green_names":
        return "green"
    elif kit == "random_kit":
        return "random"
    else:
        return kit