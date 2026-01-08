import random
from typing import Optional

from .connection_data import area_doors
from .game import Game
from .item_data import Item, Items
from .loadout import Loadout
from .location_data import new_locations, majorLocs
from .logic_boss_reach import reach_and_kill
from .logic_shortcut import LogicShortcut
from .logic_updater import updateLogic
from .romWriter import RomWriter
from .solver import PlayThrough, hard_required_locations, solve


hint_data = {
    b'THE CHOZO HAVE A WEAKNESS IN': ("Torizo", 1, reach_and_kill("bomb_torizo")),
    b'BODY IS COVERED WITH A HARDENED': ("Botwoon", 2, reach_and_kill("botwoon")),
    b'STURDY IN ORDER TO SURVIVE IN': ("Draygon", 4, reach_and_kill("draygon")),
    b'EXOSKELETON HAS BEEN MODIFIED USING SOME': ("Ridley", 4, reach_and_kill("ridley")),
    b'PIRATES\x87. THEIR SKIN IS': ("Kraid", 2, reach_and_kill("kraid")),
    b'AROUND THEM. IT IS LIKELY THAT': ("Crocomire", 3, reach_and_kill("crocomire")),
    b'PHANTOON\x87 CAN CLOAK': ("Phantoon", 3, reach_and_kill("phantoon")),
    b'FUNGUS AND CAN CHANGE THE STRUCTURE OF': ("Spore Spawn", 2, reach_and_kill("spore_spawn")),
    b'COMMANDEERED THESE AND BUILT THEM INTO': ("Aurora", 1, LogicShortcut(lambda loadout: (
        loadout.game.all_locations["Weapon Locker"] in solve(loadout.game)[2]
        # only valid if doors don't change color
    ))),
    b'ALMOST ANY LIFEFORM WHILE BEING NEARLY': ("Metroid", 4, LogicShortcut(lambda loadout: (
        loadout.game.all_locations["Extract Storage"] in solve(loadout.game)[2]
    ))),
}

_hint_rom_locations: dict[bytes, tuple[int, int]] = {
    b'THE CHOZO HAVE A WEAKNESS IN': (0x1e467c, 0x1e46ab),
    b'BODY IS COVERED WITH A HARDENED': (0x1e47a1, 0x1e47c9),
    b'STURDY IN ORDER TO SURVIVE IN': (0x1e48e5, 0x1e4917),
    b'EXOSKELETON HAS BEEN MODIFIED USING SOME': (0x1e4a32, 0x1e4a87),
    b'PIRATES\x87. THEIR SKIN IS': (0x1e4bba, 0x1e4bf7),
    b'AROUND THEM. IT IS LIKELY THAT': (0x1e4cea, 0x1e4d2d),
    b'PHANTOON\x87 CAN CLOAK': (0x1e4e4c, 0x1e4e7f),
    b'FUNGUS AND CAN CHANGE THE STRUCTURE OF': (0x1e4f86, 0x1e4fd5),
    b'COMMANDEERED THESE AND BUILT THEM INTO': (0x1e50b9, 0x1e5115),
    b'ALMOST ANY LIFEFORM WHILE BEING NEARLY': (0x1e5218, 0x1e524f),
}

# used this before for changing location names
_location_aliases: dict[str, str] = {}


def get_last_minor_hard_required_location(hard_locs: dict[str, int], play_through: PlayThrough) -> str:

    # don't want to hint an item too early, look for the 3rd sphere after falling from spaceport
    third_fallen = 1
    count_fallen = 0
    for sphere_i, sphere in enumerate(play_through.spheres):
        if sphere.fallen:
            count_fallen += 1
            if count_fallen == 3:
                third_fallen = sphere_i
                break

    for hard_loc in reversed(hard_locs):
        if hard_locs[hard_loc] < third_fallen:
            # went too early in game to hint
            # so hint last location, even though it's major
            return next(reversed(hard_locs))
        if hard_loc not in majorLocs:
            return hard_loc

    # all hard required locations are major and none are in early spheres
    # so hint last location, even though it's major
    return next(reversed(hard_locs))


