from dataclasses import dataclass, field
from typing import Optional

from .area_rando_types import AreaDoor
from .connection_data import SunkenNestL, area_doors
from .game import Game
from .item_data import Items
from .loadout import Loadout
from .location_data import Location, spacePortLocs
from .logic_goal import can_win
from .logic_shortcut_data import can_fall_from_spaceport
from .logic_updater import updateLogic
from .trick import Trick
from .trick_data import Tricks


@dataclass
class Sphere:
    fallen: bool
    pickups: dict[str, str] = field(default_factory=dict)
    new_doors: list[str] = field(default_factory=list)


@dataclass
class PlayThrough:
    spheres: list[Sphere] = field(default_factory=list)


def solve(game: Game,
          starting_items: Optional[Loadout] = None,
          excluded_door: Optional[AreaDoor] = None,
          ap_logic: bool = False) -> tuple[bool, PlayThrough, list[Location]]:
    """
    `ap_logic` means that the beginning is just get Torpedo Bay, and then fall from spaceport

    returns (whether completable, play through, accessible locations)
    """
    for loc in game.all_locations.values():
        loc['inlogic'] = False

    unused_locations: list[Location] = list(game.all_locations.values())
    used_locs: set[str] = set()
    doors_accessed: set[AreaDoor] = set()

    loadout = Loadout(game, starting_items)

    play_through = PlayThrough()

    def check_for_new_area_doors() -> None:
        new_area_doors: list[str] = []
        for thing in loadout:
            if isinstance(thing, AreaDoor) and thing not in doors_accessed:
                new_area_doors.append(thing.name)
                doors_accessed.add(thing)
        if len(new_area_doors):
            # print(new_area_doors)
            if len(play_through.spheres) == 0:
                play_through.spheres.append(Sphere(False))
            play_through.spheres[-1].new_doors.extend(new_area_doors)

    if ap_logic:
        play_through.spheres.append(Sphere(False))

        loc_name = "Torpedo Bay"
        loc = game.all_locations[loc_name]
        item = loc["item"]
        if item:
            loadout.append(item)
            play_through.spheres[-1].pickups[loc_name] = item.name
        used_locs.add(loc_name)

        unused_locations = [loc for loc in unused_locations if loc['fullitemname'] not in used_locs]
    else:  # not AP logic (multiple spheres possible before falling from spaceport)
        # this loop just for spaceport
        stuck = False
        while not stuck:
            prev_loadout_count = len(loadout)
            updateLogic(unused_locations, loadout, excluded_door)
            check_for_new_area_doors()
            play_through.spheres.append(Sphere(False))
            for loc in unused_locations:
                if loc['inlogic']:
                    loc_name = loc['fullitemname']
                    if loc_name not in spacePortLocs:
                        # debug
                        # print(f"found {loc_name} in logic while still in spaceport")
                        continue
                    item = loc['item']
                    if item:
                        loadout.append(item)
                        play_through.spheres[-1].pickups[loc_name] = item.name
                    used_locs.add(loc_name)
            # remove used locations
            unused_locations = [loc for loc in unused_locations if loc['fullitemname'] not in used_locs]
            stuck = len(loadout) == prev_loadout_count

        while (
            len(play_through.spheres) > 0 and
            len(play_through.spheres[-1].new_doors) + len(play_through.spheres[-1].pickups) == 0
        ):
            play_through.spheres.pop()

    if can_fall_from_spaceport not in loadout:
        # print("solver: couldn't get out of spaceport")
        # for loc in unused_locations:
        #     if loc['inlogic'] and loc['fullitemname'] not in spacePortLocs:
        #         print("solver: found another way out of spaceport besides Ridley")
        #         print(loadout)
        #         print("but logic doesn't support that yet")
        return False, play_through, [loc for loc in game.all_locations.values() if loc["fullitemname"] in used_locs]
    loadout.append(Items.spaceDrop)
    loadout.append(SunkenNestL)  # assuming this is where we land

    stuck = False
    while not stuck:
        prev_loadout_count = len(loadout)
        updateLogic(unused_locations, loadout, excluded_door)
        check_for_new_area_doors()
        play_through.spheres.append(Sphere(True))
        for loc in unused_locations:

            # special case: major/minor can put missiles or grav boots in sandy cache even though it's not in logic
            # old major minor code obsolete, but it doesn't hurt
            if game.options.fill_choice == "MM" and loc['fullitemname'] == "Sandy Cache" and loc['item'] in {
                Items.GravityBoots, Items.Missile
            }:
                loc['inlogic'] = True

            if loc['inlogic']:
                loc_name = loc['fullitemname']
                item = loc['item']
                if item:
                    loadout.append(item)
                    play_through.spheres[-1].pickups[loc_name] = item.name
                used_locs.add(loc_name)
        # remove used locations
        unused_locations = [loc for loc in unused_locations if loc['fullitemname'] not in used_locs]
        stuck = len(loadout) == prev_loadout_count

    while (
        len(play_through.spheres) > 0 and
        len(play_through.spheres[-1].new_doors) + len(play_through.spheres[-1].pickups) == 0
    ):
        play_through.spheres.pop()

    # note: the reason for making a new list from all_locations rather than used_locs,
    # is that used_locs is a `set`, so iterating through it is not deterministic, so seeds wouldn't be reproducible
    return (
        (can_win in loadout),
        # len(unused_locations) == 0,
        play_through,
        [loc for loc in game.all_locations.values() if loc["fullitemname"] in used_locs]
    )


