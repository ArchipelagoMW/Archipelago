"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Used to manage Regions in the Aquaria game multiworld randomizer
"""

from typing import Dict, Optional
from BaseClasses import MultiWorld, Region, Entrance, Item, ItemClassification, CollectionState
from .Items import AquariaItem, ItemNames
from .Locations import AquariaLocations, AquariaLocation, AquariaLocationNames
from .Options import AquariaOptions, UnconfineHomeWater
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
    """The secrets have been acquired in the `state` of the `player`"""
    return state.has_all({ItemNames.FIRST_SECRET_OBTAINED, ItemNames.SECOND_SECRET_OBTAINED,
                          ItemNames.THIRD_SECRET_OBTAINED}, player)

def _item_not_advancement(item: Item):
    """The `item` is not an advancement item"""
    return not item.advancement

class AquariaRegions:
    """
    Class used to create regions of the Aquaria game
    """
    menu: Region
    verse_cave_r: Region
    verse_cave_l: Region
    home_water: Region
    home_water_behind_rocks: Region
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
    sun_temple_l_entrance: Region
    sun_temple_r: Region
    sun_temple_boss_path: Region
    sun_temple_boss: Region
    abyss_l: Region
    abyss_lb: Region
    abyss_r: Region
    abyss_r_transturtle: Region
    ice_cave: Region
    frozen_feil: Region
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
        self.sun_temple_l_entrance = self.__add_region("Sun Temple left area entrance", None)
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

    def get_entrance_name(self, from_region: Region, to_region: Region):
        """
        Return the name of an entrance between `from_region` and `to_region`
        """
        return from_region.name + " to " + to_region.name

    def __connect_one_way_regions(self, source_region: Region, destination_region: Region, rule=None) -> None:
        """
        Connect from the `source_region` to the `destination_region`
        """
        entrance = Entrance(self.player, self.get_entrance_name(source_region, destination_region), source_region)
        source_region.exits.append(entrance)
        entrance.connect(destination_region)
        if rule is not None:
            set_rule(entrance, rule)

    def __connect_regions(self, source_region: Region,
                          destination_region: Region, rule=None) -> None:
        """
        Connect the `source_region` and the `destination_region` (two-way)
        """
        self.__connect_one_way_regions(source_region, destination_region, rule)
        self.__connect_one_way_regions(destination_region, source_region, rule)

    def __connect_home_water_regions(self) -> None:
        """
        Connect entrances of the different regions around `home_water`
        """
        self.__connect_one_way_regions(self.menu, self.verse_cave_r)
        self.__connect_regions(self.verse_cave_l, self.verse_cave_r)
        self.__connect_regions(self.verse_cave_l, self.home_water)
        self.__connect_regions(self.home_water, self.naija_home)
        self.__connect_regions(self.home_water, self.song_cave)
        self.__connect_regions(self.home_water, self.home_water_behind_rocks,
                               lambda state: _has_bind_song(state, self.player))
        self.__connect_regions(self.home_water_behind_rocks, self.home_water_nautilus,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.home_water, self.home_water_transturtle)
        self.__connect_regions(self.home_water_behind_rocks, self.energy_temple_1)
        self.__connect_regions(self.home_water_behind_rocks, self.energy_temple_altar,
                               lambda state: _has_energy_attack_item(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions(self.energy_temple_1, self.energy_temple_2,
                               lambda state: _has_energy_form(state, self.player))
        self.__connect_regions(self.energy_temple_1, self.energy_temple_idol,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions(self.energy_temple_idol, self.energy_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player) and
                                             _has_fish_form(state, self.player))
        self.__connect_one_way_regions(self.energy_temple_1, self.energy_temple_4,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions(self.energy_temple_4, self.energy_temple_1)
        self.__connect_regions(self.energy_temple_4, self.energy_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.energy_temple_2, self.energy_temple_3)
        self.__connect_one_way_regions(self.energy_temple_3, self.energy_temple_boss,
                                       lambda state: _has_bind_song(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.energy_temple_4, self.energy_temple_blaster_room,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_bind_song(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.home_water, self.openwater_tl)

    def __connect_open_water_regions(self) -> None:
        """
        Connect entrances of the different regions around open water
        """
        self.__connect_regions(self.openwater_tl, self.openwater_tr)
        self.__connect_regions(self.openwater_tl, self.openwater_bl)
        self.__connect_regions(self.openwater_tl, self.forest_br)
        self.__connect_one_way_regions(self.openwater_tr, self.openwater_tr_turtle,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions(self.openwater_tr_turtle, self.openwater_tr)
        self.__connect_one_way_regions(self.openwater_tr, self.openwater_tr_urns,
                                       lambda state: _has_bind_song(state, self.player) or
                                                     _has_damaging_item(state, self.player))
        self.__connect_regions(self.openwater_tr, self.openwater_br)
        self.__connect_regions(self.openwater_tr, self.mithalas_city)
        self.__connect_regions(self.openwater_tr, self.veil_b)
        self.__connect_one_way_regions(self.openwater_tr, self.veil_br,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions(self.veil_br, self.openwater_tr)
        self.__connect_regions(self.openwater_bl, self.openwater_br)
        self.__connect_regions(self.openwater_bl, self.skeleton_path)
        self.__connect_regions(self.abyss_l, self.openwater_bl)
        self.__connect_regions(self.skeleton_path, self.skeleton_path_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions(self.abyss_r, self.openwater_br)
        self.__connect_one_way_regions(self.openwater_br, self.arnassi,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions(self.arnassi, self.openwater_br)
        self.__connect_regions(self.arnassi, self.arnassi_cave)
        self.__connect_regions(self.arnassi_cave_transturtle, self.arnassi_cave,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_one_way_regions(self.arnassi_cave, self.arnassi_crab_boss,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player) and
                                                     (_has_energy_attack_item(state, self.player) or
                                                      _has_nature_form(state, self.player)))
        self.__connect_one_way_regions(self.arnassi_crab_boss, self.arnassi_cave)

    def __connect_mithalas_regions(self) -> None:
        """
        Connect entrances of the different regions around Mithalas
        """
        self.__connect_one_way_regions(self.mithalas_city, self.mithalas_city_urns,
                                       lambda state: _has_damaging_item(state, self.player))
        self.__connect_one_way_regions(self.mithalas_city, self.mithalas_city_top_path,
                                       lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        self.__connect_one_way_regions(self.mithalas_city_top_path, self.mithalas_city)
        self.__connect_regions(self.mithalas_city, self.mithalas_city_fishpass,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions(self.mithalas_city, self.mithalas_castle)
        self.__connect_one_way_regions(self.mithalas_city_top_path,
                                       self.mithalas_castle_tube,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle_tube,
                                       self.mithalas_city_top_path,
                                       lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle_tube, self.mithalas_castle_sc,
                                       lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle_tube, self.mithalas_castle,
                                       lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle, self.mithalas_castle_urns,
                                       lambda state: _has_damaging_item(state, self.player))
        self.__connect_regions(self.mithalas_castle, self.mithalas_castle_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle, self.cathedral_boss_r,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions(self.cathedral_boss_l, self.mithalas_castle,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_regions(self.mithalas_castle, self.cathedral_underground,
                               lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions(self.mithalas_castle, self.cathedral_top_start,
                                       lambda state: _has_bind_song(state, self.player))
        self.__connect_one_way_regions(self.cathedral_top_start, self.cathedral_top_start_urns,
                                       lambda state: _has_damaging_item(state, self.player))
        self.__connect_regions(self.cathedral_top_start, self.cathedral_top_end,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.cathedral_underground, self.cathedral_top_end,
                                       lambda state: _has_beast_form(state, self.player) and
                                                     _has_damaging_item(state, self.player))
        self.__connect_one_way_regions(self.cathedral_top_end, self.cathedral_underground,
                                       lambda state: _has_energy_attack_item(state, self.player)
                                       )
        self.__connect_one_way_regions(self.cathedral_underground, self.cathedral_boss_r)
        self.__connect_one_way_regions(self.cathedral_boss_r, self.cathedral_underground,
                                       lambda state: _has_beast_form(state, self.player))
        self.__connect_one_way_regions(self.cathedral_boss_r, self.cathedral_boss_l,
                                       lambda state: _has_bind_song(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.cathedral_boss_l, self.cathedral_boss_r)

    def __connect_forest_regions(self) -> None:
        """
        Connect entrances of the different regions around the Kelp Forest
        """
        self.__connect_regions(self.forest_br, self.veil_b)
        self.__connect_regions(self.forest_br, self.forest_bl)
        self.__connect_one_way_regions(self.forest_bl, self.forest_bl_sc,
                                       lambda state: _has_energy_attack_item(state, self.player) or
                                                     _has_fish_form(state, self.player))
        self.__connect_one_way_regions(self.forest_bl_sc, self.forest_bl)
        self.__connect_regions(self.forest_br, self.forest_tr)
        self.__connect_regions(self.forest_bl, self.forest_fish_cave)
        self.__connect_regions(self.forest_bl, self.forest_tl)
        self.__connect_regions(self.forest_bl, self.forest_boss_entrance,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions(self.forest_tl, self.forest_tl_verse_egg_room,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_bind_song(state, self.player) and
                                                     _has_energy_attack_item(state, self.player) and
                                                     _has_fish_form(state, self.player))
        self.__connect_one_way_regions(self.forest_tl_verse_egg_room, self.forest_tl,
                                       lambda state: _has_fish_form(state, self.player))
        self.__connect_regions(self.forest_tl, self.forest_tr)
        self.__connect_regions(self.forest_tl, self.forest_boss_entrance)
        self.__connect_one_way_regions(self.forest_boss_entrance, self.forest_boss,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.forest_boss, self.forest_boss_entrance)
        self.__connect_regions(self.forest_tr, self.forest_tr_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions(self.forest_tr, self.sprite_cave)
        self.__connect_regions(self.sprite_cave, self.sprite_cave_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions(self.forest_tr_fp, self.mermog_cave)
        self.__connect_regions(self.mermog_cave, self.mermog_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_energy_attack_item(state, self.player))

    def __connect_veil_regions(self) -> None:
        """
        Connect entrances of the different regions around The Veil
        """
        self.__connect_regions(self.veil_b, self.veil_b_fp,
                               lambda state: _has_fish_form(state, self.player) and
                                             _has_bind_song(state, self.player))
        self.__connect_regions(self.veil_b, self.veil_b_sc,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions(self.veil_b_sc, self.veil_br,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions(self.veil_br, self.veil_tl)
        self.__connect_regions(self.veil_tl, self.veil_tl_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_regions(self.veil_tl, self.veil_tr_r)
        self.__connect_regions(self.veil_tl, self.turtle_cave)
        self.__connect_regions(self.turtle_cave, self.turtle_cave_bubble)
        self.__connect_regions(self.veil_tr_r, self.sun_temple_r)

        self.__connect_one_way_regions(self.sun_temple_r, self.sun_temple_l_entrance,
                                       lambda state: _has_bind_song(state, self.player) or
                                                     _has_light(state, self.player))
        self.__connect_one_way_regions(self.sun_temple_l_entrance, self.sun_temple_r,
                                       lambda state: _has_light(state, self.player))
        self.__connect_regions(self.sun_temple_l_entrance, self.veil_tr_l)
        self.__connect_regions(self.sun_temple_l, self.sun_temple_l_entrance)
        self.__connect_one_way_regions(self.sun_temple_l, self.sun_temple_boss_path)
        self.__connect_one_way_regions(self.sun_temple_boss_path, self.sun_temple_l)
        self.__connect_regions(self.sun_temple_boss_path, self.sun_temple_boss,
                               lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.sun_temple_boss, self.veil_tr_l)
        self.__connect_regions(self.veil_tr_l, self.veil_tr_l_fp,
                               lambda state: _has_fish_form(state, self.player))
        self.__connect_one_way_regions(self.veil_tr_l_fp, self.octo_cave_t,
                                       lambda state: _has_sun_form(state, self.player) and
                                                     _has_beast_form(state, self.player) and
                                                     _has_energy_attack_item(state, self.player))
        self.__connect_one_way_regions(self.octo_cave_t, self.veil_tr_l_fp)
        self.__connect_regions(self.veil_tr_l_fp, self.octo_cave_b)

    def __connect_abyss_regions(self) -> None:
        """
        Connect entrances of the different regions around The Abyss
        """
        self.__connect_regions(self.abyss_l, self.abyss_lb,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_regions(self.abyss_lb, self.sunken_city_r,
                               lambda state: _has_li(state, self.player))
        self.__connect_one_way_regions(self.abyss_lb, self.body_c,
                                       lambda state: _has_tongue_cleared(state, self.player))
        self.__connect_one_way_regions(self.body_c, self.abyss_lb)
        self.__connect_one_way_regions(self.abyss_l, self.king_jellyfish_cave,
                                       lambda state: _has_dual_form(state, self.player) or
                                                     (_has_energy_form(state, self.player) and
                                                      _has_beast_form(state, self.player)))
        self.__connect_one_way_regions(self.king_jellyfish_cave, self.abyss_l)
        self.__connect_regions(self.abyss_l, self.abyss_r)
        self.__connect_regions(self.abyss_r, self.abyss_r_whale,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player))
        self.__connect_regions(self.abyss_r_whale, self.whale)
        self.__connect_regions(self.abyss_r, self.abyss_r_transturtle)
        self.__connect_regions(self.abyss_r, self.first_secret,
                               lambda state: _has_spirit_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_bind_song(state, self.player) and
                                             _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.abyss_r, self.ice_cave,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_regions(self.ice_cave, self.frozen_feil)
        self.__connect_one_way_regions(self.frozen_feil, self.bubble_cave,
                                       lambda state: _has_beast_form(state, self.player) or
                                                     _has_hot_soup(state, self.player))
        self.__connect_one_way_regions(self.bubble_cave, self.frozen_feil)
        self.__connect_one_way_regions(self.bubble_cave, self.bubble_cave_boss,
                                       lambda state: _has_nature_form(state, self.player) and
                                                     _has_bind_song(state, self.player)
                                       )
        self.__connect_one_way_regions(self.bubble_cave_boss, self.bubble_cave)

    def __connect_sunken_city_regions(self) -> None:
        """
        Connect entrances of the different regions around The Sunken City
        """
        self.__connect_regions(self.sunken_city_r, self.sunken_city_l)
        self.__connect_one_way_regions(self.sunken_city_r, self.sunken_city_r_crates,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.sunken_city_l, self.sunken_city_l_bedroom,
                               lambda state: _has_spirit_form(state, self.player))
        self.__connect_one_way_regions(self.sunken_city_l, self.sunken_city_l_crates,
                                       lambda state: _has_energy_attack_item(state, self.player))
        self.__connect_regions(self.sunken_city_l, self.sunken_city_boss,
                               lambda state: _has_beast_form(state, self.player) and
                                             _has_sun_form(state, self.player) and
                                             _has_energy_attack_item(state, self.player) and
                                             _has_bind_song(state, self.player))

    def __connect_body_regions(self) -> None:
        """
        Connect entrances of the different regions around The Body
        """
        self.__connect_one_way_regions(self.body_c, self.body_l,
                                       lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions(self.body_l, self.body_c)
        self.__connect_regions(self.body_c, self.body_rt)
        self.__connect_one_way_regions(self.body_c, self.body_rb,
                                       lambda state: _has_energy_form(state, self.player))
        self.__connect_one_way_regions(self.body_rb, self.body_c)
        self.__connect_regions(self.body_c, self.body_b,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions(self.body_b, self.final_boss_loby,
                               lambda state: _has_dual_form(state, self.player))
        self.__connect_regions(self.final_boss_loby, self.final_boss_tube,
                               lambda state: _has_nature_form(state, self.player))
        self.__connect_one_way_regions(self.final_boss_loby, self.final_boss,
                                       lambda state: _has_energy_form(state, self.player) and
                                                     _has_dual_form(state, self.player) and
                                                     _has_sun_form(state, self.player) and
                                                     _has_bind_song(state, self.player))
        self.__connect_one_way_regions(self.final_boss, self.final_boss_end)

    def __connect_transturtle(self, item_target: str, region_source: Region, region_target: Region) -> None:
        """Connect a single transturtle to another one"""
        if region_source != region_target:
            self.__connect_one_way_regions(region_source, region_target,
                                           lambda state: state.has(item_target, self.player))

    def _connect_transturtle_to_other(self, region: Region) -> None:
        """Connect a single transturtle to all others"""
        self.__connect_transturtle(ItemNames.TRANSTURTLE_VEIL_TOP_LEFT, region, self.veil_tl)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT, region, self.veil_tr_l)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_OPEN_WATERS, region, self.openwater_tr_turtle)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_KELP_FOREST, region, self.forest_bl)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_HOME_WATERS, region, self.home_water_transturtle)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_ABYSS, region, self.abyss_r_transturtle)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_BODY, region, self.final_boss_tube)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_SIMON_SAYS, region, self.simon)
        self.__connect_transturtle(ItemNames.TRANSTURTLE_ARNASSI_RUINS, region, self.arnassi_cave_transturtle)

    def __connect_transturtles(self) -> None:
        """Connect every transturtle with others"""
        self._connect_transturtle_to_other(self.veil_tl)
        self._connect_transturtle_to_other(self.veil_tr_l)
        self._connect_transturtle_to_other(self.openwater_tr_turtle)
        self._connect_transturtle_to_other(self.forest_bl)
        self._connect_transturtle_to_other(self.home_water_transturtle)
        self._connect_transturtle_to_other(self.abyss_r_transturtle)
        self._connect_transturtle_to_other(self.final_boss_tube)
        self._connect_transturtle_to_other(self.simon)
        self._connect_transturtle_to_other(self.arnassi_cave_transturtle)

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
                                  AquariaLocationNames.BEATING_FALLEN_GOD,
                                  ItemNames.FALLEN_GOD_BEATED)
        self.__add_event_location(self.cathedral_boss_l,
                                  AquariaLocationNames.BEATING_MITHALAN_GOD,
                                  ItemNames.MITHALAN_GOD_BEATED)
        self.__add_event_location(self.forest_boss,
                                  AquariaLocationNames.BEATING_DRUNIAN_GOD,
                                  ItemNames.DRUNIAN_GOD_BEATED)
        self.__add_event_location(self.sun_temple_boss,
                                  AquariaLocationNames.BEATING_LUMEREAN_GOD,
                                  ItemNames.LUMEREAN_GOD_BEATED)
        self.__add_event_location(self.sunken_city_boss,
                                  AquariaLocationNames.BEATING_THE_GOLEM,
                                  ItemNames.THE_GOLEM_BEATED)

    def __add_event_mini_bosses(self) -> None:
        """
        Add every mini bosses (excluding Energy Statue and Simon Says)
        events to the `world`
        """
        self.__add_event_location(self.home_water_nautilus,
                                  AquariaLocationNames.BEATING_NAUTILUS_PRIME,
                                  ItemNames.NAUTILUS_PRIME_BEATED)
        self.__add_event_location(self.energy_temple_blaster_room,
                                  AquariaLocationNames.BEATING_BLASTER_PEG_PRIME,
                                  ItemNames.BLASTER_PEG_PRIME_BEATED)
        self.__add_event_location(self.mermog_boss,
                                  AquariaLocationNames.BEATING_MERGOG,
                                  ItemNames.MERGOG_BEATED)
        self.__add_event_location(self.mithalas_castle_tube,
                                  AquariaLocationNames.BEATING_MITHALAN_PRIESTS,
                                  ItemNames.MITHALAN_PRIESTS_BEATED)
        self.__add_event_location(self.octo_cave_t,
                                  AquariaLocationNames.BEATING_OCTOPUS_PRIME,
                                  ItemNames.OCTOPUS_PRIME_BEATED)
        self.__add_event_location(self.arnassi_crab_boss,
                                  AquariaLocationNames.BEATING_CRABBIUS_MAXIMUS,
                                  ItemNames.CRABBIUS_MAXIMUS_BEATED)
        self.__add_event_location(self.bubble_cave_boss,
                                  AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
                                  ItemNames.MANTIS_SHRIMP_PRIME_BEATED)
        self.__add_event_location(self.king_jellyfish_cave,
                                  AquariaLocationNames.BEATING_KING_JELLYFISH_GOD_PRIME,
                                  ItemNames.KING_JELLYFISH_GOD_PRIME_BEATED)

    def __add_event_secrets(self) -> None:
        """
        Add secrets events to the `world`
        """
        self.__add_event_location(self.first_secret,
                                  # Doit ajouter une région pour le AquariaLocationNames.FIRST_SECRET
                                  AquariaLocationNames.FIRST_SECRET,
                                  ItemNames.FIRST_SECRET_OBTAINED)
        self.__add_event_location(self.mithalas_city,
                                  AquariaLocationNames.SECOND_SECRET,
                                  ItemNames.SECOND_SECRET_OBTAINED)
        self.__add_event_location(self.sun_temple_l,
                                  AquariaLocationNames.THIRD_SECRET,
                                  ItemNames.THIRD_SECRET_OBTAINED)

    def add_event_locations(self) -> None:
        """
        Add every event (locations and items) to the `world`
        """
        self.__add_event_mini_bosses()
        self.__add_event_big_bosses()
        self.__add_event_secrets()
        self.__add_event_location(self.sunken_city_boss,
                                  AquariaLocationNames.SUNKEN_CITY_CLEARED,
                                  ItemNames.BODY_TONGUE_CLEARED)
        self.__add_event_location(self.sun_temple_r,
                                  AquariaLocationNames.SUN_CRYSTAL,
                                  ItemNames.HAS_SUN_CRYSTAL)
        self.__add_event_location(self.final_boss_end, AquariaLocationNames.OBJECTIVE_COMPLETE,
                                  ItemNames.VICTORY)

    def __adjusting_soup_rules(self) -> None:
        """
        Modify rules for location that need soup
        """
        add_rule(self.multiworld.get_location(AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME, self.player),
                 lambda state: _has_hot_soup(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB, self.player),
                 lambda state: _has_beast_and_soup_form(state, self.player) or
                               state.has(ItemNames.LUMEREAN_GOD_BEATED, self.player), combine="or")
        add_rule(self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB, self.player),
                 lambda state: _has_beast_and_soup_form(state, self.player) or
                               state.has(ItemNames.LUMEREAN_GOD_BEATED, self.player), combine="or")
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
                                         self.player),
            lambda state: _has_beast_and_soup_form(state, self.player))

    def __adjusting_under_rock_location(self) -> None:
        """
        Modify rules implying bind song needed for bulb under rocks
        """
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.HOME_WATERS_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH_FROM_THE_VERSE_CAVE,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.VERSE_CAVE_LEFT_AREA_BULB_UNDER_THE_ROCK_AT_THE_END_OF_THE_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.NAIJA_S_HOME_BULB_UNDER_THE_ROCK_AT_THE_RIGHT_OF_THE_MAIN_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_IN_THE_PATH_TO_THE_SINGING_STATUES,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_CLOSE_TO_THE_SONG_DOOR,
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK,
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM,
                                         self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_MIDDLE_PATH,
                                              self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH,
            self.player), lambda state: _has_bind_song(state, self.player))

    def __adjusting_light_in_dark_place_rules(self) -> None:
        add_rule(self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL, self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER, self.player),
            lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.sun_temple_l_entrance, self.sun_temple_l),
                                              self.player), lambda state: _has_light(state, self.player) or
                                                                          _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.sun_temple_boss_path, self.sun_temple_l),
                                              self.player), lambda state: _has_light(state, self.player) or
                                                                          _has_sun_crystal(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.abyss_r_transturtle, self.abyss_r),
                                              self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.body_c, self.abyss_lb), self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.openwater_br, self.abyss_r), self.player),
                 lambda state: _has_light(state, self.player))
        add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.openwater_bl, self.abyss_l), self.player),
                 lambda state: _has_light(state, self.player))

    def __adjusting_manual_rules(self) -> None:
        add_rule(self.multiworld.get_location(AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS, self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS, self.player),
            lambda state: _has_fish_form(state, self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY, self.player),
            lambda state: _has_spirit_form(state, self.player))
        add_rule(
            self.multiworld.get_location(
                AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK, self.player),
            lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.TURTLE_CAVE_TURTLE_EGG, self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS,
                                              self.player),
                 lambda state: _has_fish_form(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SONG_CAVE_ANEMONE_SEED, self.player),
                 lambda state: _has_nature_form(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SONG_CAVE_VERSE_EGG, self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.VERSE_CAVE_RIGHT_AREA_BIG_SEED, self.player),
                 lambda state: _has_bind_song(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.ARNASSI_RUINS_SONG_PLANT_SPORE, self.player),
                 lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK,
            self.player), lambda state: _has_bind_song(state, self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.NAIJA_S_HOME_BULB_AFTER_THE_ENERGY_DOOR, self.player),
            lambda state: _has_energy_attack_item(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR, self.player),
                 lambda state: _has_fish_form(state, self.player) or
                               _has_beast_and_soup_form(state, self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS, self.player),
            lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE,
                                              self.player),
                 lambda state: _has_damaging_item(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF, self.player
        ), lambda state: _has_beast_form_or_arnassi_armor(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG, self.player),
                 lambda state: _has_beast_form(state, self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB, self.player),
                 lambda state: state.has("Sun God beated", self.player))
        add_rule(self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB, self.player),
                 lambda state: state.has("Sun God beated", self.player))
        add_rule(
            self.multiworld.get_location(AquariaLocationNames.THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE, self.player),
            lambda state: _has_tongue_cleared(state, self.player))
        add_rule(self.multiworld.get_location(
            AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_SMALL_PATH_BEFORE_MITHALAS,
            self.player), lambda state: _has_bind_song(state, self.player)
        )

    def __no_progression_hard_or_hidden_location(self) -> None:
        self.multiworld.get_location(AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.HOME_WATERS_NAUTILUS_EGG,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
            self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(
            AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
            self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_SUN_KEY,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART,
                                     self.player).item_rule = _item_not_advancement
        self.multiworld.get_location(AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
                                     self.player).item_rule = _item_not_advancement

    def adjusting_rules(self, options: AquariaOptions) -> None:
        """
        Modify rules for single location or optional rules
        """
        self.__adjusting_manual_rules()
        self.__adjusting_soup_rules()
        if options.light_needed_to_get_to_dark_places:
            self.__adjusting_light_in_dark_place_rules()
        if options.bind_song_needed_to_get_under_rock_bulb:
            self.__adjusting_under_rock_location()

        if options.mini_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.final_boss_loby, self.final_boss),
                                                  self.player), lambda state: _has_mini_bosses(state, self.player))
        if options.big_bosses_to_beat.value > 0:
            add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.final_boss_loby, self.final_boss),
                                                  self.player), lambda state: _has_big_bosses(state, self.player))
        if options.objective.value == options.objective.option_obtain_secrets_and_kill_the_creator:
            add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.final_boss_loby, self.final_boss),
                                                  self.player), lambda state: _has_secrets(state, self.player))
        if (options.unconfine_home_water.value == UnconfineHomeWater.option_via_energy_door or
                options.unconfine_home_water.value == UnconfineHomeWater.option_off):
            add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.home_water, self.home_water_transturtle),
                                                  self.player), lambda state: _has_bind_song(state, self.player))
        if (options.unconfine_home_water.value == UnconfineHomeWater.option_via_transturtle or
                options.unconfine_home_water.value == UnconfineHomeWater.option_off):
            add_rule(self.multiworld.get_entrance(self.get_entrance_name(self.home_water, self.openwater_tl),
                                                  self.player),
                     lambda state: _has_bind_song(state, self.player) and
                                   _has_energy_attack_item(state, self.player))
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
        self.multiworld.regions.append(self.sun_temple_l_entrance)
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