def choose_hint_location(game: Game) -> None:
    """ returns (hinted location name, bytes of boss text in log book to put hint after) """
    hard_locs, play_through = hard_required_locations(game)
    hint_loc_name = next(reversed(hard_locs))

    mmb = game.options.fill_choice == "B"

    if mmb:
        hint_loc_name = get_last_minor_hard_required_location(hard_locs, play_through)

    sphere_of_hinted_loc_i = 0
    for sphere in play_through.spheres:
        if hint_loc_name in sphere.pickups:
            for sphere_loc in sphere.pickups:
                # if screw is in the same sphere, hint that
                if (
                    game.all_locations[sphere_loc]["item"] == Items.Screw and
                    (
                        (not mmb) or
                        sphere_loc not in majorLocs
                    ) and
                    sphere_loc in hard_locs
                ):
                    hint_loc_name = sphere_loc
                    break
            break
        sphere_of_hinted_loc_i += 1

    if len(play_through.spheres) <= sphere_of_hinted_loc_i:
        print(f"WARNING: {len(play_through.spheres)} spheres found "
              f"in hint chooser with last sphere {sphere_of_hinted_loc_i}")
        game.hint_data = (hint_loc_name, b'THE CHOZO HAVE A WEAKNESS IN')  # this shouldn't happen
        return

    saved_items: dict[str, Optional[Item]] = {}
    for sphere_loc in play_through.spheres[sphere_of_hinted_loc_i].pickups:
        item = game.all_locations[sphere_loc]["item"]
        saved_items[sphere_loc] = item
        game.all_locations[sphere_loc]["item"] = None
        # print(f"removing {item.name if item else 'None'}")

    _, _, restricted_locs = solve(game)

    restricted_loadout = Loadout(game)
    for restricted_loc in restricted_locs:
        item = restricted_loc["item"]
        if item:
            restricted_loadout.append(item)

    restricted_loadout.append(Items.spaceDrop)
    restricted_loadout.append(area_doors["SunkenNestL"])

    updateLogic(game.all_locations.values(), restricted_loadout)

    allowed_bosses: list[bytes] = []
    for text_bytes, hint_info in hint_data.items():
        _name, prob, shortcut = hint_info
        if shortcut in restricted_loadout:
            for _ in range(prob):
                allowed_bosses.append(text_bytes)
            # print(f"can hint: {_name}  {repr(text_bytes)}")

    for saved_loc_name, item in saved_items.items():
        game.all_locations[saved_loc_name]["item"] = item

    if len(allowed_bosses) == 0:
        # no bosses were in logic with the sphere before go mode
        game.hint_data = (hint_loc_name, b'THE CHOZO HAVE A WEAKNESS IN')
        return

    game.hint_data = (hint_loc_name, random.choice(allowed_bosses))


def write_hint_to_rom(loc_name: str, hint_loc_marker: bytes, rom_writer: RomWriter) -> None:
    """
    replace text in the bestiary

    We have to edit all of the bestiary entries,
    otherwise someone could tell where the hint is, and possibly what the hint is,
    without going to any bosses.
    So we place a decoy for all the bosses that don't have the hint.
    """
    all_locations = tuple(loc["fullitemname"] for loc in new_locations().values())

    def get_decoy() -> str:
        """ dots that match a location name """
        decoy_target = random.choice(all_locations)
        decoy_chars = [(" " if c == " " else ".") for c in decoy_target]
        return "".join(decoy_chars)

    for each_loc_marker in hint_data:
        destination_i, end_i = _hint_rom_locations[each_loc_marker]
        length_limit = end_i - destination_i

        # make replacement text
        first_dot_length = random.randrange(2, 11)
        second_dot_length = random.randrange(12, 15) - first_dot_length
        to_write = "... " + ("." * first_dot_length) + " " + ("." * second_dot_length) + " " + (
            (
                loc_name
                if loc_name not in _location_aliases
                else _location_aliases[loc_name]
            ).upper()
            if each_loc_marker == hint_loc_marker
            else get_decoy()
        )
        to_write = to_write[:length_limit]

        assert all(32 <= ord(c) < 127 for c in to_write), f"tried to write non-ascii hint {to_write}"

        rom_writer.writeBytes(destination_i, to_write.encode() + b'\x00\x00')


def get_hint_spoiler_text(loc_name: str, hint_loc_marker: bytes) -> str:
    return f"\nhint for {loc_name} at {hint_data[hint_loc_marker][0]}\n"


def find_rom_hint_locations() -> None:
    rw = RomWriter.fromFilePaths("roms/Subversion12.sfc")
    rom = rw.rom_data
    output: dict[bytes, tuple[int, int]] = {}
    for each_loc_marker in hint_data:
        destination_i = rom.index(each_loc_marker) + len(each_loc_marker)
        end_i = rom.index(b'\x00', destination_i)
        output[each_loc_marker] = (destination_i, end_i)

    for key, [destination_i, end_i] in output.items():
        print(f"    {repr(key)}: ({hex(destination_i)}, {hex(end_i)}),")


if __name__ == "__main__":
    find_rom_hint_locations()
