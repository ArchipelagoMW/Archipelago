import os
import warnings
import pygbagfx # from package

POKEMON_FOLDERS = ["Machoke", "Nuzleaf", "Crobat", "Gloom", "Houndour", "Hypno", "Magcargo", "Noctowl", "Salamence", "Goldeen", "Whismur", "Diglett", "Lickitung", "Trapinch", "Omastar", "Roselia", "Wobbuffet", "Anorith", "Pineco", "Quilava", "Butterfree", "Gastly", "Magneton", "Deoxys", "Mareep", "Drowzee", "Cleffa", "Carvanha", "Snorunt", "Omanyte", "Articuno", "Unown", "Entei", "Sandshrew", "Gengar", "Sentret", "Igglybuff", "Chimecho", "Hoppip", "Snubbull", "Chinchou", "Gulpin", "Altaria", "Hitmontop", "Gligar", "Parasect", "Ho-Oh", "Eevee", "Alakazam", "Shuppet", "Weepinbell", "Poliwag", "Hariyama", "Chansey", "Shelgon", "Staryu", "Swalot", "Torkoal", "Walrein", "Jirachi", "Skiploom", "Nosepass", "Venonat", "Misdreavus", "Dratini", "Pidgeotto", "Electrike", "Plusle", "Ninetales", "Lombre", "Ludicolo", "Lapras", "Cloyster", "Kingdra", "Golbat", "Phanpy", "Jumpluff", "Combusken", "Zubat", "Breloom", "Mankey", "Sunflora", "Slakoth", "Granbull", "Kyogre", "Pikachu", "Zigzagoon", "Moltres", "Mewtwo", "Octillery", "Ekans", "Larvitar", "Ivysaur", "Spearow", "Ninjask", "Shellder", "Chikorita", "Illumise", "Weedle", "Silcoon", "Raticate", "Gorebyss", "Meowth", "Starmie", "Marill", "Makuhita", "Graveler", "Shiftry", "Machamp", "Castform", "Delcatty", "Paras", "Exeggcute", "Aggron", "Nincada", "Persian", "Clefairy", "Croconaw", "Minun", "Magikarp", "Tauros", "Ursaring", "Seedot", "Tyranitar", "Corsola", "Wailmer", "Shuckle", "Heracross", "Registeel", "Qwilfish", "Bellsprout", "Ledian", "Clefable", "Dugtrio", "Machop", "Seel", "Doduo", "Groudon", "Nidoran Male", "Regice", "Wingull", "Teddiursa", "Jolteon", "Totodile", "Mantine", "Magmar", "Wurmple", "Rattata", "Pupitar", "Beautifly", "Spinarak", "Swablu", "Mightyena", "Tropius", "Hitmonchan", "Zangoose", "Donphan", "Hoothoot", "Marowak", "Solrock", "Cascoon", "Metapod", "Houndoom", "Steelix", "Psyduck", "Duskull", "Caterpie", "Rapidash", "Beedrill", "Exeggutor", "Milotic", "Mew", "Shroomish", "Elekid", "Growlithe", "Onix", "Dewgong", "Bayleef", "Luvdisc", "Slugma", "Cubone", "Kabuto", "Umbreon", "Feraligatr", "Azurill", "Wailord", "Seaking", "Aerodactyl", "Marshtomp", "Mr. Mime", "Muk", "Blastoise", "Gardevoir", "Gyarados", "Aipom", "Jigglypuff", "Oddish", "Vigoroth", "Whiscash", "Spinda", "Weezing", "Yanma", "Girafarig", "Scyther", "Golem", "Surskit", "Dragonair", "Piloswine", "Slowbro", "Absol", "Grimer", "Sceptile", "Electrode", "Sunkern", "Seadra", "Dragonite", "Sableye", "Squirtle", "Forretress", "Jynx", "Wynaut", "Pelipper", "Kecleon", "Arcanine", "Linoone", "Smeargle", "Dodrio", "Lugia", "Cacturne", "Claydol", "Politoed", "Flaaffy", "Swellow", "Tangela", "Torchic", "Raichu", "Natu", "Ponyta", "Poliwhirl", "Haunter", "Pichu", "Pidgey", "Dustox", "Pidgeot", "Shedinja", "Wooper", "Barboach", "Kakuna", "Togetic", "Loudred", "Lanturn", "Bagon", "Lairon", "Charizard", "Nidoking", "Flygon", "Kingler", "Scizor", "Magnemite", "Vileplume", "Venomoth", "Pinsir", "Flareon", "Nidorino", "Spoink", "Feebas", "Wigglytuff", "Primeape", "Abra", "Skarmory", "Skitty", "Ariados", "Charmander", "Slowking", "Sandslash", "Electabuzz", "Glalie", "Cacnea", "Sharpedo", "Lileep", "Vibrava", "Cyndaquil", "Clamperl", "Koffing", "Fearow", "Porygon2", "Tyrogue", "Charmeleon", "Vaporeon", "Kadabra", "Slowpoke", "Ralts", "Meditite", "Spheal", "Arbok", "Bellossom", "Banette", "Murkrow", "Kirlia", "Mawile", "Swampert", "Huntail", "Poochyena", "Sealeo", "Victreebel", "Grovyle", "Ampharos", "Espeon", "Cradily", "Metang", "Stantler", "Geodude", "Lotad", "Suicune", "Meganium", "Ditto", "Relicanth", "Rhydon", "Medicham", "Quagsire", "Treecko", "Camerupt", "Xatu", "Sudowoodo", "Miltank", "Tentacruel", "Azumarill", "Typhlosion", "Venusaur", "Armaldo", "Swinub", "Dusclops", "Regirock", "Farfetch'd", "Kangaskhan", "Snorlax", "Metagross", "Wartortle", "Furret", "Tentacool", "Nidorina", "Delibird", "Bulbasaur", "Smoochum", "Rhyhorn", "Aron", "Blissey", "Sneasel", "Beldum", "Nidoqueen", "Zapdos", "Poliwrath", "Mudkip", "Crawdaunt", "Celebi", "Remoraid", "Exploud", "Masquerain", "Togepi", "Horsea", "Seviper", "Kabutops", "Slaking", "Grumpig", "Krabby", "Volbeat", "Nidoran Female", "Ledyba", "Lunatone", "Magby", "Vulpix", "Porygon", "Voltorb", "Blaziken", "Taillow", "Raikou", "Numel", "Golduck", "Manectric", "Baltoy", "Dunsparce", "Hitmonlee", "Latias", "Latios", "Rayquaza", "Corphish"]
POKEMON_SPRITES = ["front_anim", "front", "back", "icon", "footprint"]
POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY = ["palette", "front_anim", "front", "back"]
POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY = ["shiny_palette"]
POKEMON_PALETTES = {
    "palette": POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "shiny_palette": POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY
}

