"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Used to manage Regions in the Aquaria game multiworld randomizer
"""

from typing import Dict, Optional
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification, CollectionState
from .Items import AquariaItem
from .Locations import AquariaLocations, AquariaLocation
from .Options import AquariaOptions
from worlds.generic.Rules import add_rule, set_rule


# Every condition to connect regions

def _has_hot_soup(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the hotsoup item"""
    return state.has("Hot soup", player)


def _has_tongue_cleared(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the Body tongue cleared item"""
    return state.has("Body tongue cleared", player)


def _has_sun_crystal(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the Sun crystal item"""
    return state.has("Has sun crystal", player) and _has_bind_song(state, player)


def _has_li(state:CollectionState, player: int) -> bool:
    """`player` in `state` has Li in its team"""
    return state.has("Li and Li song", player)


def _has_damaging_item(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the shield song item"""
    return state.has_any({"Energy form",  "Nature form", "Beast form", "Li and Li song", "Baby nautilus",
                         "Baby piranha", "Baby blaster"}, player)


def _has_shield_song(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the shield song item"""
    return state.has("Shield song", player)


def _has_bind_song(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the bind song item"""
    return state.has("Bind song", player)


def _has_energy_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the energy form item"""
    return state.has("Energy form", player)


def _has_beast_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the beast form item"""
    return state.has("Beast form", player)


def _has_nature_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the nature form item"""
    return state.has("Nature form", player)


def _has_sun_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the sun form item"""
    return state.has("Sun form", player)


def _has_light(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the light item"""
    return state.has("Baby dumbo", player) or _has_sun_form(state, player)


def _has_dual_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the dual form item"""
    return _has_li(state, player) and state.has("Dual form", player)


def _has_fish_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the fish form item"""
    return state.has("Fish form", player)


def _has_spirit_form(state:CollectionState, player: int) -> bool:
    """`player` in `state` has the spirit form item"""
    return state.has("Spirit form", player)


def _has_big_bosses(state:CollectionState, player: int) -> bool:
    """`player` in `state` has beated every big bosses"""
    return state.has_all({"Fallen God beated", "Mithalan God beated", "Drunian God beated",
                         "Sun God beated", "The Golem beated"}, player)


def _has_mini_bosses(state:CollectionState, player: int) -> bool:
    """`player` in `state` has beated every big bosses"""
    return state.has_all({"Nautilus Prime beated", "Blaster Peg Prime beated", "Mergog beated",
                         "Mithalan priests beated", "Octopus Prime beated", "Crabbius Maximus beated",
                         "Mantis Shrimp Prime beated", "King Jellyfish God Prime beated"}, player)


def _has_secrets(state:CollectionState, player: int) -> bool:
    return state.has_all({"First secret obtained", "Second secret obtained", "Third secret obtained"},player)


class AquariaRegions:
    """
    Class used to create regions of the Aquaria game
    """
    menu: Region
    verse_cave_r: Region
    verse_cave_l: Region
    home_water: Region
    home_water_nautilus: Region
    home_water_transturtle: Region
    naija_home: Region
    song_cave: Region
    energy_temple_1: Region
    energy_temple_2: Region
    energy_temple_3: Region
    energy_temple_boss: Region
    energy_temple_idol: Region
    energy_temple_blaster_room: Region
    energy_temple_altar: Region
    openwater_tl: Region
    openwater_tr: Region
    openwater_tr_turtle: Region
    openwater_bl: Region
    openwater_br: Region
    skeleton_path: Region
    skeleton_path_sc: Region
    arnassi: Region
    arnassi_path: Region
    arnassi_crab_boss: Region
    simon: Region
    mithalas_city: Region
    mithalas_city_top_path: Region
    mithalas_city_fishpass: Region
    cathedral_l: Region
    cathedral_l_tube: Region
    cathedral_l_sc: Region
    cathedral_r: Region
    cathedral_underground: Region
    cathedral_boss_l: Region
    cathedral_boss_r: Region
    forest_tl: Region
    forest_tl_fp: Region
    forest_tr: Region
    forest_tr_fp: Region
    forest_bl: Region
    forest_br: Region
    forest_boss: Region
    forest_boss_entrance: Region
    forest_sprite_cave: Region
    forest_sprite_cave_tube: Region
    mermog_cave: Region
    mermog_boss: Region
    forest_fish_cave: Region
    veil_tl: Region
    veil_tl_fp: Region
    veil_tr_l: Region
    veil_tr_r: Region
    veil_bl: Region
    veil_b_sc: Region
    veil_bl_fp: Region
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
    ice_cave: Region
    bubble_cave: Region
    bubble_cave_boss: Region
    king_jellyfish_cave: Region
    whale: Region
    first_secret: Region
    sunken_city_l: Region
    sunken_city_r: Region
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
                     locations: Optional[Dict[str, Optional[int]]]) -> Region:
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
        self.home_water = self.__add_region("Home Water", AquariaLocations.locations_home_water)
        self.home_water_nautilus = self.__add_region("Home Water, Nautilus nest",
                                                     AquariaLocations.locations_home_water_nautilus)
        self.home_water_transturtle = self.__add_region("Home Water, turtle room",
                                                     AquariaLocations.locations_home_water_transturtle)
        self.naija_home = self.__add_region("Naija's home", AquariaLocations.locations_naija_home)
        self.song_cave = self.__add_region("Song cave", AquariaLocations.locations_song_cave)

    def __create_energy_temple(self) -> None:
        """
        Create the `energy_temple_*` regions
        """
        self.energy_temple_1 = self.__add_region("Energy temple first area",
                                                 AquariaLocations.locations_energy_temple_1)
        self.energy_temple_2 = self.__add_region("Energy temple second area",
                                                 AquariaLocations.locations_energy_temple_2)
        self.energy_temple_3 = self.__add_region("Energy temple third area",
                                                 AquariaLocations.locations_energy_temple_3)
        self.energy_temple_altar = self.__add_region("Energy temple bottom entrance",
                                                     AquariaLocations.locations_energy_temple_altar)
        self.energy_temple_boss = self.__add_region("Energy temple fallen God room",
                                                    AquariaLocations.locations_energy_temple_boss)
        self.energy_temple_idol = self.__add_region("Energy temple Idol room",
                                                    AquariaLocations.locations_energy_temple_idol)
        self.energy_temple_blaster_room = self.__add_region("Energy temple blaster room",
                                                            AquariaLocations.locations_energy_temple_blaster_room)

    def __create_openwater(self) -> None:
        """
        Create the `openwater_*`, `skeleton_path`, `arnassi*` and `simon`
        regions
        """
        self.openwater_tl = self.__add_region("Open water top left area",
                                              AquariaLocations.locations_openwater_tl)
        self.openwater_tr = self.__add_region("Open water top right area",
                                              AquariaLocations.locations_openwater_tr)
        self.openwater_tr_turtle = self.__add_region("Open water top right area, turtle room",
                                                     AquariaLocations.locations_openwater_tr_turtle)
        self.openwater_bl = self.__add_region("Open water bottom left area",
                                              AquariaLocations.locations_openwater_bl)
        self.openwater_br = self.__add_region("Open water bottom right area", None)
        self.skeleton_path = self.__add_region("Open water skeleton path",
                                               AquariaLocations.locations_skeleton_path)
        self.skeleton_path_sc = self.__add_region("Open water skeleton path spirit cristal",
                                                  AquariaLocations.locations_skeleton_path_sc)
        self.arnassi = self.__add_region("Arnassi Ruins", AquariaLocations.locations_arnassi)
        self.arnassi_path = self.__add_region("Arnassi Ruins, back entrance path",
                                              AquariaLocations.locations_arnassi_path)
        self.arnassi_crab_boss = self.__add_region("Arnassi Ruins, Crabbius Maximus lair",
                                                   AquariaLocations.locations_arnassi_crab_boss)

    def __create_mithalas(self) -> None:
        """
        Create the `mithalas_city*` and `cathedral_*` regions
        """
        self.mithalas_city = self.__add_region("Mithalas city",
                                               AquariaLocations.locations_mithalas_city)
        self.mithalas_city_fishpass = self.__add_region("Mithalas city fish pass",
                                                        AquariaLocations.locations_mithalas_city_fishpass)
        self.mithalas_city_top_path = self.__add_region("Mithalas city top path",
                                                        AquariaLocations.locations_mithalas_city_top_path)
        self.cathedral_l = self.__add_region("Mithalas castle", AquariaLocations.locations_cathedral_l)
        self.cathedral_l_tube = self.__add_region("Mithalas castle, plant tube entrance",
                                                  AquariaLocations.locations_cathedral_l_tube)
        self.cathedral_l_sc = self.__add_region("Mithalas castle spirit cristal",
                                                AquariaLocations.locations_cathedral_l_sc)
        self.cathedral_r = self.__add_region("Mithalas Cathedral",
                                             AquariaLocations.locations_cathedral_r)
        self.cathedral_underground = self.__add_region("Mithalas Cathedral underground area",
                                                       AquariaLocations.locations_cathedral_underground)
        self.cathedral_boss_r = self.__add_region("Mithalas Cathedral, Mithalan God room",
                                                  AquariaLocations.locations_cathedral_boss)
        self.cathedral_boss_l = self.__add_region("Mithalas Cathedral, after Mithalan God room", None)

    def __create_forest(self) -> None:
        """
        Create the `forest_*` dans `mermog_cave` regions
        """
        self.forest_tl = self.__add_region("Kelp forest top left area",
                                           AquariaLocations.locations_forest_tl)
        self.forest_tl_fp = self.__add_region("Kelp forest top left area fish pass",
                                              AquariaLocations.locations_forest_tl_fp)
        self.forest_tr = self.__add_region("Kelp forest top right area",
                                           AquariaLocations.locations_forest_tr)
        self.forest_tr_fp = self.__add_region("Kelp forest top right area fish pass",
                                              AquariaLocations.locations_forest_tr_fp)
        self.forest_bl = self.__add_region("Kelp forest bottom left area",
                                           AquariaLocations.locations_forest_bl)
        self.forest_br = self.__add_region("Kelp forest bottom right area",
                                           AquariaLocations.locations_forest_br)
        self.forest_sprite_cave = self.__add_region("Kelp forest spirit cave",
                                                    AquariaLocations.locations_forest_sprite_cave)
        self.forest_sprite_cave_tube = self.__add_region("Kelp forest spirit cave after the plant tube",
                                                         AquariaLocations.locations_forest_sprite_cave_tube)
        self.forest_boss = self.__add_region("Kelp forest Drunian God room",
                                             AquariaLocations.locations_forest_boss)
        self.forest_boss_entrance = self.__add_region("Kelp forest Drunian God room entrance",
                                                      AquariaLocations.locations_forest_boss_entrance)
        self.mermog_cave = self.__add_region("Kelp forest Mermog cave",
                                             AquariaLocations.locations_mermog_cave)
        self.mermog_boss = self.__add_region("Kelp forest Mermog cave boss",
                                             AquariaLocations.locations_mermog_boss)
        self.forest_fish_cave = self.__add_region("Kelp forest fish cave",
                                                  AquariaLocations.locations_forest_fish_cave)
        self.simon = self.__add_region("Kelp forest, Simon's room", AquariaLocations.locations_simon)

    def __create_veil(self) -> None:
        """
        Create the `veil_*`, `octo_cave` and `turtle_cave` regions
        """
        self.veil_tl = self.__add_region("The veil top left area", AquariaLocations.locations_veil_tl)
        self.veil_tl_fp = self.__add_region("The veil top left area fish pass",
                                            AquariaLocations.locations_veil_tl_fp)
        self.turtle_cave = self.__add_region("The veil top left area, turtle cave",
                                             AquariaLocations.locations_turtle_cave)
        self.turtle_cave_bubble = self.__add_region("The veil top left area, turtle cave bubble cliff",
                                                    AquariaLocations.locations_turtle_cave_bubble)
        self.veil_tr_l = self.__add_region("The veil top right area, left of temple",
                                           AquariaLocations.locations_veil_tr_l)
        self.veil_tr_r = self.__add_region("The veil top right area, right of temple",
                                           AquariaLocations.locations_veil_tr_r)
        self.octo_cave_t = self.__add_region("Octopus cave top entrance",
                                             AquariaLocations.locations_octo_cave_t)
        self.octo_cave_b = self.__add_region("Octopus cave bottom entrance",
                                             AquariaLocations.locations_octo_cave_b)
        self.veil_bl = self.__add_region("The veil bottom left area",
                                         AquariaLocations.locations_veil_bl)
        self.veil_b_sc = self.__add_region("The veil bottom spirit cristal area",
                                           AquariaLocations.locations_veil_b_sc)
        self.veil_bl_fp = self.__add_region("The veil bottom left area, in the sunken ship",
                                            AquariaLocations.locations_veil_bl_fp)
        self.veil_br = self.__add_region("The veil bottom right area",
                                         AquariaLocations.locations_veil_br)

    def __create_sun_temple(self) -> None:
        """
        Create the `sun_temple*` regions
        """
        self.sun_temple_l = self.__add_region("Sun temple left area",
                                              AquariaLocations.locations_sun_temple_l)
        self.sun_temple_r = self.__add_region("Sun temple right area",
                                              AquariaLocations.locations_sun_temple_r)
        self.sun_temple_boss_path = self.__add_region("Sun temple before boss area",
                                                    AquariaLocations.locations_sun_temple_boss_path)
        self.sun_temple_boss = self.__add_region("Sun temple boss area",
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
        self.ice_cave = self.__add_region("Ice cave", AquariaLocations.locations_ice_cave)
        self.bubble_cave = self.__add_region("Bubble cave", AquariaLocations.locations_bubble_cave)
        self.bubble_cave_boss = self.__add_region("Bubble cave boss area", AquariaLocations.locations_bubble_cave_boss)
        self.king_jellyfish_cave = self.__add_region("Abyss left area, King jellyfish cave",
                                                     AquariaLocations.locations_king_jellyfish_cave)
        self.whale = self.__add_region("Inside the whale", AquariaLocations.locations_whale)
        self.first_secret = self.__add_region("First secret area", None)

    def __create_sunken_city(self) -> None:
        """
        Create the `sunken_city_*` regions
        """
        self.sunken_city_l = self.__add_region("Sunken city left area",
                                               AquariaLocations.locations_sunken_city_l)
        self.sunken_city_l_bedroom = self.__add_region("Sunken city left area, bedroom",
                                                       AquariaLocations.locations_sunken_city_l_bedroom)
        self.sunken_city_r = self.__add_region("Sunken city right area",
                                               AquariaLocations.locations_sunken_city_r)
        self.sunken_city_boss = self.__add_region("Sunken city boss area",
                              AquariaLocations.locations_sunken_city_boss)

    def __create_body(self) -> None:
        """
        Create the `body_*` and `final_boss* regions
        """
        self.body_c = self.__add_region("The body center area",
                                        AquariaLocations.locations_body_c)
        self.body_l = self.__add_region("The body left area",
                                        AquariaLocations.locations_body_l)
        self.body_rt = self.__add_region("The body right area, top path",
                                         AquariaLocations.locations_body_rt)
        self.body_rb = self.__add_region("The body right area, bottom path",
                                         AquariaLocations.locations_body_rb)
        self.body_b = self.__add_region("The body bottom area",
                                        AquariaLocations.locations_body_b)
        self.final_boss_loby = self.__add_region("The body, before final boss", None)
        self.final_boss_tube = self.__add_region("The body, final boss area turtle room",
                                                 AquariaLocations.locations_final_boss_tube)
        self.final_boss = self.__add_region("The body, final boss",
                                                   AquariaLocations.locations_final_boss)
        self.final_boss_end = self.__add_region("The body, final boss area", None)

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
        self.__connect_regions("Menu", "Verse cave right area",
                               self.menu, self.verse_cave_r)
        self.__connect_regions("Verse cave left area", "Verse cave right area",
                               self.verse_cave_l, self.verse_cave_r)
        self.__connect_regions("Verse cave", "Home water", self.verse_cave_l, self.home_water)
        self.__connect_regions("Home Water", "Haija's home", self.home_water, self.naija_home)
        self.__connect_regions("Home Water", "Song cave", self.home_water, self.song_cave)
        self.__connect_regions("Home Water", "Home water, nautilus nest",
                               self.home_water, self.home_water_nautilus,
                               lambda state: _has_energy_form(state, self.player) and _has_bind_song(state, self.player))
        self.__connect_regions("Home Water", "Home water transturtle room",
                               self.home_water, self.home_water_transturtle)
        self.__connect_regions("Home Water", "Energy temple first area",
                               self.home_water, self.energy_temple_1,
                               lambda state: _has_bind_song(state, self.player))
        self.__connect_regions("Home Water", "Energy temple_altar",
                               self.home_water, self.energy_temple_altar,
                               lambda state: _has_energy_form(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions("Energy temple first area", "Energy temple second area",
                               self.energy_temple_1, self.energy_temple_2,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_regions("Energy temple first area", "Energy temple idol room",
                               self.energy_temple_1, self.energy_temple_idol,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Energy temple idol room", "Energy temple boss area",
                               self.energy_temple_idol, self.energy_temple_boss,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Energy temple first area", "Energy temple boss area",
                                       self.energy_temple_1, self.energy_temple_boss,
                                       lambda state: _has_beast_form(state, self.player) and
                                                     _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Energy temple boss area", "Energy temple first area",
                                       self.energy_temple_boss, self.energy_temple_1,
                                       lambda state: _has_energy_form(state, self.player))
        self.__connect_regions("Energy temple second area", "Energy temple third area",
                               self.energy_temple_2, self.energy_temple_3,
                               lambda state: _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player))
        self.__connect_regions("Energy temple boss area", "Energy temple blaster room",
                               self.energy_temple_boss, self.energy_temple_blaster_room,
                               lambda state: _has_nature_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player))
        self.__connect_regions("Energy temple first area", "Energy temple blaster room",
                               self.energy_temple_1, self.energy_temple_blaster_room,
                               lambda state: _has_nature_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player) and
                                             _has_beast_form(state, self.player))
        self.__connect_regions("Home Water", "Open water top left area",
                               self.home_water, self.openwater_tl)

    def __connect_open_water_regions(self) -> None:
        """
        Connect entrances of the different regions around open water
        """
        self.__connect_regions("Open water top left area", "Open water top right area",
                               self.openwater_tl, self.openwater_tr)
        self.__connect_regions("Open water top left area", "Open water bottom left area",
                               self.openwater_tl, self.openwater_bl)
        self.__connect_regions("Open water top left area", "forest bottom right area",
                               self.openwater_tl, self.forest_br)
        self.__connect_regions("Open water top right area", "Open water top right area, turtle room",
                               self.openwater_tr, self.openwater_tr_turtle,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Open water top right area", "Open water bottom right area",
                               self.openwater_tr, self.openwater_br)
        self.__connect_regions("Open water top right area", "Mithalas city",
                               self.openwater_tr, self.mithalas_city)
        self.__connect_regions("Open water top right area", "Veil bottom left area",
                               self.openwater_tr, self.veil_bl)
        self.__connect_one_way_regions("Open water top right area", "Veil bottom right",
                                       self.openwater_tr, self.veil_br,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Veil bottom right", "Open water top right area",
                                       self.veil_br, self.openwater_tr,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Open water bottom left area", "Open water bottom right area",
                               self.openwater_bl, self.openwater_br)
        self.__connect_regions("Open water bottom left area", "Skeleton path",
                               self.openwater_bl, self.skeleton_path)
        self.__connect_regions("Abyss left area", "Open water bottom left area",
                               self.abyss_l, self.openwater_bl)
        self.__connect_regions("Skeleton path", "skeleton_path_sc",
                               self.skeleton_path, self.skeleton_path_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Abyss right area", "Open water bottom right area",
                               self.abyss_r, self.openwater_br)
        self.__connect_one_way_regions("Open water bottom right area", "Arnassi",
                                       self.openwater_br, self.arnassi,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Arnassi", "Open water bottom right area",
                                       self.arnassi, self.openwater_br)
        self.__connect_regions("Arnassi", "Arnassi path",
                               self.arnassi, self.arnassi_path)
        self.__connect_one_way_regions("Arnassi path", "Arnassi crab boss area",
                                       self.arnassi_path, self.arnassi_crab_boss,
                                       lambda state: _has_beast_form(state, self.player) and
                                                     _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Arnassi crab boss area", "Arnassi path",
                                       self.arnassi_crab_boss, self.arnassi_path)

    def __connect_mithalas_regions(self) -> None:
        """
        Connect entrances of the different regions around Mithalas
        """
        self.__connect_one_way_regions("Mithalas city", "Mithalas city top path",
                                       self.mithalas_city, self.mithalas_city_top_path,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions("Mithalas city_top_path", "Mithalas city",
                                       self.mithalas_city_top_path, self.mithalas_city)
        self.__connect_regions("Mithalas city", "Mithalas city home with fishpass",
                               self.mithalas_city, self.mithalas_city_fishpass,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Mithalas city", "Mithalas castle",
                               self.mithalas_city, self.cathedral_l,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_one_way_regions("Mithalas city top path", "Mithalas castle, flower tube",
                                       self.mithalas_city_top_path,
                                       self.cathedral_l_tube,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle, flower tube area", "Mithalas city top path",
                                       self.cathedral_l_tube,
                                       self.mithalas_city_top_path,
                                       lambda state: _has_beast_form(state, self.player) and
                                                     _has_nature_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle flower tube area", "Mithalas castle, spirit crystals",
                               self.cathedral_l_tube, self.cathedral_l_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions("Mithalas castle_flower tube area", "Mithalas castle",
                               self.cathedral_l_tube, self.cathedral_l,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Mithalas castle", "Mithalas castle, spirit crystals",
                               self.cathedral_l, self.cathedral_l_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Mithalas castle", "Cathedral boss left area",
                               self.cathedral_l, self.cathedral_boss_l,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_energy_form(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions("Mithalas castle", "Cathedral underground",
                               self.cathedral_l, self.cathedral_underground,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions("Mithalas castle", "Cathedral right area",
                               self.cathedral_l, self.cathedral_r,
                               lambda state: _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player))
        self.__connect_regions("Cathedral right area", "Cathedral underground",
                               self.cathedral_r, self.cathedral_underground,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Cathedral underground", "Cathedral boss left area",
                                       self.cathedral_underground, self.cathedral_boss_r,
                                       lambda state: _has_energy_form(state, self.player) and
                                                     _has_bind_song(state, self.player))
        self.__connect_one_way_regions("Cathedral boss left area", "Cathedral underground",
                                       self.cathedral_boss_r, self.cathedral_underground,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Cathedral boss right area", "Cathedral boss left area",
                                       self.cathedral_boss_r, self.cathedral_boss_l,
                                       lambda state: _has_bind_song(state, self.player) and
                                                     _has_energy_form(state, self.player))

    def __connect_forest_regions(self) -> None:
        """
        Connect entrances of the different regions around the Kelp Forest
        """
        self.__connect_regions("Forest bottom right", "Veil bottom left area",
                               self.forest_br, self.veil_bl)
        self.__connect_regions("Forest bottom right", "Forest bottom left area",
                               self.forest_br, self.forest_bl)
        self.__connect_regions("Forest bottom right", "Forest top right area",
                               self.forest_br, self.forest_tr)
        self.__connect_regions("Forest bottom left area", "Forest fish cave",
                               self.forest_bl, self.forest_fish_cave)
        self.__connect_regions("Forest bottom left area", "Forest top left area",
                               self.forest_bl, self.forest_tl)
        self.__connect_regions("Forest bottom left area", "Forest boss entrance",
                               self.forest_bl, self.forest_boss_entrance,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions("Forest top left area", "Forest top left area, fish pass",
                               self.forest_tl, self.forest_tl_fp,
                               lambda state: _has_nature_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player) and
                                             _has_fish_form(state, self.player))
        self.__connect_regions("Forest top left area", "Forest top right area",
                               self.forest_tl, self.forest_tr)
        self.__connect_regions("Forest top left area", "Forest boss entrance",
                               self.forest_tl, self.forest_boss_entrance)
        self.__connect_regions("Forest boss area", "Forest boss entrance",
                               self.forest_boss, self.forest_boss_entrance,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_regions("Forest top right area", "Forest top right area fish pass",
                               self.forest_tr, self.forest_tr_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Forest top right area", "Forest sprite cave",
                               self.forest_tr, self.forest_sprite_cave)
        self.__connect_regions("Forest sprite cave", "Forest sprite cave flower tube",
                               self.forest_sprite_cave, self.forest_sprite_cave_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions("Forest top right area", "Mermog cave",
                               self.forest_tr_fp, self.mermog_cave)
        self.__connect_regions("Fermog cave", "Fermog boss",
                               self.mermog_cave, self.mermog_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_energy_form(state, self.player))

    def __connect_veil_regions(self) -> None:
        """
        Connect entrances of the different regions around The Veil
        """
        self.__connect_regions("Veil bottom left area", "Veil bottom left area, fish pass",
                               self.veil_bl, self.veil_bl_fp,
                               lambda state: _has_fish_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_damaging_item(state, self.player))
        self.__connect_regions("Veil bottom left area", "Veil bottom area spirit crystals path",
                               self.veil_bl, self.veil_b_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Veil bottom area spirit crystals path", "Veil bottom right",
                               self.veil_b_sc, self.veil_br,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Veil bottom right", "Veil top left area",
                               self.veil_br, self.veil_tl,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Veil top left area", "Veil_top left area, fish pass",
                               self.veil_tl, self.veil_tl_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions("Veil top left area", "Veil right of sun temple",
                               self.veil_tl, self.veil_tr_r)
        self.__connect_regions("Veil top left area", "Turtle cave",
                               self.veil_tl, self.turtle_cave)
        self.__connect_regions("Turtle cave", "Turtle cave bubble cliff",
                               self.turtle_cave, self.turtle_cave_bubble,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Veil right of sun temple", "Sun temple right area",
                               self.veil_tr_r, self.sun_temple_r)
        self.__connect_regions("Sun temple right area", "Sun temple left area",
                               self.sun_temple_r, self.sun_temple_l,
                               lambda state: _has_bind_song(state, self.player))
        self.__connect_regions("Sun temple left area", "Veil left of sun temple",
                               self.sun_temple_l, self.veil_tr_l)
        self.__connect_regions("Sun temple left area", "Sun temple before boss area",
                               self.sun_temple_l, self.sun_temple_boss_path)
        self.__connect_regions("Sun temple before boss area", "Sun temple boss area",
                               self.sun_temple_boss_path, self.sun_temple_boss,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions("Sun temple boss area", "Veil left of sun temple",
                                       self.sun_temple_boss, self.veil_tr_l)
        self.__connect_regions("Veil left of sun temple", "Octo cave top path",
                               self.veil_tr_l, self.octo_cave_t,
                               lambda state: _has_fish_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_beast_form(state, self.player) and
                                             _has_energy_form(state, self.player))
        self.__connect_regions("Veil left of sun temple", "Octo cave bottom path",
                               self.veil_tr_l, self.octo_cave_b,
                               lambda state: _has_fish_form(state, self.player))

    def __connect_abyss_regions(self) -> None:
        """
        Connect entrances of the different regions around The Abyss
        """
        self.__connect_regions("Abyss left area", "Abyss bottom of left area",
                               self.abyss_l, self.abyss_lb,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions("Abyss left bottom area", "Sunken city right area",
                               self.abyss_lb, self.sunken_city_r,
                               lambda state: _has_li(state, self.player))
        self.__connect_one_way_regions("Abyss left bottom area", "Body center area",
                               self.abyss_lb, self.body_c,
                               lambda state: _has_tongue_cleared(state, self.player))
        self.__connect_one_way_regions("Body center area", "Abyss left bottom area",
                               self.body_c, self.abyss_lb)
        self.__connect_regions("Abyss left area", "King jellyfish cave",
                               self.abyss_l, self.king_jellyfish_cave,
                               lambda state: _has_energy_form(state, self.player) and
                                             _has_beast_form(state, self.player))
        self.__connect_regions("Abyss left area", "Abyss right area",
                               self.abyss_l, self.abyss_r)
        self.__connect_regions("Abyss right area", "Inside the whale",
                               self.abyss_r, self.whale,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player))
        self.__connect_regions("Abyss right area", "First secret area",
                               self.abyss_r, self.first_secret,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_form(state, self.player))
        self.__connect_regions("Abyss right area", "Ice cave",
                               self.abyss_r, self.ice_cave,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Abyss right area", "Bubble cave",
                               self.ice_cave, self.bubble_cave,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_regions("Bubble cave boss area", "Bubble cave",
                               self.bubble_cave, self.bubble_cave_boss,
                               lambda state: _has_nature_form(state, self.player) and _has_bind_song(state, self.player)
                               )

    def __connect_sunken_city_regions(self) -> None:
        """
        Connect entrances of the different regions around The Sunken City
        """
        self.__connect_regions("Sunken city right area", "Sunken city left area",
                               self.sunken_city_r, self.sunken_city_l)
        self.__connect_regions("Sunken city left area", "Sunken city bedroom",
                               self.sunken_city_l, self.sunken_city_l_bedroom,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions("Sunken city left area", "Sunken city boss area",
                               self.sunken_city_l, self.sunken_city_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_energy_form(state, self.player) and
                                             _has_bind_song(state, self.player))

    def __connect_body_regions(self) -> None:
        """
        Connect entrances of the different regions around The body
        """
        self.__connect_regions("Body center area", "Body left area",
                               self.body_c, self.body_l)
        self.__connect_regions("Body center area", "Body right area top path",
                               self.body_c, self.body_rt)
        self.__connect_regions("Body center area", "Body right area bottom path",
                               self.body_c, self.body_rb)
        self.__connect_regions("Body center area", "Body bottom area",
                               self.body_c, self.body_b,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions("Body bottom area", "Final boss area",
                               self.body_b, self.final_boss_loby,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions("Before Final boss", "Final boss tube",
                               self.final_boss_loby, self.final_boss_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions("Before Final boss", "Final boss",
                                       self.final_boss_loby, self.final_boss,
                                       lambda state: _has_energy_form(state, self.player) and
                                                     _has_dual_form(state, self.player) and
                                                     _has_sun_form(state, self.player) and
                                                     _has_bind_song(state, self.player))
        self.__connect_one_way_regions("final boss third form area", "final boss end",
                                       self.final_boss, self.final_boss_end)

    def __connect_transturtle(self, item_source: str, item_target: str, region_source: Region, region_target: Region,
                              rule=None) -> None:
        """Connect a single transturtle to another one"""
        if item_source != item_target:
            if rule is None:
                self.__connect_one_way_regions(item_source, item_target, region_source, region_target,
                                               lambda state: state.has(item_target, self.player))
            else:
                self.__connect_one_way_regions(item_source, item_target, region_source, region_target, rule)

    def __connect_arnassi_path_transturtle(self, item_source: str, item_target: str, region_source: Region,
                                           region_target: Region) -> None:
        """Connect the Arnassi ruins transturtle to another one"""
        self.__connect_one_way_regions(item_source, item_target, region_source, region_target,
                                       lambda state: state.has(item_target, self.player) and
                                                     _has_fish_form(state, self.player))

    def _connect_transturtle_to_other(self, item: str, region: Region) -> None:
        """Connect a single transturtle to all others"""
        self.__connect_transturtle(item, "Transturtle Veil top left", region, self.veil_tl)
        self.__connect_transturtle(item, "Transturtle Veil top right", region, self.veil_tr_l)
        self.__connect_transturtle(item, "Transturtle Open Water top right", region, self.openwater_tr_turtle)
        self.__connect_transturtle(item, "Transturtle Forest bottom left", region, self.forest_bl)
        self.__connect_transturtle(item, "Transturtle Home water", region, self.home_water_transturtle)
        self.__connect_transturtle(item, "Transturtle Abyss right", region, self.abyss_r)
        self.__connect_transturtle(item, "Transturtle Final Boss", region, self.final_boss_tube)
        self.__connect_transturtle(item, "Transturtle Simon says", region, self.simon)
        self.__connect_transturtle(item, "Transturtle Arnassi ruins", region, self.arnassi_path,
                                       lambda state: state.has("Transturtle Arnassi ruins", self.player) and
                                                     _has_fish_form(state, self.player))

    def _connect_arnassi_path_transturtle_to_other(self, item: str, region: Region) -> None:
        """Connect the Arnassi ruins transturtle to all others"""
        self.__connect_arnassi_path_transturtle(item, "Transturtle Veil top left", region, self.veil_tl)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Veil top right", region, self.veil_tr_l)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Open Water top right", region,
                                                self.openwater_tr_turtle)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Forest bottom left", region, self.forest_bl)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Home water", region, self.home_water_transturtle)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Abyss right", region, self.abyss_r)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Final Boss", region, self.final_boss_tube)
        self.__connect_arnassi_path_transturtle(item, "Transturtle Simon says", region, self.simon)

    def __connect_transturtles(self) -> None:
        """Connect every transturtle with others"""
        self._connect_transturtle_to_other("Transturtle Veil top left", self.veil_tl)
        self._connect_transturtle_to_other("Transturtle Veil top right", self.veil_tr_l)
        self._connect_transturtle_to_other("Transturtle Open Water top right", self.openwater_tr_turtle)
        self._connect_transturtle_to_other("Transturtle Forest bottom left", self.forest_bl)
        self._connect_transturtle_to_other("Transturtle Home water", self.home_water_transturtle)
        self._connect_transturtle_to_other("Transturtle Abyss right", self.abyss_r)
        self._connect_transturtle_to_other("Transturtle Final Boss", self.final_boss_tube)
        self._connect_transturtle_to_other("Transturtle Simon says", self.simon)
        self._connect_arnassi_path_transturtle_to_other("Transturtle Arnassi ruins", self.arnassi_path)

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
                                  "Fallen God beated")
        self.__add_event_location(self.cathedral_boss_r,
                                  "Beating Mithalan God",
                                  "Mithalan God beated")
        self.__add_event_location(self.forest_boss,
                                  "Beating Drunian God",
                                  "Drunian God beated")
        self.__add_event_location(self.sun_temple_boss,
                                  "Beating Sun God",
                                  "Sun God beated")
        self.__add_event_location(self.sunken_city_boss,
                                  "Beating the Golem",
                                  "The Golem beated")

    def __add_event_mini_bosses(self) -> None:
        """
        Add every mini bosses (excluding Energy statue and Simon says)
        events to the `world`
        """
        self.__add_event_location(self.home_water_nautilus,
                                  "Beating Nautilus Prime",
                                  "Nautilus Prime beated")
        self.__add_event_location(self.energy_temple_blaster_room,
                                  "Beating Blaster Peg Prime",
                                  "Blaster Peg Prime beated")
        self.__add_event_location(self.mermog_boss,
                                  "Beating Mergog",
                                  "Mergog beated")
        self.__add_event_location(self.cathedral_l_tube,
                                  "Beating Mithalan priests",
                                  "Mithalan priests beated")
        self.__add_event_location(self.octo_cave_t,
                                  "Beating Octopus Prime",
                                  "Octopus Prime beated")
        self.__add_event_location(self.arnassi_crab_boss,
                                  "Beating Crabbius Maximus",
                                  "Crabbius Maximus beated")
        self.__add_event_location(self.bubble_cave_boss,
                                  "Beating Mantis Shrimp Prime",
                                  "Mantis Shrimp Prime beated")
        self.__add_event_location(self.king_jellyfish_cave,
                                  "Beating King Jellyfish God Prime",
                                  "King Jellyfish God Prime beated")

    def __add_event_secrets(self) -> None:
        """
        Add secrets events to the `world`
        """
        self.__add_event_location(self.first_secret,  # Doit ajouter une région pour le "first secret"
                                  "First secret",
                                  "First secret obtained")
        self.__add_event_location(self.mithalas_city,
                                  "Second secret",
                                  "Second secret obtained")
        self.__add_event_location(self.sun_temple_l,
                                  "Third secret",
                                  "Third secret obtained")

    def add_event_locations(self) -> None:
        """
        Add every event (locations and items) to the `world`
        """
        self.__add_event_mini_bosses()
        self.__add_event_big_bosses()
        self.__add_event_secrets()
        self.__add_event_location(self.sunken_city_boss,
                                  "Sunken City cleared",
                                  "Body tongue cleared")
        self.__add_event_location(self.sun_temple_r,
                                  "Sun Crystal",
                                  "Has sun crystal")
        self.__add_event_location(self.final_boss_end, "Objective complete",
                                  "Victory")

    def __adjusting_urns_rules(self) -> None:
        """Since Urns need to be broken, add a damaging item to rules"""
        add_rule(self.multiworld.get_location("Open water top right area, first urn in the Mithalas exit", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Open water top right area, second urn in the Mithalas exit", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Open water top right area, third urn in the Mithalas exit", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, first urn in one of the homes", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, second urn in one of the homes", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, first urn in the city reserve", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, second urn in the city reserve", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, third urn in the city reserve", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, urn in the cathedral flower tube entrance", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, urn in the bedroom", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, first urn of the single lamp path", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, second urn of the single lamp path", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, urn in the bottom room", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, first urn on the entrance path", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city castle, second urn on the entrance path", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Mithalas city, urn inside a home fish pass", self.player),
                 lambda state: _has_damaging_item(state, self.player))

    def __adjusting_crates_rules(self) -> None:
        """Since Crate need to be broken, add a damaging item to rules"""
        add_rule(self.multiworld.get_location("Sunken city right area, crate close to the save cristal", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Sunken city right area, crate in the left bottom room", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Sunken city left area, crate in the little pipe room", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Sunken city left area, crate close to the save cristal", self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location("Sunken city left area, crate before the bedroom", self.player),
                 lambda state: _has_damaging_item(state, self.player))

    def __adjusting_soup_rules(self) -> None:
        """
        Modify rules for location that need soup
        """
        add_rule(self.multiworld.get_location("Turtle cave, Urchin costume", self.player),
                 lambda state: _has_hot_soup(state, self.player) and _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("Sun Worm path, first cliff bulb", self.player),
                 lambda state: _has_hot_soup(state, self.player) and _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("Sun Worm path, second cliff bulb", self.player),
                 lambda state: _has_hot_soup(state, self.player) and _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("The veil top right area, bulb in the top of the water fall", self.player),
                 lambda state: _has_hot_soup(state, self.player) and _has_beast_form(state, self.player))

    def __adjusting_under_rock_location(self) -> None:
        """
        Modify rules implying bind song needed for bulb under rocks
        """
        add_rule(self.multiworld.get_location("Home water, bulb under the rock in the left path from the verse cave",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Verse cave left area, bulb under the rock at the end of the path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Naija's home, bulb under the rock at the right of the main path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Song cave, bulb under the rock in the path to the singing statues",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Song cave, bulb under the rock close to the song door",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Energy temple second area, bulb under the rock",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Open water top left area, bulb under the rock in the right path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Open water top left area, bulb under the rock in the left path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Kelp Forest top right area, bulb under the rock in the right path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("The veil top left area, bulb under the rock in the top right path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss right area, bulb behind the rock in the whale room",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss right area, bulb in the middle path",
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("The veil top left area, bulb under the rock in the top right path",
                                         self.player), lambda state: _has_bind_song(state, self.player))

    def __adjusting_light_in_dark_place_rules(self) -> None:
        add_rule(self.multiworld.get_location("Kelp forest top right area, Black pearl", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_location("Kelp forest bottom right area, Odd Container", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Veil top left to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Open Water top right to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Veil top right to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Forest bottom left to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Home water to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Final Boss to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Simon says to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Transturtle Arnassi ruins to Transturtle Abyss right", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Body center area to Abyss left bottom area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Veil left of sun temple to Octo cave top path", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Open water bottom right area to Abyss right area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Open water bottom left area to Abyss left area", self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance("Sun temple left area to Sun temple right area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance("Sun temple right area to Sun temple left area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance("Veil left of sun temple to Sun temple left area", self.player),
                 lambda state: _has_light(state, self.player) or _has_sun_crystal(state, self.player))

    def __adjusting_manual_rules(self) -> None:
        add_rule(self.multiworld.get_location("Mithalas cathedral, Mithalan Dress", self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("Open water bottom left area, bulb inside the lowest fish pass", self.player),
                 lambda state: _has_fish_form(state, self.player))
        add_rule(self.multiworld.get_location("Kelp forest bottom left area, Walker baby", self.player),
                 lambda state: _has_spirit_form(state, self.player))
        add_rule(self.multiworld.get_location("The veil top left area, bulb hidden behind the blocking rock", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Turtle cave, Turtle Egg", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Abyss left area, bulb in the bottom fish pass", self.player),
                 lambda state: _has_fish_form(state, self.player))
        add_rule(self.multiworld.get_location("Song cave, Anemone seed", self.player),
                 lambda state: _has_nature_form(state, self.player))
        add_rule(self.multiworld.get_location("Song cave, Verse egg", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Verse cave right area, Big Seed", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Arnassi ruins, Song plant spore on the top of the ruins", self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location("Energy temple first area, bulb in the bottom room blocked by a rock",
                                         self.player), lambda state: _has_energy_form(state, self.player))
        add_rule(self.multiworld.get_location("Home water, bulb in the bottom left room", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Home water, bulb in the path below Nautilus Prime", self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location("Naija's home, bulb after the energy door", self.player),
                 lambda state: _has_energy_form(state, self.player))
        add_rule(self.multiworld.get_location("Abyss right area, bulb behind the rock in the whale room", self.player),
                 lambda state: _has_spirit_form(state, self.player) and
                               _has_sun_form(state, self.player))
        add_rule(self.multiworld.get_location("Arnassi ruins, Arnassi Armor", self.player),
                 lambda state: _has_fish_form(state, self.player) and
                               _has_spirit_form(state, self.player))

    def __no_progression_hard_or_hidden_location(self) -> None:
        self.multiworld.get_location("Energy temple boss area, Fallen god tooth",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Cathedral boss area, beating Mithalan God",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp forest boss area, beating Drunian God",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun temple boss area, beating Sun God",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sunken city, bulb on the top of the boss area (boiler room)",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Home water, Nautilus Egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Energy temple blaster room, Blaster egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Mithalas castle, beating the priests",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Mermog cave, Piranha Egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Octopus cave, Dumbo Egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("King Jellyfish cave, bulb in the right path from King Jelly",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("King Jellyfish cave, Jellyfish Costume",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Final boss area, bulb in the boss third form room",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Worm path, first cliff bulb",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun Worm path, second cliff bulb",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("The veil top right area, bulb in the top of the water fall",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble cave, bulb in the left cave wall",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble cave, bulb in the right cave wall (behind the ice cristal)",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Bubble cave, Verse egg",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp Forest bottom left area, bulb close to the spirit crystals",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Kelp forest bottom left area, Walker baby",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun temple, Sun key",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("The body bottom area, Mutant Costume",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Sun temple, bulb in the hidden room of the right part",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression
        self.multiworld.get_location("Arnassi ruins, Arnassi Armor",
                                     self.player).item_rule =\
            lambda item: item.classification != ItemClassification.progression

    def adjusting_rules(self, options: AquariaOptions) -> None:
        """
        Modify rules for single location or optional rules
        """
        self.__adjusting_urns_rules()
        self.__adjusting_crates_rules()
        self.__adjusting_soup_rules()
        self.__adjusting_manual_rules()
        if options.light_needed_to_get_to_dark_places:
            self.__adjusting_light_in_dark_place_rules()
        if options.bind_song_needed_to_get_under_rock_bulb:
            self.__adjusting_under_rock_location()

        if options.mini_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance("Before Final boss to Final boss", self.player),
                     lambda state: _has_mini_bosses(state, self.player))
        if options.big_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance("Before Final boss to Final boss", self.player),
                     lambda state: _has_big_bosses(state, self.player))
        if options.objective.value == 1:
            add_rule(self.multiworld.get_entrance("Before Final boss to Final boss", self.player),
                     lambda state: _has_secrets(state, self.player))
        if options.unconfine_home_water.value in [0, 1]:
            add_rule(self.multiworld.get_entrance("Home Water to Home water transturtle room", self.player),
                     lambda state: _has_bind_song(state, self.player))
        if options.unconfine_home_water.value in [0, 2]:
            add_rule(self.multiworld.get_entrance("Home Water to Open water top left area", self.player),
                     lambda state: _has_bind_song(state, self.player) and _has_energy_form(state, self.player))
        if options.early_energy_form:
            self.multiworld.early_items[self.player]["Energy form"] = 1

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
        self.multiworld.regions.append(self.arnassi_path)
        self.multiworld.regions.append(self.arnassi_crab_boss)
        self.multiworld.regions.append(self.simon)

    def __add_mithalas_regions_to_world(self) -> None:
        """
        Add every region around Mithalas to the `world`
        """
        self.multiworld.regions.append(self.mithalas_city)
        self.multiworld.regions.append(self.mithalas_city_top_path)
        self.multiworld.regions.append(self.mithalas_city_fishpass)
        self.multiworld.regions.append(self.cathedral_l)
        self.multiworld.regions.append(self.cathedral_l_tube)
        self.multiworld.regions.append(self.cathedral_l_sc)
        self.multiworld.regions.append(self.cathedral_r)
        self.multiworld.regions.append(self.cathedral_underground)
        self.multiworld.regions.append(self.cathedral_boss_l)
        self.multiworld.regions.append(self.cathedral_boss_r)

    def __add_forest_regions_to_world(self) -> None:
        """
        Add every region around the kelp forest to the `world`
        """
        self.multiworld.regions.append(self.forest_tl)
        self.multiworld.regions.append(self.forest_tl_fp)
        self.multiworld.regions.append(self.forest_tr)
        self.multiworld.regions.append(self.forest_tr_fp)
        self.multiworld.regions.append(self.forest_bl)
        self.multiworld.regions.append(self.forest_br)
        self.multiworld.regions.append(self.forest_boss)
        self.multiworld.regions.append(self.forest_boss_entrance)
        self.multiworld.regions.append(self.forest_sprite_cave)
        self.multiworld.regions.append(self.forest_sprite_cave_tube)
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
        self.multiworld.regions.append(self.veil_tr_r)
        self.multiworld.regions.append(self.veil_bl)
        self.multiworld.regions.append(self.veil_b_sc)
        self.multiworld.regions.append(self.veil_bl_fp)
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
