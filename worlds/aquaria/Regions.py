"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Used to manage Regions in the Aquaria game multiworld randomizer
"""

from typing import Dict, Optional
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification, CollectionState
from .Items import AquariaItem, ItemNames
from .Locations import AquariaLocations, AquariaLocation
from .Options import AquariaOptions
from worlds.generic.Rules import add_rule, set_rule


# Every condition to connect regions

def _has_hot_soup(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the hotsoup item"""
    return state.has_any({ItemNames.HOT_SOUP, ItemNames.HOT_SOUP_X_2}, player)


def _has_tongue_cleared(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the Body tongue cleared item"""
    return state.has(ItemNames.BODY_TONGUE_CLEARED, player)


def _has_sun_crystal(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the Sun crystal item"""
    return state.has(ItemNames.HAS_SUN_CRYSTAL, player) and _has_bind_song(state, player)


def _has_li(state: CollectionState, player: int) -> bool:
    """`player` in `state` has Li in its team"""
    return state.has(ItemNames.LI_AND_LI_SONG, player)


def _has_damaging_item(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the shield song item"""
    return state.has_any({ItemNames.ENERGY_FORM, ItemNames.NATURE_FORM, ItemNames.BEAST_FORM, ItemNames.LI_AND_LI_SONG,
                          ItemNames.BABY_NAUTILUS, ItemNames.BABY_PIRANHA, ItemNames.BABY_BLASTER}, player)


def _has_energy_attack_item(state: CollectionState, player: int) -> bool:
    """`player` in `state` has items that can do a lot of damage (enough to beat bosses)"""
    return _has_energy_form(state, player) or _has_dual_form(state, player)


def _has_shield_song(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the shield song item"""
    return state.has(ItemNames.SHIELD_SONG, player)


def _has_bind_song(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the bind song item"""
    return state.has(ItemNames.BIND_SONG, player)


def _has_energy_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the energy form item"""
    return state.has(ItemNames.ENERGY_FORM, player)


def _has_beast_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the beast form item"""
    return state.has(ItemNames.BEAST_FORM, player)


def _has_beast_and_soup_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the beast form item"""
    return _has_beast_form(state, player) and _has_hot_soup(state, player)


def _has_beast_form_or_arnassi_armor(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the beast form item"""
    return _has_beast_form(state, player) or state.has(ItemNames.ARNASSI_ARMOR, player)


def _has_nature_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the nature form item"""
    return state.has(ItemNames.NATURE_FORM, player)


def _has_sun_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the sun form item"""
    return state.has(ItemNames.SUN_FORM, player)


def _has_light(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the light item"""
    return state.has(ItemNames.BABY_DUMBO, player) or _has_sun_form(state, player)


def _has_dual_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the dual form item"""
    return _has_li(state, player) and state.has(ItemNames.DUAL_FORM, player)


def _has_fish_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the fish form item"""
    return state.has(ItemNames.FISH_FORM, player)


def _has_spirit_form(state: CollectionState, player: int) -> bool:
    """`player` in `state` has the spirit form item"""
    return state.has(ItemNames.SPIRIT_FORM, player)


def _has_big_bosses(state: CollectionState, player: int) -> bool:
    """`player` in `state` has beated every big bosses"""
    return state.has_all({ItemNames.FALLEN_GOD_BEATED, ItemNames.MITHALAN_GOD_BEATED, ItemNames.DRUNIAN_GOD_BEATED,
                          ItemNames.LUMEREAN_GOD_BEATED, ItemNames.THE_GOLEM_BEATED}, player)


def _has_mini_bosses(state: CollectionState, player: int) -> bool:
    """`player` in `state` has beated every big bosses"""
    return state.has_all({ItemNames.NAUTILUS_PRIME_BEATED, ItemNames.BLASTER_PEG_PRIME_BEATED, ItemNames.MERGOG_BEATED,
                          ItemNames.MITHALAN_PRIESTS_BEATED, ItemNames.OCTOPUS_PRIME_BEATED,
                          ItemNames.CRABBIUS_MAXIMUS_BEATED, ItemNames.MANTIS_SHRIMP_PRIME_BEATED,
                          ItemNames.KING_JELLYFISH_GOD_PRIME_BEATED}, player)



def _has_secrets(state: CollectionState, player: int) -> bool:
    return state.has_all({ItemNames.FIRST_SECRET_OBTAINED, ItemNames.SECOND_SECRET_OBTAINED,
                          ItemNames.THIRD_SECRET_OBTAINED}, player)

class AquariaRegions:
    """
    Class used to create regions of the Aquaria game
    """
    menu: Region
    verse_cave_r: Region
    verse_cave_l: Region
    home_water: Region
    home_water_behind_rocks:Region
    home_water_nautilus: Region
    home_water_transturtle: Region
    naija_home: Region
    song_cave: Region
    energy_temple_1: Region
    energy_temple_2: Region
    energy_temple_3: Region
    energy_temple_boss: Region
    energy_temple_4: Region
    energy_temple_idol: Region
    energy_temple_blaster_room: Region
    energy_temple_altar: Region
    openwater_tl: Region
    openwater_tr: Region
    openwater_tr_turtle: Region
    openwater_tr_urns: Region
    openwater_bl: Region
    openwater_br: Region
    skeleton_path: Region
    skeleton_path_sc: Region
    arnassi: Region
    arnassi_cave_transturtle: Region
    arnassi_cave: Region
    arnassi_crab_boss: Region
    simon: Region
    mithalas_city: Region
    mithalas_city_urns: Region
    mithalas_city_top_path: Region
    mithalas_city_fishpass: Region
    mithalas_castle: Region
    mithalas_castle_urns: Region
    mithalas_castle_tube: Region
    mithalas_castle_sc: Region
    cathedral_top: Region
    cathedral_top_start: Region
    cathedral_top_start_urns: Region
    cathedral_top_end: Region
    cathedral_underground: Region
    cathedral_boss_l: Region
    cathedral_boss_r: Region
    forest_tl: Region
    forest_tl_verse_egg_room: Region
    forest_tr: Region
    forest_tr_fp: Region
    forest_bl: Region
    forest_bl_sc: Region
    forest_br: Region
    forest_boss: Region
    forest_boss_entrance: Region
    sprite_cave: Region
    sprite_cave_tube: Region
    mermog_cave: Region
    mermog_boss: Region
    forest_fish_cave: Region
    veil_tl: Region
    veil_tl_fp: Region
    veil_tr_l: Region
    veil_tr_l_fp: Region
    veil_tr_r: Region
    veil_b: Region
    veil_b_sc: Region
    veil_b_fp: Region
    veil_br: Region
    octo_cave_t: Region
    octo_cave_b: Region
    turtle_cave: Region
    turtle_cave_bubble: Region
    sun_temple_l: Region
    sun_temple_r: Region
    sun_temple_boss_path: Region
    sun_temple_boss: Region
    abyss_l: Region
    abyss_lb: Region
    abyss_r: Region
    abyss_r_transturtle: Region
    ice_cave: Region
    frozen_feil:Region
    bubble_cave: Region
    bubble_cave_boss: Region
    king_jellyfish_cave: Region
    abyss_r_whale: Region
    whale: Region
    first_secret: Region
    sunken_city_l: Region
    sunken_city_l_crates: Region
    sunken_city_r_crates: Region
    sunken_city_boss: Region
    sunken_city_l_bedroom: Region
    body_c: Region
    body_l: Region
    body_rt: Region
    body_rb: Region
    body_b: Region
    final_boss_loby: Region
    final_boss_tube: Region
    final_boss: Region
    final_boss_end: Region
    """
    Every Region of the game
    """

    multiworld: MultiWorld
    """
    The Current Multiworld game.
    """

    player: int
    """
    The ID of the player
    """

    def __add_region(self, hint: str,
                     locations: Optional[Dict[str, int]]) -> Region:
        """
        Create a new Region, add it to the `world` regions and return it.
        Be aware that this function have a side effect on ``world`.`regions`
        """
        region: Region = Region(hint, self.player, self.multiworld, hint)
        if locations is not None:
            region.add_locations(locations, AquariaLocation)
        return region

    def __create_home_water_area(self) -> None:
        """
        Create the `verse_cave`, `home_water` and `song_cave*` regions
        """
        self.menu = self.__add_region("Menu", None)
        self.verse_cave_r = self.__add_region("Verse Cave right area",
                                              AquariaLocations.locations_verse_cave_r)
        self.verse_cave_l = self.__add_region("Verse Cave left area",
                                              AquariaLocations.locations_verse_cave_l)
        self.home_water = self.__add_region("Home Waters", AquariaLocations.locations_home_water)
        self.home_water_nautilus = self.__add_region("Home Waters, Nautilus nest",
                                                     AquariaLocations.locations_home_water_nautilus)
        self.home_water_transturtle = self.__add_region("Home Waters, turtle room",
                                                        AquariaLocations.locations_home_water_transturtle)
        self.home_water_behind_rocks = self.__add_region("Home Waters, behind rock",
                                                         AquariaLocations.locations_home_water_behind_rocks)
        self.naija_home = self.__add_region("Naija's Home", AquariaLocations.locations_naija_home)
        self.song_cave = self.__add_region("Song Cave", AquariaLocations.locations_song_cave)

    def __create_energy_temple(self) -> None:
        """
        Create the `energy_temple_*` regions
        """
        self.energy_temple_1 = self.__add_region("Energy Temple first area",
                                                 AquariaLocations.locations_energy_temple_1)
        self.energy_temple_2 = self.__add_region("Energy Temple second area",
                                                 AquariaLocations.locations_energy_temple_2)
        self.energy_temple_3 = self.__add_region("Energy Temple third area",
                                                 AquariaLocations.locations_energy_temple_3)
        self.energy_temple_altar = self.__add_region("Energy Temple bottom entrance",
                                                     AquariaLocations.locations_energy_temple_altar)
        self.energy_temple_boss = self.__add_region("Energy Temple fallen God room",
                                                    AquariaLocations.locations_energy_temple_boss)
        self.energy_temple_idol = self.__add_region("Energy Temple Idol room",
                                                    AquariaLocations.locations_energy_temple_idol)
        self.energy_temple_blaster_room = self.__add_region("Energy Temple blaster room",
                                                            AquariaLocations.locations_energy_temple_blaster_room)
        self.energy_temple_4 = self.__add_region("Energy Temple after boss path", None)

    def __create_openwater(self) -> None:
        """
        Create the `openwater_*`, `skeleton_path`, `arnassi*` and `simon`
        regions
        """
        self.openwater_tl = self.__add_region("Open Waters top left area",
                                              AquariaLocations.locations_openwater_tl)
        self.openwater_tr = self.__add_region("Open Waters top right area",
                                              AquariaLocations.locations_openwater_tr)
        self.openwater_tr_turtle = self.__add_region("Open Waters top right area, turtle room",
                                                     AquariaLocations.locations_openwater_tr_turtle)
        self.openwater_tr_urns = self.__add_region("Open Waters top right area, Mithalas entrance",
                                                   AquariaLocations.locations_openwater_tr_urns)
        self.openwater_bl = self.__add_region("Open Waters bottom left area",
                                              AquariaLocations.locations_openwater_bl)
        self.openwater_br = self.__add_region("Open Waters bottom right area", None)
        self.skeleton_path = self.__add_region("Open Waters skeleton path",
                                               AquariaLocations.locations_skeleton_path)
        self.skeleton_path_sc = self.__add_region("Open Waters skeleton path spirit crystal",
                                                  AquariaLocations.locations_skeleton_path_sc)
        self.arnassi = self.__add_region("Arnassi Ruins", AquariaLocations.locations_arnassi)
        self.arnassi_cave = self.__add_region("Arnassi Ruins cave",
                                              AquariaLocations.locations_arnassi_cave)
        self.arnassi_cave_transturtle = self.__add_region("Arnassi Ruins cave, transturtle area",
                                                          AquariaLocations.locations_arnassi_cave_transturtle)
        self.arnassi_crab_boss = self.__add_region("Arnassi Ruins, Crabbius Maximus lair",
                                                   AquariaLocations.locations_arnassi_crab_boss)

    def __create_mithalas(self) -> None:
        """
        Create the `mithalas_city*` and `cathedral_*` regions
        """
        self.mithalas_city = self.__add_region("Mithalas City",
                                               AquariaLocations.locations_mithalas_city)
        self.mithalas_city_urns = self.__add_region("Mithalas City urns", AquariaLocations.locations_mithalas_city_urns)
        self.mithalas_city_fishpass = self.__add_region("Mithalas City fish pass",
                                                        AquariaLocations.locations_mithalas_city_fishpass)
        self.mithalas_city_top_path = self.__add_region("Mithalas City top path",
                                                        AquariaLocations.locations_mithalas_city_top_path)
        self.mithalas_castle = self.__add_region("Mithalas castle", AquariaLocations.locations_mithalas_castle)
        self.mithalas_castle_urns = self.__add_region("Mithalas castle urns",
                                                      AquariaLocations.locations_mithalas_castle_urns)
        self.mithalas_castle_tube = self.__add_region("Mithalas castle, plant tube entrance",
                                                  AquariaLocations.locations_mithalas_castle_tube)
        self.mithalas_castle_sc = self.__add_region("Mithalas castle spirit crystal",
                                                AquariaLocations.locations_mithalas_castle_sc)
        self.cathedral_top_start = self.__add_region("Mithalas Cathedral start",
                                             AquariaLocations.locations_cathedral_top_start)
        self.cathedral_top_start_urns = self.__add_region("Mithalas Cathedral start urns",
                                             AquariaLocations.locations_cathedral_top_start_urns)
        self.cathedral_top_end = self.__add_region("Mithalas Cathedral end",
                                             AquariaLocations.locations_cathedral_top_end)
        self.cathedral_underground = self.__add_region("Mithalas Cathedral underground",
                                                       AquariaLocations.locations_cathedral_underground)
        self.cathedral_boss_l = self.__add_region("Mithalas Cathedral, after Mithalan God",
                                                  AquariaLocations.locations_cathedral_boss)
        self.cathedral_boss_r = self.__add_region("Mithalas Cathedral, before Mithalan God", None)

    def __create_forest(self) -> None:
        """
        Create the `forest_*` dans `mermog_cave` regions
        """
        self.forest_tl = self.__add_region("Kelp Forest top left area",
                                           AquariaLocations.locations_forest_tl)
        self.forest_tl_verse_egg_room = self.__add_region("Kelp Forest top left area fish pass",
                                              AquariaLocations.locations_forest_tl_verse_egg_room)
        self.forest_tr = self.__add_region("Kelp Forest top right area",
                                           AquariaLocations.locations_forest_tr)
        self.forest_tr_fp = self.__add_region("Kelp Forest top right area fish pass",
                                              AquariaLocations.locations_forest_tr_fp)
        self.forest_bl = self.__add_region("Kelp Forest bottom left area",
                                           AquariaLocations.locations_forest_bl)
        self.forest_bl_sc = self.__add_region("Kelp Forest bottom left area, spirit crystals",
                                              AquariaLocations.locations_forest_bl_sc)
        self.forest_br = self.__add_region("Kelp Forest bottom right area",
                                           AquariaLocations.locations_forest_br)
        self.sprite_cave = self.__add_region("Sprite cave",
                                                    AquariaLocations.locations_sprite_cave)
        self.sprite_cave_tube = self.__add_region("Sprite cave after the plant tube",
                                                         AquariaLocations.locations_sprite_cave_tube)
        self.forest_boss = self.__add_region("Kelp Forest Drunian God room",
                                             AquariaLocations.locations_forest_boss)
        self.forest_boss_entrance = self.__add_region("Kelp Forest Drunian God room entrance",
                                                      AquariaLocations.locations_forest_boss_entrance)
        self.mermog_cave = self.__add_region("Mermog cave",
                                             AquariaLocations.locations_mermog_cave)
        self.mermog_boss = self.__add_region("Mermog cave boss",
                                             AquariaLocations.locations_mermog_boss)
        self.forest_fish_cave = self.__add_region("Kelp Forest fish cave",
                                                  AquariaLocations.locations_forest_fish_cave)
        self.simon = self.__add_region("Simon Says area", AquariaLocations.locations_simon)

    def __create_veil(self) -> None:
        """
        Create the `veil_*`, `octo_cave` and `turtle_cave` regions
        """
        self.veil_tl = self.__add_region("The Veil top left area", AquariaLocations.locations_veil_tl)
        self.veil_tl_fp = self.__add_region("The Veil top left area fish pass",
                                            AquariaLocations.locations_veil_tl_fp)
        self.turtle_cave = self.__add_region("The Veil top left area, turtle cave",
                                             AquariaLocations.locations_turtle_cave)
        self.turtle_cave_bubble = self.__add_region("The Veil top left area, turtle cave Bubble Cliff",
                                                    AquariaLocations.locations_turtle_cave_bubble)
        self.veil_tr_l = self.__add_region("The Veil top right area, left of temple",
                                           AquariaLocations.locations_veil_tr_l)
        self.veil_tr_l_fp = self.__add_region("The Veil top right area, fish pass left of temple", None)
        self.veil_tr_r = self.__add_region("The Veil top right area, right of temple",
                                           AquariaLocations.locations_veil_tr_r)
        self.octo_cave_t = self.__add_region("Octopus Cave top entrance",
                                             AquariaLocations.locations_octo_cave_t)
        self.octo_cave_b = self.__add_region("Octopus Cave bottom entrance",
                                             AquariaLocations.locations_octo_cave_b)
        self.veil_b = self.__add_region("The Veil bottom left area",
                                         AquariaLocations.locations_veil_b)
        self.veil_b_sc = self.__add_region("The Veil bottom spirit crystal area",
                                           AquariaLocations.locations_veil_b_sc)
        self.veil_b_fp = self.__add_region("The Veil bottom left area, in the sunken ship",
                                            AquariaLocations.locations_veil_b_fp)
        self.veil_br = self.__add_region("The Veil bottom right area",
                                         AquariaLocations.locations_veil_br)

    def __create_sun_temple(self) -> None:
        """
        Create the `sun_temple*` regions
        """
        self.sun_temple_l = self.__add_region("Sun Temple left area",
                                              AquariaLocations.locations_sun_temple_l)
        self.sun_temple_r = self.__add_region("Sun Temple right area",
                                              AquariaLocations.locations_sun_temple_r)
        self.sun_temple_boss_path = self.__add_region("Sun Temple before boss area",
                                                      AquariaLocations.locations_sun_temple_boss_path)
        self.sun_temple_boss = self.__add_region("Sun Temple boss area",
                                                 AquariaLocations.locations_sun_temple_boss)

    def __create_abyss(self) -> None:
        """
        Create the `abyss_*`, `ice_cave`, `king_jellyfish_cave` and `whale`
        regions
        """
        self.abyss_l = self.__add_region("Abyss left area",
                                         AquariaLocations.locations_abyss_l)
        self.abyss_lb = self.__add_region("Abyss left bottom area", AquariaLocations.locations_abyss_lb)
        self.abyss_r = self.__add_region("Abyss right area", AquariaLocations.locations_abyss_r)
        self.abyss_r_transturtle = self.__add_region("Abyss right area, transturtle",
                                                     AquariaLocations.locations_abyss_r_transturtle)
        self.abyss_r_whale = self.__add_region("Abyss right area, outside the whale",
                                                     AquariaLocations.locations_abyss_r_whale)
        self.ice_cave = self.__add_region("Ice Cavern", AquariaLocations.locations_ice_cave)
        self.frozen_feil = self.__add_region("Frozen Veil", None)
        self.bubble_cave = self.__add_region("Bubble Cave", AquariaLocations.locations_bubble_cave)
        self.bubble_cave_boss = self.__add_region("Bubble Cave boss area", AquariaLocations.locations_bubble_cave_boss)
        self.king_jellyfish_cave = self.__add_region("Abyss left area, King jellyfish cave",
                                                     AquariaLocations.locations_king_jellyfish_cave)
        self.whale = self.__add_region("Inside the whale", AquariaLocations.locations_whale)
        self.first_secret = self.__add_region("First Secret area", None)

    def __create_sunken_city(self) -> None:
        """
        Create the `sunken_city_*` regions
        """
        self.sunken_city_l = self.__add_region("Sunken City left area", None)
        self.sunken_city_l_crates = self.__add_region("Sunken City left area",
                                                      AquariaLocations.locations_sunken_city_l)
        self.sunken_city_l_bedroom = self.__add_region("Sunken City left area, bedroom",
                                                       AquariaLocations.locations_sunken_city_l_bedroom)
        self.sunken_city_r = self.__add_region("Sunken City right area", None)
        self.sunken_city_r_crates = self.__add_region("Sunken City right area crates",
                                                      AquariaLocations.locations_sunken_city_r)
        self.sunken_city_boss = self.__add_region("Sunken City boss area",
                                                  AquariaLocations.locations_sunken_city_boss)

    def __create_body(self) -> None:
        """
        Create the `body_*` and `final_boss* regions
        """
        self.body_c = self.__add_region("The Body center area",
                                        AquariaLocations.locations_body_c)
        self.body_l = self.__add_region("The Body left area",
                                        AquariaLocations.locations_body_l)
        self.body_rt = self.__add_region("The Body right area, top path",
                                         AquariaLocations.locations_body_rt)
        self.body_rb = self.__add_region("The Body right area, bottom path",
                                         AquariaLocations.locations_body_rb)
        self.body_b = self.__add_region("The Body bottom area",
                                        AquariaLocations.locations_body_b)
        self.final_boss_loby = self.__add_region("The Body, before final boss", None)
        self.final_boss_tube = self.__add_region("The Body, final boss area turtle room",
                                                 AquariaLocations.locations_final_boss_tube)
        self.final_boss = self.__add_region("The Body, final boss",
                                            AquariaLocations.locations_final_boss)
        self.final_boss_end = self.__add_region("The Body, final boss area", None)

    def __connect_one_way_regions(self, source_name: str, destination_name: str,
                                  source_region: Region,
                                  destination_region: Region, rule=None) -> None:
        """
        Connect from the `source_region` to the `destination_region`
        """
        entrance = Entrance(source_region.player, source_name + " to " + destination_name, source_region)
        source_region.exits.append(entrance)
        entrance.connect(destination_region)
        if rule is not None:
            set_rule(entrance, rule)

    def __connect_regions(self, source_name: str, destination_name: str,
                          source_region: Region,
                          destination_region: Region, rule=None) -> None:
        """
        Connect the `source_region` and the `destination_region` (two-way)
        """
        self.__connect_one_way_regions(source_name, destination_name, source_region, destination_region, rule)
        self.__connect_one_way_regions(destination_name, source_name, destination_region, source_region, rule)

    def __connect_home_water_regions(self) -> None:
        """
        Connect entrances of the different regions around `home_water`
        """
        self.__connect_one_way_regions("Menu", "Verse Cave right area",
                                       self.menu, self.verse_cave_r)
        self.__connect_regions("Verse Cave left area", "Verse Cave right area",
                               self.verse_cave_l, self.verse_cave_r)
        self.__connect_regions("Verse Cave", "Home Waters", self.verse_cave_l, self.home_water)
        self.__connect_regions("Home Waters", "Naija's home", self.home_water, self.naija_home)
        self.__connect_regions("Home Waters", "Song Cave", self.home_water, self.song_cave)
        self.__connect_regions("Home Waters", "Home Waters behind rocks", self.home_water,
                               self.home_water_behind_rocks, lambda state: _has_bind_song(state, self.player))
        self.__connect_regions("Home Waters behind rocks", "Home Waters, nautilus nest",
                               self.home_water_behind_rocks, self.home_water_nautilus,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions("Home Waters", "Home Waters transturtle room",
                               self.home_water, self.home_water_transturtle)
        self.__connect_regions("Home Waters behind rocks", "Energy Temple first area",
                               self.home_water_behind_rocks, self.energy_temple_1)
        self.__connect_regions("Home Waters behind rocks", "Energy Temple altar",
                               self.home_water_behind_rocks, self.energy_temple_altar,
                               lambda state: _has_energy_attack_item(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions("Energy Temple first area", "Energy Temple second area",
                               self.energy_temple_1, self.energy_temple_2,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_regions("Energy Temple first area", "Energy Temple idol room",
                               self.energy_temple_1, self.energy_temple_idol,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Energy Temple idol room", "Energy Temple boss area",
                               self.energy_temple_idol, self.energy_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player) and
                                             _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Energy Temple first area", "Energy Temple after boss path",
                                       self.energy_temple_1, self.energy_temple_4,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Energy Temple after boss path", "Energy Temple first area",
                                       self.energy_temple_4, self.energy_temple_1)
        self.__connect_regions("Energy Temple after boss path", "Energy Temple boss area",
                               self.energy_temple_4, self.energy_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions("Energy Temple second area", "Energy Temple third area",
                               self.energy_temple_2, self.energy_temple_3)
        self.__connect_one_way_regions("Energy Temple third area", "Energy Temple boss area",
                               self.energy_temple_3, self.energy_temple_boss,
                               lambda state: _has_bind_song(state, self.player) and
                                             _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Energy Temple after boss path", "Energy Temple blaster room",
                               self.energy_temple_4, self.energy_temple_blaster_room,
                               lambda state: _has_nature_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_attack_item(state, self.player))
        self.__connect_regions("Home Waters", "Open Waters top left area",
                               self.home_water, self.openwater_tl)

    def __connect_open_water_regions(self) -> None:
        """
        Connect entrances of the different regions around open water
        """
        self.__connect_regions("Open Waters top left area", "Open Waters top right area",
                               self.openwater_tl, self.openwater_tr)
        self.__connect_regions("Open Waters top left area", "Open Waters bottom left area",
                               self.openwater_tl, self.openwater_bl)
        self.__connect_regions("Open Waters top left area", "Kelp forest bottom right area",
                               self.openwater_tl, self.forest_br)
        self.__connect_one_way_regions("Open Waters top right area", "Open Waters top right area, turtle room",
                               self.openwater_tr, self.openwater_tr_turtle,
                               lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions("Open Waters top right area, turtle room", "Open Waters top right area",
                               self.openwater_tr_turtle, self.openwater_tr)
        self.__connect_one_way_regions("Open Waters top right area", "Open Waters top right area, Mithalas exit urns",
                               self.openwater_tr, self.openwater_tr_urns,
                               lambda state: _has_bind_song(state, self.player) or
                                             _has_damaging_item(state, self.player))
        self.__connect_regions("Open Waters top right area", "Open Waters bottom right area",
                               self.openwater_tr, self.openwater_br)
        self.__connect_regions("Open Waters top right area", "Mithalas City",
                               self.openwater_tr, self.mithalas_city)
        self.__connect_regions("Open Waters top right area", "Veil bottom left area",
                               self.openwater_tr, self.veil_b)
        self.__connect_one_way_regions("Open Waters top right area", "Veil bottom right",
                                       self.openwater_tr, self.veil_br,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions("Veil bottom right", "Open Waters top right area",
                                       self.veil_br, self.openwater_tr)
        self.__connect_regions("Open Waters bottom left area", "Open Waters bottom right area",
                               self.openwater_bl, self.openwater_br)
        self.__connect_regions("Open Waters bottom left area", "Skeleton path",
                               self.openwater_bl, self.skeleton_path)
        self.__connect_regions("Abyss left area", "Open Waters bottom left area",
                               self.abyss_l, self.openwater_bl)
        self.__connect_regions("Skeleton path", "Skeleton path spirit cristals",
                               self.skeleton_path, self.skeleton_path_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Abyss right area", "Open Waters bottom right area",
                               self.abyss_r, self.openwater_br)
        self.__connect_one_way_regions("Open Waters bottom right area", "Arnassi ruins",
                                       self.openwater_br, self.arnassi,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Arnassi ruins", "Open Waters bottom right area",
                                       self.arnassi, self.openwater_br)
        self.__connect_regions("Arnassi ruins", "Arnassi ruins cave",
                               self.arnassi, self.arnassi_cave)
        self.__connect_regions("Arnassi ruins cave, transturtle area", "Arnassi ruins cave",
                               self.arnassi_cave_transturtle, self.arnassi_cave,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Arnassi ruins cave", "Arnassi crab boss area",
                                       self.arnassi_cave, self.arnassi_crab_boss,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player) and
                                                     (_has_energy_attack_item(state, self.player) or
                                                      _has_nature_form(state, self.player)))
        self.__connect_one_way_regions("Arnassi crab boss area", "Arnassi ruins cave",
                                       self.arnassi_crab_boss, self.arnassi_cave)

    def __connect_mithalas_regions(self) -> None:
        """
        Connect entrances of the different regions around Mithalas
        """
        self.__connect_one_way_regions("Mithalas City", "Mithalas City urns",
                                       self.mithalas_city, self.mithalas_city_urns,
                                       lambda state: _has_damaging_item(state, self.player))
        self.__connect_one_way_regions("Mithalas City", "Mithalas City top path",
                                       self.mithalas_city, self.mithalas_city_top_path,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions("Mithalas City_top_path", "Mithalas City",
                                       self.mithalas_city_top_path, self.mithalas_city)
        self.__connect_regions("Mithalas City", "Mithalas City home with fishpass",
                               self.mithalas_city, self.mithalas_city_fishpass,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Mithalas City", "Mithalas castle",
                               self.mithalas_city, self.mithalas_castle)
        self.__connect_one_way_regions("Mithalas City top path", "Mithalas castle, flower tube",
                                       self.mithalas_city_top_path,
                                       self.mithalas_castle_tube,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Mithalas castle, flower tube area", "Mithalas City top path",
                                       self.mithalas_castle_tube,
                                       self.mithalas_city_top_path,
                                       lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle flower tube area", "Mithalas castle, spirit crystals",
                               self.mithalas_castle_tube, self.mithalas_castle_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle flower tube area", "Mithalas castle",
                               self.mithalas_castle_tube, self.mithalas_castle,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle", "Mithalas castle urns",
                               self.mithalas_castle, self.mithalas_castle_urns,
                               lambda state: _has_damaging_item(state, self.player))
        self.__connect_regions("Mithalas castle", "Mithalas castle, spirit crystals",
                               self.mithalas_castle, self.mithalas_castle_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle", "Cathedral boss right area",
                                       self.mithalas_castle, self.cathedral_boss_r,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Cathedral boss left area", "Mithalas castle",
                                       self.cathedral_boss_l, self.mithalas_castle,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Mithalas castle", "Mithalas Cathedral underground",
                               self.mithalas_castle, self.cathedral_underground,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle", "Mithalas Cathedral start",
                                       self.mithalas_castle, self.cathedral_top_start,
                                       lambda state: _has_bind_song(state, self.player))
        self.__connect_one_way_regions("Mithalas Cathedral start", "Mithalas Cathedral start urns",
                                       self.cathedral_top_start, self.cathedral_top_start_urns,
                                       lambda state: _has_damaging_item(state, self.player))
        self.__connect_regions("Mithalas Cathedral start", "Mithalas Cathedral end",
                               self.cathedral_top_start, self.cathedral_top_end,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Mithalas Cathedral underground", "Mithalas Cathedral end",
                                       self.cathedral_underground, self.cathedral_top_end,
                                       lambda state: _has_beast_form(state, self.player) and
                                                     _has_damaging_item(state, self.player))
        self.__connect_one_way_regions("Mithalas Cathedral end", "Mithalas Cathedral underground",
                                       self.cathedral_top_end, self.cathedral_underground,
                                       lambda state: _has_energy_attack_item(state, self.player)
                                       )
        self.__connect_one_way_regions("Mithalas Cathedral underground", "Cathedral boss right area",
                                       self.cathedral_underground, self.cathedral_boss_r)
        self.__connect_one_way_regions("Cathedral boss right area", "Mithalas Cathedral underground",
                                       self.cathedral_boss_r, self.cathedral_underground,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Cathedral boss right area", "Cathedral boss left area",
                                       self.cathedral_boss_r, self.cathedral_boss_l,
                                       lambda state: _has_bind_song(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Cathedral boss left area", "Cathedral boss right area",
                                       self.cathedral_boss_l, self.cathedral_boss_r)

    def __connect_forest_regions(self) -> None:
        """
        Connect entrances of the different regions around the Kelp Forest
        """
        self.__connect_regions("Kelp Forest bottom right area", "Veil bottom left area",
                               self.forest_br, self.veil_b)
        self.__connect_regions("Kelp Forest bottom right area", "Kelp Forest bottom left area",
                               self.forest_br, self.forest_bl)
        self.__connect_one_way_regions("Kelp Forest bottom left area", "Kelp Forest bottom left area, spirit crystals",
                                       self.forest_bl, self.forest_bl_sc,
                                       lambda state: _has_energy_attack_item(state, self.player) or
                                                     _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Kelp Forest bottom left area, spirit crystals", "Kelp Forest bottom left area",
                               self.forest_bl_sc, self.forest_bl)
        self.__connect_regions("Kelp Forest bottom right area", "Kelp Forest top right area",
                               self.forest_br, self.forest_tr)
        self.__connect_regions("Kelp Forest bottom left area", "Kelp Forest fish cave",
                               self.forest_bl, self.forest_fish_cave)
        self.__connect_regions("Kelp Forest bottom left area", "Kelp Forest top left area",
                               self.forest_bl, self.forest_tl)
        self.__connect_regions("Kelp Forest bottom left area", "Kelp Forest boss entrance",
                               self.forest_bl, self.forest_boss_entrance,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions("Kelp Forest top left area", "Kelp Forest top left area, Verse Egg room",
                               self.forest_tl, self.forest_tl_verse_egg_room,
                               lambda state: _has_nature_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_attack_item(state, self.player) and
                                             _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Kelp Forest top left area, Verse Egg room", "Kelp Forest top left area",
                               self.forest_tl_verse_egg_room, self.forest_tl,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Kelp Forest top left area", "Kelp Forest top right area",
                               self.forest_tl, self.forest_tr)
        self.__connect_regions("Kelp Forest top left area", "Kelp Forest boss entrance",
                               self.forest_tl, self.forest_boss_entrance)
        self.__connect_one_way_regions("Kelp Forest boss entrance", "Kelp Forest boss area",
                                       self.forest_boss_entrance, self.forest_boss,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Kelp Forest boss area", "Kelp Forest boss entrance",
                               self.forest_boss, self.forest_boss_entrance)
        self.__connect_regions("Kelp Forest top right area", "Kelp Forest top right area fish pass",
                               self.forest_tr, self.forest_tr_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Kelp Forest top right area", "Sprite cave",
                               self.forest_tr, self.sprite_cave)
        self.__connect_regions("Sprite cave", "Sprite cave flower tube",
                               self.sprite_cave, self.sprite_cave_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions("Kelp Forest top right area fish pass", "Mermog cave",
                               self.forest_tr_fp, self.mermog_cave)
        self.__connect_regions("Mermog cave", "Mergog boss",
                               self.mermog_cave, self.mermog_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_energy_attack_item(state, self.player))

    def __connect_veil_regions(self) -> None:
        """
        Connect entrances of the different regions around The Veil
        """
        self.__connect_regions("Veil bottom left area", "Veil bottom left area, fish pass",
                               self.veil_b, self.veil_b_fp,
                               lambda state: _has_fish_form(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions("Veil bottom left area", "Veil bottom area spirit crystals path",
                               self.veil_b, self.veil_b_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Veil bottom area spirit crystals path", "Veil bottom right",
                               self.veil_b_sc, self.veil_br,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Veil bottom right", "Veil top left area",
                               self.veil_br, self.veil_tl)
        self.__connect_regions("Veil top left area", "Veil top left area, fish pass",
                               self.veil_tl, self.veil_tl_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Veil top left area", "Veil right of sun temple",
                               self.veil_tl, self.veil_tr_r)
        self.__connect_regions("Veil top left area", "Turtle cave",
                               self.veil_tl, self.turtle_cave)
        self.__connect_regions("Turtle cave", "Turtle cave Bubble Cliff",
                               self.turtle_cave, self.turtle_cave_bubble)
        self.__connect_regions("Veil right of sun temple", "Sun Temple right area",
                               self.veil_tr_r, self.sun_temple_r)
        self.__connect_one_way_regions("Sun Temple right area", "Sun Temple left area",
                                       self.sun_temple_r, self.sun_temple_l,
                                       lambda state: _has_bind_song(state, self.player) or
                                                     _has_light(state, self.player))
        self.__connect_one_way_regions("Sun Temple left area", "Sun Temple right area",
                                       self.sun_temple_l, self.sun_temple_r,
                                       lambda state: _has_light(state, self.player))
        self.__connect_regions("Sun Temple left area", "Veil left of sun temple",
                               self.sun_temple_l, self.veil_tr_l)
        self.__connect_one_way_regions("Sun Temple left area", "Sun Temple before boss area",
                               self.sun_temple_l, self.sun_temple_boss_path,
                               lambda state: _has_light(state, self.player) or
                                             _has_sun_crystal(state, self.player))
        self.__connect_one_way_regions("Sun Temple before boss area", "Sun Temple left area",
                               self.sun_temple_boss_path, self.sun_temple_l)
        self.__connect_regions("Sun Temple before boss area", "Sun Temple boss area",
                               self.sun_temple_boss_path, self.sun_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Sun Temple boss area", "Veil left of sun temple",
                                       self.sun_temple_boss, self.veil_tr_l)
        self.__connect_regions("Veil left of sun temple", "Veil fish pass left of sun temple",
                               self.veil_tr_l, self.veil_tr_l_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Veil fish pass left of sun temple", "Octo cave top path",
                               self.veil_tr_l_fp, self.octo_cave_t,
                               lambda state: _has_sun_form(state, self.player) and
                                             _has_beast_form(state, self.player) and
                                             _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions("Octo cave top path", "Veil fish pass left of sun temple",
                                       self.octo_cave_t, self.veil_tr_l_fp)
        self.__connect_regions("Veil fish pass left of sun temple", "Octo cave bottom path",
                               self.veil_tr_l_fp, self.octo_cave_b)

    def __connect_abyss_regions(self) -> None:
        """
        Connect entrances of the different regions around The Abyss
        """
        self.__connect_regions("Abyss left area", "Abyss left bottom area",
                               self.abyss_l, self.abyss_lb,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions("Abyss left bottom area", "Sunken City right area",
                               self.abyss_lb, self.sunken_city_r,
                               lambda state: _has_li(state, self.player))
        self.__connect_one_way_regions("Abyss left bottom area", "Body center area",
                                       self.abyss_lb, self.body_c,
                                       lambda state: _has_tongue_cleared(state, self.player))
        self.__connect_one_way_regions("Body center area", "Abyss left bottom area",
                               self.body_c, self.abyss_lb)
        self.__connect_one_way_regions("Abyss left area", "King jellyfish cave",
                                       self.abyss_l, self.king_jellyfish_cave,
                                       lambda state: _has_dual_form(state, self.player) or
                                                     (_has_energy_form(state, self.player) and
                                                      _has_beast_form(state, self.player)))
        self.__connect_one_way_regions("King jellyfish cave", "Abyss left area",
                                       self.king_jellyfish_cave, self.abyss_l)
        self.__connect_regions("Abyss left area", "Abyss right area",
                               self.abyss_l, self.abyss_r)
        self.__connect_regions("Abyss right area", "Abyss right area, outside the whale",
                               self.abyss_r, self.abyss_r_whale,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player))
        self.__connect_regions("Abyss right area, outside the whale", "Inside the whale",
                               self.abyss_r_whale, self.whale)
        self.__connect_regions("Abyss right area", "Abyss right area, transturtle",
                               self.abyss_r, self.abyss_r_transturtle)
        self.__connect_regions("Abyss right area", "First Secret area",
                               self.abyss_r, self.first_secret,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_attack_item(state, self.player))
        self.__connect_regions("Abyss right area", "Ice Cavern",
                               self.abyss_r, self.ice_cave,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Ice cave", "Frozen Veil",
                               self.ice_cave, self.frozen_feil)
        self.__connect_one_way_regions("Frozen Veil", "Bubble Cave",
                               self.frozen_feil, self.bubble_cave,
                               lambda state: _has_beast_form(state, self.player) or
                                             _has_hot_soup(state, self.player))
        self.__connect_one_way_regions("Bubble Cave", "Frozen Veil",
                               self.bubble_cave, self.frozen_feil)
        self.__connect_one_way_regions("Bubble Cave", "Bubble Cave boss area",
                               self.bubble_cave, self.bubble_cave_boss,
                               lambda state: _has_nature_form(state, self.player) and _has_bind_song(state, self.player)
                               )
        self.__connect_one_way_regions("Bubble Cave boss area", "Bubble Cave",
                               self.bubble_cave_boss, self.bubble_cave)

    def __connect_sunken_city_regions(self) -> None:
        """
        Connect entrances of the different regions around The Sunken City
        """
        self.__connect_regions("Sunken City right area", "Sunken City left area",
                               self.sunken_city_r, self.sunken_city_l)
        self.__connect_one_way_regions("Sunken City right area", "Sunken City right area crates",
                                       self.sunken_city_r, self.sunken_city_r_crates,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions("Sunken City left area", "Sunken City bedroom",
                               self.sunken_city_l, self.sunken_city_l_bedroom,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions("Sunken City left area", "Sunken City left area crates",
                                       self.sunken_city_l, self.sunken_city_l_crates,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions("Sunken City left area", "Sunken City boss area",
                               self.sunken_city_l, self.sunken_city_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_energy_attack_item(state, self.player) and
                                             _has_bind_song(state, self.player))

    def __connect_body_regions(self) -> None:
        """
        Connect entrances of the different regions around The Body
        """
        self.__connect_one_way_regions("Body center area", "Body left area",
                                       self.body_c, self.body_l,
                                       lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Body left area", "Body center area",
                                       self.body_l, self.body_c)
        self.__connect_regions("Body center area", "Body right area top path",
                               self.body_c, self.body_rt)
        self.__connect_one_way_regions("Body center area", "Body right area bottom path",
                                       self.body_c, self.body_rb,
                                       lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Body right area bottom path", "Body center area",
                                       self.body_rb, self.body_c)
        self.__connect_regions("Body center area", "Body bottom area",
                               self.body_c, self.body_b,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions("Body bottom area", "Final Boss area",
                               self.body_b, self.final_boss_loby,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions("Before Final Boss", "Final Boss tube",
                               self.final_boss_loby, self.final_boss_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions("Before Final Boss", "Final Boss",
                                       self.final_boss_loby, self.final_boss,
                                       lambda state: _has_energy_form(state, self.player) and
                                                     _has_dual_form(state, self.player) and
                                                     _has_sun_form(state, self.player) and
                                                     _has_bind_song(state, self.player))
        self.__connect_one_way_regions("Final Boss", "Final Boss end",
                                       self.final_boss, self.final_boss_end)

    def __connect_transturtle(self, item_source: str, item_target: str, region_source: Region,
                              region_target: Region) -> None:
        """Connect a single transturtle to another one"""
        if item_source != item_target:
            self.__connect_one_way_regions(item_source, item_target, region_source, region_target,
                                           lambda state: state.has(item_target, self.player))

    def _connect_transturtle_to_other(self, item: str, region: Region) -> None:
        """Connect a single transturtle to all others"""
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_VEIL_TOP_LEFT, region, self.veil_tl)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT, region, self.veil_tr_l)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_OPEN_WATERS, region, self.openwater_tr_turtle)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_KELP_FOREST, region, self.forest_bl)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_HOME_WATERS, region, self.home_water_transturtle)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_ABYSS, region, self.abyss_r_transturtle)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_BODY, region, self.final_boss_tube)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_SIMON_SAYS, region, self.simon)
        self.__connect_transturtle(item, ItemNames.TRANSTURTLE_ARNASSI_RUINS, region, self.arnassi_cave_transturtle)

    def __connect_transturtles(self) -> None:
        """Connect every transturtle with others"""
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_VEIL_TOP_LEFT, self.veil_tl)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT, self.veil_tr_l)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_OPEN_WATERS, self.openwater_tr_turtle)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_KELP_FOREST, self.forest_bl)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_HOME_WATERS, self.home_water_transturtle)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_ABYSS, self.abyss_r_transturtle)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_BODY, self.final_boss_tube)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_SIMON_SAYS, self.simon)
        self._connect_transturtle_to_other(ItemNames.TRANSTURTLE_ARNASSI_RUINS, self.arnassi_cave_transturtle)

    def connect_regions(self) -> None:
        """
        Connect every region (entrances and exits)
        """
        self.__connect_home_water_regions()
        self.__connect_open_water_regions()
        self.__connect_mithalas_regions()
        self.__connect_forest_regions()
        self.__connect_veil_regions()
        self.__connect_abyss_regions()
        self.__connect_sunken_city_regions()
        self.__connect_body_regions()
        self.__connect_transturtles()

    def __add_event_location(self, region: Region, name: str, event_name: str) -> None:
        """
        Add an event to the `region` with the name `name` and the item
        `event_name`
        """
        location: AquariaLocation = AquariaLocation(
            self.player, name, None, region
        )
        region.locations.append(location)
        location.place_locked_item(AquariaItem(event_name,
                                               ItemClassification.progression,
                                               None,
                                               self.player))

    def __add_event_big_bosses(self) -> None:
        """
        Add every bit bosses (other than the creator) events to the `world`
        """
        self.__add_event_location(self.energy_temple_boss,
                                  "Beating Fallen God",
                                  ItemNames.FALLEN_GOD_BEATED)
        self.__add_event_location(self.cathedral_boss_l,
                                  "Beating Mithalan God",
                                  ItemNames.MITHALAN_GOD_BEATED)
        self.__add_event_location(self.forest_boss,
                                  "Beating Drunian God",
                                  ItemNames.DRUNIAN_GOD_BEATED)
        self.__add_event_location(self.sun_temple_boss,
                                  "Beating Lumerean God",
                                  ItemNames.LUMEREAN_GOD_BEATED)
        self.__add_event_location(self.sunken_city_boss,
                                  "Beating the Golem",
                                  ItemNames.THE_GOLEM_BEATED)

    def __add_event_mini_bosses(self) -> None:
        """
        Add every mini bosses (excluding Energy Statue and Simon Says)
        events to the `world`
        """
        self.__add_event_location(self.home_water_nautilus,
                                  "Beating Nautilus Prime",
                                  ItemNames.NAUTILUS_PRIME_BEATED)
        self.__add_event_location(self.energy_temple_blaster_room,
                                  "Beating Blaster Peg Prime",
                                  ItemNames.BLASTER_PEG_PRIME_BEATED)
        self.__add_event_location(self.mermog_boss,
                                  "Beating Mergog",
                                  ItemNames.MERGOG_BEATED)
        self.__add_event_location(self.mithalas_castle_tube,
                                  "Beating Mithalan priests",
                                  ItemNames.MITHALAN_PRIESTS_BEATED)
        self.__add_event_location(self.octo_cave_t,
                                  "Beating Octopus Prime",
                                  ItemNames.OCTOPUS_PRIME_BEATED)
        self.__add_event_location(self.arnassi_crab_boss,
                                  "Beating Crabbius Maximus",
                                  ItemNames.CRABBIUS_MAXIMUS_BEATED)
        self.__add_event_location(self.bubble_cave_boss,
                                  "Beating Mantis Shrimp Prime",
                                  ItemNames.MANTIS_SHRIMP_PRIME_BEATED)
        self.__add_event_location(self.king_jellyfish_cave,
                                  "Beating King Jellyfish God Prime",
                                  ItemNames.KING_JELLYFISH_GOD_PRIME_BEATED)

    def __add_event_secrets(self) -> None:
        """
        Add secrets events to the `world`
        """
        self.__add_event_location(self.first_secret,  # Doit ajouter une région pour le "First Secret"
                                  "First Secret",
                                  ItemNames.FIRST_SECRET_OBTAINED)
        self.__add_event_location(self.mithalas_city,
                                  "Second Secret",
                                  ItemNames.SECOND_SECRET_OBTAINED)
        self.__add_event_location(self.sun_temple_l,
                                  "Third Secret",
                                  ItemNames.THIRD_SECRET_OBTAINED)

    def add_event_locations(self) -> None:
        """
        Add every event (locations and items) to the `world`
        """
        self.__add_event_mini_bosses()
        self.__add_event_big_bosses()
        self.__add_event_secrets()
        self.__add_event_location(self.sunken_city_boss,
                                  "Sunken City cleared",
                                  ItemNames.BODY_TONGUE_CLEARED)
        self.__add_event_location(self.sun_temple_r,
                                  "Sun Crystal",
                                  ItemNames.HAS_SUN_CRYSTAL)
        self.__add_event_location(self.final_boss_end, "Objective complete",
                                  ItemNames.VICTORY)

    def __adjusting_soup_rules(self) -> None:
        """
        Modify rules for location that need soup
        """
        add_rule(self.multiworld.get_location("Turtle cave, Urchin Costume", self.player),
                 lambda state: _has_hot_soup(state, self.player))
        add_rule(self.multiworld.get_location("Sun Worm path, first cliff bulb", self.player),
                 lambda state: _has_beast_and_soup_form(state, self.player) or
                               state.has(ItemNames.LUMEREAN_GOD_BEATED, self.player))
        add_rule(self.multiworld.get_location("Sun Worm path, second cliff bulb", self.player),
                 lambda state: _has_beast_and_soup_form(state, self.player) or
                               state.has(ItemNames.LUMEREAN_GOD_BEATED, self.player))
        add_rule(self.multiworld.get_location("The Veil top right area, bulb at the top of the waterfall", self.player),
                 lambda state: _has_beast_and_soup_form(state, self.player))

    def __adjusting_under_rock_location(self) -> None:
        """
        Modify rules implying bind song needed for bulb under rocks
        """
        add_rule(self.multiworld.get_location("Home Waters, bulb under the rock in the left path from the Verse Cave",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Verse Cave left area, bulb under the rock at the end of the path",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Naija's Home, bulb under the rock at the right of the main path",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Song Cave, bulb under the rock in the path to the singing statues",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Song Cave, bulb under the rock close to the song door",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Energy Temple second area, bulb under the rock",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Open Waters top left area, bulb under the rock in the right path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Open Waters top left area, bulb under the rock in the left path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Kelp Forest top right area, bulb under the rock in the right path",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("The Veil top left area, bulb under the rock in the top right path",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss right area, bulb behind the rock in the whale room",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss right area, bulb in the middle path",
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("The Veil top left area, bulb under the rock in the top right path",
                                              self.player), lambda state: _has_bind_song(state, self.player))

    def __adjusting_light_in_dark_place_rules(self) -> None:
        add_rule(self.multiworld.get_location("Kelp Forest top right area, Black Pearl", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_location("Kelp Forest bottom right area, Odd Container", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Abyss right area, transturtle to Abyss right area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Body center area to Abyss left bottom area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Veil fish pass left of sun temple to Octo cave top path", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Open Waters bottom right area to Abyss right area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Open Waters bottom left area to Abyss left area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Sun Temple left area to Sun Temple right area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance("Sun Temple right area to Sun Temple left area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance("Veil left of sun temple to Sun Temple left area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))

    def __adjusting_manual_rules(self) -> None:
        add_rule(self.multiworld.get_location("Mithalas Cathedral, Mithalan Dress", self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("Open Waters bottom left area, bulb inside the lowest fish pass", self.player),
                 lambda state: _has_fish_form(state, self.player))
        add_rule(self.multiworld.get_location("Kelp Forest bottom left area, Walker Baby", self.player),
                 lambda state: _has_spirit_form(state, self.player))
        add_rule(
            self.multiworld.get_location("The Veil top left area, bulb hidden behind the blocking rock", self.player),
            lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Turtle cave, Turtle Egg", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss left area, bulb in the bottom fish pass", self.player),
                 lambda state: _has_fish_form(state, self.player))
        add_rule(self.multiworld.get_location("Song Cave, Anemone Seed", self.player),
                 lambda state: _has_nature_form(state, self.player))
        add_rule(self.multiworld.get_location("Song Cave, Verse Egg", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Verse Cave right area, Big Seed", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Arnassi Ruins, Song Plant Spore", self.player),
                 lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        add_rule(self.multiworld.get_location("Energy Temple first area, bulb in the bottom room blocked by a rock",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Naija's Home, bulb after the energy door", self.player),
                 lambda state: _has_energy_attack_item(state, self.player))
        add_rule(self.multiworld.get_location("Arnassi Ruins, Arnassi Armor", self.player),
                 lambda state: _has_fish_form(state, self.player) or
                               _has_beast_and_soup_form(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas City, urn inside a home fish pass", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas City, urn in the Castle flower tube entrance", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location(
            "The Veil top right area, bulb in the middle of the wall jump cliff", self.player
        ), lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        add_rule(self.multiworld.get_location("Kelp Forest top left area, Jelly Egg", self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("The Body center area, breaking Li's cage", self.player),
                 lambda state: _has_tongue_cleared(state, self.player))

    def __no_progression_hard_or_hidden_location(self) -> None:
        self.multiworld.get_location("Energy Temple boss area, Fallen God Tooth",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Mithalas boss area, beating Mithalan God",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp Forest boss area, beating Drunian God",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Temple boss area, beating Lumerean God",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sunken City, bulb on top of the boss area",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Home Waters, Nautilus Egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Energy Temple blaster room, Blaster Egg",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Mithalas City Castle, beating the Priests",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Mermog cave, Piranha Egg",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Octopus Cave, Dumbo Egg",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("King Jellyfish Cave, bulb in the right path from King Jelly",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("King Jellyfish Cave, Jellyfish Costume",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Final Boss area, bulb in the boss third form room",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Worm path, first cliff bulb",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Worm path, second cliff bulb",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("The Veil top right area, bulb at the top of the waterfall",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble Cave, bulb in the left cave wall",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble Cave, Verse Egg",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp Forest bottom left area, bulb close to the spirit crystals",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp Forest bottom left area, Walker Baby",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Temple, Sun Key",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("The Body bottom area, Mutant Costume",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Temple, bulb in the hidden room of the right part",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Arnassi Ruins, Arnassi Armor",
                                     self.player).item_rule = \
            lambda item: item.classification != ItemClassification.progression

    def adjusting_rules(self, options: AquariaOptions) -> None:
        """
        Modify rules for single location or optional rules
        """
        self.__adjusting_soup_rules()
        self.__adjusting_manual_rules()
        if options.light_needed_to_get_to_dark_places:
            self.__adjusting_light_in_dark_place_rules()
        if options.bind_song_needed_to_get_under_rock_bulb:
            self.__adjusting_under_rock_location()

        if options.mini_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance("Before Final Boss to Final Boss", self.player),
                     lambda state: _has_mini_bosses(state, self.player))
        if options.big_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance("Before Final Boss to Final Boss", self.player),
                     lambda state: _has_big_bosses(state, self.player))
        if options.objective.value == 1:
            add_rule(self.multiworld.get_entrance("Before Final Boss to Final Boss", self.player),
                     lambda state: _has_secrets(state, self.player))
        if options.unconfine_home_water.value in [0, 1]:
            add_rule(self.multiworld.get_entrance("Home Waters to Home Waters transturtle room", self.player),
                     lambda state: _has_bind_song(state, self.player))
        if options.unconfine_home_water.value in [0, 2]:
            add_rule(self.multiworld.get_entrance("Home Waters to Open Waters top left area", self.player),
                     lambda state: _has_bind_song(state, self.player) and _has_energy_attack_item(state, self.player))
        if options.no_progression_hard_or_hidden_locations:
            self.__no_progression_hard_or_hidden_location()

    def __add_home_water_regions_to_world(self) -> None:
        """
        Add every region around home water to the `world`
        """
        self.multiworld.regions.append(self.menu)
        self.multiworld.regions.append(self.verse_cave_r)
        self.multiworld.regions.append(self.verse_cave_l)
        self.multiworld.regions.append(self.home_water)
        self.multiworld.regions.append(self.home_water_nautilus)
        self.multiworld.regions.append(self.home_water_transturtle)
        self.multiworld.regions.append(self.naija_home)
        self.multiworld.regions.append(self.song_cave)
        self.multiworld.regions.append(self.energy_temple_1)
        self.multiworld.regions.append(self.energy_temple_2)
        self.multiworld.regions.append(self.energy_temple_3)
        self.multiworld.regions.append(self.energy_temple_boss)
        self.multiworld.regions.append(self.energy_temple_blaster_room)
        self.multiworld.regions.append(self.energy_temple_altar)

    def __add_open_water_regions_to_world(self) -> None:
        """
        Add every region around open water to the `world`
        """
        self.multiworld.regions.append(self.openwater_tl)
        self.multiworld.regions.append(self.openwater_tr)
        self.multiworld.regions.append(self.openwater_tr_turtle)
        self.multiworld.regions.append(self.openwater_bl)
        self.multiworld.regions.append(self.openwater_br)
        self.multiworld.regions.append(self.skeleton_path)
        self.multiworld.regions.append(self.skeleton_path_sc)
        self.multiworld.regions.append(self.arnassi)
        self.multiworld.regions.append(self.arnassi_cave)
        self.multiworld.regions.append(self.arnassi_cave_transturtle)
        self.multiworld.regions.append(self.arnassi_crab_boss)
        self.multiworld.regions.append(self.simon)

    def __add_mithalas_regions_to_world(self) -> None:
        """
        Add every region around Mithalas to the `world`
        """
        self.multiworld.regions.append(self.mithalas_city)
        self.multiworld.regions.append(self.mithalas_city_top_path)
        self.multiworld.regions.append(self.mithalas_city_fishpass)
        self.multiworld.regions.append(self.mithalas_castle)
        self.multiworld.regions.append(self.mithalas_castle_tube)
        self.multiworld.regions.append(self.mithalas_castle_sc)
        self.multiworld.regions.append(self.cathedral_top_start)
        self.multiworld.regions.append(self.cathedral_top_start_urns)
        self.multiworld.regions.append(self.cathedral_top_end)
        self.multiworld.regions.append(self.cathedral_underground)
        self.multiworld.regions.append(self.cathedral_boss_l)
        self.multiworld.regions.append(self.cathedral_boss_r)

    def __add_forest_regions_to_world(self) -> None:
        """
        Add every region around the kelp forest to the `world`
        """
        self.multiworld.regions.append(self.forest_tl)
        self.multiworld.regions.append(self.forest_tl_verse_egg_room)
        self.multiworld.regions.append(self.forest_tr)
        self.multiworld.regions.append(self.forest_tr_fp)
        self.multiworld.regions.append(self.forest_bl)
        self.multiworld.regions.append(self.forest_bl_sc)
        self.multiworld.regions.append(self.forest_br)
        self.multiworld.regions.append(self.forest_boss)
        self.multiworld.regions.append(self.forest_boss_entrance)
        self.multiworld.regions.append(self.sprite_cave)
        self.multiworld.regions.append(self.sprite_cave_tube)
        self.multiworld.regions.append(self.mermog_cave)
        self.multiworld.regions.append(self.mermog_boss)
        self.multiworld.regions.append(self.forest_fish_cave)

    def __add_veil_regions_to_world(self) -> None:
        """
        Add every region around the Veil to the `world`
        """
        self.multiworld.regions.append(self.veil_tl)
        self.multiworld.regions.append(self.veil_tl_fp)
        self.multiworld.regions.append(self.veil_tr_l)
        self.multiworld.regions.append(self.veil_tr_l_fp)
        self.multiworld.regions.append(self.veil_tr_r)
        self.multiworld.regions.append(self.veil_b)
        self.multiworld.regions.append(self.veil_b_sc)
        self.multiworld.regions.append(self.veil_b_fp)
        self.multiworld.regions.append(self.veil_br)
        self.multiworld.regions.append(self.octo_cave_t)
        self.multiworld.regions.append(self.octo_cave_b)
        self.multiworld.regions.append(self.turtle_cave)
        self.multiworld.regions.append(self.turtle_cave_bubble)
        self.multiworld.regions.append(self.sun_temple_l)
        self.multiworld.regions.append(self.sun_temple_r)
        self.multiworld.regions.append(self.sun_temple_boss_path)
        self.multiworld.regions.append(self.sun_temple_boss)

    def __add_abyss_regions_to_world(self) -> None:
        """
        Add every region around the Abyss to the `world`
        """
        self.multiworld.regions.append(self.abyss_l)
        self.multiworld.regions.append(self.abyss_lb)
        self.multiworld.regions.append(self.abyss_r)
        self.multiworld.regions.append(self.abyss_r_whale)
        self.multiworld.regions.append(self.abyss_r_transturtle)
        self.multiworld.regions.append(self.ice_cave)
        self.multiworld.regions.append(self.bubble_cave)
        self.multiworld.regions.append(self.bubble_cave_boss)
        self.multiworld.regions.append(self.king_jellyfish_cave)
        self.multiworld.regions.append(self.whale)
        self.multiworld.regions.append(self.sunken_city_l)
        self.multiworld.regions.append(self.sunken_city_r)
        self.multiworld.regions.append(self.sunken_city_boss)
        self.multiworld.regions.append(self.sunken_city_l_bedroom)

    def __add_body_regions_to_world(self) -> None:
        """
        Add every region around the Body to the `world`
        """
        self.multiworld.regions.append(self.body_c)
        self.multiworld.regions.append(self.body_l)
        self.multiworld.regions.append(self.body_rt)
        self.multiworld.regions.append(self.body_rb)
        self.multiworld.regions.append(self.body_b)
        self.multiworld.regions.append(self.final_boss_loby)
        self.multiworld.regions.append(self.final_boss_tube)
        self.multiworld.regions.append(self.final_boss)
        self.multiworld.regions.append(self.final_boss_end)

    def add_regions_to_world(self) -> None:
        """
        Add every region to the `world`
        """
        self.__add_home_water_regions_to_world()
        self.__add_open_water_regions_to_world()
        self.__add_mithalas_regions_to_world()
        self.__add_forest_regions_to_world()
        self.__add_veil_regions_to_world()
        self.__add_abyss_regions_to_world()
        self.__add_body_regions_to_world()

    def __init__(self, multiworld: MultiWorld, player: int):
        """
        Initialisation of the regions
        """
        self.multiworld = multiworld
        self.player = player
        self.__create_home_water_area()
        self.__create_energy_temple()
        self.__create_openwater()
        self.__create_mithalas()
        self.__create_forest()
        self.__create_veil()
        self.__create_sun_temple()
        self.__create_abyss()
        self.__create_sunken_city()
        self.__create_body()