TRAINER_FOLDERS = ["Brendan", "May"]
TRAINER_SPRITES = ["walking_running", "surfing", "acro_bike", "mach_bike", "underwater", "field_move", "fishing", "watering", "decorating", "battle_front", "battle_back"]
TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ["palette", "walking_running", "surfing", "acro_bike", "mach_bike", "fishing", "watering", "decorating"]
TRAINER_BATTLE_PALETTE_EXTRACTION_PRIORITY = ["battle_palette", "battle_front", "battle_back"]
TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY = ["reflection_palette"]
TRAINER_PALETTES = {
    "palette": TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "battle_palette": TRAINER_BATTLE_PALETTE_EXTRACTION_PRIORITY,
    "reflection_palette": TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY
}

SPRITE_KEY_TO_ADDRESS_LABEL = {
    "pokemon_front_anim": "gMonFrontPic_OBJECT",
    "pokemon_front": "gMonStillFrontPic_OBJECT",
    "pokemon_back": "gMonBackPic_OBJECT",
    "pokemon_icon": "gMonIcon_OBJECT",
    "pokemon_footprint": "gMonFootprint_OBJECT",

    "pokemon_palette": "gMonPalette_OBJECT",
    "pokemon_shiny_palette": "gMonShinyPalette_OBJECT",

    "trainer_walking_running": "gObjectEventPic_OBJECTNormal",
    "trainer_surfing": "gObjectEventPic_OBJECTSurfing",
    "trainer_acro_bike": "gObjectEventPic_OBJECTAcroBike",
    "trainer_mach_bike": "gObjectEventPic_OBJECTMachBike",
    "trainer_underwater": "gObjectEventPic_OBJECTUnderwater",
    "trainer_field_move": "gObjectEventPic_OBJECTFieldMove",
    "trainer_fishing": "gObjectEventPic_OBJECTFishing",
    "trainer_watering": "gObjectEventPic_OBJECTWatering",
    "trainer_decorating": "gObjectEventPic_OBJECTDecorating",
    "trainer_battle_front": "gTrainerFrontPic_OBJECT",
    "trainer_battle_back": "gTrainerBackPic_OBJECT",

    "trainer_palette": "gObjectEventPal_OBJECT",
    "trainer_battle_palette": "gTrainerPalette_OBJECT",
    "trainer_reflection_palette": "gObjectEventPal_OBJECTReflection",
}
address_label_to_resource_path_list = { }