def spoil_play_through(play_through: PlayThrough) -> list[str]:
    items_to_display = {
        "Missile": 999,
        "Morph Ball": 999,
        "Gravity Boots": 999,
        "Super Missile": 999,
        "Grapple Beam": 999,
        "Power Bomb": 999,
        "Speed Ball": 999,
        "Bombs": 999,
        "HiJump": 999,
        "Aqua Suit": 999,
        "Dark Visor": 999,
        "Wave Beam": 999,
        "Speed Booster": 999,
        "Spazer": 999,
        "Varia Suit": 999,
        "Ice Beam": 999,
        "Metroid Suit": 999,
        "Plasma Beam": 999,
        "Screw Attack": 999,
        "Space Jump": 999,
        "Charge Beam": 999,
        "Hypercharge": 999,
        "X-Ray Scope": 999,
        "Energy Tank": 5,
        "Small Ammo": 4,
        "Large Ammo": 6,
        "Space Jump Boost": 1,
        "Damage Amp": 1,
        "Accel Charge": 1,
        "Refuel Tank": 0,
    }

    seen_fallen = False
    log_lines = [" - spaceport -"]
    for sphere in play_through.spheres:
        if sphere.fallen and not seen_fallen:
            log_lines.append(" - fall from spaceport -")
            seen_fallen = True

        log_lines.append("sphere:")
        for loc_name, item in sphere.pickups.items():
            if items_to_display[item] > 0:  # TODO: or hard required
                log_lines.append(f"    get {item} from {loc_name}")
                items_to_display[item] -= 1
        # TODO: if didn't display any pickups in sphere, display all pickups in sphere (unless last sphere)
        if len(sphere.new_doors):
            log_lines.append(f"  new area doors: {', '.join(sphere.new_doors)}")

    # TODO: delete "sphere:" from end
    return log_lines


def _locations_in_prog_order(play_through: PlayThrough) -> dict[str, int]:
    """
    { location name: sphere number }

    0 sphere means not in log lines

    If locations aren't in the solve log lines, they're at the end of this list.
    """
    locations: dict[str, int] = {}

    for sphere_i, sphere in enumerate(play_through.spheres):
        for loc_name in sphere.pickups:
            locations[loc_name] = sphere_i

    return locations


def hard_required_locations(game: Game) -> tuple[dict[str, int], PlayThrough]:
    """ list of names of hard required locations in progression order """
    completable, play_through, _ = solve(game)
    if not completable:
        # not sure what I want to do with this function if I pass a game that isn't completable
        # maybe exception
        return {}, play_through

    locations = _locations_in_prog_order(play_through)

    req_locs: dict[str, int] = {}
    for excluded_loc_name in locations:
        excluded_loc = game.all_locations[excluded_loc_name]
        saved_item = excluded_loc['item']
        excluded_loc['item'] = None
        completable, _, _ = solve(game)
        if not completable:
            req_locs[excluded_loc_name] = locations[excluded_loc_name]
        excluded_loc['item'] = saved_item

    return req_locs, play_through


