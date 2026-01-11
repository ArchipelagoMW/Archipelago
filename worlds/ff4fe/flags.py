from . import FF4FEOptions
# This file just translates our AP options into FE flagsets.

def create_flags_from_options(options: FF4FEOptions, objective_count: int):
    flags = (f"{build_objective_flags(options, objective_count)} "
             f"Kmain/summon/moon/unsafe/miab "
             f"{build_pass_flags(options)} "
             f"{build_characters_flags(options)} "
             f"Twild/junk "
             f"{build_shops_flags(options)} "
             f"{build_bosses_flags(options)} "
             f"{build_encounters_flags(options)} "
             f"Gdupe/mp/warp/life/sylph/backrow "
             f"{build_misc_flags(options)}"
             f"{build_starter_kit_flags(options)}")
    return flags

def build_objective_flags(options: FF4FEOptions, objective_count: int):
    objective_flags = "Omode:"
    primary_objectives = []
    if options.ForgeTheCrystal:
        primary_objectives.append("classicforge")
    if options.ConquerTheGiant:
        primary_objectives.append("classicgiant")
    if options.DefeatTheFiends:
        primary_objectives.append("fiends")
    if options.FindTheDarkMatter:
        primary_objectives.append("dkmatter")
    objective_flags += ",".join(primary_objectives)
    if objective_flags == "Omode:":
        objective_flags += "none"
    if options.AdditionalObjectives.value != 0:
        objective_flags += f"/random:{options.AdditionalObjectives.value}"
    if options.ObjectiveReward.current_key == "crystal" or options.ForgeTheCrystal:
        objective_flags += "/win:crystal"
    else:
        objective_flags += "/win:game"
    objective_flags += f"/req:{min(objective_count, options.RequiredObjectiveCount.value)}"
    return objective_flags

def build_key_items_flags(options: FF4FEOptions):
    pass

def build_pass_flags(options: FF4FEOptions):
    pass_flags = ""
    pass_key_flags = ""
    pass_shop_flags = ""
    if options.PassEnabled:
        pass_key_flags = f"key"
    if options.PassInShops:
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
    if options.NoFreeCharacters:
        free_character_flags += "nofree/"
    if options.NoEarnedCharacters:
        free_character_flags += "noearned/"
    duplicate_character_flags = ""
    if not options.AllowDuplicateCharacters:
        duplicate_character_flags += "nodupes/"
    permajoin_flags = ""
    if options.CharactersPermajoin:
        permajoin_flags = "permajoin/"
    permadeath_flags = ""
    if options.CharactersPermadie.current_key == "yes":
        permadeath_flags = "permadeath/"
    if options.CharactersPermadie.current_key == "extreme":
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
    if options.FreeShops:
        shops_flags += "/free"
    if options.JItems == options.JItems.option_no_shops or options.JItems == options.JItems.option_none:
        shops_flags += "/no:j"
    return shops_flags

def build_bosses_flags(options: FF4FEOptions):
    bosses_flags = "Bstandard/alt:gauntlet/whichburn"
    if options.NoFreeBosses:
        bosses_flags += "/nofree"
    return bosses_flags

def build_encounters_flags(options: FF4FEOptions):
    encounters_flags = "Etoggle"
    if options.KeepDoorsBehemoths:
        encounters_flags += "/keep:doors,behemoths"
    return encounters_flags

def build_glitches_flags(options: FF4FEOptions):
    pass

def build_misc_flags(options: FF4FEOptions):
    spoon_flag = "-spoon"
    adamant_flag = "-noadamants" if options.NoAdamantArmors else ""
    wacky_flag = process_wacky_name(options.WackyChallenge.current_key)
    return f"{spoon_flag} {adamant_flag} {wacky_flag}"

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

def process_wacky_name(wacky: str):
    wacky_flag = ""
    if wacky == "none":
        return wacky_flag
    wacky_flag = "-wacky:"
    if wacky == "battle_scars":
        wacky_flag += "battlescars"
    elif wacky == "the_bodyguard":
        wacky_flag += "bodyguard"
    elif wacky == "enemy_unknown":
        wacky_flag += "enemyunknown"
    elif wacky == "ff4_the_musical":
        wacky_flag += "musical"
    elif wacky == "fist_fight":
        wacky_flag += "fistfight"
    elif wacky == "the_floor_is_made_of_lava":
        wacky_flag += "floorislava"
    elif wacky == "forward_is_the_new_back":
        wacky_flag += "forwardisback"
    elif wacky == "friendly_fire":
        wacky_flag += "friendlyfire"
    elif wacky == "gotta_go_fast":
        wacky_flag += "gottagofast"
    elif wacky == "holy_onomatopoeia_batman":
        wacky_flag += "batman"
    elif wacky == "imaginary_numbers":
        wacky_flag += "imaginarynumbers"
    elif wacky == "is_this_even_randomized":
        wacky_flag += "isthisrandomized"
    elif wacky == "men_are_pigs":
        wacky_flag += "menarepigs"
    elif wacky == "a_much_bigger_magnet":
        wacky_flag += "biggermagnet"
    elif wacky == "mystery_juice":
        wacky_flag += "mysteryjuice"
    elif wacky == "neat_freak":
        wacky_flag += "neatfreak"
    elif wacky == "night_mode":
        wacky_flag += "nightmode"
    elif wacky == "payable_golbez":
        wacky_flag += "payablegolbez"
    elif wacky == "save_us_big_chocobo":
        wacky_flag += "saveusbigchocobo"
    elif wacky == "six_legged_race":
        wacky_flag += "sixleggedrace"
    elif wacky == "the_sky_warriors":
        wacky_flag += "skywarriors"
    elif wacky == "three_point_system":
        wacky_flag += "3point"
    elif wacky == "time_is_money":
        wacky_flag += "timeismoney"
    elif wacky == "world_championship_of_darts":
        wacky_flag += "darts"
    elif wacky == "random_challenge":
        wacky_flag += "random"
    else:
        wacky_flag += wacky
    return wacky_flag