def handle_sprite_pack(_sprite_pack_path):
    for pokemon_name in POKEMON_FOLDERS:
        pokemon_folder_path = os.path.join(_sprite_pack_path, pokemon_name)
        if os.path.exists(pokemon_folder_path):
            handle_pokemon_folder(pokemon_folder_path, pokemon_name)
    for trainer_name in TRAINER_FOLDERS:
        trainer_folder_path = os.path.join(_sprite_pack_path, trainer_name)
        if os.path.exists(trainer_folder_path):
            handle_trainer_folder(trainer_folder_path, trainer_name)

def handle_pokemon_folder(_pokemon_folder_path, _pokemon_name):
    for sprite_name in POKEMON_SPRITES:
        sprite_path = os.path.join(_pokemon_folder_path, sprite_name) + ".png"
        if os.path.exists(sprite_path):
            link_resource_to_address(True, _pokemon_name, sprite_name, handle_sprite_to_gba_sprite(sprite_path))
    for palette, palette_extraction_priority_queue in POKEMON_PALETTES.items():
        palette_extracted = False
        for sprite_name in palette_extraction_priority_queue:
            sprite_path = os.path.join(_pokemon_folder_path, sprite_name) + ".png"
            if os.path.exists(sprite_path):
                link_resource_to_address(True, _pokemon_name, palette, handle_sprite_to_palette(sprite_path))
                palette_extracted = True
                break
        if not palette_extracted:
            warnings.warn(f"Could not generate the palette \"{palette}\" for the Pokemon \"{_pokemon_name}\".")

def handle_trainer_folder(_trainer_folder_path, _trainer_name):
    for sprite_name in TRAINER_SPRITES:
        sprite_path = os.path.join(_trainer_folder_path, sprite_name) + ".png"
        if os.path.exists(sprite_path):
            link_resource_to_address(False, _trainer_name, sprite_name, handle_sprite_to_gba_sprite(sprite_path))
    for palette, palette_extraction_priority_queue in TRAINER_PALETTES.items():
        palette_extracted = False
        for sprite_name in palette_extraction_priority_queue:
            sprite_path = os.path.join(_trainer_folder_path, sprite_name) + ".png"
            if os.path.exists(sprite_path):
                link_resource_to_address(False, _trainer_name, palette, handle_sprite_to_palette(sprite_path))
                palette_extracted = True
                break
        if not palette_extracted:
            warnings.warn(f"Could not generate the palette \"{palette}\" for the Trainer \"{_trainer_name}\".")


def handle_sprite_to_gba_sprite(_sprite_path) -> str:
    sprite_path_with_no_extension = os.path.splitext(_sprite_path)[0]
    file_format = ".1bpp" if sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    gba_sprite_path = sprite_path_with_no_extension + file_format
    compressed_gba_sprite_path = gba_sprite_path + ".lz"
    call_gbagfx(_sprite_path, gba_sprite_path, False)
    call_gbagfx(gba_sprite_path, compressed_gba_sprite_path, True)
    return compressed_gba_sprite_path

def handle_sprite_to_palette(_sprite_path) -> str:
    sprite_path_with_no_extension = os.path.splitext(_sprite_path)[0]
    palette_path = sprite_path_with_no_extension + ".pal"
    gba_palette_path = sprite_path_with_no_extension + ".gbapal"
    compressed_gba_palette_path = gba_palette_path + ".lz"
    call_gbagfx(_sprite_path, palette_path, False)
    call_gbagfx(palette_path, gba_palette_path, True)
    call_gbagfx(gba_palette_path, compressed_gba_palette_path, True)
    return compressed_gba_palette_path

def call_gbagfx(_input, _output, _delete_input = False):
    pygbagfx.main(_input, _output)
    if _delete_input:
        os.remove(_input)

def link_resource_to_address(_is_pokemon, _object_name, _sprite_name, _path):
    sprite_key = ("pokemon" if _is_pokemon else "trainer") + "_" + _sprite_name
    address_label = SPRITE_KEY_TO_ADDRESS_LABEL[sprite_key]
    address_label.replace("OBJECT", _object_name)
    address_label_to_resource_path_list[address_label] = _path

# TODO: Find a good IPS library and build the patch