def _excluded_tricks(t: Trick) -> set[Trick]:
    """
    all of the tricks that should be excluded to exclude this trick

    "If you can't do the easier one, then you can't do the harder one."
    """
    data = {
        Tricks.hell_run_easy:
            {Tricks.hell_run_easy, Tricks.hell_run_medium, Tricks.hell_run_hard},
        Tricks.hell_run_medium:
            {Tricks.hell_run_medium, Tricks.hell_run_hard},

        Tricks.dark_easy:
            {Tricks.dark_easy, Tricks.dark_medium, Tricks.dark_hard},
        Tricks.dark_medium:
            {Tricks.dark_medium, Tricks.dark_hard},

        Tricks.movement_moderate:
            {Tricks.movement_moderate, Tricks.movement_zoast},

        Tricks.sbj_underwater_w_hjb:
            {Tricks.sbj_underwater_w_hjb, Tricks.sbj_underwater_no_hjb},

        Tricks.wall_jump_precise:
            {Tricks.wall_jump_precise, Tricks.wall_jump_delayed},

        Tricks.morph_jump_4_tile:
            {Tricks.morph_jump_4_tile, Tricks.morph_jump_3_tile},

        Tricks.crouch_or_downgrab:
            {Tricks.crouch_or_downgrab, Tricks.crouch_precise},

        Tricks.short_charge_2:
            {Tricks.short_charge_2, Tricks.short_charge_3, Tricks.short_charge_4},

        Tricks.uwu_2_tile:
            {Tricks.uwu_2_tile, Tricks.uwu_2_tile_surface}
    }
    if t in data:
        return data[t]
    return {t}


def obsoletes(t: str) -> set[str]:
    data = {
        "hell_run_hard": {"hell_run_medium", "hell_run_easy"},
        "hell_run_medium": {"hell_run_easy"},
        "dark_hard": {"dark_medium", "dark_easy"},
        "dark_medium": {"dark_easy"},
        "movement_zoast": {"movement_moderate"},
    }
    if t in data:
        return data[t]
    return set()


def required_tricks(game: Game) -> tuple[list[str], list[str]]:
    """ lists of names of (tricks required to win, tricks required to get all locations) """
    completable, _, _ = solve(game)
    if not completable:
        # not sure what I want to do with this function if I pass a game that isn't completable
        # maybe exception
        return [], []

    req_for_win: list[str] = []
    req_for_locs: list[str] = []
    all_tricks = {t: n for n, t in vars(Tricks).items() if isinstance(t, Trick)}
    tricks_allowed = game.options.logic
    for excluded_trick in tricks_allowed:
        game.options.logic = tricks_allowed - _excluded_tricks(excluded_trick)
        completable, _, locs = solve(game)
        if not completable:
            req_for_win.append(all_tricks[excluded_trick])
        if len(locs) != 122:
            req_for_locs.append(all_tricks[excluded_trick])
    game.options.logic = tricks_allowed

    obsoleted: set[str] = set()
    for trick_name in req_for_win:
        obsoleted.update(obsoletes(trick_name))
    req_for_win = [trick_name for trick_name in req_for_win if trick_name not in obsoleted]

    obsoleted = set()
    for trick_name in req_for_locs:
        obsoleted.update(obsoletes(trick_name))
    req_for_locs = [trick_name for trick_name in req_for_locs if trick_name not in obsoleted]

    return req_for_win, req_for_locs


def required_doors(loadout: Loadout, loc_name: str) -> list[str]:
    """ what doors are required to get to this location with this loadout """
    temp_loadout = Loadout(loadout.game, loadout)
    _, play_through, acc_locs = solve(temp_loadout.game, temp_loadout)

    assert temp_loadout.game.all_locations[loc_name] in acc_locs, f"{loc_name} not in logic"

    doors: list[str] = []
    for sphere in play_through.spheres:
        for door_name in sphere.new_doors:
            doors.append(door_name)
            temp_loadout.contents[area_doors[door_name]] = 0

    tr: list[str] = []
    for excluded_door in doors:
        # empty doors from loadout
        for thing in temp_loadout:
            if isinstance(thing, AreaDoor):
                temp_loadout.contents[thing] = 0

        _, _, acc_locs = solve(temp_loadout.game, temp_loadout, area_doors[excluded_door])
        if temp_loadout.game.all_locations[loc_name] not in acc_locs:
            tr.append(excluded_door)

    return tr
