"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage locations in the Aquaria game multiworld randomizer
"""

from BaseClasses import Location


class AquariaLocation(Location):
    """
    A location in the game.
    """
    game: str = "Aquaria"
    """The name of the game"""

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        """
        Initialisation of the object
        :param player: the ID of the player
        :param name: the name of the location
        :param code: the ID (or address) of the location (Event if None)
        :param parent: the Region that this location belongs to
        """
        super(AquariaLocation, self).__init__(player, name, code, parent)
        self.event = code is None


class AquariaLocations:

    locations_verse_cave_r = {
        "Verse Cave, bulb in the skeleton room": 698107,
        "Verse Cave, bulb in the path right of the skeleton room": 698108,
        "Verse Cave right area, Big Seed": 698175,
    }

    locations_verse_cave_l = {
        "Verse Cave, the Naija hint about the shield ability": 698200,
        "Verse Cave left area, bulb in the center part": 698021,
        "Verse Cave left area, bulb in the right part": 698022,
        "Verse Cave left area, bulb under the rock at the end of the path": 698023,
    }

    locations_home_water = {
        "Home Water, bulb below the grouper fish": 698058,
        "Home Water, bulb in the path below Nautilus Prime": 698059,
        "Home Water, bulb in the little room above the grouper fish": 698060,
        "Home Water, bulb in the end of the path close to the Verse Cave": 698061,
        "Home Water, bulb in the top left path": 698062,
        "Home Water, bulb in the bottom left room": 698063,
        "Home Water, bulb close to Naija's Home": 698064,
        "Home Water, bulb under the rock in the left path from the Verse Cave": 698065,
    }

    locations_home_water_nautilus = {
        "Home Water, Nautilus Egg": 698194,
    }

    locations_home_water_transturtle = {
        "Home Water, Transturtle": 698213,
    }

    locations_naija_home = {
        "Naija's Home, bulb after the energy door": 698119,
        "Naija's Home, bulb under the rock at the right of the main path": 698120,
    }

    locations_song_cave = {
        "Song Cave, Erulian spirit": 698206,
        "Song Cave, bulb in the top right part": 698071,
        "Song Cave, bulb in the big anemone room": 698072,
        "Song Cave, bulb in the path to the singing statues": 698073,
        "Song Cave, bulb under the rock in the path to the singing statues": 698074,
        "Song Cave, bulb under the rock close to the song door": 698075,
        "Song Cave, Verse Egg": 698160,
        "Song Cave, Jelly Beacon": 698178,
        "Song Cave, Anemone Seed": 698162,
    }

    locations_energy_temple_1 = {
        "Energy Temple first area, beating the Energy Statue": 698205,
        "Energy Temple first area, bulb in the bottom room blocked by a rock": 698027,
    }

    locations_energy_temple_idol = {
        "Energy Temple first area, Energy Idol": 698170,
    }

    locations_energy_temple_2 = {
        "Energy Temple second area, bulb under the rock": 698028,
    }

    locations_energy_temple_altar = {
        "Energy Temple bottom entrance, Krotite Armor": 698163,
    }

    locations_energy_temple_3 = {
        "Energy Temple third area, bulb in the bottom path": 698029,
    }

    locations_energy_temple_boss = {
        "Energy Temple boss area, Fallen God Tooth": 698169,
    }

    locations_energy_temple_blaster_room = {
        "Energy Temple blaster room, Blaster Egg": 698195,
    }

    locations_openwater_tl = {
        "Open Water top left area, bulb under the rock in the right path": 698001,
        "Open Water top left area, bulb under the rock in the left path": 698002,
        "Open Water top left area, bulb to the right of the save crystal": 698003,
    }

    locations_openwater_tr = {
        "Open Water top right area, bulb in the small path before Mithalas": 698004,
        "Open Water top right area, bulb in the path from the left entrance": 698005,
        "Open Water top right area, bulb in the clearing close to the bottom exit": 698006,
        "Open Water top right area, bulb in the big clearing close to the save crystal": 698007,
        "Open Water top right area, bulb in the big clearing to the top exit": 698008,
        "Open Water top right area, first urn in the Mithalas exit": 698148,
        "Open Water top right area, second urn in the Mithalas exit": 698149,
        "Open Water top right area, third urn in the Mithalas exit": 698150,
    }

    locations_openwater_tr_turtle = {
        "Open Water top right area, bulb in the turtle room": 698009,
        "Open Water top right area, Transturtle": 698211,
    }

    locations_openwater_bl = {
        "Open Water bottom left area, bulb behind the chomper fish": 698011,
        "Open Water bottom left area, bulb inside the lowest fish pass": 698010,
    }

    locations_skeleton_path = {
        "Open Water skeleton path, bulb close to the right exit": 698012,
        "Open Water skeleton path, bulb behind the chomper fish": 698013,
    }

    locations_skeleton_path_sc = {
        "Open Water skeleton path, King Skull": 698177,
    }

    locations_arnassi = {
        "Arnassi Ruins, bulb in the right part": 698014,
        "Arnassi Ruins, bulb in the left part": 698015,
        "Arnassi Ruins, bulb in the center part": 698016,
        "Arnassi Ruins, Song Plant Spore": 698179,
        "Arnassi Ruins, Arnassi Armor": 698191,
    }

    locations_arnassi_path = {
        "Arnassi Ruins, Arnassi Statue": 698164,
    }

    locations_arnassi_cave_transturtle = {
        "Arnassi Ruins, Transturtle": 698217,
    }

    locations_arnassi_crab_boss = {
        "Arnassi Ruins, Crab Armor": 698187,
    }

    locations_simon = {
        "Simon Says area, beating Simon Says": 698156,
        "Simon Says area, Transturtle": 698216,
    }

    locations_mithalas_city = {
        "Mithalas City, first bulb in the left city part": 698030,
        "Mithalas City, second bulb in the left city part": 698035,
        "Mithalas City, bulb in the right part": 698031,
        "Mithalas City, bulb at the top of the city": 698033,
        "Mithalas City, first bulb in a broken home": 698034,
        "Mithalas City, second bulb in a broken home": 698041,
        "Mithalas City, bulb in the bottom left part": 698037,
        "Mithalas City, first bulb in one of the homes": 698038,
        "Mithalas City, second bulb in one of the homes": 698039,
        "Mithalas City, first urn in one of the homes": 698123,
        "Mithalas City, second urn in one of the homes": 698124,
        "Mithalas City, first urn in the city reserve": 698125,
        "Mithalas City, second urn in the city reserve": 698126,
        "Mithalas City, third urn in the city reserve": 698127,
    }

    locations_mithalas_city_top_path = {
        "Mithalas City, first bulb at the end of the top path": 698032,
        "Mithalas City, second bulb at the end of the top path": 698040,
        "Mithalas City, bulb in the top path": 698036,
        "Mithalas City, Mithalas Pot": 698174,
        "Mithalas City, urn in the Castle flower tube entrance": 698128,
    }

    locations_mithalas_city_fishpass = {
        "Mithalas City, Doll": 698173,
        "Mithalas City, urn inside a home fish pass": 698129,
    }

    locations_cathedral_l = {
        "Mithalas City Castle, bulb in the flesh hole": 698042,
        "Mithalas City Castle, Blue Banner": 698165,
        "Mithalas City Castle, urn in the bedroom": 698130,
        "Mithalas City Castle, first urn of the single lamp path": 698131,
        "Mithalas City Castle, second urn of the single lamp path": 698132,
        "Mithalas City Castle, urn in the bottom room": 698133,
        "Mithalas City Castle, first urn on the entrance path": 698134,
        "Mithalas City Castle, second urn on the entrance path": 698135,
    }

    locations_cathedral_l_tube = {
        "Mithalas City Castle, beating the Priests": 698208,
    }

    locations_cathedral_l_sc = {
        "Mithalas City Castle, Trident Head": 698183,
    }

    locations_cathedral_r = {
        "Mithalas Cathedral, first urn in the top right room": 698136,
        "Mithalas Cathedral, second urn in the top right room": 698137,
        "Mithalas Cathedral, third urn in the top right room": 698138,
        "Mithalas Cathedral, urn in the flesh room with fleas": 698139,
        "Mithalas Cathedral, first urn in the bottom right path": 698140,
        "Mithalas Cathedral, second urn in the bottom right path": 698141,
        "Mithalas Cathedral, urn behind the flesh vein": 698142,
        "Mithalas Cathedral, urn in the top left eyes boss room": 698143,
        "Mithalas Cathedral, first urn in the path behind the flesh vein": 698144,
        "Mithalas Cathedral, second urn in the path behind the flesh vein": 698145,
        "Mithalas Cathedral, third urn in the path behind the flesh vein": 698146,
        "Mithalas Cathedral, fourth urn in the top right room": 698147,
        "Mithalas Cathedral, Mithalan Dress": 698189,
        "Mithalas Cathedral, urn below the left entrance": 698198,
    }

    locations_cathedral_underground = {
        "Cathedral Underground, bulb in the center part": 698113,
        "Cathedral Underground, first bulb in the top left part": 698114,
        "Cathedral Underground, second bulb in the top left part": 698115,
        "Cathedral Underground, third bulb in the top left part": 698116,
        "Cathedral Underground, bulb close to the save crystal": 698117,
        "Cathedral Underground, bulb in the bottom right path": 698118,
    }

    locations_cathedral_boss = {
        "Mithalas boss area, beating Mithalan God": 698202,
    }

    locations_forest_tl = {
        "Kelp Forest top left area, bulb in the bottom left clearing": 698044,
        "Kelp Forest top left area, bulb in the path down from the top left clearing": 698045,
        "Kelp Forest top left area, bulb in the top left clearing": 698046,
        "Kelp Forest top left area, Jelly Egg": 698185,
    }

    locations_forest_tl_fp = {
        "Kelp Forest top left area, bulb close to the Verse Egg": 698047,
        "Kelp Forest top left area, Verse Egg": 698158,
    }

    locations_forest_tr = {
        "Kelp Forest top right area, bulb under the rock in the right path": 698048,
        "Kelp Forest top right area, bulb at the left of the center clearing": 698049,
        "Kelp Forest top right area, bulb in the left path's big room": 698051,
        "Kelp Forest top right area, bulb in the left path's small room": 698052,
        "Kelp Forest top right area, bulb at the top of the center clearing": 698053,
        "Kelp Forest top right area, Black Pearl": 698167,
    }

    locations_forest_tr_fp = {
        "Kelp Forest top right area, bulb in the top fish pass": 698050,
    }

    locations_forest_bl = {
        "Kelp Forest bottom left area, Transturtle": 698212,
    }

    locations_forest_bl_sc = {
        "Kelp Forest bottom left area, bulb close to the spirit crystals": 698054,
        "Kelp Forest bottom left area, Walker Baby": 698186,
    }

    locations_forest_br = {
        "Kelp Forest bottom right area, Odd Container": 698168,
    }

    locations_forest_boss = {
        "Kelp Forest boss area, beating Drunian God": 698204,
    }

    locations_forest_boss_entrance = {
        "Kelp Forest boss room, bulb at the bottom of the area": 698055,
    }

    locations_forest_fish_cave = {
        "Kelp Forest bottom left area, Fish Cave puzzle": 698207,
    }

    locations_forest_sprite_cave = {
        "Kelp Forest sprite cave, bulb inside the fish pass": 698056,
    }

    locations_forest_sprite_cave_tube = {
        "Kelp Forest sprite cave, bulb in the second room": 698057,
        "Kelp Forest sprite cave, Seed Bag": 698176,
    }

    locations_mermog_cave = {
        "Mermog cave, bulb in the left part of the cave": 698121,
    }

    locations_mermog_boss = {
        "Mermog cave, Piranha Egg": 698197,
    }

    locations_veil_tl = {
        "The Veil top left area, In Li's cave": 698199,
        "The Veil top left area, bulb under the rock in the top right path": 698078,
        "The Veil top left area, bulb hidden behind the blocking rock": 698076,
        "The Veil top left area, Transturtle": 698209,
    }

    locations_veil_tl_fp = {
        "The Veil top left area, bulb inside the fish pass": 698077,
    }

    locations_turtle_cave = {
        "Turtle cave, Turtle Egg": 698184,
    }

    locations_turtle_cave_bubble = {
        "Turtle cave, bulb in Bubble Cliff": 698000,
        "Turtle cave, Urchin Costume": 698193,
    }

    locations_veil_tr_r = {
        "The Veil top right area, bulb in the middle of the wall jump cliff": 698079,
        "The Veil top right area, Golden Starfish": 698180,
    }

    locations_veil_tr_l = {
        "The Veil top right area, bulb at the top of the waterfall": 698080,
        "The Veil top right area, Transturtle": 698210,
    }

    locations_veil_bl = {
        "The Veil bottom area, bulb in the left path": 698082,
    }

    locations_veil_b_sc = {
        "The Veil bottom area, bulb in the spirit path": 698081,
    }

    locations_veil_bl_fp = {
        "The Veil bottom area, Verse Egg": 698157,
    }

    locations_veil_br = {
        "The Veil bottom area, Stone Head": 698181,
    }

    locations_octo_cave_t = {
        "Octopus Cave, Dumbo Egg": 698196,
    }

    locations_octo_cave_b = {
        "Octopus Cave, bulb in the path below the Octopus Cave path": 698122,
    }

    locations_sun_temple_l = {
        "Sun Temple, bulb in the top left part": 698094,
        "Sun Temple, bulb in the top right part": 698095,
        "Sun Temple, bulb at the top of the high dark room": 698096,
        "Sun Temple, Golden Gear": 698171,
    }

    locations_sun_temple_r = {
        "Sun Temple, first bulb of the temple": 698091,
        "Sun Temple, bulb on the right part": 698092,
        "Sun Temple, bulb in the hidden room of the right part": 698093,
        "Sun Temple, Sun Key": 698182,
    }

    locations_sun_temple_boss_path = {
        "Sun Worm path, first path bulb": 698017,
        "Sun Worm path, second path bulb": 698018,
        "Sun Worm path, first cliff bulb": 698019,
        "Sun Worm path, second cliff bulb": 698020,
    }

    locations_sun_temple_boss = {
        "Sun Temple boss area, beating Sun God": 698203,
    }

    locations_abyss_l = {
        "Abyss left area, bulb in hidden path room": 698024,
        "Abyss left area, bulb in the right part": 698025,
        "Abyss left area, Glowing Seed": 698166,
        "Abyss left area, Glowing Plant": 698172,
    }

    locations_abyss_lb = {
        "Abyss left area, bulb in the bottom fish pass": 698026,
    }

    locations_abyss_r = {
        "Abyss right area, bulb behind the rock in the whale room": 698109,
        "Abyss right area, bulb in the middle path": 698110,
        "Abyss right area, bulb behind the rock in the middle path": 698111,
        "Abyss right area, bulb in the left green room": 698112,
    }

    locations_abyss_r_transturtle = {
        "Abyss right area, Transturtle": 698214,
    }

    locations_ice_cave = {
        "Ice Cave, bulb in the room to the right": 698083,
        "Ice Cave, first bulb in the top exit room": 698084,
        "Ice Cave, second bulb in the top exit room": 698085,
        "Ice Cave, third bulb in the top exit room": 698086,
        "Ice Cave, bulb in the left room": 698087,
    }

    locations_bubble_cave = {
        "Bubble Cave, bulb in the left cave wall": 698089,
        "Bubble Cave, bulb in the right cave wall (behind the ice crystal)": 698090,
    }

    locations_bubble_cave_boss = {
        "Bubble Cave, Verse Egg": 698161,
    }

    locations_king_jellyfish_cave = {
        "King Jellyfish Cave, bulb in the right path from King Jelly": 698088,
        "King Jellyfish Cave, Jellyfish Costume": 698188,
    }

    locations_whale = {
        "The Whale, Verse Egg": 698159,
    }

    locations_sunken_city_r = {
        "Sunken City right area, crate close to the save crystal": 698154,
        "Sunken City right area, crate in the left bottom room": 698155,
    }

    locations_sunken_city_l = {
        "Sunken City left area, crate in the little pipe room": 698151,
        "Sunken City left area, crate close to the save crystal": 698152,
        "Sunken City left area, crate before the bedroom": 698153,
    }

    locations_sunken_city_l_bedroom = {
        "Sunken City left area, Girl Costume": 698192,
    }

    locations_sunken_city_boss = {
        "Sunken City, bulb on top of the boss area": 698043,
    }

    locations_body_c = {
        "The Body center area, breaking Li's cage": 698201,
        "The Body center area, bulb on the main path blocking tube": 698097,
    }

    locations_body_l = {
        "The Body left area, first bulb in the top face room": 698066,
        "The Body left area, second bulb in the top face room": 698069,
        "The Body left area, bulb below the water stream": 698067,
        "The Body left area, bulb in the top path to the top face room": 698068,
        "The Body left area, bulb in the bottom face room": 698070,
    }

    locations_body_rt = {
        "The Body right area, bulb in the top face room": 698100,
    }

    locations_body_rb = {
        "The Body right area, bulb in the top path to the bottom face room": 698098,
        "The Body right area, bulb in the bottom face room": 698099,
    }

    locations_body_b = {
        "The Body bottom area, bulb in the Jelly Zap room": 698101,
        "The Body bottom area, bulb in the nautilus room": 698102,
        "The Body bottom area, Mutant Costume": 698190,
    }

    locations_final_boss_tube = {
        "Final Boss area, first bulb in the turtle room": 698103,
        "Final Boss area, second bulb in the turtle room": 698104,
        "Final Boss area, third bulb in the turtle room": 698105,
        "Final Boss area, Transturtle": 698215,
    }

    locations_final_boss = {
        "Final Boss area, bulb in the boss third form room": 698106,
    }


location_table = {
    **AquariaLocations.locations_openwater_tl,
    **AquariaLocations.locations_openwater_tr,
    **AquariaLocations.locations_openwater_tr_turtle,
    **AquariaLocations.locations_openwater_bl,
    **AquariaLocations.locations_skeleton_path,
    **AquariaLocations.locations_skeleton_path_sc,
    **AquariaLocations.locations_arnassi,
    **AquariaLocations.locations_arnassi_path,
    **AquariaLocations.locations_arnassi_cave_transturtle,
    **AquariaLocations.locations_arnassi_crab_boss,
    **AquariaLocations.locations_sun_temple_l,
    **AquariaLocations.locations_sun_temple_r,
    **AquariaLocations.locations_sun_temple_boss_path,
    **AquariaLocations.locations_sun_temple_boss,
    **AquariaLocations.locations_verse_cave_r,
    **AquariaLocations.locations_verse_cave_l,
    **AquariaLocations.locations_abyss_l,
    **AquariaLocations.locations_abyss_lb,
    **AquariaLocations.locations_abyss_r,
    **AquariaLocations.locations_abyss_r_transturtle,
    **AquariaLocations.locations_energy_temple_1,
    **AquariaLocations.locations_energy_temple_2,
    **AquariaLocations.locations_energy_temple_3,
    **AquariaLocations.locations_energy_temple_boss,
    **AquariaLocations.locations_energy_temple_blaster_room,
    **AquariaLocations.locations_energy_temple_altar,
    **AquariaLocations.locations_energy_temple_idol,
    **AquariaLocations.locations_mithalas_city,
    **AquariaLocations.locations_mithalas_city_top_path,
    **AquariaLocations.locations_mithalas_city_fishpass,
    **AquariaLocations.locations_cathedral_l,
    **AquariaLocations.locations_cathedral_l_tube,
    **AquariaLocations.locations_cathedral_l_sc,
    **AquariaLocations.locations_cathedral_r,
    **AquariaLocations.locations_cathedral_underground,
    **AquariaLocations.locations_cathedral_boss,
    **AquariaLocations.locations_forest_tl,
    **AquariaLocations.locations_forest_tl_fp,
    **AquariaLocations.locations_forest_tr,
    **AquariaLocations.locations_forest_tr_fp,
    **AquariaLocations.locations_forest_bl,
    **AquariaLocations.locations_forest_bl_sc,
    **AquariaLocations.locations_forest_br,
    **AquariaLocations.locations_forest_boss,
    **AquariaLocations.locations_forest_boss_entrance,
    **AquariaLocations.locations_forest_sprite_cave,
    **AquariaLocations.locations_forest_sprite_cave_tube,
    **AquariaLocations.locations_forest_fish_cave,
    **AquariaLocations.locations_home_water,
    **AquariaLocations.locations_home_water_transturtle,
    **AquariaLocations.locations_home_water_nautilus,
    **AquariaLocations.locations_body_l,
    **AquariaLocations.locations_body_rt,
    **AquariaLocations.locations_body_rb,
    **AquariaLocations.locations_body_c,
    **AquariaLocations.locations_body_b,
    **AquariaLocations.locations_final_boss_tube,
    **AquariaLocations.locations_final_boss,
    **AquariaLocations.locations_song_cave,
    **AquariaLocations.locations_veil_tl,
    **AquariaLocations.locations_veil_tl_fp,
    **AquariaLocations.locations_turtle_cave,
    **AquariaLocations.locations_turtle_cave_bubble,
    **AquariaLocations.locations_veil_tr_r,
    **AquariaLocations.locations_veil_tr_l,
    **AquariaLocations.locations_veil_bl,
    **AquariaLocations.locations_veil_b_sc,
    **AquariaLocations.locations_veil_bl_fp,
    **AquariaLocations.locations_veil_br,
    **AquariaLocations.locations_ice_cave,
    **AquariaLocations.locations_king_jellyfish_cave,
    **AquariaLocations.locations_bubble_cave,
    **AquariaLocations.locations_bubble_cave_boss,
    **AquariaLocations.locations_naija_home,
    **AquariaLocations.locations_mermog_cave,
    **AquariaLocations.locations_mermog_boss,
    **AquariaLocations.locations_octo_cave_t,
    **AquariaLocations.locations_octo_cave_b,
    **AquariaLocations.locations_sunken_city_l,
    **AquariaLocations.locations_sunken_city_r,
    **AquariaLocations.locations_sunken_city_boss,
    **AquariaLocations.locations_sunken_city_l_bedroom,
    **AquariaLocations.locations_simon,
    **AquariaLocations.locations_whale,
}
